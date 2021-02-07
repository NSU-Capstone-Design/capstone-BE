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
problemInfo = soup.select("table#problem-info > tbody > tr > td")
problem["timeout"] = problemInfo[0].text
problem["memory_limit"] = problemInfo[1].text
problem["submission"] = problemInfo[2].text
problem["correct"] = problemInfo[3].text
problem["correct_people"] = problemInfo[4].text
problem["correct_answer_rate"] = problemInfo[5].text

problem["problem_content"] = soup.select("#description > .headline > h2")[0].text
problemContent = soup.select("#problem_description > p")
problem["problem_content1"] = problemContent[0].text
problem["problem_content2"] = problemContent[1].text
problem["problem_content4"] = problemContent[3].img['src']
problem["problem_content5"] = problemContent[4].text
problem["problem_content6"] = problemContent[5].text
problem["problem_content7"] = problemContent[6].text
problem["problem_content8"] = problemContent[7].text

problem["problem_input"] = soup.select("#input > .headline > h2")[0].text
problemInput = soup.select("#problem_input > p")
problem["problem_input1"] = problemInput[0].text
problem["problem_input2"] = problemInput[1].text
problem["problem_input3"] = problemInput[2].text

problem["problem_output"] = soup.select("#output > .headline > h2")[0].text
problemOutput = soup.select("#problem_output > p")
problem["problem_output1"] = problemOutput[0].text
problem["problem_output2"] = problemOutput[1].text

problem["problem_limit"] = soup.select("#limit > .headline > h2")[0].text
problemLimit = soup.select("#problem_limit > ul > li")
problem["problem_limit1"] = problemLimit[0].text
problem["problem_limit2"] = problemLimit[1].text
problem["problem_limit3"] = problemLimit[2].text
problem["problem_limit4"] = problemLimit[3].text

problem["problem_sampleinput1"] = soup.select("#sampleinput1 > .headline > h2")[0].text
problem["problem_sampleinput1_data"] = soup.select("#sample-input-1")[0].text

problem["problem_sampleoutput1"] = soup.select("#sampleoutput1 > .headline > h2")[0].text
problem["problem_sampleoutput1_data"] = soup.select("#sample-output-1")[0].text

problem["problem_sampleinput2"] = soup.select("#sampleinput2 > .headline > h2")[0].text
problem["problem_sampleinput2_data"] = soup.select("#sample-input-2")[0].text


problem["problem_sampleoutput2"] = soup.select("#sampleoutput2 > .headline > h2")[0].text
problem["problem_sampleoutput2_data"] = soup.select("#sample-output-2")[0].text

# problem_title = soup.select('tr > td:nth-child(2) > a')

print(problem)