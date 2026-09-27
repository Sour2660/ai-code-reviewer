import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from services.ast_parser import count_max_loop_depth
from services.ai_reviewer import review_code_with_ai

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="AI Code Reviewer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeSubmission(BaseModel):
    language: str
    code: str

@app.post("/api/review")
async def review_code(submission: CodeSubmission):
    if submission.language != "python":
        raise HTTPException(status_code=400, detail="Only Python is supported initially.")
    
    # 1. Structural Analysis (DSA - AST Traversal)
    try:
        max_depth = count_max_loop_depth(submission.code)
    except SyntaxError:
        raise HTTPException(status_code=400, detail="Syntax Error: The provided Python code is invalid.")

    # Calculate Big-O based on loop nesting
    if max_depth == 0:
        time_complexity = "O(1) or O(N) depending on built-in functions"
    elif max_depth == 1:
        time_complexity = "O(N)"
    elif max_depth == 2:
        time_complexity = "O(N^2)"
    else:
        time_complexity = f"O(N^{max_depth})"

    # 2. Qualitative Analysis (AI / LLM)
    try:
        ai_feedback = review_code_with_ai(submission.code, time_complexity)
    except Exception as e:
        print(f"AI Error: {e}")
        ai_feedback = "AI analysis failed. Please check your OpenAI API key and balance."

    # 3. Return Combined Payload
    return {
        "status": "success",
        "ast_analysis": {
            "max_nested_loops": max_depth,
            "estimated_complexity": time_complexity
        },
        "ai_feedback": ai_feedback
    }