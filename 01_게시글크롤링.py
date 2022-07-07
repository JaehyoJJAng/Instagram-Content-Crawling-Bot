from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import  pyautogui , time , os , re
import urllib.parse as rep
import urllib.request as req
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests as rq
from bs4 import BeautifulSoup as bs
import csv
from conf import get_login_info

class ChromeDriver:
    def __init__(self):
        # options 객체
        self.chrome_options = Options()

        # headless Chrome 선언
        self.chrome_options.add_argument('--headless')

        # 브라우저 꺼짐 방지
        self.chrome_options.add_experimental_option('detach', True)

        self.chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.104 Whale/3.13.131.36 Safari/537.36")

        # 불필요한 에러메시지 없애기
        self.chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

        self.service = Service(executable_path=ChromeDriverManager().install())
        self.browser = webdriver.Chrome(service=self.service, options=self.chrome_options)
        self.browser.maximize_window()

class FaceBookLogin:
    def __init__(self):
        # ChromeDriver class의 browser 객체 불러오기
        self.browser = ChromeDriver().browser

        # 페이스북 id , pw 가져오기
        self.id = get_login_info('FACEBOOK_ID')
        self.pw = get_login_info('FACEBOOK_PW')

    def login_execute(self):
        URL = "https://www.instagram.com/"

        print("""
        페이스북 로그인 중 ..""")
        # 페이지 상태 체크
        response = rq.get(URL)
        if response.status_code == 200:
            self.browser.get(URL)
            self.browser.implicitly_wait(5)

            try:
                # 페이스북으로 로그인하기 버튼 클릭
                fb_login = self.browser.find_element(By.CSS_SELECTOR, "button.sqdOP.yWX7d.y3zKF")
                self.browser.execute_script('arguments[0].click()', fb_login)
                time.sleep(1)

                # 페이스북 아이디 입력
                self.browser.find_element(By.CSS_SELECTOR, "input#email").send_keys(self.id)
                time.sleep(2)

                # 페이스북 패스워드 입력
                self.browser.find_element(By.CSS_SELECTOR, "input#pass").send_keys(self.pw)
                time.sleep(2)

                # 로그인 버튼 클릭
                login_btn = self.browser.find_element(By.CSS_SELECTOR, "button#loginbutton")
                self.browser.execute_script('arguments[0].click()', login_btn)
                time.sleep(2)

                # 페이지 잠깐 로딩
                WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body')))

                # 알림설정 문구 뜨는 경우 : 설정 누르기
                try:
                    # 페이지 잠깐 로딩
                    WebDriverWait(self.browser, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'button.aOOlW.bIiDR')))

                    alarm_btn = self.browser.find_element(By.CSS_SELECTOR, "button.aOOlW.bIiDR")
                    self.browser.execute_script('arguments[0].click()', alarm_btn)
                    time.sleep(1)

                    print("""
                        --- 페이스북 로그인 완료 ! ---""")
                except:  # 알림설정 문구가 뜨지 않는경우
                    pass

                if "오류" in self.browser.find_element(By.CSS_SELECTOR, "body").text:
                    pyautogui.alert('페이지 오류!')
                    return 0

            except:  # 로그인 중 문제가 생긴 경우
                pyautogui.alert('로그인을 실패하였습니다!')
                return 0

        else:  # 페이지 status code가 200이 아닌경우
            pyautogui.alert(f"INSTAGRAM NOW PAGE STATUS CODE : {response.status_code} !!!")
            return 0

class AppInstagram():
    def __init__(self):
        # 타겟 닉네임 멤버변수로 정의
        self.target_nick = self.target_nickname()

        # FaceBookLogin class 객체 멤버변수로 정의
        self.login = FaceBookLogin()

        # FaceBookLogin class 에서 Driver 객체 불러오기
        self.browser = self.login.browser

        # headers
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.57 Whale/3.14.133.23 Safari/537.36'
        self.headers = {'User-Agent': self.user_agent}

        # URL
        self.url = "https://www.instagram.com" + '/' + self.target_nick + '/'

    def run(self):
        # 페이스북 로그인하기
        login_result = self.login.login_execute()

        if login_result != 0 :
            # 페이지 유효성 검사(비공개 계정 또는 게시글 0인 계정)
            urlCheck = self.content_check(url=self.url)

            # 비공개 계정 x , 게시글 1개 이상인 계정의 경우 아래 코드 실행
            if urlCheck != 0 :
                pass


    def click_content(self):
        try:
            self.browser.get(url=self.url)

            # 로딩 대기하기
            element = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.v1Nh3.kIKUG._bz0w > a'))
            )

            # 게시글 길이 가져오기
            content_list_len = len(self.browser.find_elements(By.CSS_SELECTOR, "div.v1Nh3.kIKUG._bz0w > a"))

            # 게시글이 12개 이상인 경우 스크롤 내리기
            if content_list_len > 12:
                self.scroll()

                # 게시글 길이 업데이트 하기
                content_list_len = len(self.browser.find_elements(By.CSS_SELECTOR, "div.v1Nh3.kIKUG._bz0w > a"))

            # 첫 번째 게시글 클릭하기
            a_tags = self.browser.find_elements(By.CSS_SELECTOR, 'div.v1Nh3.kIKUG._bz0w > a')[0]
            self.browser.execute_script('arguments[0].click()', a_tags)
            time.sleep(3)

            ## 수집할 게시물의 수 ##
            target_cnt = content_list_len
            for i in range(1, target_cnt + 1):
                try:
                    # 댓글 정보 가져오기
                    self.get_content(browser=self.browser,count=i)

                    # 현재 카운트가 target_cnt와 동일한경우
                    if i == target_cnt:
                        break

                    # 다음 게시글 넘어가기
                    self.move_next(browser=self.browser)
                except:
                    print("DATA CRAWLING FAILED")
                    time.sleep(2)

                    # 게시글 크롤링 오류 시 다음 게시글 이동
                    self.move_next(browser=self.browser)
        except:
            pyautogui.alert('현재 페이지에 문제가 있습니다!')
            return 0

    def get_content(self,browser, count):
        # 현재 드라이버의 페이지소스 파싱하기
        soup = bs(browser.page_source, 'html.parser')

        # 본문내용
        content = soup.select('div.MOdxS')[0]

        # 게시글 등록일
        content_time = soup.select('time.FH9sR.RhOlS')[0]

        # 좋아요 개수
        like_cnt = soup.select_one('div._7UhW9.xLCgt.qyrsm.KV-D4.fDxYl.T0kll > span')

        # 이미지 가져오기 (여러 이미지가 있는 경우 썸네일만 가져옴)
        image = soup.select_one('div.pbNvD.QZZGH.bW6vo div.KL4Bh > img')

        # content 분기처리
        if content == None or content.text == '':
            content = '-'
        else:
            content = content.text.strip()
            content = re.sub('#.*', '', content)

        # content_time 분기처리
        if content_time == None or content_time.text == '':
            content_time = '-'
        else:
            content_time = content_time.text.strip()

        if like_cnt == None or like_cnt.text == '':
            like_cnt = 0
        else:
            like_cnt = like_cnt.text.strip()
            like_cnt = int(re.sub('[,]', '', like_cnt))

        #* --- 이미지 다운로드 ---

        # # 이미지 링크주소 추출하기
        # image_link = image.attrs['src']
        #
        # # 이미지 파일명 지정하기
        # fileName = os.path.join(imagePath, f'{count}.png')
        #
        # # 이미지 다운로드하기
        # req.urlretrieve(image_link, fileName)
        #
        # # 열린 csv 파일에 데이터 옮겨담기
        # csvWriter.writerow([content, content_time, like_cnt])

        #* --- 이미지 다운로드 ---

        # 추출데이터 출력하기
        print(
            f"본문내용 : {content}\n등록일 : {content_time}\n좋아요 수 : {like_cnt}\n")

    def move_next(self,browser):
        next_btn = self.browser.find_element(By.CSS_SELECTOR, 'div.l8mY4.feth3 > button')
        self.browser.execute_script('arguments[0].click()', next_btn)
        time.sleep(2)

    def content_check(self,url):
        self.browser.get(url=self.url)
        self.browser.implicitly_wait(15)

        # 웹페이지 로딩대기
        WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'h2._7UhW9.fKFbl.yUEEX.KV-D4.fDxYl')))

        # bs로 파싱하기
        soup = bs(self.browser.page_source, 'html.parser')

        # 비공개 계정인 경우
        secret_account = soup.select_one('h2.rkEop')

        # 비공개 계정은 아니나 게시글이 하나도 없는 경우
        no_content_account = soup.select_one('h1._7UhW9.fKFbl.yUEEX.KV-D4.uL8Hv')

        if secret_account:  # 비공개 계정 분기처리
            pyautogui.alert("비공개 계정은 크롤링할 수 없습니다")
            return 0

        elif no_content_account:  # 게시글이 하나도 없는경우 분기처리
            pyautogui.alert('게시글이 없어 크롤링할 수 없습니다')
            return 0


    def target_nickname(self):
        while True:
            os.system('cls')
            nickname = input("""크롤링 하길 원하시는 상대방의 인스타그램 닉네임 또는 아이디를 입력해주세요

    :""")
            if nickname == "":
                pyautogui.alert("키워드 값이 정상적이지 않습니다")
                os.system('cls')
                continue

            if re.match('[0-9]', nickname):
                print("입력이 올바르지 않습니다")
                os.system('cls')
                continue

            return nickname

    def scroll(self):
        prev_height = self.browser.execute_script("return document.documentElement.scrollHeight")

        while True:
            # 스크롤 내리기
            self.browser.execute_script("window.scrollTo(0 , document.documentElement.scrollHeight)")

            # 대기시간 할당하기
            time.sleep(2)

            # 새로운 높이 값 받기
            curr_height = self.browser.execute_script("return document.documentElement.scrollHeight")

            if curr_height == prev_height:
                break

            prev_height = curr_height



if __name__ == '__main__' :
    app = AppInstagram()

    # run 메소드 실행
    app.run()












