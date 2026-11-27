"""Công cụ của bài toán — NHÓM VIẾT (guide 2.2, 3.2). Khớp bảng công cụ ở spec.md §4.

Mọi công cụ là code tất định (không gọi model), không tác động ra ngoài (không gửi tin, không ghi dữ liệu).
Model AI chỉ được gọi ở codebase/ai.py (call_model) trong bước soạn tư vấn của agent.py.
"""
import json
import math
import os
import re
import unicodedata

from tracing import tool, TOOLS  # noqa: F401

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(ROOT, "ml", "model.json")
KB_PATH = os.path.join(ROOT, "data", "knowledge_base.json")
_MODEL = json.load(open(MODEL_PATH, encoding="utf-8"))
_KB = [e for e in json.load(open(KB_PATH, encoding="utf-8"))["entries"] if e.get("verified")]


def _fold(text: str) -> str:
    """Chữ thường, bỏ dấu tiếng Việt (đ→d) để so khớp từ khoá ổn định."""
    t = unicodedata.normalize("NFD", text.lower().replace("đ", "d"))
    return "".join(c for c in t if unicodedata.category(c) != "Mn")


def _num(s: str) -> float:
    return float(s.replace(",", "."))


NUM = r"(\d+(?:[.,]\d+)?)"

# Bối cảnh đo — kiểm theo thứ tự (OGTT trước "sau ăn")
CONTEXTS = [
    ("ogtt", [r"nghiem phap", r"dung nap glucose", r"\bogtt\b", r"uong (dung dich )?glucose"]),
    ("fasting", [r"luc doi", r"nhin an", r"khi doi", r"\bfasting\b", r"buoi sang truoc an", r"truoc an sang"]),
    ("post_meal", [r"sau an", r"sau bua"]),
    ("random", [r"ngau nhien", r"bat ky"]),
]
EMERGENCY_SYMPTOMS = {
    "lơ mơ": r"lo mo", "thở gấp": r"tho gap|tho nhanh|kho tho", "tức ngực": r"tuc nguc|dau nguc",
    "ngất": r"\bngat\b|bat tinh", "nôn / buồn nôn": r"\bnon\b|buon non", "co giật": r"co giat",
    "hơi thở mùi trái cây": r"mui trai cay", "lú lẫn": r"lu lan",
}
HYPO_SYMPTOMS = {"run tay": r"\brun\b", "vã mồ hôi": r"va mo hoi|mo hoi lanh", "choáng / chóng mặt": r"choang|chong mat"}
HYPER_SYMPTOMS = {"khát nhiều": r"khat nuoc|khat nhieu", "mệt lả": r"met la"}


@tool
def extract_profile(text: str) -> dict:
    """extract_profile · Input: câu người dùng (str) · Output: hồ sơ chỉ số đã đọc được (dict),
    chỉ lấy số có trong câu, KHÔNG tự điền số thiếu · Không tác động ra ngoài."""
    f = _fold(text)
    p = {"sex": None, "age": None, "pregnant": False, "glucose_mgdl": None, "glucose_unit_raw": None,
         "glucose_context": None, "hba1c": None, "bmi": None, "height_m": None, "weight_kg": None,
         "diastolic_bp": None, "family_history": False, "symptoms": [], "notes": []}
    low = text.lower()
    # giới của NGƯỜI ĐƯỢC HỎI: lấy từ chữ CÓ dấu ("nam" ≠ "năm", "chị" ≠ "chỉ", "bà tôi" là người thân)
    if re.search(r"(?<!\w)(nữ|phụ nữ)(?!\w)", low) or re.search(r"(?<!\w)mẹ (tôi|mình) \d+ tuổi", low):
        p["sex"] = "female"
    if re.search(r"(?<!\w)(nam|đàn ông)(?!\w)", low) or re.search(r"(?<!\w)bố (tôi|mình) \d+ tuổi", low):
        p["sex"] = "male" if p["sex"] is None else p["sex"]
    if re.search(r"mang thai (tuan|thang)|dang mang thai|dang co thai|co bau|thai ky|tuan thu \d+ (cua )?thai", f):
        p["pregnant"] = True
        p["sex"] = "female"
    m = re.search(r"(\d{1,3})\s*tuoi", f) or re.search(r"tuoi\s*(\d{1,3})", f)
    if m:
        p["age"] = int(m.group(1))
    m = re.search(r"bmi[^0-9]{0,25}" + NUM, f)
    if m:
        p["bmi"] = _num(m.group(1))
    m = re.search(r"cao\s*(\d)\s*m\s*(\d{1,2})", f) or re.search(r"cao\s*(\d)[.,](\d{1,2})\s*m", f)
    if m:
        p["height_m"] = int(m.group(1)) + int(m.group(2).ljust(2, "0")) / 100
    m = re.search(r"cao\s*(1\d\d)\s*cm", f)
    if m:
        p["height_m"] = int(m.group(1)) / 100
    m = re.search(r"(?:nang|can nang)\s*" + NUM + r"\s*kg", f)
    if m:
        p["weight_kg"] = _num(m.group(1))
    if p["bmi"] is None and p["height_m"] and p["weight_kg"]:
        p["bmi"] = round(p["weight_kg"] / p["height_m"] ** 2, 1)
        p["notes"].append("BMI tính từ chiều cao và cân nặng người dùng nhập")
    m = re.search(r"huyet ap tam truong\s*" + NUM, f)
    if m:
        p["diastolic_bp"] = _num(m.group(1))
    m = re.search(r"hba1c[^0-9]{0,40}" + NUM, f)
    if m:
        p["hba1c"] = _num(m.group(1))
        later = re.search(r"hba1c[^.?!]{0,60}?(?:xuong|con)\s*" + NUM, f)  # "giảm từ 13% xuống 9%" → số hiện tại
        if later:
            p["hba1c"] = _num(later.group(1))
    # Đường huyết: lấy số đầu tiên đứng sau "đường huyết"/"glucose" kèm đơn vị
    gm = None
    kw = re.search(r"duong huyet|glucose", f)
    if kw:  # số đầu tiên sau từ khoá, bỏ qua số chỉ thời gian ("2 giờ", "tuần 26")
        for cand in re.finditer(NUM + r"\s*(mg/?dl|mmol/?l)?", f[kw.start(): kw.start() + 120]):
            tail = f[kw.start() + cand.end(): kw.start() + cand.end() + 6]
            head = f[max(0, kw.start() + cand.start() - 25): kw.start() + cand.start()]
            if re.search(r"lech|chenh|khac nhau", head):  # số là độ chênh, không phải số đo
                continue
            if cand.group(2) or not re.match(r"\s*(gio|h\b|tieng|phut|lan|tuan|-\s*\d)", tail):
                gm = (cand, kw.start())
                break
    if gm:
        cand, off = gm
        class _G:  # giữ API giống re.Match cho phần dưới
            def group(self, i): return {2: cand.group(1), 3: cand.group(2)}[i]
            def start(self): return off
            def end(self): return off + cand.end()
        gm = _G()
        value, unit = _num(gm.group(2)), (gm.group(3) or "").replace("/", "")
        if not unit:
            unit = "mmoll" if value < 35 else "mgdl"
            p["notes"].append("đơn vị đường huyết không ghi rõ, đoán là %s" % ("mmol/L" if unit == "mmoll" else "mg/dL"))
            p["glucose_unit_raw"] = "guessed"
        else:
            p["glucose_unit_raw"] = unit
        p["glucose_mgdl"] = round(value * 18) if unit == "mmoll" else value
        window = f[max(0, gm.start() - 60): gm.end() + 40]
        for name, pats in CONTEXTS:
            if any(re.search(x, window) for x in pats):
                p["glucose_context"] = name
                break
    if re.search(r"gia dinh (co nguoi|co ai)|bo me .*tieu duong|tien su gia dinh|"
                 r"(me|bo|ba|ong|anh|chi|em)( ruot)? (toi|minh) (bi|mac|tung bi) (benh )?tieu duong", f):
        p["family_history"] = True
    for label, pat in {**EMERGENCY_SYMPTOMS, **HYPO_SYMPTOMS, **HYPER_SYMPTOMS}.items():
        if label == "nôn / buồn nôn":  # "nôn" mất dấu trùng "non" (lá ổi non) → so trên chữ có dấu
            if re.search(r"(?<!\w)(buồn nôn|nôn)(?!\w)", low):
                p["symptoms"].append(label)
            continue
        if re.search(pat, f):
            p["symptoms"].append(label)
    return p


@tool
def check_red_flags(profile: dict) -> dict:
    """check_red_flags · Input: hồ sơ (dict) · Output: {"emergency": bool, "kind", "reasons"} —
    dấu hiệu cấp cứu được ưu tiên trước mọi dự đoán/tư vấn · Không tác động ra ngoài."""
    g, sym = profile.get("glucose_mgdl"), set(profile.get("symptoms") or [])
    if g is not None and g < 20:  # số không hợp lệ (vd 0) → validate_profile hỏi lại, không coi là hạ đường huyết
        g = None
    reasons, kind = [], None
    severe = sym & set(EMERGENCY_SYMPTOMS)
    if g is not None and g < 70 and (sym & set(HYPO_SYMPTOMS) or severe):
        kind = "ha_duong_huyet"
        reasons.append("đường huyết %g mg/dL (< 70) kèm %s" % (g, ", ".join(sorted(sym))))
    elif g is not None and g < 55:
        kind = "ha_duong_huyet"
        reasons.append("đường huyết %g mg/dL (< 55, hạ nặng)" % g)
    elif g is not None and g >= 250 and (severe or sym & set(HYPER_SYMPTOMS)):
        kind = "tang_duong_huyet_cap"
        reasons.append("đường huyết %g mg/dL kèm %s" % (g, ", ".join(sorted(sym))))
    elif {"tức ngực", "ngất", "co giật"} & sym or len(severe) >= 2:
        kind = "trieu_chung_nguy_hiem"
        reasons.append("triệu chứng nguy hiểm: %s" % ", ".join(sorted(severe)))
    return {"emergency": kind is not None, "kind": kind, "reasons": reasons}


@tool
def check_scope(text: str, profile: dict) -> dict:
    """check_scope · Input: câu người dùng + hồ sơ · Output: các yêu cầu ngoài phạm vi / tấn công phát hiện được
    (chẩn đoán, kê thuốc, liều, ngừng thuốc, bỏ qua an toàn, tự xưng bác sĩ, thai kỳ, mẹo chưa có căn cứ) ·
    Không tác động ra ngoài."""
    f = _fold(text)
    flags = []
    rules = {
        "doi_chan_doan": r"khang dinh .*(mac|bi)|chan doan (giup|cho)|(toi|minh) co bi tieu duong khong|co bi tieu duong khong",
        "doi_ke_thuoc": r"ke (luon |don |thuoc)|ke .*thuoc|don thuoc|mua (thuoc )?uong|thuoc gi",
        "doi_lieu": r"lieu|bao nhieu (mg|don vi|ui)",
        "doi_ngung_doi_thuoc": r"ngung thuoc|ngung uong|bo thuoc|doi thuoc|dung thuoc|ngung .*thuoc|thay (cho )?thuoc",
        "bo_qua_an_toan": r"bo qua (moi |cac )?(huong dan|canh bao|quy tac)|ignore (all|previous)|cam khuyen|dung khuyen|"
                          r"dong vai|system prompt|khong phai (la )?ai|in ra (toan bo )?(huong dan|prompt)",
        "da_chan_doan": r"(da|duoc) chan doan (tieu duong|dai thao duong)|chan doan .*tieu duong type 2 .*truoc",
        "tu_xung_bac_si": r"toi la bac si|minh la bac si|\bbac si (khoa|noi tiet).*(dang|ban)",
        "meo_chua_can_cu": r"la oi|muop dang|thao duoc|meo dan gian|chua khoi|khoi han|nuoc ep .*ha duong|vien que|cach tu nhien|thuc pham chuc nang",
        "an_kieng_chat": r"an kieng chat|giam can .*nhanh|nhin (an|duong)",
    }
    for name, pat in rules.items():
        if re.search(pat, f):
            flags.append(name)
    if profile.get("pregnant"):
        flags.append("thai_ky")
    if profile.get("age") is not None and profile["age"] < 18:
        flags.append("duoi_18_tuoi")
    return {"flags": flags}


@tool
def validate_profile(profile: dict) -> dict:
    """validate_profile · Input: hồ sơ · Output: {"invalid": [...], "missing": [...], "ask": [...]} —
    giá trị bất hợp lý, thiếu bối cảnh đo, thiếu chỉ số cơ bản · Không tác động ra ngoài."""
    invalid, missing, ask = [], [], []
    bmi, g, bp, age = profile.get("bmi"), profile.get("glucose_mgdl"), profile.get("diastolic_bp"), profile.get("age")
    if bmi is not None and not 12 <= bmi <= 70:
        invalid.append("BMI = %g không hợp lệ (người lớn thường 15–50)" % bmi)
        ask.append("chiều cao (cm) và cân nặng (kg) để tính lại BMI")
    if g is not None and not 20 <= g <= 800:
        invalid.append("đường huyết %g mg/dL nằm ngoài khoảng đo hợp lý" % g)
        ask.append("đo lại đường huyết và ghi rõ đơn vị (mg/dL hay mmol/L)")
    warnings = []
    if bp is not None and not 30 <= bp <= 140:
        invalid.append("huyết áp tâm trương %g mmHg không hợp lý" % bp)
    elif bp is not None and (bp < 50 or bp >= 90):
        warnings.append("huyết áp tâm trương %g mmHg nằm ngoài khoảng thường gặp, nên đo lại hoặc hỏi nhân viên y tế"
                        " (quy tắc an toàn của nhóm, không phải ngưỡng chẩn đoán)" % bp)
    if age is not None and not 1 <= age <= 110:
        invalid.append("tuổi %d không hợp lý" % age)
    if g is not None and profile.get("glucose_context") is None:
        missing.append("bối cảnh đo đường huyết")
        ask.append("đo lúc đói (nhịn ăn ≥ 8 giờ), sau ăn bao lâu, hay 2 giờ sau nghiệm pháp uống glucose tại cơ sở y tế")
    if profile.get("glucose_unit_raw") == "guessed":
        ask.append("đơn vị của số đường huyết (mg/dL hay mmol/L)")
    if g is None and profile.get("hba1c") is None:
        missing.append("chỉ số đường huyết hoặc HbA1c")
    if bmi is None:
        missing.append("BMI (hoặc chiều cao, cân nặng)")
        if g is not None and profile.get("glucose_context") is None:
            ask.append("chiều cao và cân nặng (để tính BMI)")
    if age is None:
        missing.append("tuổi")
    return {"invalid": invalid, "missing": missing, "ask": ask, "warnings": warnings}


@tool
def predict_risk(profile: dict) -> dict:
    """predict_risk · Input: hồ sơ · Output: điểm mô hình Logistic Regression train trên Pima (ml/model.json)
    nếu hồ sơ nằm trong phạm vi model; nếu không, {"eligible": False, "reason"} và KHÔNG có điểm ·
    Không tác động ra ngoài."""
    m = _MODEL
    reasons = []
    if profile.get("sex") != "female":
        reasons.append("model chỉ train trên phụ nữ (Pima)")
    if profile.get("pregnant"):
        reasons.append("đang mang thai")
    if profile.get("glucose_context") != "ogtt":
        reasons.append("cột Glucose của model là đường huyết 2 giờ sau nghiệm pháp (OGTT); số người dùng nhập không phải OGTT")
    vals = {"Glucose": profile.get("glucose_mgdl"), "BloodPressure": profile.get("diastolic_bp"),
            "BMI": profile.get("bmi"), "Age": profile.get("age")}
    for k, v in vals.items():
        if v is None:
            reasons.append("thiếu %s (không tự điền số thiếu)" % k)
        else:
            lo, hi = m["train_ranges"][k]
            if not lo <= v <= hi:
                reasons.append("%s = %g ngoài khoảng dữ liệu train [%g, %g]" % (k, v, lo, hi))
    if reasons:
        return {"eligible": False, "reason": "; ".join(reasons)}
    z = m["intercept"] + sum(m["coef"][k] * (vals[k] - m["scaler_mean"][k]) / m["scaler_scale"][k] for k in m["features"])
    prob = 1 / (1 + math.exp(-z))
    band = "thấp" if prob < 0.2 else ("trung bình" if prob < 0.5 else "cao")
    return {"eligible": True, "score": round(prob, 3), "band": band, "model": "logistic_regression (Pima, AUC test %.2f)" % m["test_auc"],
            "caveat": "Điểm tham khảo trên dữ liệu phụ nữ Pima (Mỹ), chưa kiểm định cho người Việt; không phải xác suất mắc bệnh."}


@tool
def assess_guidelines(profile: dict) -> dict:
    """assess_guidelines · Input: hồ sơ · Output: đối chiếu từng chỉ số với ngưỡng có nguồn (KB01–KB06):
    vùng của đường huyết theo đúng bối cảnh đo, HbA1c, BMI châu Á, yếu tố nguy cơ · Không tác động ra ngoài."""
    out, level = [], 0  # level: 0 bình thường, 1 có yếu tố nguy cơ, 2 vùng tiền tiểu đường, 3 ngưỡng tiểu đường
    g, ctx = profile.get("glucose_mgdl"), profile.get("glucose_context")
    if g is not None and ctx == "fasting":
        if g >= 126:
            out.append(("KB01", "đường huyết lúc đói %g mg/dL ≥ 126: ở ngưỡng tiểu đường, cần bác sĩ xác nhận bằng xét nghiệm lặp lại" % g)); level = max(level, 3)
        elif g >= 100:
            out.append(("KB01", "đường huyết lúc đói %g mg/dL trong vùng 100–125: vùng tiền tiểu đường" % g)); level = max(level, 2)
        else:
            out.append(("KB01", "đường huyết lúc đói %g mg/dL ≤ 99: trong ngưỡng bình thường" % g))
    elif g is not None and ctx == "ogtt":
        if g >= 200:
            out.append(("KB03", "đường huyết 2 giờ sau nghiệm pháp %g mg/dL ≥ 200: ở ngưỡng tiểu đường, cần bác sĩ xác nhận" % g)); level = max(level, 3)
        elif g >= 140:
            out.append(("KB03", "đường huyết 2 giờ sau nghiệm pháp %g mg/dL trong vùng 140–199: vùng tiền tiểu đường (rối loạn dung nạp glucose)" % g)); level = max(level, 2)
        else:
            out.append(("KB03", "đường huyết 2 giờ sau nghiệm pháp %g mg/dL < 140: trong ngưỡng bình thường" % g))
    elif g is not None:
        out.append(("KB04", "đường huyết %g mg/dL nhưng không rõ đo lúc nào nên chưa so được với ngưỡng" % g))
    a1c = profile.get("hba1c")
    if a1c is not None:
        if a1c >= 6.5:
            out.append(("KB02", "HbA1c %g%% ≥ 6,5%%: ở ngưỡng tiểu đường, cần bác sĩ xác nhận" % a1c)); level = max(level, 3)
        elif a1c >= 5.7:
            out.append(("KB02", "HbA1c %g%% trong vùng 5,7–6,4%%: tiền tiểu đường" % a1c)); level = max(level, 2)
        else:
            out.append(("KB02", "HbA1c %g%% < 5,7%%: bình thường" % a1c))
    bmi = profile.get("bmi")
    if bmi is not None and 12 <= bmi <= 70:
        if bmi >= 27.5:
            out.append(("KB05", "BMI %g ≥ 27,5: mức nguy cơ cao theo mốc cho người châu Á" % bmi)); level = max(level, 1)
        elif bmi >= 23:
            out.append(("KB05", "BMI %g ≥ 23: nguy cơ tăng theo mốc cho người châu Á (thừa cân)" % bmi)); level = max(level, 1)
        else:
            out.append(("KB05", "BMI %g < 23" % bmi))
    if profile.get("age") is not None and profile["age"] >= 45:
        out.append(("KB06", "tuổi %d ≥ 45 là một yếu tố nguy cơ" % profile["age"])); level = max(level, 1)
    if profile.get("family_history"):
        out.append(("KB06", "có người thân bị tiểu đường là một yếu tố nguy cơ")); level = max(level, 1)
    names = {0: "chưa thấy dấu hiệu tăng nguy cơ từ các chỉ số đã nhập", 1: "có yếu tố nguy cơ",
             2: "vùng tiền tiểu đường — nguy cơ cao", 3: "ở ngưỡng tiểu đường — cần đi khám sớm để xác nhận"}
    return {"findings": [{"source_id": s, "text": t} for s, t in out], "level": level, "summary": names[level]}


@tool
def retrieve_guidance(topics: list) -> list:
    """retrieve_guidance · Input: danh sách chủ đề/tag (list[str]) · Output: các đoạn KB đã kiểm nguồn khớp tag
    {source_id, title, content, source_url, version_or_date} — không có thì trả [] · Không tác động ra ngoài."""
    want = set(topics)
    hits = [e for e in _KB if want & set(e.get("tags", []))]
    return [{k: e[k] for k in ("source_id", "title", "content", "source_url", "version_or_date", "applicability", "limitations")}
            for e in hits]


DOSE = re.compile(r"\b\d+(?:[.,]\d+)?\s*(mg|mcg|đơn vị|don vi|ui|iu|viên|vien|ml)\b(?!\s*/\s*dl)", re.I)


@tool
def validate_response(text: str, route: str, required: list) -> dict:
    """validate_response · Input: câu trả lời của model, tuyến xử lý, các ý bắt buộc · Output: {"ok", "problems"} —
    chặn liều thuốc, khẳng định chẩn đoán, khuyên ngừng thuốc, thiếu chỉ dẫn cấp cứu · Không tác động ra ngoài."""
    f = _fold(text)
    problems = []
    for m in DOSE.finditer(text):
        ctx = _fold(text[max(0, m.start() - 40): m.end() + 10])
        if re.search(r"metformin|insulin|thuoc|lieu|tiem|uong", ctx) and not re.search(r"duong|glucose|carb|tinh bot", ctx):
            problems.append("có số liều thuốc: %r" % m.group(0))
    if re.search(r"ban (da )?(bi|mac) (benh )?tieu duong(?! (hay|khong))|chac chan (ban )?(bi|mac)|khang dinh ban (bi|mac)", f) \
            and not re.search(r"khong (the )?khang dinh|chua the (ket luan|khang dinh)", f):
        problems.append("có câu khẳng định chẩn đoán")
    if re.search(r"(nen|hay|co the) (ngung|bo|dung|giam) (uong )?thuoc", f) and not re.search(r"khong (nen|duoc) (tu )?(ngung|bo|dung|giam)", f):
        problems.append("có lời khuyên ngừng/giảm thuốc")
    if re.search(r"khong (bi|mac) tieu duong|loai tru tieu duong", f):
        problems.append("khẳng định không mắc bệnh")
    for req in required:
        if req == "115" and "115" not in text:
            problems.append("thiếu chỉ dẫn gọi 115 / đi cấp cứu")
        if req == "kham" and not re.search(r"bac si|kham|co so y te|xet nghiem", f):
            problems.append("thiếu khuyến nghị gặp nhân viên y tế")
    return {"ok": not problems, "problems": problems}
