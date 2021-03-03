from urllib.request import urlopen, Request
import time
import urllib.request
from bs4 import BeautifulSoup
from urllib.error import HTTPError, URLError
import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Capstone_Design.settings")

django.setup()

from problemInfo.models import problemInfo

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

    problem = {"problem_sampleinput2_data": '', "problem_sampleoutput2_data": ''}

    problem_data = problem_info(soup, problem)
    problemInfo(title=problem_data['title'],
                timeout=problem_data['timeout'],
                memory_limit=problem_data['memory_limit'],
                submission=problem_data['submission'],
                correct=problem_data['correct'],
                correct_people=problem_data['correct_people'],
                correct_answer_rate=problem_data['correct_answer_rate'],
                problem_content=problem_data['problem_content'],
                problem_input=problem_data['problem_input'],
                problem_output=problem_data['problem_output'],
                problem_sampleinput1_data=problem_data['problem_sampleinput1_data'],
                problem_sampleoutput1_data=problem_data['problem_sampleoutput1_data'],
                problem_sampleinput2_data=problem_data['problem_sampleinput2_data'],
                problem_sampleoutput2_data=problem_data['problem_sampleoutput2_data']).save()


def problem_info(soup, problem):
    problem["title"] = soup.find("span", id="problem_title").text
    for i in soup.select("table#problem-info > tbody > tr"):
        problemInfo = i.select("td")
        problem["timeout"] = problemInfo[0].text
        problem["memory_limit"] = problemInfo[1].text
        problem["submission"] = problemInfo[2].text
        problem["correct"] = problemInfo[3].text
        problem["correct_people"] = problemInfo[4].text
        problem["correct_answer_rate"] = problemInfo[5].text

    problemContent = soup.select("#problem_description")[0].find_all(["p", "pre", "ol"])
    problem["problem_content"] =problemContent

    problemInput = soup.select("#problem_input > p")
    problem["problem_input"] = problemInput

    problemOutput = soup.select("#problem_output > p")
    problem["problem_output"] = problemOutput

    for i in soup.select("#problem_limit > ul"):
        problemLimit = i.select("li")
        for j in range(len(problemLimit)):
            problem["problem_limit" + str(j + 1)] = problemLimit[j].text

    problem["problem_sampleinput1_data"] = soup.select("#sample-input-1")[0].text
    problem["problem_sampleoutput1_data"] = soup.select("#sample-output-1")[0].text

    try:
        problem["problem_sampleinput2_data"] = soup.select("#sample-input-2")[0].text
    except IndexError:
        pass
    try:
        problem["problem_sampleoutput2_data"] = soup.select("#sample-output-2")[0].text
    except IndexError:
        pass

    try:
        base_url = "https://www.acmicpc.net"
        img = soup.find("div", {"class": "problem-text"})
        img_src = img.find("img")["src"]
        img_url = base_url + img_src
        urllib.request.urlretrieve(img_url, "testimg.jpg")
    except TypeError:
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
page_data = {}

count = 0
for i in pages:
    count += 1
    if count <= 2 or count > 3:
        continue
    page_data[count - 2] = int(i.text) // 100

# 레벨별 페이지수로 페이지별 문제 링크 가져오기
for i in page_data:
    urls = []  # solved.ac 레벨기준으로 한 레벨의 url들
    for j in range(page_data[i] + 1):
        url = "https://solved.ac/problems/level/" + str(i) + "?page=" + str(j + 1)
        urls.append(url)

    for url in urls:
        # 2초 기다리고 실행
        time.sleep(3)
        soup_temp = urlRequest(make_req(url))
        problems_link = soup_temp.select("a.ivEtZs")
        for link in problems_link:
            print(str(i) + "__")
            print(link.get('href'))
            time.sleep(3)
            crawl_prob(link.get('href'), i)
