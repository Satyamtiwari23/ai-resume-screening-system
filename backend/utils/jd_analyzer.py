import os
import json

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def analyze_job_description(job_description):

    prompt = f"""
You are an experienced Technical Recruiter.

Analyze the following Job Description.

Job Description

{job_description}

Return ONLY valid JSON.

Extract:

1. Job Role
2. Seniority
3. Mandatory Skills
4. Preferred Skills
5. Required Experience
6. Education
7. Responsibilities

Return exactly:

{{
    "role":"",
    "level":"",
    "required_skills":[],
    "preferred_skills":[],
    "experience":"",
    "education":"",
    "responsibilities":[]
}}

Do not write anything else.
"""

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ],

        response_format={
            "type":"json_object"
        },

        temperature=0.2

    )

    return json.loads(
        response.choices[0].message.content
    )