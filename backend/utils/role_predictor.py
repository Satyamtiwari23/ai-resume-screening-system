import joblib

import os
import joblib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "model",
    "resume_classifier.pkl"
)

model = joblib.load(MODEL_PATH)

def predict_role(resume_text):

    role = model.predict([resume_text])[0]

    role_requirements = {

        "IT": {
            "role": "IT",
            "required_skills": [
                "Python",
                "Java",
                "JavaScript",
                "Git",
                "SQL",
                "HTML",
                "CSS",
                "React"
            ],
            "preferred_skills": [
                "Docker",
                "AWS"
            ],
            "experience": "Fresher",
            "education": "Bachelor"
        },

        "Business": {
            "role": "Business",
            "required_skills": [
                "Excel",
                "SQL",
                "Power BI",
                "Communication"
            ],
            "preferred_skills": [
                "Tableau"
            ],
            "experience": "0-2 Years",
            "education": "Bachelor"
        },

        "Finance": {
            "role": "Finance",
            "required_skills": [
                "Excel",
                "Accounting",
                "Financial Analysis"
            ],
            "preferred_skills": [
                "Power BI"
            ],
            "experience": "0-2 Years",
            "education": "Bachelor"
        },

        "HR": {
            "role": "HR",
            "required_skills": [
                "Communication",
                "Recruitment"
            ],
            "preferred_skills": [
                "MS Office"
            ],
            "experience": "Fresher",
            "education": "Bachelor"
        }

    }

    return role_requirements.get(role, {
        "role": role,
        "required_skills": [],
        "preferred_skills": [],
        "experience": "",
        "education": ""
    })