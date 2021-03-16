from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.error import HTTPError, URLError
import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Capstone_Design.settings")

django.setup()

from problemInfo.models import problemInfo, IOExam


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

#    problem["problem_level"] = soup.select(".text-gold")
#    problem["problem_level"] = soup.find("span", class_="text-gold")

    for i in soup.select("table#problem-info > tbody > tr"):
        problem_info_list = i.select("td")
        problem["timeout"] = problem_info_list[0].text
        problem["memory_limit"] = problem_info_list[1].text
        problem["submission"] = problem_info_list[2].text
        problem["correct"] = problem_info_list[3].text
        problem["correct_people"] = problem_info_list[4].text
        problem["correct_answer_rate"] = problem_info_list[5].text

    problem_content_info = []
    problem_content = soup.select("#problem_description")[0].find_all(["p", "pre", "ol"])
    for i in problem_content:
        problem_content_info.append(i.text)
    problem["problem_content"] = problem_content_info

    problem_input_info = []
    problem_input = soup.select("#problem_input > p")
    for i in problem_input:
        problem_input_info.append(i.text)
    problem["problem_input"] = problem_input_info

    problem_output_info = []
    problem_output = soup.select("#problem_input > p")
    for i in problem_output:
        problem_output_info.append(i.text)
    problem["problem_output"] = problem_output_info

    for i in range(1, 6):
        try:
            problem["problem_sampleinput" + str(i) + "_data"] = soup.select("#sample-input-" + str(i))[0].text
        except IndexError:
            problem["problem_sampleinput" + str(i) + "_data"] = ""
        try:
            problem["problem_sampleoutput" + str(i) + "_data"] = soup.select("#sample-output-" + str(i))[0].text
        except IndexError:
            problem["problem_sampleoutput" + str(i) + "_data"] = ""

    try:
        base_url = "https://www.acmicpc.net"
        img = soup.find("div", {"class": "problem-text"})
        img_src = img.find("img")["src"]
        img_url = base_url + img_src
        problem["imgurl"] = img_url
    except TypeError:
        problem["imgurl"] = ""

    return problem

print(problem_info(soup, problem))

problem_data = problem_info(soup, problem)
problemInfo(title = problem_data["title"],
            timeout = problem_data["timeout"],
            memory_limit = problem_data["memory_limit"],
            submission = problem_data["submission"],
            correct = problem_data["correct"],
            correct_people = problem_data["correct_people"],
            correct_answer_rate = problem_data["correct_answer_rate"],
            problem_content = problem_data["problem_content"],
            problem_input = problem_data["problem_input"],
            problem_output = problem_data["problem_output"],
            imgurl = problem_data["imgurl"]).save()

IOExam(title=problem_data["title"],
       problem_sampleinput1_data = problem_data["problem_sampleinput1_data"],
       problem_sampleoutput1_data = problem_data["problem_sampleoutput1_data"],
       problem_sampleinput2_data = problem_data["problem_sampleinput2_data"],
       problem_sampleoutput2_data = problem_data["problem_sampleoutput2_data"],
       problem_sampleinput3_data = problem_data["problem_sampleinput3_data"],
       problem_sampleoutput3_data = problem_data["problem_sampleoutput3_data"],
       problem_sampleinput4_data = problem_data["problem_sampleinput4_data"],
       problem_sampleoutput4_data = problem_data["problem_sampleoutput4_data"],
       problem_sampleinput5_data = problem_data["problem_sampleinput5_data"],
       problem_sampleoutput5_data = problem_data["problem_sampleoutput5_data"]).save()\

