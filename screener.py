import os
from groq import Groq

client = Groq(api_key=os.environ.get("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"))

def analyze_resume(resume_text: str, job_description: str) -> dict:
    prompt = f"""
    You are an expert HR assistant and resume screener.
    
    Analyze the following resume against the job description and provide:
    1. A match score out of 100
    2. Missing skills or qualifications
    3. Suggestions to improve the resume for this job
    
    Job Description:
    {job_description}
    
    Resume:
    {resume_text}
    
    Respond in this exact format:
    MATCH SCORE: [score]/100
    MISSING SKILLS: [list the missing skills separated by commas]
    SUGGESTIONS: [list your suggestions]
    """

    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile",
    )

    response = chat_completion.choices[0].message.content

    lines = response.strip().split('\n')
    result = {
        "match_score": "",
        "missing_skills": "",
        "suggestions": ""
    }

    current_key = None
    for line in lines:
        if line.startswith("MATCH SCORE:"):
            current_key = "match_score"
            result["match_score"] = line.replace("MATCH SCORE:", "").strip()
        elif line.startswith("MISSING SKILLS:"):
            current_key = "missing_skills"
            result["missing_skills"] = line.replace("MISSING SKILLS:", "").strip()
        elif line.startswith("SUGGESTIONS:"):
            current_key = "suggestions"
            result["suggestions"] = line.replace("SUGGESTIONS:", "").strip()
        elif current_key and line.strip():
            result[current_key] += " " + line.strip()

    return result