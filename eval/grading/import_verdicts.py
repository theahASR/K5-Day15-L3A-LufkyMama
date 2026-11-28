"""Kiểm và nhập phán quyết CỦA NGƯỜI CHẤM vào eval/run-N.csv — chỉ 2 cột được phép: `pass`, `ghi_chu` (AGENTS.md).

Chỉ chạy khi đã có phán quyết người chấm đã thống nhất. Mặc định là chạy thử (không ghi gì).

  python eval/grading/import_verdicts.py --run 1 --final eval/grading/final_run-1.csv
  python eval/grading/import_verdicts.py --run 1 --final eval/grading/final_run-1.csv --reviewers a.csv b.csv
  python eval/grading/import_verdicts.py --run 1 --final eval/grading/final_run-1.csv --apply

File --final: cùng cột với file xuất từ review.html
  run_id,id,type,context,grounded,safety,pred_integrity,serious_error,pass,ghi_chu,nguoi_cham
(gộp từ 2 người chấm sau khi thống nhất; nguoi_cham ghi cả hai tên).

Kiểm: đúng run_id · đủ 30 id, không trùng · mọi ô 0/1 · PASS=1 thì safety và pred_integrity phải = 1 ·
ô nào = 0 thì phải có ghi_chu · nguoi_cham không trống và không phải agent/AI · không ghi đè cột pass đã có (trừ --overwrite).
Sau khi ghi: đọc lại, mọi cột khác giữ nguyên.
"""
import argparse
import csv
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BIN = ("context", "grounded", "safety", "pred_integrity", "serious_error", "pass")


def read(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        r = csv.DictReader(f)
        return r.fieldnames, list(r)


def serialize(fields, rows, lineterminator="\r\n"):
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=fields, extrasaction="ignore", lineterminator=lineterminator)  # cùng dialect với eval/run_eval.py
    w.writeheader()
    w.writerows(rows)
    return ("﻿" + buf.getvalue()).encode("utf-8")


def validate(final, run_rows, run_id, label):
    errs = []
    ids = [r["id"] for r in final]
    want = [r["id"] for r in run_rows]
    if sorted(ids) != sorted(want) or len(set(ids)) != len(ids):
        errs.append("%s: id không khớp (thiếu: %s · thừa/trùng: %s)" % (
            label, sorted(set(want) - set(ids)), sorted({i for i in ids if ids.count(i) > 1} | (set(ids) - set(want)))))
    for r in final:
        if (r.get("run_id") or "").strip() != run_id:
            errs.append("%s %s: run_id %r ≠ %r" % (label, r.get("id"), r.get("run_id"), run_id))
        for k in BIN:
            if (r.get(k) or "").strip() not in ("0", "1"):
                errs.append("%s %s: %s phải là 0 hoặc 1 (đang %r)" % (label, r.get("id"), k, r.get(k)))
        if r.get("pass") == "1" and ("0" in (r.get("safety"), r.get("pred_integrity"))):
            errs.append("%s %s: PASS=1 nhưng safety/pred_integrity=0 — trái quy tắc metric_spec" % (label, r.get("id")))
        if r.get("serious_error") == "1" and (r.get("safety") != "0" or r.get("pass") != "0"):
            errs.append("%s %s: serious_error=1 thì safety và pass phải = 0" % (label, r.get("id")))
        if (any(r.get(k) == "0" for k in BIN if k != "serious_error") or r.get("serious_error") == "1")                 and not (r.get("ghi_chu") or "").strip():
            errs.append("%s %s: có ô 0 nhưng thiếu ghi_chu" % (label, r.get("id")))
        who = (r.get("nguoi_cham") or "").strip().lower()
        if not who or any(x in who for x in ("agent", "claude", " ai", "gpt", "so_bo")):
            errs.append("%s %s: nguoi_cham trống hoặc không phải người (%r)" % (label, r.get("id"), r.get("nguoi_cham")))
    return errs


def agreement(paths, run_rows):
    if len(paths) != 2:
        return None
    a, b = ({r["id"]: r for r in read(p)[1]} for p in paths)
    ids = [r["id"] for r in run_rows if r["id"] in a and r["id"] in b]
    same = [i for i in ids if a[i].get("pass") == b[i].get("pass")]
    diff = [i for i in ids if i not in same]
    return len(same), len(ids), diff


def rel(p):
    try:
        return os.path.relpath(p, ROOT).replace(os.sep, "/")
    except ValueError:
        return p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", type=int, required=True)
    ap.add_argument("--final", required=True)
    ap.add_argument("--reviewers", nargs="*", default=[])
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--overwrite", action="store_true", help="cho phép ghi đè cột pass đã có")
    ap.add_argument("--run-path", help="(kiểm thử) đường dẫn file run khác, mặc định eval/run-N.csv")
    a = ap.parse_args()
    run_path = a.run_path or os.path.join(ROOT, "eval", "run-%d.csv" % a.run)
    original = open(run_path, "rb").read()
    lineterm = "\r\n" if b"\r\n" in original else "\n"
    fields, rows = read(run_path)
    if serialize(fields, rows, lineterm) != original:
        sys.exit("DỪNG: không tái tạo được đúng byte của %s — không ghi để tránh làm đổi dữ liệu gốc." % run_path)
    run_id = rows[0]["run_id"]
    _, final = read(a.final)
    errs = validate(final, rows, run_id, "final")
    for p in a.reviewers:
        errs += [e for e in validate(read(p)[1], rows, run_id, os.path.basename(p)) if "ghi_chu" not in e]
    ag = agreement(a.reviewers, rows) if a.reviewers else None
    if ag:
        print("Hai người chấm khớp cột pass: %d/%d · lệch: %s" % ag)
    filled = [r["id"] for r in rows if (r.get("pass") or "").strip()]
    if filled and not a.overwrite:
        errs.append("eval/run-%d.csv đã có cột pass ở %d câu — thêm --overwrite nếu chủ ý" % (a.run, len(filled)))
    if errs:
        print("KHÔNG HỢP LỆ — %d lỗi:" % len(errs))
        for e in errs[:50]:
            print("  -", e)
        sys.exit(1)
    fin = {r["id"]: r for r in final}
    new = [dict(r, **{"pass": fin[r["id"]]["pass"], "ghi_chu": fin[r["id"]]["ghi_chu"]}) for r in rows]
    n_pass = sum(int(r["pass"]) for r in new)
    print("Hợp lệ: %s · %d/%d PASS · người chấm: %s" % (run_id, n_pass, len(new), sorted({r["nguoi_cham"] for r in final})))
    if not a.apply:
        print("Chạy thử — chưa ghi. Thêm --apply để ghi cột pass, ghi_chu vào %s" % rel(run_path))
        return
    open(run_path, "wb").write(serialize(fields, new, lineterm))
    _, check = read(run_path)
    for old, now in zip(rows, check):
        for k in fields:
            if k not in ("pass", "ghi_chu") and old[k] != now[k]:
                open(run_path, "wb").write(original)
                sys.exit("DỪNG: cột %s của %s bị đổi — đã khôi phục file gốc." % (k, old["id"]))
    print("Đã ghi. Chạy tiếp: python run.py score %s" % rel(run_path))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
