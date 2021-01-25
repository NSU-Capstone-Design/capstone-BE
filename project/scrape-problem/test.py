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
problemInfo = soup.select("table#problem-info > tbody > tr > td")
problem["timeout"] = problemInfo[0].text
problem["memory_limit"] = problemInfo[1].text
problem["submission"] = problemInfo[2].text
problem["correct"] = problemInfo[3].text
problem["correct_people"] = problemInfo[4].text
problem["correct_answer_rate"] = problemInfo[5].text

# problem_title = soup.select('tr > td:nth-child(2) > a')

print(problem)