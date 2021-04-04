from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.error import HTTPError, URLError
import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Capstone_Design.settings")

django.setup()

from problemInfo.models import ProblemInfo, IOExam


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

def problem_info(soup, problem):
    problem["title"] = soup.find("span", id="problem_title").text

    problem_content_info = ""
    imgurl = "https://www.acmicpc.net"
    problem_content = soup.select("#problem_description")[0].find_all(["p", "pre", "ol", "img"])
    for i in problem_content:
        problem_content_info = problem_content_info + str(i.text) + str(i.get("src")).replace("None", "")
    problem["problem_content"] = problem_content_info

    return problem

print(problem_info(soup, problem))

problem_data = problem_info(soup, problem)
problem_pk = ProblemInfo(title=problem_data["title"],
                         problem_content=problem_data["problem_content"])
problem_pk.save()

