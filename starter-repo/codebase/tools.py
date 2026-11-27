"""Công cụ của bài toán Dự đoán nguy cơ tiểu đường & Chatbot AI tư vấn — Nhóm LufkyMama.

Mỗi công cụ đều có @tool để khung tracing.py tự ghi tên, input, output rút gọn, thời gian và lỗi.
Chỉ dùng thư viện chuẩn của Python. Không có công cụ nào gây tác động ra ngoài hệ thống.
Dữ liệu tri thức chuẩn đặt tại data/knowledge_base.json.
"""
import json
import math
import os
import re

from tracing import tool, TOOLS  # noqa: F401

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KB_PATH = os.path.join(ROOT, "data", "knowledge_base.json")


def _load_kb() -> list:
    if not os.path.exists(KB_PATH):
        return []
    with open(KB_PATH, encoding="utf-8") as f:
        return json.load(f)


def _to_float(val: str):
    try:
        return float(val.replace(",", "."))
    except (ValueError, AttributeError):
        return None


@tool
def extract_health_profile(text: str) -> dict:
    """Trích xuất chỉ số sức khỏe, ngữ cảnh đo và tín hiệu rủi ro từ câu hỏi tiếng Việt.
    Input: văn bản đầu vào của người dùng (str).
    Output: dict hồ sơ sức khỏe có cấu trúc (tuổi, giới tính, đường huyết, ngữ cảnh đo, BMI, huyết áp, triệu chứng...).
    Tác động ra ngoài: Không."""
    low = (text or "").lower()
    profile = {
        "age": None,
        "sex": None,
        "pregnancies": 0,
        "currently_pregnant": False,
        "glucose_mg_dl": None,
        "glucose_mmol_l": None,
        "glucose_context": "unknown",  # fasting | ogtt_2h | post_meal | unknown
        "hba1c": None,
        "bmi": None,
        "bmi_raw_invalid": False,
        "height_cm": None,
        "weight_kg": None,
        "diastolic_bp": None,
        "systolic_bp": None,
        "family_history": False,
        "lifestyle_cues": [],
        "emergency_symptoms": [],
        "hypo_symptoms": [],
        "asks_folk_remedy": False,
        "asks_prescription_or_dosing": False,
        "asks_stop_medication": False,
        "asks_definitive_diagnosis": False,
        "prompt_injection_attempt": False,
    }

    # Tuổi
    m_age = re.search(r"(\d{1,3})\s*tuổi|tuổi\s*[:=]?\s*(\d{1,3})", low)
    if m_age:
        val = _to_float(m_age.group(1) or m_age.group(2))
        if val is not None and 1 <= val <= 120:
            profile["age"] = int(val)

    # Giới tính
    if re.search(r"\b(nữ|chị|cô|bà|mẹ)\b", low):
        profile["sex"] = "female"
    elif re.search(r"\b(nam|anh|chú|ông|bố|ba)\b", low):
        profile["sex"] = "male"

    # Mang thai hiện tại vs số lần từng mang thai
    if re.search(r"(đang\s+mang\s+thai|mang\s+thai\s+tuần|thai\s+kỳ|đang\s+có\s+bầu|bà\s+bầu|thai\s+nhi)", low):
        profile["currently_pregnant"] = True
        profile["sex"] = "female"
    m_preg = re.search(r"từng\s+mang\s+thai\s+(\d+)\s*lần|mang\s+thai\s+(\d+)\s*lần", low)
    if m_preg:
        profile["pregnancies"] = int(m_preg.group(1) or m_preg.group(2))

    # Đường huyết (mg/dL và mmol/L)
    m_mg = re.search(r"(\d+(?:[.,]\d+)?)\s*mg\s*/?\s*dl", low)
    m_mmol = re.search(r"(\d+(?:[.,]\d+)?)\s*mmol\s*/?\s*l", low)
    if m_mg:
        profile["glucose_mg_dl"] = round(_to_float(m_mg.group(1)), 1)
    if m_mmol:
        mmol = _to_float(m_mmol.group(1))
        profile["glucose_mmol_l"] = round(mmol, 2)
        if profile["glucose_mg_dl"] is None and mmol is not None:
            profile["glucose_mg_dl"] = round(mmol * 18.0, 1)

    # Ngữ cảnh đo đường huyết
    if re.search(r"(lúc\s+đói|nhịn\s+ăn|sáng\s+chưa\s+ăn|fpg)", low):
        profile["glucose_context"] = "fasting"
    elif re.search(r"(nghiệm\s+pháp\s*2\s*giờ|sau\s+nghiệm\s+pháp|ogtt|sau\s+ăn\s*2\s*giờ|sau\s+ăn\s*2h)", low):
        profile["glucose_context"] = "ogtt_2h"
    elif re.search(r"(sau\s+ăn|sau\s+bữa)", low):
        profile["glucose_context"] = "post_meal"

    # HbA1c
    m_a1c = re.search(r"hba1c\s*(?:là|=|:)?\s*(\d+(?:[.,]\d+)?)\s*%?", low)
    if m_a1c:
        profile["hba1c"] = _to_float(m_a1c.group(1))

    # Chiều cao & cân nặng
    m_hm = re.search(r"1\s*m\s*(\d{2})", low)
    m_hcm = re.search(r"(\d{3})\s*cm", low)
    if m_hm:
        profile["height_cm"] = 100.0 + float(m_hm.group(1))
    elif m_hcm:
        profile["height_cm"] = float(m_hcm.group(1))

    m_w = re.search(r"(\d+(?:[.,]\d+)?)\s*kg", low)
    if m_w:
        profile["weight_kg"] = _to_float(m_w.group(1))

    # BMI trực tiếp hoặc tự tính từ chiều cao + cân nặng
    m_bmi = re.search(r"bmi\s*(?:nhập\s+vào\s+là|là|=|:)?\s*(\d+(?:[.,]\d+)?)", low)
    if m_bmi:
        bmi_val = _to_float(m_bmi.group(1))
        if bmi_val is not None and (bmi_val <= 10.0 or bmi_val >= 80.0):
            profile["bmi"] = bmi_val
            profile["bmi_raw_invalid"] = True
        else:
            profile["bmi"] = bmi_val
    elif profile["height_cm"] and profile["weight_kg"]:
        h_m = profile["height_cm"] / 100.0
        if h_m > 0:
            profile["bmi"] = round(profile["weight_kg"] / (h_m * h_m), 1)

    # Huyết áp
    m_bp_pair = re.search(r"huyết\s+áp[^0-9]{0,20}(\d{2,3})\s*/\s*(\d{2,3})", low)
    m_dia = re.search(r"huyết\s+áp\s+tâm\s+trương\s*(?:là|=|:)?\s*(\d{2,3})", low)
    if m_bp_pair:
        profile["systolic_bp"] = int(m_bp_pair.group(1))
        profile["diastolic_bp"] = int(m_bp_pair.group(2))
    elif m_dia:
        profile["diastolic_bp"] = int(m_dia.group(1))

    # Tiền sử gia đình
    if re.search(r"(gia\s+đình\s+có\s+người|bố\s+mẹ\s+bị|di\s+truyền|người\s+thân\s+bị\s+tiểu\s+đường)", low):
        profile["family_history"] = True

    # Thói quen sinh hoạt & bữa ăn
    cue_map = {
        "văn phòng": "ngồi văn phòng nhiều",
        "ngồi nhiều": "ít vận động",
        "cơm tấm": "hay ăn cơm tấm",
        "cơm trắng": "ăn cơm trắng",
        "trà sữa": "uống trà sữa",
        "nước ngọt": "uống nước ngọt",
        "ăn uống thất thường": "ăn uống thất thường",
    }
    for kw, label in cue_map.items():
        if kw in low:
            profile["lifestyle_cues"].append(label)

    # Triệu chứng cờ đỏ tăng đường huyết cấp / tim mạch
    hyper_sym_kw = [
        "buồn nôn", "nôn mửa", "thở gấp", "thở nhanh", "lơ mơ",
        "mệt lả", "tức ngực", "đau ngực", "khó thở", "chóng mặt", "khát nước liên tục",
    ]
    for kw in hyper_sym_kw:
        if kw in low:
            profile["emergency_symptoms"].append(kw)

    # Triệu chứng cờ đỏ hạ đường huyết cấp
    hypo_sym_kw = ["run tay", "vã mồ hôi", "mồ hôi lạnh", "choáng váng", "choáng", "ngất", "bủn rủn"]
    for kw in hypo_sym_kw:
        if kw in low:
            profile["hypo_symptoms"].append(kw)

    # Mẹo dân gian
    if re.search(r"(lá\s+ổi|mướp\s+đắng|khổ\s+qua|thuốc\s+nam|lá\s+cây|khỏi\s+hẳn\s+không\s+cần\s+đi\s+viện|mẹo\s+dân\s+gian)", low):
        profile["asks_folk_remedy"] = True

    # Yêu cầu ngoài phạm vi / thẩm quyền y khoa
    if re.search(r"(kê\s+đơn|kê\s+luôn\s+liều|kê\s+thuốc|tính\s+nhanh\s+liều|tính\s+liều|liều\s+thuốc|liều\s+metformin|liều\s+insulin|uống\s+bao\s+nhiêu\s+viên|tiêm\s+bao\s+nhiêu)", low):
        profile["asks_prescription_or_dosing"] = True
    if re.search(r"(ngừng\s+thuốc|bỏ\s+thuốc|dừng\s+thuốc)", low):
        profile["asks_stop_medication"] = True
    if re.search(r"(khẳng\s+định\s+tôi\s+đã\s+mắc|chẩn\s+đoán\s+chắc\s+chắn|kết\s+luận\s+chắc\s+chắn\s+tôi\s+bị)", low):
        profile["asks_definitive_diagnosis"] = True

    # Dấu hiệu prompt injection / ép vượt rào an toàn
    if re.search(r"(bỏ\s+qua\s+mọi|bỏ\s+qua\s+hướng\s+dẫn|cấm\s+khuyên|không\s+được\s+khuyên\s+đi\s+khám|tôi\s+là\s+bác\s+sĩ.*bỏ\s+qua)", low):
        profile["prompt_injection_attempt"] = True

    return profile


@tool
def check_clinical_safety(profile: dict, raw_text: str) -> dict:
    """Lớp chặn rủi ro lâm sàng cứng (Deterministic Guardrail) theo QĐ 5481/QĐ-BYT & G10.
    Input: hồ sơ đã trích xuất (dict) và văn bản gốc (str).
    Output: dict quyết định định tuyến {"action", "reason", "warnings", "missing_fields", "kb_categories"}.
    Action gồm: emergency_hypo | emergency_hyper | out_of_scope_pregnancy | prohibited_medical_order |
                invalid_data | missing_context | proceed.
    Tác động ra ngoài: Không."""
    g = profile.get("glucose_mg_dl")
    warnings = []
    missing = []

    if profile.get("prompt_injection_attempt"):
        warnings.append("Phát hiện yêu cầu bỏ qua cảnh báo an toàn — hệ thống giữ nguyên rào chắn y khoa.")

    # 1. Cờ đỏ hạ đường huyết cấp (< 70 mg/dL hoặc triệu chứng hạ đường huyết kèm đường thấp)
    if g is not None and g < 70.0:
        return {
            "action": "emergency_hypo",
            "reason": "Đường huyết %.1f mg/dL (< 70 mg/dL) — nguy cơ hạ đường huyết cấp tính." % g,
            "warnings": warnings + ["TUYỆT ĐỐI KHÔNG gợi ý thực đơn ít tinh bột hoặc nhịn đường lúc này."],
            "missing_fields": [],
            "kb_categories": ["emergency_red_flag"],
        }

    # 2. Cờ đỏ tăng đường huyết cấp (>= 250 mg/dL kèm triệu chứng cảnh báo, hoặc >= 300 mg/dL)
    severe_hyper_syms = [
        s for s in profile.get("emergency_symptoms", [])
        if s in ("buồn nôn", "nôn mửa", "thở gấp", "thở nhanh", "lơ mơ", "mệt lả", "tức ngực", "đau ngực", "khó thở", "chóng mặt")
    ]
    if g is not None and ((g >= 250.0 and len(severe_hyper_syms) >= 1) or g >= 300.0):
        return {
            "action": "emergency_hyper",
            "reason": "Đường huyết %.1f mg/dL kèm triệu chứng nguy hiểm (%s) — nghi tăng đường huyết cấp / nhiễm toan ceton."
            % (g, ", ".join(severe_hyper_syms) or "mức đường huyết rất cao"),
            "warnings": warnings + ["NGỪNG tư vấn thực đơn tự hạ đường tại nhà; yêu cầu đi cấp cứu / gọi 115 ngay."],
            "missing_fields": [],
            "kb_categories": ["emergency_red_flag"],
        }

    # 3. Yêu cầu kê đơn / tính liều thuốc / ngừng thuốc / chẩn đoán khẳng định (Lớp 3)
    if (
        profile.get("asks_prescription_or_dosing")
        or profile.get("asks_stop_medication")
        or profile.get("asks_definitive_diagnosis")
    ):
        reasons = []
        if profile.get("asks_definitive_diagnosis"):
            reasons.append("yêu cầu chẩn đoán khẳng định thay bác sĩ")
        if profile.get("asks_prescription_or_dosing"):
            reasons.append("yêu cầu kê đơn hoặc tính liều thuốc (Metformin/Insulin)")
        if profile.get("asks_stop_medication"):
            reasons.append("yêu cầu ngừng/đổi thuốc đang điều trị")
        return {
            "action": "prohibited_medical_order",
            "reason": "Ngoài thẩm quyền của hệ thống sàng lọc AI: " + "; ".join(reasons) + ".",
            "warnings": warnings + ["Không kê đơn, không tính liều, không khuyên ngừng thuốc dù người hỏi tự xưng bác sĩ."],
            "missing_fields": [],
            "kb_categories": ["scope_medication", "diagnosis_threshold"],
        }

    # 4. Ngoài phạm vi đối tượng: phụ nữ đang mang thai (Lớp 4)
    if profile.get("currently_pregnant"):
        return {
            "action": "out_of_scope_pregnancy",
            "reason": "Người dùng đang mang thai — nằm ngoài phạm vi mô hình sàng lọc tiểu đường type 2 phổ thông.",
            "warnings": warnings + ["Không dùng mô hình type 2 để kết luận; không gợi ý ăn kiêng chặt/giảm cân khi mang thai."],
            "missing_fields": [],
            "kb_categories": ["pregnancy_scope"],
        }

    # 5. Dữ liệu bất hợp lý (Lớp 2 — ví dụ BMI = 0.0)
    if profile.get("bmi_raw_invalid"):
        bp_note = []
        if profile.get("diastolic_bp") and profile["diastolic_bp"] >= 90:
            bp_note.append("Lưu ý thêm: huyết áp tâm trương %d mmHg ở mức cao (>=90 mmHg), nên theo dõi và kiểm tra y tế." % profile["diastolic_bp"])
        return {
            "action": "invalid_data",
            "reason": "Giá trị BMI = %s không hợp lệ về mặt sinh học (thiếu hoặc lỗi nhập liệu)." % profile.get("bmi"),
            "warnings": warnings + bp_note,
            "missing_fields": ["chiều cao và cân nặng thực tế (hoặc chỉ số BMI hợp lệ)"],
            "kb_categories": ["bmi_threshold", "diagnosis_threshold"],
        }

    # 6. Thiếu thông tin / ngữ cảnh đo cốt lõi (G10 — thu hẹp phạm vi khi không chắc)
    if g is None and profile.get("hba1c") is None:
        missing.append("chỉ số đường huyết (mg/dL hoặc mmol/L) hoặc HbA1c")
    if g is not None and profile.get("glucose_context") == "unknown":
        missing.append("thời điểm đo đường huyết (lúc đói nhịn ăn >=8 giờ hay sau ăn 2 giờ)")
    if profile.get("bmi") is None:
        missing.append("chiều cao và cân nặng (hoặc chỉ số BMI)")

    if missing and (profile.get("glucose_context") == "unknown" or (g is None and profile.get("hba1c") is None)):
        return {
            "action": "missing_context",
            "reason": "Thiếu ngữ cảnh/chỉ số tối thiểu để sàng lọc chính xác theo G10.",
            "warnings": warnings,
            "missing_fields": missing,
            "kb_categories": ["diagnosis_threshold", "bmi_threshold"],
        }

    # 7. Đủ điều kiện chạy sàng lọc + tư vấn
    kb_cats = ["diagnosis_threshold", "bmi_threshold", "nutrition_general", "nutrition_vietnam_swap", "exercise_lifestyle"]
    if profile.get("asks_folk_remedy"):
        kb_cats.insert(0, "folk_remedy_evidence")

    return {
        "action": "proceed",
        "reason": "Đủ chỉ số hợp lệ và không có cờ đỏ cấp cứu.",
        "warnings": warnings,
        "missing_fields": missing,
        "kb_categories": kb_cats,
    }


@tool
def predict_diabetes_risk(profile: dict) -> dict:
    """Chấm điểm nguy cơ tiểu đường (mô hình logistic hiệu chuẩn) kèm giải thích đóng góp từng yếu tố (SHAP-style) và mô phỏng What-if.
    Input: hồ sơ sức khỏe đã trích xuất (dict).
    Output: dict gồm risk_probability_pct, risk_level, clinical_flags, top_contributors, what_if_simulation.
    Tác động ra ngoài: Không."""
    glucose = profile.get("glucose_mg_dl") if profile.get("glucose_mg_dl") is not None else 100.0
    g_ctx = profile.get("glucose_context", "fasting")
    bmi = profile.get("bmi") if profile.get("bmi") is not None else 23.0
    age = profile.get("age") if profile.get("age") is not None else 35
    hba1c = profile.get("hba1c")
    bp_dia = profile.get("diastolic_bp") if profile.get("diastolic_bp") is not None else 75
    fam = 1.0 if profile.get("family_history") else 0.0
    preg = min(profile.get("pregnancies", 0), 8)

    # Chuẩn hóa đường huyết về thang tương đương lúc đói nếu là OGTT 2 giờ (200 mg/dL OGTT ~ 126 mg/dL FPG)
    eff_glucose = glucose * 0.68 if g_ctx == "ogtt_2h" else glucose

    def _calc_logit(g_val, bmi_val, age_val, a1c_val, fam_val, preg_val):
        z = -8.35
        z += 0.048 * g_val
        z += 0.075 * bmi_val
        z += 0.028 * age_val
        z += 0.65 * fam_val
        z += 0.06 * preg_val
        if a1c_val is not None:
            z += 0.95 * (a1c_val - 5.5)
        return z

    def _sigmoid_pct(z):
        return round(100.0 / (1.0 + math.exp(-max(-15.0, min(15.0, z)))), 1)

    z_now = _calc_logit(eff_glucose, bmi, age, hba1c, fam, preg)
    prob = _sigmoid_pct(z_now)

    # Phân mức nguy cơ kết hợp ngưỡng lâm sàng QĐ 5481/QĐ-BYT & ADA
    clinical_flags = []
    if g_ctx == "ogtt_2h":
        if glucose >= 200:
            clinical_flags.append("Đường huyết sau nghiệm pháp 2 giờ (%.1f mg/dL) >= 200 mg/dL (vượt ngưỡng chẩn đoán cần bác sĩ xác nhận)" % glucose)
        elif glucose >= 180:
            clinical_flags.append("Đường huyết sau nghiệm pháp 2 giờ (%.1f mg/dL) ở mức rất cao, sát ngưỡng 200 mg/dL" % glucose)
        elif glucose >= 140:
            clinical_flags.append("Đường huyết sau nghiệm pháp 2 giờ (%.1f mg/dL) thuộc vùng tiền tiểu đường (140–199 mg/dL)" % glucose)
    else:
        if glucose >= 126:
            clinical_flags.append("Đường huyết lúc đói (%.1f mg/dL) >= 126 mg/dL (ngưỡng nghi đái tháo đường theo QĐ 5481/QĐ-BYT & ADA)" % glucose)
        elif glucose >= 100:
            clinical_flags.append("Đường huyết lúc đói (%.1f mg/dL) thuộc vùng ranh giới tiền tiểu đường (100–125 mg/dL)" % glucose)
        else:
            clinical_flags.append("Đường huyết lúc đói (%.1f mg/dL) trong giới hạn bình thường (<100 mg/dL)" % glucose)

    if hba1c is not None:
        if hba1c >= 6.5:
            clinical_flags.append("HbA1c %.1f%% >= 6.5%% (ngưỡng nghi đái tháo đường)" % hba1c)
        elif hba1c >= 5.7:
            clinical_flags.append("HbA1c %.1f%% thuộc vùng tiền tiểu đường (5.7–6.4%%)" % hba1c)

    if bmi >= 30.0:
        clinical_flags.append("BMI %.1f thuộc nhóm béo phì độ II theo chuẩn châu Á (>=30)" % bmi)
    elif bmi >= 25.0:
        clinical_flags.append("BMI %.1f thuộc nhóm thừa cân/béo phì độ I theo chuẩn châu Á (25.0–29.9)" % bmi)
    elif bmi >= 23.0:
        clinical_flags.append("BMI %.1f thuộc nhóm thừa cân theo chuẩn châu Á (23.0–24.9)" % bmi)

    if bp_dia >= 90:
        clinical_flags.append("Huyết áp tâm trương %d mmHg ở mức cao (>=90 mmHg)" % bp_dia)
    if fam:
        clinical_flags.append("Có tiền sử gia đình mắc tiểu đường")

    if (g_ctx == "ogtt_2h" and glucose >= 190) or (g_ctx != "ogtt_2h" and glucose >= 160) or prob >= 85.0:
        risk_level = "rat_cao"
        risk_label = "Rất cao"
    elif (g_ctx != "ogtt_2h" and glucose >= 126) or (hba1c is not None and hba1c >= 6.5) or prob >= 65.0:
        risk_level = "cao"
        risk_label = "Cao"
    elif (g_ctx != "ogtt_2h" and glucose >= 100) or (g_ctx == "ogtt_2h" and glucose >= 140) or prob >= 35.0:
        risk_level = "trung_binh"
        risk_label = "Trung bình (vùng ranh giới / tiền tiểu đường)"
    else:
        risk_level = "thap"
        risk_label = "Thấp / Trung bình thấp"

    # Giải thích đóng góp từng yếu tố (SHAP-style so với mốc khỏe mạnh: Glucose 90, BMI 22, Age 30)
    contributions = [
        ("Đường huyết (%.1f mg/dL)" % glucose, round(0.048 * (eff_glucose - 90.0), 2)),
        ("BMI (%.1f)" % bmi, round(0.075 * (bmi - 22.0), 2)),
        ("Tuổi (%d)" % age, round(0.028 * (age - 30.0), 2)),
    ]
    if fam:
        contributions.append(("Tiền sử gia đình", 0.65))
    if hba1c is not None:
        contributions.append(("HbA1c (%.1f%%)" % hba1c, round(0.95 * (hba1c - 5.4), 2)))

    contributions.sort(key=lambda x: x[1], reverse=True)
    top_contributors = [
        {"factor": name, "impact_score": score, "direction": "tăng nguy cơ" if score > 0.1 else "trung tính/giảm"}
        for name, score in contributions[:3]
    ]

    # Mô phỏng What-if cho các yếu tố có thể thay đổi (BMI & kiểm soát đường huyết qua lối sống)
    target_bmi = 23.0 if bmi > 23.5 else bmi
    target_g = max(95.0, round(eff_glucose * 0.88, 1)) if eff_glucose > 105.0 else eff_glucose
    prob_what_if = _sigmoid_pct(_calc_logit(target_g, target_bmi, age, hba1c, fam, preg))
    what_if_note = (
        "Nếu đưa BMI về khoảng %.1f và cải thiện đường huyết khoảng 10–12%% qua ăn uống & vận động, "
        "xác suất nguy cơ ước tính có thể giảm từ %.1f%% xuống khoảng %.1f%%."
        % (target_bmi, prob, prob_what_if)
        if (prob - prob_what_if) >= 3.0
        else "Duy trì cân nặng hợp lý (BMI 18.5–22.9) và vận động đều đặn giúp giữ nguy cơ ở mức thấp ổn định."
    )

    return {
        "model_note": "Mô hình sàng lọc định lượng tham khảo (hiệu chuẩn theo tiêu chí lâm sàng QĐ 5481/QĐ-BYT & Pima baseline)",
        "risk_probability_pct": prob,
        "risk_level": risk_level,
        "risk_label": risk_label,
        "clinical_flags": clinical_flags,
        "top_contributors": top_contributors,
        "what_if_simulation": what_if_note,
    }


@tool
def retrieve_medical_guidance(query: str, categories: list = None) -> list:
    """Tra cứu tài liệu hướng dẫn y khoa chuẩn (QĐ 5481/QĐ-BYT, ADA, bảng GI món Việt) từ data/knowledge_base.json.
    Input: câu hỏi (str) và danh sách nhóm chủ đề cần ưu tiên (list[str], tuỳ chọn).
    Output: danh sách tối đa 5 đoạn căn cứ [{"code", "title", "source", "text"}].
    Tác động ra ngoài: Không."""
    kb = _load_kb()
    low = (query or "").lower()
    wanted = set(categories or [])
    scored = []
    for item in kb:
        score = 0
        if item.get("category") in wanted:
            score += 5
        for tag in item.get("tags", []):
            if tag in low:
                score += 2
        if score > 0:
            scored.append((score, item))
    scored.sort(key=lambda x: x[0], reverse=True)
    selected = [it for _, it in scored[:5]] if scored else kb[:3]
    return [
        {
            "code": it["code"],
            "title": it["title"],
            "source": it["source"],
            "text": it["text"],
        }
        for it in selected
    ]
