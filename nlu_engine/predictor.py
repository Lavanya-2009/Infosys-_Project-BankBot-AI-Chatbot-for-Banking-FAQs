import joblib
import os
import numpy as np
from sklearn.pipeline import Pipeline

# ---------------- BASE PATH ----------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

MODEL_PATH = os.path.join(
    BASE_DIR, "ui", "models", "intent_model", "intent_model.pkl"
)
VECTORIZER_PATH = os.path.join(
    BASE_DIR, "ui", "models", "intent_model", "vectorizer.pkl"
)

print("✅ LOADING MODEL FROM:", MODEL_PATH)

# ---------------- LOAD MODEL ----------------
model = joblib.load(MODEL_PATH)

# Vectorizer is only needed when the stored model is a bare classifier
try:
    vectorizer = joblib.load(VECTORIZER_PATH)
except Exception:
    vectorizer = None


# ---------------- PREDICT INTENT ----------------
def predict_intent(text: str):
    """Predict user intent and confidence from raw text.

    Handles both cases where the saved model is:
    - a full scikit-learn Pipeline (TfidfVectorizer + classifier)
    - a bare classifier that expects vectorized input (uses separate vectorizer).
    """

    cleaned = (text or "").strip().lower()

    # If model is a Pipeline, feed it raw text (no manual vectorizer).
    if isinstance(model, Pipeline):
        X = [cleaned]
    else:
        if vectorizer is None:
            raise RuntimeError("Vectorizer not found for non-pipeline intent model")
        X = vectorizer.transform([cleaned])

    # If model supports probability
    if hasattr(model, "predict_proba"):
        probs = model.predict_proba(X)[0]
        confidence = float(np.max(probs))
        intent = model.classes_[np.argmax(probs)]
    else:
        # Fallback (no confidence support)
        intent = model.predict(X)[0]
        confidence = 1.0

    print(f"🧠 USER TEXT: {text}")
    print(f"🎯 PREDICTED INTENT: {intent} | CONFIDENCE: {confidence:.2f}")

    return intent, confidence
