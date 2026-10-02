import os
import time 
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

client = None

if API_KEY:
    client = genai.Client(api_key=API_KEY)


def ask_ai(question, students):

    if not client:

        return (
            "Gemini API key is not configured. "
            "Please add GEMINI_API_KEY to the .env file."
        )

    student_data = []

    for student in students:

        student_data.append({
            "id": student.id,
            "name": student.name,
            "email": student.email,
            "age": student.age,
            "course": student.course,
            "year": student.year,
            "marks": student.marks
        })

    prompt = f"""
You are an AI assistant inside a Student Database Management System.

Your job is to answer questions about the students in the database.

IMPORTANT RULES:

1. Use ONLY the student data provided below.
2. Never invent student information.
3. Perform calculations when required.
4. Answer clearly and concisely.
5. If the requested information does not exist, say so.

STUDENT DATABASE:

{student_data}

USER QUESTION:

{question}
"""

    try:
        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt
                )

                return response.text

            except Exception as e:
                if "503" in str(e) and attempt < 2:
                    time.sleep(3)
                else:
                    return f"Gemini error: {str(e)}"

    except Exception as e:
        return f"Gemini error: {str(e)}"