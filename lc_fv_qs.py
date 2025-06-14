import requests
import os
from dotenv import load_dotenv
import json
load_dotenv()

csrf_token = os.environ.get("LEETCODE_CSRF")
session = os.environ.get("LEETCODE_SESSION")
# print(f"csrf token -> {csrf_token}, session -> {session}")
if not csrf_token or not session:
    print("No Keys")
    exit()

headers = {
    "Content-Type": "application/json",
    "x-csrftoken": csrf_token,
    "Cookie": f"LEETCODE_SESSION={session}; csrftoken={csrf_token}"
}
query="""
query favoriteQuestionList($favoriteSlug: String!, $filter: FavoriteQuestionFilterInput, $filtersV2: QuestionFilterInput, $searchKeyword: String, $sortBy: QuestionSortByInput, $limit: Int, $skip: Int, $version: String = "v2") {
  favoriteQuestionList(
    favoriteSlug: $favoriteSlug
    filter: $filter
    filtersV2: $filtersV2
    searchKeyword: $searchKeyword
    sortBy: $sortBy
    limit: $limit
    skip: $skip
    version: $version
  ) {
    questions {
      difficulty
      id
      paidOnly
      questionFrontendId
      status
      title
      titleSlug
      translatedTitle
      isInMyFavorites
      frequency
      acRate
      topicTags {
        name
        nameTranslated
        slug
      }
    }
    totalLength
    hasMore
  }
}
"""
# Define the variables as seen in your raw request payload
variables = {
    "skip": 0,
    "limit": 100,
    "favoriteSlug": "afut4ga7", # This slug might need to be dynamic depending on what list you want
    "filtersV2": {
        "filterCombineType": "ALL",
        "statusFilter": {"questionStatuses": [], "operator": "IS"},
        "difficultyFilter": {"difficulties": [], "operator": "IS"},
        "languageFilter": {"languageSlugs": [], "operator": "IS"},
        "topicFilter": {"topicSlugs": [], "operator": "IS"},
        "acceptanceFilter": {},
        "frequencyFilter": {},
        "frontendIdFilter": {},
        "lastSubmittedFilter": {},
        "publishedFilter": {},
        "companyFilter": {"companySlugs": [], "operator": "IS"},
        "positionFilter": {"positionSlugs": [], "operator": "IS"},
        "premiumFilter": {"premiumStatus": [], "operator": "IS"}
    },
    "searchKeyword": "",
    "sortBy": {"sortField": "CUSTOM", "sortOrder": "ASCENDING"}
}

# Define the operation name
operation_name = "favoriteQuestionList"

# Construct the payload
payload = {
    "query": query,
    "variables": variables,
    "operationName": operation_name
}

# Make the POST request with the JSON payload
response = requests.post(
    "https://leetcode.com/graphql",
    headers=headers,
    json=payload # Use the json parameter to send the payload as JSON
)

# Print in pretty format
print("Status:", response.status_code)
try:
    # print(json.dumps(response.json(), indent=2))
    print(type(response))
    for question in response.json()["data"]["favoriteQuestionList"]["questions"]:
        print(question["title"])
except json.JSONDecodeError:
    print("Response body is not valid JSON:")
    print(response.text)
