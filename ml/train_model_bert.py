import pandas as pd
import joblib
import torch

from sentence_transformers import SentenceTransformer

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# -----------------------------
# Device
# -----------------------------

if torch.backends.mps.is_available():
    device = "mps"
elif torch.cuda.is_available():
    device = "cuda"
else:
    device = "cpu"

print(f"\nUsing Device : {device}")

# -----------------------------
# Load Dataset
# -----------------------------

df = pd.read_csv("dataset/merged/final_resume_dataset.csv")

print("\nDataset Shape :", df.shape)

X = df["Resume"].astype(str)

y = df["Category"]

# -----------------------------
# Train Test Split
# -----------------------------

X_train, X_test, y_train, y_test = train_test_split(

    X,

    y,

    test_size=0.20,

    random_state=42,

    stratify=y

)

# -----------------------------
# Load BERT Model
# -----------------------------

print("\nLoading Sentence Transformer...")

model = SentenceTransformer(

    "all-mpnet-base-v2",

    device=device

)

# -----------------------------
# Convert Resume -> Embedding
# -----------------------------

print("\nGenerating Training Embeddings...")

X_train_embed = model.encode(

    X_train.tolist(),

    show_progress_bar=True,

    batch_size=32

)

print("\nGenerating Testing Embeddings...")

X_test_embed = model.encode(

    X_test.tolist(),

    show_progress_bar=True,

    batch_size=32

)

# -----------------------------
# Logistic Regression
# -----------------------------

classifier = RandomForestClassifier(
    n_estimators=500,
    random_state=42,
    n_jobs=-1
)

print("\nTraining Classifier...")

classifier.fit(

    X_train_embed,

    y_train

)

pred = classifier.predict(

    X_test_embed

)

accuracy = accuracy_score(

    y_test,

    pred

)

print("\n"+"="*50)

print(f"Accuracy : {accuracy*100:.2f}%")

print("="*50)

print(

    classification_report(

        y_test,

        pred

    )

)

# -----------------------------
# Save
# -----------------------------

joblib.dump(

    model,

    "model/bert_encoder.pkl"

)

joblib.dump(

    classifier,

    "model/bert_classifier.pkl"

)

print("\nModels Saved Successfully!")
