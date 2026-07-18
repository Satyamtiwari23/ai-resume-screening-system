from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os

from utils.pdf_reader import extract_text

from utils.parser import (
    extract_name,
    extract_email,
    extract_phone,
    extract_education,
    extract_experience
)

from utils.skills import extract_skills
from utils.ats import calculate_score
from utils.resume_analyzer import analyze_resume
from utils.role_predictor import predict_role

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print("=" * 50)
print(BASE_DIR)
print(os.path.exists(os.path.join(BASE_DIR, "frontend")))
print(os.path.exists(os.path.join(BASE_DIR, "frontend", "templates", "index.html")))
print("=" * 50)

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "frontend", "templates"),
    static_folder=os.path.join(BASE_DIR, "frontend", "static")
)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def process_resume(file, jd_data=None):
    """
    Process a resume PDF and return a structured
    candidate analysis report.
    """
    filepath = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    file.save(filepath)

    resume_text = extract_text(filepath)

    name = extract_name(
        resume_text,
        file.filename
    )

    email = extract_email(resume_text)

    phone = extract_phone(resume_text)

    education = extract_education(resume_text)

    experience = extract_experience(resume_text)

    resume_text_lower = resume_text.lower()

    relevant_experience = False
    
    it_keywords = [
        "python",
        "java",
        "javascript",
        "react",
        "node",
        "sql",
        "mongodb",
        "html",
        "css",
        "docker",
        "aws",
        "git"
    ]
    
    experience_keywords = [
        "intern",
        "experience",
        "worked",
        "developer",
        "engineer"
    ]
    
    if any(exp in resume_text_lower for exp in experience_keywords):
    
        if any(skill in resume_text_lower for skill in it_keywords):
    
            relevant_experience = True

    skills = extract_skills(resume_text)

    if jd_data:

        ats_result = calculate_score(
            resume_text,
            jd_data
        )

    else:

        try:
    
            jd_data = predict_role(
                resume_text
            )
    
        except Exception as e:
    
            # Default JD for local fallback
            jd_data = {
                "role": "Software Developer",
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
                "preferred_skills": [],
                "experience": "Fresher",
                "education": "Bachelor"
            }
    
        ats_result = calculate_score(
            resume_text,
            jd_data
        )

    score = ats_result["overall_score"]

    matched = ats_result["matched"]

    missing = ats_result["missing"]

    ai_feedback = analyze_resume(
        role=jd_data.get("role", ""),
        score=score,
        skills=skills,
        matched=matched,
        missing=missing,
        experience=ats_result["experience_level"],
        education=education,
        relevant_experience=relevant_experience
    )
    is_hr = request.form.get("jobRole", "").strip() != ""
    recommendation = (

        "Highly Recommended"

        if score>=80

        else

        "Recommended"

        if score>=60

        else

        "Needs Improvement"

    )

    return {

        "candidate":{

            "name":name,

            "email":email,

            "phone":phone,

            "education":education,
        
            "experience": ats_result["experience_level"],

            "resume":file.filename

        },

        "predictedRole":jd_data.get("role",""),

        "skills":skills,

        "matchedSkills":matched,

        "missingSkills":missing,

        "summary": ai_feedback.get("summary",""),

        "strengths": ai_feedback.get("strengths", []),
        
        "weaknesses": ai_feedback.get("weaknesses", []),
        
        "suggestions": [] if is_hr else ai_feedback.get("suggestions", []),
        
        "hiring": ai_feedback.get("hiring", {}),
        
        "interviewQuestions": [] if is_hr else ai_feedback.get("interview_questions", []),

        "atsBreakdown":ats_result["breakdown"],

        "score":score,

        "recommendation":recommendation

    }

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_resume():


    if "resumes" not in request.files:
        return jsonify({
            "error": "No Resume Uploaded"
        }), 400

    files = request.files.getlist("resumes")

    if len(files) == 0:
        return jsonify({
            "error": "No Resume Uploaded"
        }), 400

    import json

    job_role = request.form.get(
        "jobRole",
        ""
    )
    
    department = request.form.get(
        "department",
        ""
    )
    experience = request.form.get(
        "experience",
        ""
    )
    
    education_required = request.form.get(
        "education",
        ""
    )
    
    required_skills = [

        skill.strip()
    
        for skill in request.form.get(
            "requiredSkills",
            ""
        ).replace("\r", "").split("\n")
    
        if skill.strip()
    
    ]
    
    jd_data = None

    # ===================================
    # MODE 1
    # Recruiter filled form
    # ===================================
    
    recruiter_mode = any([
        job_role,
        department,
        experience,
        education_required,
        len(required_skills)
    ])
    
    if recruiter_mode:
    
        jd_data = {

            "role": job_role,
        
            "department": department,
        
            "experience": experience,
        
            "education": education_required,
        
            "required_skills": required_skills,
        
            "preferred_skills": [],
        
            "recruiter_mode": True
        
        }
    
        print("\n====== RECRUITER MODE ======")
    
        print(jd_data)
    
        print("============================")

    # -------------------------
    # Student Mode
    # -------------------------
    
    if len(files) == 1:
    
        result = process_resume(
            files[0],
            jd_data
        )
    
        return jsonify(result)
    
    
    # -------------------------
    # HR Mode
    # -------------------------
    
    results = []
    
    for file in files:
    
        result = process_resume(
            file,
            jd_data
        )
    
        results.append(result)
    
    
    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )
    
    return jsonify({
        "candidates": results
    })
    

if __name__ == "__main__":
    app.run(
    host="127.0.0.1",
    port=5001,
    debug=True,
    use_reloader=False
    )