from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.error import HTTPError, URLError
import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Capstone_Design.settings")

django.setup()

from problemInfo.models import ProblemInfo, IOExam
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
for tp in testProbs:
    url = f'https://www.acmicpc.net/problem/{str(tp["prob_num"])}'
    try:
        with urlopen(url) as f:
            # http응답 객체
            # print(f)  # <http.client.HTTPResponse object at 0x103c51490>
            html = f.read()
    except HTTPError as e:
        print(e)
    except URLError as e:
        print("server could not be found")

    soup = BeautifulSoup(html, "html5lib")

    problem = {}


    def problem_info(soup, problem):
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
        problem_content = soup.select("#problem_description")[0].find_all(["p", "pre", "ol", "img"])
        for i in problem_content:
            problem_content_info = problem_content_info + str(i.text) + str(i.get("src")).replace("None", "")
        problem["problem_content"] = problem_content_info

        problem_input_info = ""
        problem_input = soup.select("#problem_input > p")
        for i in problem_input:
            problem_input_info = problem_input_info + str(i.text)
        problem["problem_input"] = problem_input_info

        problem_output_info = ""
        problem_output = soup.select("#problem_input > p")
        for i in problem_output:
            problem_output_info = problem_output_info + str(i.text)
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
        try:
            base_url = "https://www.acmicpc.net"
            img = soup.find("div", {"class": "problem-text"})
            img_src = img.find("img")["src"]
            img_url = base_url + img_src
            problem["imgurl"] = img_url
        except TypeError:
            problem["imgurl"] = ""

        return problem


    prob_num = int(url.split("/")[-1])

    problem_data = problem_info(soup, problem)
    problem_pk = ProblemInfo(prob_num=prob_num,
                             title=problem_data["title"],
                             level=1,
                             timeout=problem_data["timeout"],
                             memory_limit=problem_data["memory_limit"],
                             submission=problem_data["submission"],
                             correct=problem_data["correct"],
                             correct_people=problem_data["correct_people"],
                             correct_answer_rate=problem_data["correct_answer_rate"],
                             problem_content=problem_data["problem_content"],
                             problem_input=problem_data["problem_input"],
                             problem_output=problem_data["problem_output"],
                             imgurl=problem_data["imgurl"])
    problem_pk.save()
    print(tp["num"])
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
