from utils.skills import extract_skills


def calculate_default_score(resume_text, jd_data):

    resume_lower = resume_text.lower()

    resume_skills = [
        skill.lower()
        for skill in extract_skills(resume_text)
    ]

    required = [
        skill.lower()
        for skill in jd_data.get(
            "required_skills",
            []
        )
    ]

    preferred = [
        skill.lower()
        for skill in jd_data.get(
            "preferred_skills",
            []
        )
    ]

    matched = []

    missing = []

    # -----------------------------
    # Skill Matching
    # -----------------------------

    for skill in required:

        if skill in resume_skills:

            matched.append(skill)

        else:

            missing.append(skill)

    for skill in preferred:

        if skill in resume_skills:

            matched.append(skill)

        else:

            missing.append(skill)

    matched = list(set(matched))

    missing = list(set(missing))

    # ----------------------------------
    # Skills Score (40)
    # ----------------------------------

    total_required = len(required) + len(preferred)

    if total_required == 0:

        skill_score = 0

    else:

        skill_score = (
            len(matched) /
            total_required
        ) * 40

    # ----------------------------------
    # Experience (20)
    # ----------------------------------
    
    experience_score = 0
    experience_level = "Fresher"
    
    exp_keywords = [
        "intern",
        "internship",
        "experience",
        "worked",
        "developer",
        "engineer",
        "software engineer",
        "software developer",
        "full stack",
        "backend",
        "frontend",
        "company",
        "organization",
        "employment",
        "professional"
    ]
    
    if any(word in resume_lower for word in exp_keywords):
    
        experience_score = 20
        experience_level = "Experienced"
    
    elif (
        len(resume_skills) >= 8
        and any(
            word in resume_lower
            for word in [
                "project",
                "github",
                "developed",
                "built",
                "created",
                "implemented"
            ]
        )
    ):
    
        experience_score = 12
        experience_level = "Project Based"
    
    else:
    
        experience_score = 0
        experience_level = "Fresher"

    # ----------------------------------
    # Education (10)
    # ----------------------------------

    education_score = 0

    edu_keywords = [

        "b.tech",

        "btech",

        "b.e",

        "mca",

        "bca",

        "m.tech",

        "master",

        "bachelor"

    ]

    for word in edu_keywords:

        if word in resume_lower:

            education_score = 10

            break

    # ----------------------------------
    # Projects (15)
    # ----------------------------------

    project_score = 0

    project_keywords = [
        "project",
        "developed",
        "built",
        "created",
        "implemented",
        "github"
    ]
    
    if any(
        word in resume_lower
        for word in project_keywords
    ):
        project_score = 15

    # ----------------------------------
    # Resume Quality (10)
    # ----------------------------------

    words = len(
        resume_text.split()
    )

    if words > 350:

        quality_score = 10

    elif words > 200:

        quality_score = 8

    elif words > 100:

        quality_score = 5

    else:

        quality_score = 2

    # ----------------------------------
    # Certifications (5)
    # ----------------------------------

    certification_score = 0

    cert_keywords = [

        "certificate",

        "certification",

        "nptel",

        "coursera",

        "udemy",

        "aws"

    ]

    for word in cert_keywords:

        if word in resume_lower:

            certification_score = 5

            break

    score = round(

        skill_score +

        experience_score +

        education_score +

        project_score +

        quality_score +

        certification_score

    )

    if score > 100:

        score = 100

    return {
        "overall_score": score,
    
        "breakdown": {
    
            "skills": round(skill_score),
            "experience": round(experience_score),
            "education": round(education_score),
            "projects": round(project_score),
            "resume_quality": round(quality_score),
            "certifications": round(certification_score)
    
        },
    
        "matched": matched,
        "missing": missing,
    
        "experience_level": experience_level
    }


# ==========================================
# Recruiter ATS Scoring
# (Temporary - same logic as default)
# ==========================================

def calculate_recruiter_score(resume_text, jd_data):
    return calculate_default_score(resume_text, jd_data)


# ==========================================
# Main Entry Point
# ==========================================

def calculate_score(resume_text, jd_data):

    if jd_data.get("recruiter_mode", False):
        return calculate_recruiter_score(
            resume_text,
            jd_data
        )

    return calculate_default_score(
        resume_text,
        jd_data
    )