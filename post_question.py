from datetime import time
import json,os,requests,time
from dotenv import load_dotenv
load_dotenv()
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
payload = {
    "lang": "cpp", # Change to the appropriate language slug (e.g., "python3", "java")
    "question_id": "121", # Change to the actual question_id for the problem
    "typed_code": """class Solution {
public:
    int maxProfit(vector<int>& prices) {
        int start=0;
        int maxpri=0;
        for(int i=0;i<prices.size();i++){
            if(prices[i]<prices[start]) start=i;
            maxpri=max(maxpri,prices[i]-prices[start]);
        }
        return maxpri;
    }
};"""
}
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
reply_url=f"https://leetcode.com/submissions/detail/{submission_id}/check/"

max_check=4
check_delay=0.5
time.sleep(1)
check_data=""
for i in range(max_check):
    check_response=requests.get(
        reply_url,
        headers=headers
    )
    # print(f"Attempt {i+1}: Status -> {check_response.status_code}")
    if check_response.status_code==200:
        check_data=check_response.json()
        if check_data.get("run_success") is not None:
                break
    else:
        print(f"Error{check_response.text}")
    if i<max_check-1:
        print(f"Status not final, waiting for {check_delay} seconds")
        time.sleep(check_delay)

print(f"The code ran {'Successfully' if check_data.get('run_success') else 'Failed'}")
