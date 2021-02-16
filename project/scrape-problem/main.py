from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from urllib.error import HTTPError, URLError
import time

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
    if count <= 2 or count > 5:
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
        time.sleep(2)
        soup_temp = urlRequest(make_req(url))
        problems_link = soup_temp.select("a.ivEtZs")
        for link in problems_link:
            problem_scrape(i, link)


def problem_scrape(level, link):
    problem = {
        "id": link[32:],  # 문제 번호
        "title": None,  # 문제 제목
        "level": level,
        "solved_count": 0,  # 푼 횟수
        "average_try": 0,  # 평균시도
    }
