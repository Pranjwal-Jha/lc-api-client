import requests,json,os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv()

def get_submission_id():
    csrf_token = os.environ.get("LEETCODE_CSRF")
    session = os.environ.get("LEETCODE_SESSION")

    if not csrf_token or not session:
        print("No Keys")
        exit()

    headers = {
        "Content-Type": "application/json",
        "x-csrftoken": csrf_token,
        "Cookie": f"LEETCODE_SESSION={session}; csrftoken={csrf_token}",
        "Referer": "https://leetcode.com/", # Often required for submission endpoints
        "Origin": "https://leetcode.com",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    }
    problem_slug="best-time-to-buy-and-sell-stock"
    submission_url=f"https://leetcode.com/problems/{problem_slug}/submit/"
    cpp=Path('main.cpp')
    typed_code=cpp.read_text()
    print(typed_code)
    payload = {
        "lang": "cpp", # Change to the appropriate language slug (e.g., "python3", "java")
        "question_id": "121", # Change to the actual question_id for the problem
        "typed_code":typed_code}
    submit_response=requests.post(
        submission_url,
        headers=headers,
        json=payload
    )
    print("Status ->",submit_response.status_code)
    if submit_response.status_code==200:
        response_data=submit_response.json()
        # print(json.dumps(response_data,indent=2))
        submission_id=response_data["submission_id"]
    else:
        print(f"Error -> {submit_response.status_code}")
        print(f"Error -> {submit_response.text}")
        exit()
    print("The code submitted succesfully!")
    return submission_id
    
