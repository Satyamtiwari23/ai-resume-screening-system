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

    blacklist = {
        "resume",
        "curriculum vitae",
        "profile",
        "summary",
        "objective",
        "education",
        "experience",
        "skills",
        "projects",
        "certifications",
        "achievements",
        "software engineer",
        "developer",
        "engineer"
    }

    invalid_words = {
        "school",
        "college",
        "university",
        "institute",
        "building",
        "road",
        "street",
        "nagar",
        "city",
        "district",
        "state",
        "india",
        "public",
        "private",
        "government",
        "vidyalaya",
        "jawahar",
        "navodaya"
    }

    job_words = {
        "developer",
        "engineer",
        "manager",
        "analyst",
        "consultant",
        "designer",
        "executive",
        "intern",
        "student",
        "technologist",
        "specialist"
    }

    # ====================================================
    # STEP 1
    # Search only first 8 non-empty lines
    # ====================================================

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    for line in lines[:8]:

        words = line.split()

        if len(words) < 2 or len(words) > 4:
            continue

        if any(char.isdigit() for char in line):
            continue

        lower = line.lower()

        if lower in blacklist:
            continue

        if any(w.lower() in job_words for w in words):
            continue

        if any(w.lower() in invalid_words for w in words):
            continue

        if not all(word.replace(".", "").isalpha() for word in words):
            continue

        return line.title()

    # ====================================================
    # STEP 2
    # Email username
    # ====================================================

    email = extract_email(text)

    if email != "Not Found":

        username = email.split("@")[0]

        username = username.replace(".", " ")
        username = username.replace("_", " ")
        username = username.replace("-", " ")

        username = re.sub(r"\d+", "", username)

        words = [
            w.capitalize()
            for w in username.split()
            if len(w) > 1
        ]

        if 2 <= len(words) <= 4:
            return " ".join(words)

    # ====================================================
    # STEP 3
    # spaCy fallback
    # ====================================================

    entities = ai_entities(text)

    for person in entities["person"]:

        words = person.split()

        if len(words) < 2 or len(words) > 4:
            continue

        if any(char.isdigit() for char in person):
            continue

        if any(w.lower() in invalid_words for w in words):
            continue

        if any(w.lower() in job_words for w in words):
            continue

        if person.lower() in blacklist:
            continue

        return person.title()

    # ====================================================
    # STEP 4
    # Filename fallback
    # ====================================================

    base = os.path.splitext(filename)[0]

    base = re.sub(
        r"(resume|cv|updated|latest|final)",
        "",
        base,
        flags=re.I
    )

    base = re.sub(r"[_\-.]+", " ", base)

    base = re.sub(r"\d+", "", base)

    words = [
        w.capitalize()
        for w in base.split()
        if len(w) > 1
    ]

    if 2 <= len(words) <= 4:
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