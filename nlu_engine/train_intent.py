import json
import joblib
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# ---------- LOAD INTENTS ----------
import json
import joblib
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
INTENTS_PATH = os.path.join(BASE_DIR, "nlu_engine", "intents.json")
MODEL_DIR = os.path.join(BASE_DIR, "models", "intent_model")

with open(INTENTS_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)


texts = []
labels = []

for intent in data["intents"]:
    for example in intent["examples"]:
        texts.append(example.lower())
        labels.append(intent["name"])

# ---------- VECTORIZATION ----------
vectorizer = TfidfVectorizer(
    lowercase=True,
    stop_words="english",
    ngram_range=(1, 2),
    min_df=1
)

X = vectorizer.fit_transform(texts)

# ---------- MODEL ----------
model = LogisticRegression(
    max_iter=1000,
    solver="lbfgs"
)

model.fit(X, labels)

# ---------- SAVE ----------
os.makedirs("models/intent_model", exist_ok=True)
joblib.dump(model, "models/intent_model/intent_model.pkl")
joblib.dump(vectorizer, "models/intent_model/vectorizer.pkl")

print("✅ NLU training completed successfully")
