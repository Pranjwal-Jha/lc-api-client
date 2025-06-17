import os,requests,time
from dotenv import load_dotenv
from submit_question import get_submission_id
load_dotenv()

def get_submission_detail():
    csrf_token = os.environ.get("LEETCODE_CSRF")
    session = os.environ.get("LEETCODE_SESSION")

    headers = {
        "Content-Type": "application/json",
        "x-csrftoken": csrf_token,
        "Cookie": f"LEETCODE_SESSION={session}; csrftoken={csrf_token}",
        "Referer": "https://leetcode.com/", # Often required for submission endpoints
        "Origin": "https://leetcode.com",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    }

    reply_url=f"https://leetcode.com/submissions/detail/{get_submission_id()}/check/"
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

if __name__=='__main__':
    get_submission_detail()
