"""Train mô hình sàng lọc nguy cơ tham khảo trên Pima Indians Diabetes — chạy MỘT lần, offline.

Chạy:  py -3.12 -m pip install -r ml/requirements-train.txt
       py -3.12 ml/train.py            (tải data về thư mục tạm, kiểm SHA-256, không commit data)
Ra:    ml/model.json   — hệ số Logistic Regression + trung vị + chuẩn hoá (đọc bằng thư viện chuẩn lúc chạy)
       ml/metrics.json — kết quả đánh giá trên tập test
Lúc chạy bản chạy thử KHÔNG cần scikit-learn: codebase/tools.py tự tính từ model.json.
"""
import hashlib
import json
import os
import sys
sys.stdout.reconfigure(encoding="utf-8")
import tempfile
import urllib.request

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, confusion_matrix, f1_score, precision_score,
                             recall_score, roc_auc_score)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

URL = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
SHA256 = "6bfe5d0f379d17a0e0819b996407e3c09bf80febd4287f2ed212190dfff154af"
COLS = ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI",
        "DiabetesPedigreeFunction", "Age", "Outcome"]
# Chỉ dùng chỉ số người dùng có thể có: bỏ SkinThickness, Insulin (thiếu 30–49%, không đo tại nhà),
# DiabetesPedigreeFunction (người dùng không tự tính được) và Pregnancies (người dùng thường không nhập;
# không muốn tự điền số thiếu lúc dự đoán).
FEATURES = ["Glucose", "BloodPressure", "BMI", "Age"]
ZERO_IS_MISSING = ["Glucose", "BloodPressure", "BMI"]
SEED = 42
HERE = os.path.dirname(os.path.abspath(__file__))


def load():
    path = os.path.join(tempfile.gettempdir(), "pima-indians-diabetes.data.csv")
    if not os.path.exists(path):
        urllib.request.urlretrieve(URL, path)
    raw = open(path, "rb").read()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != SHA256:
        sys.exit("SHA-256 khác bản đã ghi ở DATA_CARD: %s" % digest)
    rows = [list(map(float, line.split(","))) for line in raw.decode().splitlines() if line.strip()]
    data = np.array(rows)
    assert data.shape == (768, 9), data.shape
    return data


def metrics(y, prob, thr=0.5):
    pred = (prob >= thr).astype(int)
    tn, fp, fn, tp = confusion_matrix(y, pred).ravel()
    return {"accuracy": round(accuracy_score(y, pred), 4), "precision": round(precision_score(y, pred), 4),
            "recall": round(recall_score(y, pred), 4), "f1": round(f1_score(y, pred), 4),
            "roc_auc": round(roc_auc_score(y, prob), 4),
            "confusion_matrix": {"tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp)}, "threshold": thr}


def main():
    data = load()
    idx = [COLS.index(f) for f in FEATURES]
    X = data[:, idx].copy()
    y = data[:, COLS.index("Outcome")].astype(int)
    for f in ZERO_IS_MISSING:
        j = FEATURES.index(f)
        X[X[:, j] == 0, j] = np.nan
    missing = {f: int(np.isnan(X[:, FEATURES.index(f)]).sum()) for f in FEATURES}

    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, stratify=y, random_state=SEED)
    # Kiểm rò rỉ: imputer + scaler nằm trong Pipeline nên chỉ fit trên tập train.
    lr = Pipeline([("imp", SimpleImputer(strategy="median")), ("sc", StandardScaler()),
                   ("clf", LogisticRegression(max_iter=1000, random_state=SEED))]).fit(X_tr, y_tr)
    rf = Pipeline([("imp", SimpleImputer(strategy="median")),
                   ("clf", RandomForestClassifier(n_estimators=300, min_samples_leaf=5, random_state=SEED))]
                  ).fit(X_tr, y_tr)
    p_lr, p_rf = lr.predict_proba(X_te)[:, 1], rf.predict_proba(X_te)[:, 1]
    res = {
        "dataset": {"name": "Pima Indians Diabetes", "rows": int(len(y)), "positives": int(y.sum()),
                    "sha256": SHA256, "missing_as_zero": missing},
        "split": {"test_size": 0.2, "stratify": True, "seed": SEED, "n_train": int(len(y_tr)), "n_test": int(len(y_te))},
        "features": FEATURES,
        "logistic_regression": metrics(y_te, p_lr),
        "random_forest": metrics(y_te, p_rf),
        "baseline_majority_accuracy": round(float(1 - y_te.mean()), 4),
        "chosen": "logistic_regression",
        "why_chosen": "RF cao hơn LR một chút trên 154 dòng test (xem số ở trên) nhưng chênh nhỏ so với độ dao động của tập test nhỏ; chọn LR vì hệ số đọc được, giải thích được cho người dùng, suy luận bằng thư viện chuẩn.",
    }
    imp, sc, clf = lr.named_steps["imp"], lr.named_steps["sc"], lr.named_steps["clf"]
    model = {
        "type": "logistic_regression", "features": FEATURES,
        "impute_median": dict(zip(FEATURES, map(float, imp.statistics_))),
        "scaler_mean": dict(zip(FEATURES, map(float, sc.mean_))),
        "scaler_scale": dict(zip(FEATURES, map(float, sc.scale_))),
        "coef": dict(zip(FEATURES, map(float, clf.coef_[0]))), "intercept": float(clf.intercept_[0]),
        "train_seed": SEED, "data_sha256": SHA256,
        "valid_population": "Phụ nữ 21–81 tuổi; Glucose = đường huyết 2 giờ sau OGTT (mg/dL). Không đại diện người Việt.",
        "train_ranges": {f: [float(np.nanmin(X_tr[:, i])), float(np.nanmax(X_tr[:, i]))] for i, f in enumerate(FEATURES)},
        "test_auc": res["logistic_regression"]["roc_auc"],
        "sklearn_check": {"input": [85, 66, 26.6, 31],
                          "prob": float(lr.predict_proba(np.array([[85, 66, 26.6, 31]]))[0, 1])},
    }
    json.dump(model, open(os.path.join(HERE, "model.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    json.dump(res, open(os.path.join(HERE, "metrics.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(json.dumps(res, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
