"""Đào data câu hỏi công khai về tiểu đường — Medical Sciences Stack Exchange (CC BY-SA 4.0).

Cách đếm chốt trước ở evidence/data-mining.md mục 1. Luật từ khoá dưới đây viết TRƯỚC khi xem kết quả.
Chạy:   python evidence/mine_stackexchange.py            (tải qua API, ghi evidence/mining_labels.csv)
        python evidence/mine_stackexchange.py --offline  (đếm lại từ evidence/mining_labels.csv, gồm cả nhãn đọc tay)
Riêng tư: chỉ lưu question_id, ngày, tiêu đề, nhãn, trích đoạn ≤ 200 ký tự — không lưu tên tài khoản.
Chỉ dùng thư viện chuẩn.
"""
import csv
import gzip
import html
import json
import os
import re
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "mining_labels.csv")
API = ("https://api.stackexchange.com/2.3/questions?order=asc&sort=creation&site=medicalsciences"
       "&tagged=%s&pagesize=100&page=%d&filter=withbody")
TAGS = ["diabetes", "blood-sugar"]

NUM_UNIT = r"\b\d+(?:[.,]\d+)?\s*(?:mg\s*/\s*dl|mmol\s*/?\s*l|%|kg\b|lbs?\b)"
SELF = r"\b(my|i|i'm|i am|i've|me|mine|my (?:mother|mom|father|dad|wife|husband|son|daughter|friend|brother|sister|grandmother|grandfather))\b"
RULES = {
    # L1: chỉ số đo cụ thể của chính mình / người thân, kèm số
    "L1_so_cua_minh": lambda t: bool(re.search(SELF, t)) and bool(
        re.search(r"(glucose|sugar|a1c|hba1c|bmi|weigh)[^.?!]{0,80}" + NUM_UNIT + "|" + NUM_UNIT + r"[^.?!]{0,60}(glucose|sugar|a1c|hba1c|reading|level)", t)),
    # L2: hỏi số đó nghĩa là gì / bình thường không / đáng lo / có phải tiểu đường
    "L2_hoi_dien_giai": lambda t: bool(re.search(
        r"\b(is (this|that|it|my \w+) (normal|high|low|bad|dangerous|concerning|ok|okay)|should i (be )?(worried|concerned)|"
        r"do i have (diabetes|prediabetes)|am i (diabetic|prediabetic|at risk)|does (this|that) mean|what does (this|that|it) mean|"
        r"is (this|that) (diabetes|prediabetes)|could (this|i|it) be (diabetes|diabetic|prediabetes)|normal range|considered (high|normal))\b", t)),
    # L3: hỏi nên làm gì tiếp (ăn, vận động, đi khám / xét nghiệm)
    "L3_hoi_buoc_tiep": lambda t: bool(re.search(
        r"\b(what should i (do|eat)|should i (see|go to|get|visit|ask)|do i need to (see|get|go)|what (can|could) i do|"
        r"how (can|do) i (lower|reduce|prevent|bring down|control)|what (test|tests) should|next step)\b", t)),
    # L4: không rõ / nhầm bối cảnh đo hoặc đơn vị
    "L4_boi_canh_do": lambda t: bool(re.search(
        r"\b(fasting or|before or after|after (eating|meal)s? or|which (reading|number|test)|mg/dl (or|vs|to) mmol|mmol (or|vs|to) mg|"
        r"difference between (fasting|a1c|hba1c)|(random|fasting) (vs|versus)|convert)\b", t)),
}


def fetch_all():
    seen = {}
    for tag in TAGS:
        page = 1
        while True:
            req = urllib.request.Request(API % (tag, page), headers={"Accept-Encoding": "gzip", "User-Agent": "edu-hackathon-script"})
            raw = urllib.request.urlopen(req, timeout=30).read()
            data = json.loads(gzip.decompress(raw) if raw[:2] == b"\x1f\x8b" else raw)
            for q in data.get("items", []):
                seen[q["question_id"]] = q
            if not data.get("has_more"):
                break
            page += 1
            time.sleep(max(1, data.get("backoff", 0)))
    return [seen[k] for k in sorted(seen)]


def clean(body):
    t = re.sub(r"<[^>]+>", " ", body or "")
    return re.sub(r"\s+", " ", html.unescape(t)).strip()


def label(q):
    text = (html.unescape(q["title"]) + " . " + clean(q.get("body", ""))).lower()
    return {k: int(f(text)) for k, f in RULES.items()}, text


def report(rows):
    N = len(rows)
    col = lambda r, k: int(r.get(k + "_tay") or r[k]) if (r.get(k + "_tay") or "").strip() != "" else int(r[k])
    for src, get in (("luật từ khoá", lambda r, k: int(r[k])), ("sau đọc tay (nếu có)", col)):
        c = {k: sum(get(r, k) for r in rows) for k in RULES}
        pain = sum(1 for r in rows if get(r, "L2_hoi_dien_giai") or get(r, "L3_hoi_buoc_tiep"))
        l1 = [r for r in rows if get(r, "L1_so_cua_minh")]
        l1_pain = sum(1 for r in l1 if get(r, "L2_hoi_dien_giai") or get(r, "L3_hoi_buoc_tiep"))
        print("== %s · N = %d câu hỏi" % (src, N))
        for k, v in c.items():
            print("  %-18s %3d/%d (%.1f%%)" % (k, v, N, 100 * v / N))
        print("  L2 ∪ L3           %3d/%d (%.1f%%)" % (pain, N, 100 * pain / N))
        if l1:
            print("  L1 ∩ (L2 ∪ L3)    %3d/%d trong L1 (%.1f%%)" % (l1_pain, len(l1), 100 * l1_pain / len(l1)))


def main():
    if "--offline" in sys.argv:
        rows = list(csv.DictReader(open(OUT, encoding="utf-8")))
        return report(rows)
    qs = fetch_all()
    rows = []
    for q in qs:
        labels, text = label(q)
        rows.append({"question_id": q["question_id"], "link": "https://medicalsciences.stackexchange.com/q/%d" % q["question_id"],
                     "creation_date": time.strftime("%Y-%m-%d", time.gmtime(q["creation_date"])),
                     "title": html.unescape(q["title"]), **labels,
                     **{k + "_tay": "" for k in RULES}, "excerpt": clean(q.get("body", ""))[:200], "ghi_chu_tay": ""})
    with open(OUT, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print("Tải %d câu hỏi (tag: %s) lúc %s UTC → %s" % (len(rows), ", ".join(TAGS), time.strftime("%Y-%m-%d %H:%M", time.gmtime()), OUT))
    report(rows)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
