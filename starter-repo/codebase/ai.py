"""Nối model — chỗ DUY NHẤT trong bản chạy thử gọi model AI.

Hợp đồng (giữ nguyên để khung đo được token):
    call_model(system: str, user: str) -> dict với 4 khoá:
        "text":       str   chữ model trả về
        "model":      str   tên model đã gọi (để tra giá ở bảng giá model)
        "tokens_in":  int   số token vào, lấy từ trường usage trong phản hồi API — KHÔNG ước lượng
        "tokens_out": int   số token ra, gồm cả token suy luận nếu API tính riêng

Chế độ giả (mặc định khi .env chưa có MODEL_PROVIDER hoặc MODEL_PROVIDER=fake):
    trả câu giả, model "fake", token 0 — dùng cho khung CP2.
Chế độ thật (CP3+):
    điền .env với MODEL_PROVIDER (openai | anthropic | gemini | ollama), MODEL_NAME, API_KEY.
    Chỉ dùng thư viện chuẩn của Python (urllib).
"""
import json
import os
import urllib.error
import urllib.request

from tracing import model_call

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHOW_RAW = False


def load_env(path=os.path.join(ROOT, ".env")):
    """Đọc file .env (KEY=VALUE mỗi dòng) vào biến môi trường, không ghi đè biến đã có."""
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_env()
MODEL_PROVIDER = (os.environ.get("MODEL_PROVIDER") or "fake").strip().lower()
MODEL_NAME = (os.environ.get("MODEL_NAME") or "").strip()
API_KEY = (os.environ.get("API_KEY") or "").strip()
API_BASE_URL = (os.environ.get("API_BASE_URL") or "").strip()


def post_json(url: str, headers: dict, body: dict, timeout: int = 60) -> dict:
    """Gửi POST JSON bằng thư viện chuẩn urllib."""
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        method="POST",
        headers=dict({"Content-Type": "application/json"}, **headers),
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise RuntimeError("HTTP %d: %s" % (e.code, e.read().decode("utf-8", "replace")[:300]))
    if SHOW_RAW:
        print(json.dumps(data, ensure_ascii=False, indent=2)[:3000])
    return data


def _call_openai(system: str, user: str) -> dict:
    url = API_BASE_URL or "https://api.openai.com/v1/chat/completions"
    messages = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": user}]
    data = post_json(
        url,
        {"Authorization": "Bearer " + API_KEY},
        {"model": MODEL_NAME, "messages": messages, "temperature": 0.2},
    )
    u = data.get("usage") or {}
    return {
        "text": data["choices"][0]["message"]["content"],
        "tokens_in": int(u.get("prompt_tokens", 0)),
        "tokens_out": int(u.get("completion_tokens", 0)),
    }


def _call_claude(system: str, user: str) -> dict:
    url = API_BASE_URL or "https://api.anthropic.com/v1/messages"
    data = post_json(
        url,
        {"x-api-key": API_KEY, "anthropic-version": "2023-06-01"},
        {
            "model": MODEL_NAME,
            "max_tokens": 1024,
            "system": system or "",
            "messages": [{"role": "user", "content": user}],
        },
    )
    text = "".join(b.get("text", "") for b in data.get("content", []) if b.get("type") == "text")
    u = data.get("usage") or {}
    return {
        "text": text,
        "tokens_in": int(u.get("input_tokens", 0)),
        "tokens_out": int(u.get("output_tokens", 0)),
    }


def _call_gemini(system: str, user: str) -> dict:
    base = API_BASE_URL or ("https://generativelanguage.googleapis.com/v1beta/models/%s:generateContent" % MODEL_NAME)
    url = base + ("&key=" if "?" in base else "?key=") + API_KEY
    body = {
        "contents": [{"role": "user", "parts": [{"text": user}]}],
        "generationConfig": {"temperature": 0.2},
    }
    if system:
        body["systemInstruction"] = {"parts": [{"text": system}]}
    data = post_json(url, {}, body)
    parts = data["candidates"][0]["content"].get("parts", [])
    text = "".join(p.get("text", "") for p in parts)
    u = data.get("usageMetadata") or {}
    tokens_out = int(u.get("candidatesTokenCount", 0)) + int(u.get("thoughtsTokenCount", 0))
    return {
        "text": text,
        "tokens_in": int(u.get("promptTokenCount", 0)),
        "tokens_out": tokens_out,
    }


def _call_ollama(system: str, user: str) -> dict:
    url = API_BASE_URL or "http://localhost:11434/api/chat"
    messages = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": user}]
    data = post_json(url, {}, {"model": MODEL_NAME, "messages": messages, "stream": False}, timeout=300)
    return {
        "text": data["message"]["content"],
        "tokens_in": int(data.get("prompt_eval_count", 0)),
        "tokens_out": int(data.get("eval_count", 0)),
    }


@model_call
def call_model(system: str, user: str) -> dict:
    if MODEL_PROVIDER == "fake":
        last = (user.strip().splitlines() or [""])[-1]
        return {
            "text": "[câu trả lời giả — chưa nối model] " + last[:60],
            "model": "fake",
            "tokens_in": 0,
            "tokens_out": 0,
        }

    if MODEL_PROVIDER == "openai":
        r = _call_openai(system, user)
    elif MODEL_PROVIDER == "anthropic":
        r = _call_claude(system, user)
    elif MODEL_PROVIDER == "gemini":
        r = _call_gemini(system, user)
    elif MODEL_PROVIDER == "ollama":
        r = _call_ollama(system, user)
    else:
        raise NotImplementedError(
            "Không hỗ trợ MODEL_PROVIDER=%s — dùng openai, anthropic, gemini, ollama hoặc fake" % MODEL_PROVIDER
        )

    return {
        "text": r["text"],
        "model": MODEL_NAME,
        "tokens_in": int(r["tokens_in"]),
        "tokens_out": int(r["tokens_out"]),
    }
