import random

def build_candidate_profile(
    score,
    skills,
    matched,
    missing,
    experience,
    education
):

    profile = {}

    # ---------------- Skill Match ----------------
    if len(matched) >= 8:
        profile["skill_match"] = "Excellent"
    elif len(matched) >= 5:
        profile["skill_match"] = "Good"
    elif len(matched) >= 2:
        profile["skill_match"] = "Average"
    else:
        profile["skill_match"] = "Poor"

    # ---------------- Experience ----------------
    profile["experience"] = experience

    # ---------------- Education ----------------
    if education:
        profile["education"] = "Available"
    else:
        profile["education"] = "Missing"

    # ---------------- Technical Diversity ----------------
    if len(skills) >= 12:
        profile["technical"] = "Excellent"

    elif len(skills) >= 8:
        profile["technical"] = "Good"

    elif len(skills) >= 4:
        profile["technical"] = "Average"

    else:
        profile["technical"] = "Poor"

    # ---------------- Resume Quality ----------------
    if score >= 85:
        profile["resume_quality"] = "Excellent"

    elif score >= 70:
        profile["resume_quality"] = "Good"

    elif score >= 50:
        profile["resume_quality"] = "Average"

    else:
        profile["resume_quality"] = "Poor"

    profile["missing_skills"] = len(missing)

    profile["ats"] = score

    return profile



def analyze_resume(
    role,
    score,
    skills,
    matched,
    missing,
    experience,
    education,
    relevant_experience
):
    
    profile = build_candidate_profile(
        score,
        skills,
        matched,
        missing,
        experience,
        education
    )
    
    profile["relevant_experience"] = relevant_experience

    # -----------------------------
    # Summary
    # -----------------------------

    if score >= 80:
        suitability = f"The candidate is highly suitable for the role of {role}."
    
    elif score >= 60:
        suitability = f"The candidate is reasonably suitable for the role of {role}, but some improvements are recommended."
    
    elif score >= 40:
        suitability = f"The candidate shows partial alignment with the role of {role}."
    
    else:
        suitability = f"The candidate is currently not suitable for the role of {role}."
    
    summary = f"""
    {suitability}
    
    The resume achieved an ATS score of {score}%.
    
    The candidate possesses {len(skills)} identified technical skills.
    
    Overall profile shows {'strong' if score>=80 else 'moderate' if score>=60 else 'basic'} alignment with the job requirements.
    """.strip()

    # -----------------------------
    # AI Strengths
    # -----------------------------
    
    strengths = []
    
    if profile["skill_match"] == "Excellent":
        strengths.append("Excellent alignment with required job skills.")
    
    elif profile["skill_match"] == "Good":
        strengths.append("Good alignment with required technical skills.")
    
    if profile["technical"] == "Excellent":
        strengths.append("Strong and diverse technical stack.")
    
    elif profile["technical"] == "Good":
        strengths.append("Good technical skill diversity.")
    
    if profile["experience"] == "Experienced":
    
        if profile["relevant_experience"]:
    
            strengths.append(
                "Relevant IT professional experience detected."
            )
    
        else:
    
            strengths.append(
                "Professional experience detected in another domain."
            )
    
    elif profile["experience"] == "Project Based":
        strengths.append(
        "Strong project portfolio demonstrates practical technical experience."
    )
    
    if profile["education"] == "Available":
        strengths.append("Educational qualifications verified.")
    
    if score >= 85:
        strengths.append("High ATS compatibility with the job description.")
    
    if len(strengths) == 0:
        strengths.append("Resume contains basic candidate information.")
    
    # -----------------------------
    # AI Weaknesses
    # -----------------------------
    
    weaknesses = []
    
    if profile["missing_skills"] > 0:
    
        weaknesses.append(
            f"{profile['missing_skills']} required skill(s) are missing."
        )
    
    if profile["technical"] == "Poor":
    
        weaknesses.append(
            "Very limited technical stack detected."
        )
    
    elif profile["technical"] == "Average":
    
        weaknesses.append(
            "Technical skill diversity can be improved."
        )
    
    if profile["experience"] == "Fresher":

        weaknesses.append(
            "No professional experience detected."
        )
    
    elif profile["experience"] == "Experienced" and not profile["relevant_experience"]:
    
        weaknesses.append(
            "Professional experience is not directly related to the target IT role."
        )
    
    if score < 70:
    
        weaknesses.append(
            "ATS compatibility is below recruiter expectations."
        )
    
    if len(weaknesses) == 0:
    
        weaknesses.append(
            "No major weaknesses detected."
        )
    # -----------------------------
    # Suggestions
    # -----------------------------

    suggestions = []

    for skill in missing[:5]:
        suggestions.append(
            f"Learn {skill}"
        )

    if score < 80:
        suggestions.append(
            "Improve resume with more measurable project achievements."
        )

    suggestions.append(
        "Customize resume according to every Job Description."
    )


    # -----------------------------
    # AI Confidence
    # -----------------------------
    
    confidence = 50
    
    confidence += len(matched) * 4
    
    confidence -= len(missing) * 2
    
    if profile["experience"] == "Experienced":
        confidence += 10
    
    if profile["technical"] == "Excellent":
        confidence += 10
    
    elif profile["technical"] == "Good":
        confidence += 5
    
    confidence = max(40, min(confidence, 99))
    

    # -----------------------------
    # AI Hiring Verdict
    # -----------------------------
    
    if score >= 85:
    
        hiring = {

            "status": "Strong Match",
        
            "icon": "🟢",
        
            "confidence": confidence,
        
            "risk": "Low",
        
            "notes":
            "Candidate demonstrates excellent technical alignment and satisfies most hiring requirements.",
        
            "decision":
            "Shortlist for Technical Interview",
        
            "reason":[
        
                f"Technical Stack : {profile['technical']}",
        
                f"Skill Match : {profile['skill_match']}",
        
                f"Experience : {'Relevant IT Experience' if profile['relevant_experience'] else 'Non-IT Experience'}",
        
                f"Resume Quality : {profile['resume_quality']}"
        
            ]
        
        }
    
    elif score >= 70:
    
        hiring = {

            "status":"Moderate Match",
        
            "icon":"🟡",
        
            "confidence":confidence,
        
            "risk":"Medium",
        
            "notes":
            "Candidate meets several requirements but requires recruiter review before proceeding.",
        
            "decision":
            "Screening Interview Recommended",
        
            "reason":[
        
                f"Technical Stack : {profile['technical']}",
        
                f"Skill Match : {profile['skill_match']}",

                f"Experience : {'Relevant IT Experience' if profile['relevant_experience'] else 'Non-IT Experience'}" 
        
                f"Missing Skills : {profile['missing_skills']}"
        
            ]
        
        }
    
    elif score >= 50:
    
        hiring = {

            "status":"Weak Match",
        
            "icon":"🟠",
        
            "confidence":confidence,
        
            "risk":"Medium",
        
            "notes":
            "Candidate has potential but lacks several required competencies.",
        
            "decision":
            "Keep as Backup Candidate",
        
            "reason":[
        
                f"Technical Stack : {profile['technical']}",
        
                f"Missing Skills : {profile['missing_skills']}",
        
                f"Experience : {'Relevant IT Experience' if profile['relevant_experience'] else 'Non-IT Experience'}"
        
            ]
        
        }
    
    else:
    
        hiring = {

            "status":"Reject",
        
            "icon":"🔴",
        
            "confidence":confidence,
        
            "risk":"High",
        
            "notes":
            "Candidate does not currently satisfy the minimum hiring criteria.",
        
            "decision":
            "Do Not Shortlist",
        
            "reason":[
        
                f"{profile['missing_skills']} required skills missing",
        
                f"Technical Stack : {profile['technical']}",
        
                f"Experience : {'Relevant IT Experience' if profile['relevant_experience'] else 'Non-IT Experience'}"
        
                f"Resume Quality : {profile['resume_quality']}"
        
            ]
        
        }

    # -----------------------------
    # Interview Questions
    # -----------------------------

    interview_questions = []

    skill_questions = {

        "python":"Explain Python decorators.",

        "java":"Difference between JVM and JDK?",

        "react":"What are React Hooks?",

        "mongodb":"Explain MongoDB Aggregation.",

        "sql":"Difference between JOIN and UNION?",

        "docker":"Why do we use Docker?",

        "aws":"What is EC2?",

        "javascript":"Explain closures.",

        "git":"Difference between Merge and Rebase."

    }

    for skill in skills:

        key = skill.lower()

        if key in skill_questions:

            interview_questions.append(
                skill_questions[key]
            )

    if len(interview_questions) == 0:

        interview_questions.append(
            "Tell me about yourself."
        )

    return {

        "summary": summary,

        "strengths": strengths,

        "weaknesses": weaknesses,

        "suggestions": suggestions,

        "hiring": hiring,

        "interview_questions": interview_questions

    }