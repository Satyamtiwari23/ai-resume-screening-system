import pandas as pd
import re
import string


def clean_text(text):
    text = str(text)

    text = re.sub(r"<.*?>", " ", text)
    text = re.sub(r"http\S+|www\S+", " ", text)
    text = re.sub(r"\S+@\S+", " ", text)
    text = re.sub(r"\+?\d[\d\s\-]{8,}", " ", text)

    text = text.lower()

    text = text.translate(
        str.maketrans("", "", string.punctuation)
    )

    text = re.sub(r"\d+", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ====================================
# DATASET 1
# ====================================

print("Cleaning Dataset 1...")

df1 = pd.read_csv("dataset/raw/Resume.csv")

df1 = df1[["Resume_str", "Category"]]

df1.rename(columns={"Resume_str": "Resume"}, inplace=True)

df1["Resume"] = df1["Resume"].apply(clean_text)

print("Before removing duplicates :", len(df1))

df1.drop_duplicates(subset="Resume", inplace=True)

print("After removing duplicates :", len(df1))

df1.dropna(inplace=True)

print("After removing NA :", len(df1))

df1.to_csv("dataset/cleaned/clean_resume1.csv", index=False)

print("Dataset 1 cleaned.")
print(df1.shape)


# ====================================
# DATASET 2
# ====================================

print("\nCleaning Dataset 2...")

df2 = pd.read_csv("dataset/raw/ResumeDataSet.csv")

df2 = df2[["Resume", "Category"]]

df2["Resume"] = df2["Resume"].apply(clean_text)

print("Before removing duplicates :", len(df2))

# Keep this commented for now
# df2.drop_duplicates(subset="Resume", inplace=True)

print("After removing duplicates :", len(df2))

df2.dropna(inplace=True)

print("After removing NA :", len(df2))

df2.to_csv("dataset/cleaned/clean_resume2.csv", index=False)

print("Dataset 2 cleaned.")
print(df2.shape)

print("\nCleaning Completed Successfully!")


# ====================================
# DATASET 3
# ====================================

print("\nCleaning Dataset 3...")

df3 = pd.read_csv("dataset/raw/Resume dataset.csv")

# Keep only required columns
df3 = df3[["Text", "category"]]

# Rename columns to match existing datasets
df3.rename(
    columns={
        "Text": "Resume",
        "category": "Category"
    },
    inplace=True
)

# Clean text
df3["Resume"] = df3["Resume"].apply(clean_text)

print("Before removing duplicates :", len(df3))

df3.drop_duplicates(
    subset="Resume",
    inplace=True
)

print("After removing duplicates :", len(df3))

df3.dropna(inplace=True)

print("After removing NA :", len(df3))

df3.to_csv(
    "dataset/cleaned/clean_resume3.csv",
    index=False
)

print("Dataset 3 cleaned.")
print(df3.shape)



# ====================================
# DATASET 4
# ====================================

print("\nCleaning Dataset 4...")

df4 = pd.read_csv("dataset/raw/Resume_dataset2.csv")

df4 = df4[["Resume","Category"]]

df4["Resume"] = df4["Resume"].apply(clean_text)

df4.drop_duplicates(subset="Resume", inplace=True)

df4.dropna(inplace=True)

df4.to_csv(
    "dataset/cleaned/clean_resume4.csv",
    index=False
)

print("Dataset 4 cleaned.")
print(df4.shape)



# ====================================
# DATASET 5
# ====================================

print("\nCleaning Dataset 5...")

df5 = pd.read_csv("dataset/raw/UpdatedResumeDataSet2.csv")

df5 = df5[["Resume","Category"]]

df5["Resume"] = df5["Resume"].apply(clean_text)

df5.drop_duplicates(subset="Resume", inplace=True)

df5.dropna(inplace=True)

df5.to_csv(
    "dataset/cleaned/clean_resume5.csv",
    index=False
)

print("Dataset 5 cleaned.")
print(df5.shape)


# ====================================
# DATASET 6
# ====================================

print("\nCleaning Dataset 6...")

df6 = pd.read_excel("dataset/raw/CareerCorpus.xlsx")

# Keep required columns
df6 = df6[[
    "Domain",
    "Education",
    "Skills and Achievements",
    "Experience"
]]

# Create Resume text
df6["Resume"] = (
    df6["Education"].fillna("") + " " +
    df6["Skills and Achievements"].fillna("") + " " +
    df6["Experience"].fillna("")
)

# Category
df6["Category"] = df6["Domain"]

# Keep only required columns
df6 = df6[["Resume", "Category"]]

# Clean resume
df6["Resume"] = df6["Resume"].apply(clean_text)

# Remove duplicates
df6.drop_duplicates(subset="Resume", inplace=True)

# Remove NA
df6.dropna(inplace=True)

# Save
df6.to_csv(
    "dataset/cleaned/clean_resume6.csv",
    index=False
)

print("Dataset 6 cleaned.")
print(df6.shape)