import pandas as pd

print("Loading cleaned datasets...")

df1 = pd.read_csv("dataset/cleaned/clean_resume1.csv")
df2 = pd.read_csv("dataset/cleaned/clean_resume2.csv")
df3 = pd.read_csv("dataset/cleaned/clean_resume3.csv")
df4 = pd.read_csv("dataset/cleaned/clean_resume4.csv")
df5 = pd.read_csv("dataset/cleaned/clean_resume5.csv")
df6 = pd.read_csv("dataset/cleaned/clean_resume6.csv")

print("Dataset 1:", df1.shape)
print("Dataset 2:", df2.shape)
print("Dataset 3:", df3.shape)
print("Dataset 4:", df4.shape)
print("Dataset 5:", df5.shape)
print("Dataset 6:", df6.shape)

# Merge
df = pd.concat(
    [
        df1,
        df2,
        df3,
        df4,
        df5,
        df6
    ],
    ignore_index=True
)
print("After Merge:", df.shape)

# Remove duplicate resumes
df.drop_duplicates(subset=["Resume"], inplace=True)

print("After Removing Duplicates:", df.shape)

# Remove empty rows
df.dropna(inplace=True)

# Remove very short resumes
df = df[df["Resume"].str.len() > 100]

print("Final Dataset:", df.shape)

# Shuffle
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# Save
mapping = {

    # IT
    "INFORMATION-TECHNOLOGY":"IT",
    "Java Developer":"IT",
    "Python Developer":"IT",
    "Web Designing":"IT",
    "Database":"IT",
    "Data Science":"IT",
    "DevOps Engineer":"IT",
    "Testing":"IT",
    "Automation Testing":"IT",
    "Hadoop":"IT",
    "SAP Developer":"IT",
    "ETL Developer":"IT",
    "Blockchain":"IT",
    "Network Security Engineer":"IT",
    "DotNet Developer":"IT",

    # Business
    "BUSINESS-DEVELOPMENT":"Business",
    "Business Analyst":"Business",
    "SALES":"Business",
    "Sales":"Business",
    "CONSULTANT":"Business",
    "BPO":"Business",
    "Operations Manager":"Business",
    "PMO":"Business",

    # Engineering
    "ENGINEERING":"Engineering",
    "Mechanical Engineer":"Engineering",
    "Civil Engineer":"Engineering",
    "Electrical Engineering":"Engineering",

    # HR
    "HR":"HR",

    # Finance
    "FINANCE":"Finance",
    "ACCOUNTANT":"Finance",
    "BANKING":"Finance",

    # Healthcare
    "HEALTHCARE":"Healthcare",
    "Health and fitness":"Healthcare",
    "FITNESS":"Healthcare",

    # Legal
    "ADVOCATE":"Legal",
    "Advocate":"Legal",

    # Creative
    "DESIGNER":"Creative",
    "DIGITAL-MEDIA":"Creative",
    "ARTS":"Creative",
    "Arts":"Creative",
    "APPAREL":"Creative",

    # Education
    "TEACHER":"Education",

    # Agriculture
    "AGRICULTURE":"Agriculture",

    # Hospitality
    "CHEF":"Hospitality",

    # Construction
    "CONSTRUCTION":"Construction",

    # Automobile
    "AUTOMOBILE":"Automobile",

    # Aviation
    "AVIATION":"Aviation",

    # PR
    "PUBLIC-RELATIONS":"Public Relations",


    # -------------------------
    # Dataset 3 Mapping
    # -------------------------
    
    "Java Developers/Architects Resumes":"IT",
    "Web Developer Resumes": "IT",
    "SQL Developers Resumes": "IT",
    "Network and Systems Administrator Resumes": "IT",
    "Datawarehousing, ETL, Informatica Resumes": "IT",
    "Business Intelligence, Business Object Resumes": "IT",
    
    "Business Analyst (BA) Resumes": "Business",
    
    "Project Manager Resumes": "Business",
    
    "Recruiter Resumes": "HR",


    # Dataset 6
    "Banking": "Finance",
    "Finance": "Finance",
    "ACCOUNTANT": "Finance",
    
    "TEACHER": "Education",
    
    "Apparel": "Creative",
    
    "Research Assistant": "Education",
    
}

# Convert all labels
df["Category"] = df["Category"].replace(mapping)

# Remove categories we don't support
supported = [
    "IT",
    "Business",
    "Engineering",
    "HR",
    "Finance",
    "Healthcare",
    "Legal",
    "Creative",
    "Education",
    "Agriculture",
    "Hospitality",
    "Construction",
    "Automobile",
    "Aviation",
    "Public Relations"
]

df = df[df["Category"].isin(supported)]
df.to_csv("dataset/merged/final_resume_dataset.csv", index=False)

print("\nMerged dataset saved successfully!")