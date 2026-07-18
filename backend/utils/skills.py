import re

SKILLS = [

    "python",

    "java",

    "c",

    "c++",

    "html",

    "css",

    "javascript",

    "react",

    "node",

    "express",

    "mongodb",

    "mysql",

    "sql",

    "git",

    "github",

    "flask",

    "django",

    "docker",

    "aws",

    "linux"

]

def extract_skills(text):

    found = []

    text = text.lower()

    for skill in SKILLS:

        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"
    
        if re.search(pattern, text):
    
            found.append(skill.title())

    return sorted(set(found))