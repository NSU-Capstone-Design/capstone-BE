from urllib.request import urlopen, Request
import time
from bs4 import BeautifulSoup
from urllib.error import HTTPError, URLError
import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Capstone_Design.settings")

django.setup()

from problemInfo.models import ProblemInfo, IOExam


def crawl_prob(url, level):
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
    prob_num = int(url.split("/")[-1])
    problem = {}

    problem_data = problem_info(soup, problem)
    problem_pk = ProblemInfo(prob_num=prob_num,
                             title=problem_data["title"],
                             level=level,
                             timeout=problem_data["timeout"],
                             memory_limit=problem_data["memory_limit"],
                             submission=problem_data["submission"],
                             correct=problem_data["correct"],
                             correct_people=problem_data["correct_people"],
                             correct_answer_rate=problem_data["correct_answer_rate"],
                             problem_content=problem_data["problem_content"],
                             problem_input=problem_data["problem_input"],
                             problem_output=problem_data["problem_output"])
    problem_pk.save()
    count = 0
    for input, output in zip(problem_data['input_exam_list'], problem_data['output_exam_list']):
        count = count + 1
        IOExam(problem=problem_pk,
               value=input,
               io_num=count,
               is_input=True,
               ).save()
        IOExam(problem=problem_pk,
               value=output,
               io_num=count,
               is_input=False,
               ).save()


def problem_info(soup, problem):
    baseUrl = "https://www.acmicpc.net/upload/"
    problem["title"] = soup.find("span", id="problem_title").text
    for i in soup.select("table#problem-info > tbody > tr"):
        problem_info_list = i.select("td")
        problem["timeout"] = problem_info_list[0].text
        problem["memory_limit"] = problem_info_list[1].text
        problem["submission"] = problem_info_list[2].text
        problem["correct"] = problem_info_list[3].text
        problem["correct_people"] = problem_info_list[4].text
        problem["correct_answer_rate"] = problem_info_list[5].text

    problem_content_info = ""
    problem_content = soup.select("#problem_description")[0].find_all(["p", "pre", "ol", "table", "ul"])
    for i in problem_content:
        problem_content_info = problem_content_info + str(i).replace("/upload/", baseUrl)
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


"""
1. 처음에 https://solved.ac/problems/level여기서 레벨별 문제 개수를 가지고 딕셔너리로 만듦
2. 레벨별 백준 문제링크를 가져옴
3. 문제링크를 통해서 problem모델에 넣을 데이터를 가져옴
"""


# 헤더에 User-Agent를 추가시켜주는 함수 : 안하면 403뜰 수 있음
def make_req(site):
    hdr = {"User-Agent": "Mozilla/5.0"}
    return Request(site, headers=hdr)


# 요청 처리 함수
def urlRequest(req):
    try:
        with urlopen(req) as f:
            # http응답 객체
            # print(f)  # <http.client.HTTPResponse object at 0x103c51490>
            html = BeautifulSoup(f.read(), "html5lib")
            return html
    except HTTPError as e:
        return e
    except URLError as e:
        return "server could not be found"


LEVELS = make_req("https://solved.ac/problems/level")
# html 형식으로 파싱 된 문자열로 만듦
soup = urlRequest(LEVELS)

# problem_title = soup.findAll("a")
# problem_title = soup.select("a.ivEtZs")
pages = soup.select("div.cDWUBS > div:nth-child(4)")
# for i in problem_title:
#     print(i["href"])

# 난이도별 문제 개수로 추가 페이지 알아내기 { "난이도" : "추가페이지 수" }
testProbs = [
    {
        "num": 1,
        "weight": 3,
        "prob_num": 10172
    },
    {
        "num": 2,
        "weight": 3,
        "prob_num": 14681
    },
    {
        "num": 3,
        "weight": 3,
        "prob_num": 2439
    },
    {
        "num": 4,
        "weight": 3,
        "prob_num": 2577
    },
    {
        "num": 5,
        "weight": 3,
        "prob_num": 2869
    },
    {
        "num": 6,
        "weight": 3,
        "prob_num": 1018
    },
    {
        "num": 7,
        "weight": 3,
        "prob_num": 10845
    },
    {
        "num": 8,
        "weight": 3,
        "prob_num": 2606
    },
    {
        "num": 9,
        "weight": 3,
        "prob_num": 1912
    },
    {
        "num": 10,
        "weight": 3,
        "prob_num": 1927
    },
    {
        "num": 11,
        "weight": 3,
        "prob_num": 1753
    },
    {
        "num": 12,
        "weight": 3,
        "prob_num": 1922
    },
    {
        "num": 13,
        "weight": 3,
        "prob_num": 1613
    },
    {
        "num": 14,
        "weight": 3,
        "prob_num": 1753
    },
    {
        "num": 15,
        "weight": 3,
        "prob_num": 2585
    },
]

for i in testProbs:
    crawl_prob(f'https://www.acmicpc.net/problem/{i["prob_num"]}', level=i["num"])

