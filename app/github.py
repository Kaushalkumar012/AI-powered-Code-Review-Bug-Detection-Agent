import requests
from app.config import GITHUB_TOKEN

headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}


def get_pr_diff(repo, pr_number):
    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}"

    response = requests.get(url, headers=headers)

    print("PR FETCH STATUS:", response.status_code)

    return response.json()


def post_comment(repo, pr_number, comment):
    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"

    data = {"body": comment}

    response = requests.post(url, headers=headers, json=data)

    print("COMMENT STATUS:", response.status_code)
    print("RESPONSE:", response.text)