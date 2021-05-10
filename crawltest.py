from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.error import HTTPError, URLError
import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Capstone_Design.settings")

django.setup()

from problemInfo.models import ProblemInfo, IOExam

url = "https://www.acmicpc.net/problem/1030"
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
    baseurl = "https://www.acmicpc.net/upload/"
    problem["title"] = soup.find("span", id="problem_title").text

    problem_content_info = ""
    problem_content = soup.select("#problem_description")[0].find_all(["p", "pre", "ol", "table", "ul"])
    for i in problem_content:
        problem_content_info = problem_content_info + str(i).replace("/upload/", baseurl)
    problem["problem_content"] = problem_content_info

    problem_input_info = ""
    problem_input = soup.select("#problem_input")[0].find_all(["p", "pre", "ol", "table", "ul"])
    for i in problem_input:
        problem_input_info = problem_input_info + str(i)
    problem["problem_input"] = problem_input_info

    problem_output_info = ""
    problem_output = soup.select("#problem_output")[0].find_all(["p", "pre", "ol", "table", "ul"])
    for i in problem_output:
        problem_output_info = problem_output_info + str(i)
    problem["problem_output"] = problem_output_info

    problem["input_exam_list"] = []
    problem["output_exam_list"] = []
    for i in range(1, 11):
        try:
            problem["input_exam_list"].append(soup.select("#sample-input-" + str(i))[0].text)
        except IndexError:
            pass
        try:
            problem["output_exam_list"].append(soup.select("#sample-output-" + str(i))[0].text)
        except IndexError:
            pass
    return problem


print(problem_info(soup, problem))

problem_data = problem_info(soup, problem)
problem_pk = ProblemInfo(title=problem_data["title"],
                         level=1,
                         problem_content=problem_data["problem_content"],
                         problem_input=problem_data["problem_input"],
                         problem_output=problem_data["problem_output"])
problem_pk.save()
