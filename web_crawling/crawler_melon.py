# selenium import
from selenium import webdriver
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import urllib.request as req
from datetime import datetime
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import codecs


d = datetime.today()

file_path = f'C:/test/멜론일간차트순위_{d.year}년{d.month}월{d.day}일{d.hour}시기준.txt'
# 헤더 정보 초기화
opener = req.build_opener()
# User Agent 정보
opener.addheaders = [('User-agent', UserAgent().edge)]
# 헤더 정보 삽입
req.install_opener(opener)


# 크롬 드라이버에게 전달할 옵션 설정.
options = webdriver.ChromeOptions()
options.add_experimental_option('detach', True)


# 크롬 드라이버를 버전에 맞게 자동으로 지원해주는 객체
service = webdriver.ChromeService(ChromeDriverManager().install())

# 크롬 드라이버 구동
browser = webdriver.Chrome(service=service, options=options)

# 브라우저 사이즈 조정
browser.set_window_size(800, 600)

'''
- with문을 사용하면 with 블록을 벗어나는 순간
 객체가 자동으로 해제됩니다. (자바의 try with resource와 비슷)

- with 작성 시 사용할 객체의 이름을 as 뒤에 작성해 줍니다.
'''

with codecs.open(file_path, mode='w', encoding='utf-8') as f:

    # 페이지 이동
    target_page = 'https://www.melon.com/chart/day/index.htm'
    browser.get(target_page)

    soup = BeautifulSoup(browser.page_source, 'html.parser')

    for cnt in [50, 100]:

        song_tr_list = soup.select(f'#lst{cnt}')

        for song_tr in song_tr_list:

            # 순위 찾기
            rank = song_tr.select_one('div.wrap.t_center').text.strip()
            print(rank)

            # 가수 이름 찾기
            artist_name = song_tr.select_one('div.wrap div.ellipsis.rank02 > a').text.strip()
            print(artist_name)

            # 앨범명 찾기
            album_name = song_tr.select_one('div.wrap div.ellipsis.rank03 > a').text.strip()
            print(album_name)

            # 노래명 찾기
            song_name = song_tr.select_one('div.wrap div.ellipsis.rank01 > span > a').text.strip()
            print(song_name)


            print("=" * 40)

            f.write(f'# 순위: {rank}\n')
            f.write(f'# 가수명: {artist_name}\n')
            f.write(f'# 앨범명: {album_name}\n')
            f.write(f'# 노래 제목: {song_name}\n')
            f.write('-' * 40 + '\n')


browser.close()