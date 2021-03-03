import urllib.request

from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.error import HTTPError, URLError

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Capstone_Design.settings")
import django

django.setup()
from problemInfo.models import problemInfo

url = "https://www.acmicpc.net/problem/1006"
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

problem = {"problem_sampleinput2_data":'',"problem_sampleoutput2_data":''}

def problem_info():
    problem["title"] = soup.find("span", id="problem_title").text
    for i in soup.select("table#problem-info > tbody > tr"):
        problemInfo = i.select("td")
        problem["timeout"] = problemInfo[0].text
        problem["memory_limit"] = problemInfo[1].text
        problem["submission"] = problemInfo[2].text
        problem["correct"] = problemInfo[3].text
        problem["correct_people"] = problemInfo[4].text
        problem["correct_answer_rate"] = problemInfo[5].text

    problemContent = soup.select("#problem_description > p")
    problem["problem_content"] = problemContent

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

problem_data = problem_info()
problemInfo(title = problem_data['title'],
            timeout = problem_data['timeout'],
            memory_limit = problem_data['memory_limit'],
            submission = problem_data['submission'],
            correct = problem_data['correct'],
            correct_people = problem_data['correct_people'],
            correct_answer_rate = problem_data['correct_answer_rate'],
            problem_content = problem_data['problem_content'],
            problem_input = problem_data['problem_input'],
            problem_output = problem_data['problem_output'],
            problem_sampleinput1_data = problem_data['problem_sampleinput1_data'],
            problem_sampleoutput1_data = problem_data['problem_sampleoutput1_data'],
            problem_sampleinput2_data=problem_data['problem_sampleinput2_data'],
            problem_sampleoutput2_data=problem_data['problem_sampleoutput2_data']).save()

print(problem_info())