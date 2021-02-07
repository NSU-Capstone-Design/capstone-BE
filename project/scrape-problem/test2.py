import urllib.request

from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.error import HTTPError, URLError


url = "https://www.acmicpc.net/problem/1005"
try:
    with urlopen(url) as f:
        # http응답 객체
        print(f)  # <http.client.HTTPResponse object at 0x103c51490>
        html = f.read()
except HTTPError as e:
    print(e)
except URLError as e:
    print("server could not be found")

soup = BeautifulSoup(html, "html5lib")

problem = {}

problem["title"] = soup.find("span", id="problem_title").text
for i in soup.select("table#problem-info > tbody > tr"):
    problemInfo = i.select("td")
    problem["timeout"] = problemInfo[0].text
    problem["memory_limit"] = problemInfo[1].text
    problem["submission"] = problemInfo[2].text
    problem["correct"] = problemInfo[3].text
    problem["correct_people"] = problemInfo[4].text
    problem["correct_answer_rate"] = problemInfo[5].text

for i in soup.select("#problem_description"):
    problemContent = i.select("p")
    for j in range(len(problemContent)):
        problem["problem_content" + str(j+1)] = problemContent[j].text

for i in soup.select("#problem_input"):
    problemInput = i.select("p")
    for j in range(len(problemInput)):
        problem["problem_input" + str(j+1)] = problemInput[j].text

for i in soup.select("#problem_output"):
    problemOutput = i.select("p")
    for j in range(len(problemOutput)):
        problem["problem_output" + str(j+1)] = problemOutput[j].text

for i in soup.select("#problem_limit > ul"):
    problemLimit = i.select("li")
    for j in range(len(problemLimit)):
        problem["problem_limit" + str(j+1)] = problemLimit[j].text


print(problem)