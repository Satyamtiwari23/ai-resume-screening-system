import pandas as pd
import joblib
import re
import string

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, classification_report


# ----------------------------
# Text Cleaning
# ----------------------------
def clean_text(text):
    text = str(text)

    # Remove HTML
    text = re.sub(r"<.*?>", " ", text)

    # Remove URLs
    text = re.sub(r"http\S+|www\S+", " ", text)

    # Remove emails
    text = re.sub(r"\S+@\S+", " ", text)

    # Remove phone numbers
    text = re.sub(r"\+?\d[\d\s\-]{8,}", " ", text)

    # Lowercase
    text = text.lower()

    # Remove punctuation
    text = text.translate(str.maketrans("", "", string.punctuation))

    # Remove numbers
    text = re.sub(r"\d+", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ----------------------------
# Load Dataset
# ----------------------------
df = pd.read_csv("dataset/merged/final_resume_dataset.csv")

print("Dataset Shape:", df.shape)

X = df["Resume"].apply(clean_text)
y = df["Category"]

print("\nCategories:")
print(sorted(y.unique()))

# ----------------------------
# Train Test Split
# ----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# ----------------------------
# Pipeline
# ----------------------------
pipeline = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(stop_words="english")
    ),
    (
        "classifier",
        LinearSVC()
    )
])


params = {

    "tfidf__max_features":[15000,25000,35000],

    "tfidf__ngram_range":[(1,1),(1,2)],

    "tfidf__min_df":[1,2],

    "classifier__C":[0.5,1,2,5]

}

model = GridSearchCV(
    pipeline,
    params,
    cv=5,
    n_jobs=-1,
    verbose=2
)


print("\nTraining Model...\n")

model.fit(X_train, y_train)
print(model.best_params_)
pred = model.predict(X_test)

accuracy = accuracy_score(y_test, pred)

print("="*50)
print(f"Accuracy : {accuracy*100:.2f}%")
print("="*50)

print(classification_report(y_test, pred))

joblib.dump(model, "model/resume_classifier.pkl")

print("\nModel Saved Successfully!")