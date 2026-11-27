"""Nối model — chỗ DUY NHẤT trong bản chạy thử gọi model AI (guide 3.3, docs/connect-model.md).

Hợp đồng: call_model(system, user) -> {"text", "model", "tokens_in", "tokens_out"}; token lấy từ trường usage
của API, không ước lượng. Lỗi gọi model để exception bay ra (khung ghi cột error); agent.py quyết định có dùng
câu trả lời dự phòng hay không.

MODEL_PROVIDER: fake (mặc định) · gemini · openai · anthropic · ollama. Key đọc từ .env, không ghi vào code.
"""
import json
import os
import time
import urllib.error
import urllib.request

from tracing import model_call

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_env(path=os.path.join(ROOT, ".env")):
    """Đọc file .env (KEY=VALUE mỗi dòng) vào biến môi trường, không ghi đè biến đã có. Khung — không cần sửa."""
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
TIMEOUT_S = int(os.environ.get("MODEL_TIMEOUT_S") or 60)
MAX_TOKENS = int(os.environ.get("MODEL_MAX_TOKENS") or 1200)
TEMPERATURE = 0.2
SHOW_RAW = False

URL_OPENAI = os.environ.get("OPENAI_BASE_URL") or "https://api.openai.com/v1/chat/completions"
URL_CLAUDE = "https://api.anthropic.com/v1/messages"
URL_GEMINI = "https://generativelanguage.googleapis.com/v1beta/models/%s:generateContent"
URL_OLLAMA = "http://localhost:11434/api/chat"


def post_json(url, headers, body, timeout=TIMEOUT_S, retries=2):
    """POST JSON bằng urllib. Thử lại tối đa `retries` lần khi gặp 429 / 5xx / timeout (chờ 2s, 4s)."""
    req_body = json.dumps(body).encode("utf-8")
    for attempt in range(retries + 1):
        req = urllib.request.Request(url, data=req_body, method="POST",
                                     headers=dict({"Content-Type": "application/json"}, **headers))
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                data = json.loads(r.read().decode("utf-8"))
            break
        except urllib.error.HTTPError as e:
            msg = "HTTP %d: %s" % (e.code, e.read().decode("utf-8", "replace")[:300])
            if e.code in (429, 500, 502, 503, 504) and attempt < retries:
                time.sleep(2 * (attempt + 1))
                continue
            raise RuntimeError(msg)
        except (urllib.error.URLError, TimeoutError) as e:
            if attempt < retries:
                time.sleep(2 * (attempt + 1))
                continue
            raise RuntimeError("Không kết nối được model: %s" % e)
    if SHOW_RAW:
        print(json.dumps(data, ensure_ascii=False, indent=2)[:3000])
    return data


def call_gemini(system, user):
    body = {"contents": [{"role": "user", "parts": [{"text": user}]}],
            "generationConfig": {"temperature": TEMPERATURE, "maxOutputTokens": MAX_TOKENS}}
    if system:
        body["systemInstruction"] = {"parts": [{"text": system}]}
    data = post_json(URL_GEMINI % MODEL_NAME, {"x-goog-api-key": API_KEY}, body)
    cand = (data.get("candidates") or [{}])[0]
    text = "".join(p.get("text", "") for p in cand.get("content", {}).get("parts", []) if not p.get("thought"))
    u = data.get("usageMetadata") or {}
    if "promptTokenCount" not in u:
        raise RuntimeError("Phản hồi Gemini không có usageMetadata — không ước lượng token")
    # token ra = token trả lời + token suy nghĩ (nếu model tính riêng)
    return {"text": text, "tokens_in": u["promptTokenCount"],
            "tokens_out": u.get("candidatesTokenCount", 0) + u.get("thoughtsTokenCount", 0)}


def call_openai(system, user):
    messages = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": user}]
    data = post_json(URL_OPENAI, {"Authorization": "Bearer " + API_KEY},
                     {"model": MODEL_NAME, "messages": messages, "max_completion_tokens": MAX_TOKENS})
    u = data["usage"]
    return {"text": data["choices"][0]["message"]["content"] or "",
            "tokens_in": u["prompt_tokens"], "tokens_out": u["completion_tokens"]}


def call_claude(system, user):
    data = post_json(URL_CLAUDE, {"x-api-key": API_KEY, "anthropic-version": "2023-06-01"},
                     {"model": MODEL_NAME, "max_tokens": MAX_TOKENS, "temperature": TEMPERATURE,
                      "system": system or "", "messages": [{"role": "user", "content": user}]})
    text = "".join(b.get("text", "") for b in data.get("content", []) if b.get("type") == "text")
    u = data["usage"]
    return {"text": text, "tokens_in": u["input_tokens"], "tokens_out": u["output_tokens"]}


def call_ollama(system, user):
    messages = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": user}]
    data = post_json(URL_OLLAMA, {}, {"model": MODEL_NAME, "messages": messages, "stream": False}, timeout=300)
    return {"text": data["message"]["content"],
            "tokens_in": data.get("prompt_eval_count", 0), "tokens_out": data.get("eval_count", 0)}


PROVIDERS = {"gemini": call_gemini, "openai": call_openai, "anthropic": call_claude, "claude": call_claude,
             "ollama": call_ollama}


@model_call
def call_model(system: str, user: str) -> dict:
    if MODEL_PROVIDER == "fake":
        last = (user.strip().splitlines() or [""])[-1]
        return {"text": "[câu trả lời giả — chưa nối model] " + last[:60], "model": "fake", "tokens_in": 0, "tokens_out": 0}
    fn = PROVIDERS.get(MODEL_PROVIDER)
    if fn is None:
        raise NotImplementedError("MODEL_PROVIDER=%s chưa hỗ trợ — dùng gemini / openai / anthropic / ollama" % MODEL_PROVIDER)
    if not MODEL_NAME or (MODEL_PROVIDER != "ollama" and not API_KEY):
        raise NotImplementedError("Thiếu MODEL_NAME hoặc API_KEY trong .env")
    r = fn(system, user)
    return {"text": r["text"], "model": MODEL_NAME, "tokens_in": int(r["tokens_in"]), "tokens_out": int(r["tokens_out"])}
