from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from datetime import datetime
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import codecs
import traceback

import mysql.connector

# DB 접속을 위한 정보 세팅
mydb = mysql.connector.connect(
    host='localhost', 
    user='root',
    passwd='mysql',
    database='jpa'
)

# sql 실행을 위한 커서 생성
mycursor = mydb.cursor()

# user-agent 정보를 변환해 주는 모듈 임포트
# 특정 브라우저로 크롤링을 진행할 때 차단되는 것을 방지
# pip install fake_useragent
from fake_useragent import UserAgent

# 요청 헤더 정보를 꺼내올 수 있는 모듈
import urllib.request as req

# User Agent 정보 변환 (필수는 아닙니다.)
opener = req.build_opener() # 헤더 정보를 초기화
opener.addheaders = [('User-agent', UserAgent().edge)]
req.install_opener(opener) # 새로운 헤더 정보를 삽입

# 크롬 드라이버에게 전달할 옵션 설정.
options = webdriver.ChromeOptions()
options.add_experimental_option('detach', True)

# 브라우저 안뜨게 하기
# options.add_argument('--headless')

# 크롬 드라이버를 버전에 맞게 자동으로 지원해주는 객체
service = webdriver.ChromeService(ChromeDriverManager().install())

d = datetime.today()

file_path = f'C:/test/멜론 TOP 100_{d.year}_{d.month}_{d.day}.txt'

# 크롬 드라이버 구동
browser = webdriver.Chrome(service=service, options=options)

# 브라우저 사이즈 조정
browser.set_window_size(800, 600)

# 페이지 이동 (베스트셀러 페이지)
browser.get('https://www.melon.com/chart/index.htm')

# 브라우저 내부 대기
# time.sleep(10) -> 브라우저 로딩에 상관 없이 무조건 10초 대기.

# 웹 페이지 전체가 로딩될 때 까지 대기 후 남은 시간 무시
browser.implicitly_wait(10)

soup = BeautifulSoup(browser.page_source, 'html.parser')

try: 
    f = codecs.open(file_path, mode='w', encoding='utf-8')

    top_list = soup.find_all('tr', class_='lst50')
    bottom_list = soup.find_all('tr', class_='lst100')
    # print(top_list[0])
    line1 = top_list[0].find_all('td')
    line2 = bottom_list[0].find_all('td')

    for i in range(50):
        line1 = top_list[i].find_all('td')
        # print(top_list[0].find_all('td'))
        # print(line[1]) # 순위
        # print(f'# 순위: {line1[1].select_one("td>div>span").text}위')
        # print(f'# 곡명: {line1[5].select_one("td div.rank01 > span > a").text}')
        # print(f'# 가수: {line1[5].select_one("td div.rank02 > a").text}')
        # print('-' * 40)
        f.write('\n')
        f.write(f'# 순위: {line1[1].select_one("td>div>span").text}위\n')
        f.write(f'# 곡명: {line1[5].select_one("td div.rank01 > span > a").text}\n')
        f.write(f'# 가수: {line1[5].select_one("td div.rank02 > a").text}\n')
        f.write('-' * 40)   


    for i in range(50):
        line2 = bottom_list[i].find_all('td')
        # print(top_list[0].find_all('td'))
        # print(line[1]) # 순위
        # print(f'# 순위: {line2[1].select_one("td>div>span").text}위')
        # print(f'# 곡명: {line2[5].select_one("td div.rank01 > span > a").text}')
        # print(f'# 가수: {line2[5].select_one("td div.rank02 > a").text}')
        # print('-' * 40)
        f.write('\n')
        f.write(f'# 순위: {line2[1].select_one("td>div>span").text}위\n')
        f.write(f'# 곡명: {line2[5].select_one("td div.rank01 > span > a").text}\n')
        f.write(f'# 가수: {line2[5].select_one("td div.rank02 > a").text}\n')
        f.write('-' * 40)
except:
    print('파일 출력 실패!')
    print(traceback.format_exc())

finally:
    f.close()


#     mydb.commit()


# browser.close()
# mycursor.close()
# mydb.close()