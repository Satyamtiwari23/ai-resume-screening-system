import re
import spacy
import os

nlp = spacy.load("en_core_web_sm")
def ai_entities(text):

    doc = nlp(text[:5000])

    entities = {
        "person": [],
        "org": [],
        "gpe": []
    }

    for ent in doc.ents:

        if ent.label_ == "PERSON":
            entities["person"].append(ent.text)

        elif ent.label_ == "ORG":
            entities["org"].append(ent.text)

        elif ent.label_ in ["GPE", "LOC"]:
            entities["gpe"].append(ent.text)

    return entities


def extract_email(text):

    match = re.search(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text
    )

    return match.group() if match else "Not Found"


def extract_phone(text):

    match = re.search(
        r"(\+91[\s-]?)?[6-9]\d{9}",
        text
    )

    return match.group() if match else "Not Found"





def extract_name(text, filename):
    print("USING NEW extract_name")
    """
    AI + Email + Filename based name extraction.
    """

    entities = ai_entities(text)

    blacklist = {
        "resume",
        "curriculum vitae",
        "food technologist",
        "software engineer",
        "developer",
        "engineer",
        "experience",
        "education",
        "skills",
        "profile",
        "summary",
        "objective"
    }
    job_words = {
        "developer",
        "engineer",
        "manager",
        "analyst",
        "consultant",
        "designer",
        "specialist",
        "technologist",
        "intern",
        "executive",
        "student"
    }

    # -----------------------
    # 1. spaCy PERSON
    # -----------------------
    for person in entities["person"]:

        person = person.strip()
    
        words = person.split()
    
        if len(words) < 2 or len(words) > 4:
            continue
    
        if any(ch.isdigit() for ch in person):
            continue
    
        if person.lower() in blacklist:
            continue
    
        # Reject all-uppercase non-name headings
        if person.isupper() and len(words) > 3:
            continue
    
        if any(word.lower() in job_words for word in words):
            continue
    
        return person.title()
    
    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]
    
    for line in lines[:10]:
    
        words = line.split()
    
        if len(words) < 2 or len(words) > 4:
            continue
    
        if any(ch.isdigit() for ch in line):
            continue
    
        lower = line.lower()
    
        if lower in blacklist:
            continue
    
        if any(word.lower() in job_words for word in words):
            continue
    
        return line.title()
    
    # -----------------------
    # 3. Email username
    # -----------------------
    email = extract_email(text)

    if email != "Not Found":

        username = email.split("@")[0]

        username = re.sub(r"[0-9._-]+", " ", username)

        words = [
            w.capitalize()
            for w in username.split()
            if len(w) > 1
        ]

        if len(words) >= 2:
            return " ".join(words)

    # -----------------------
    # 4. Filename
    # -----------------------
    base = os.path.splitext(filename)[0]

    base = re.sub(
        r"(resume|cv|final|updated|latest)",
        "",
        base,
        flags=re.I
    )

    base = re.sub(r"[_\-.]+", " ", base)

    words = [
        w.capitalize()
        for w in base.split()
        if len(w) > 1
    ]

    if len(words) >= 2:
        return " ".join(words)

    return "Unknown"


def extract_education(text):

    lower = text.lower()

    patterns = [
        ("Bachelor of Technology", ["b.tech", "btech", "bachelor of technology"]),
        ("Bachelor of Engineering", ["b.e", "be", "bachelor of engineering"]),
        ("Bachelor Degree", ["bachelor"]),
        ("Master Degree", ["master", "m.tech", "mca", "m.sc"]),
        ("Diploma", ["diploma"])
    ]

    for degree, keywords in patterns:
        if any(k in lower for k in keywords):
            return degree

    return "Not Found"


def extract_experience(text):

    lower = text.lower()

    fresher_words = {
        "fresher",
        "internship",
        "intern",
        "student"
    }

    if any(word in lower for word in fresher_words):
        return "Fresher"

    match = re.search(
        r"(\d+)\+?\s*(year|years)",
        lower
    )

    if match:
        return f"{match.group(1)} Years"

    return "Not Found"