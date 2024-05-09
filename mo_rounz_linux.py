import os

os.system('pip install --upgrade selenium')

from selenium import webdriver
from selenium.webdriver.common.by import By
import time, sys, shutil
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup
import random

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service

aos_user_agent = 'Mozilla/5.0 (Linux; Android 13; SM-F721N Build/TP1A.220624.014; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/118.0.5993.111 Mobile Safari/537.36'

# Chrome 옵션 설정
chrome_driver_path = 'chromedriver-linux64/chromedriver'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f'user-agent={aos_user_agent}')
chrome_options.add_argument("--headless=new")  # 헤드리스 모드 활성화
chrome_options.add_argument("--no-sandbox")  # 샌드박스 모드 비활성화
chrome_options.add_argument("--disable-dev-shm-usage")  # /dev/shm 사용 안함
chrome_options.add_argument('window-size=412,915') # 모바일 해상도
chrome_options.add_argument('--disable-gpu') # 그래픽 모드 사용
chrome_options.add_argument('--ignore-certificate-errors') # https 인증 스킵

print(webdriver.__version__)

# WebDriver 인스턴스 생성
service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

login_url = 'https://rounz.com/home.php'
create_date = datetime.now().strftime("%Y%m%d_%H%M%S")
screenshot_path = f'screenshot/{create_date}'
driver.implicitly_wait(10)
wait = WebDriverWait(driver, 30)


def pc_login():
    # 웹사이트 타이틀 출력
    driver.get(login_url)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    print(driver.title)

    # 스크린샷 폴더 생성
    if not os.path.exists(screenshot_path):
        os.makedirs(screenshot_path)

    # 세션 생성
    session = requests.session()

    # token 로그인
    headers = {
        'Authorization': 'Bearer W9l7js-2dRr8D0B1sGf2qbyKTxmAK1yc307jTBiGfL_m5E3T0cplwlS933zLydu6',
    }
    
    token_response = session.post(login_url, headers=headers, verify=False)

    try:
        if token_response.ok:
            for cookie in session.cookies:
                cookie_dict = {
                    'name': cookie.name,
                    'value': cookie.value,
                    'path': '/',
                    'secure': cookie.secure,
                    'domain': 'rounz.com'
                }
                driver.add_cookie(cookie_dict)
            print(login_url, "로그인 성공")
            print(f"응답 코드: {token_response.status_code}")
            print(f"응답 헤더: {token_response.headers}")
            print(f"응답 쿠키: {token_response.cookies}")
            time.sleep(random.uniform(1, 5))
        else:
            print(f"로그인 실패: {token_response.status_code}")
            print(token_response.text)  # 상세한 에러 메시지 출력
            driver.save_screenshot(f'{screenshot_path}/m_error.png')
            sys.exit(1)  # 실패 시 스크립트 종료
    except Exception as e:
        print("웹 페이지 접속 실패", str(e))
        driver.save_screenshot(f'{screenshot_path}/m_error.png')
        sys.exit(1)  # 실패 시 스크립트 종료
    
def pc_order():
    while True:
        # 랜덤 제품 선택
        try:
            driver.get(login_url)
            time.sleep(random.uniform(1, 5))
            driver.save_screenshot(f'{screenshot_path}/m_ROUNZ1.png')

            # 셀레니움으로부터 페이지의 HTML 얻기
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            # 특정 ul 클래스 내의 모든 a 태그 검색
            product_links = soup.select('ul.list a[href]')

            # href 속성에서 URL 추출
            product_urls = [link['href'] for link in product_links if 'productIndex' in link['href']]

            # URL 리스트에서 랜덤하게 하나의 URL 선택
            selected_url = random.choice(product_urls) if product_urls else None
            driver.get(f'https://rounz.com/{selected_url}')
            #driver.get('https://rounz.com/product.php?productIndex=2566741') # 임시 품절 상품
            #driver.get('https://rounz.com/product.php?productIndex=3009202') # 다중 선택 상품
            #driver.get('https://rounz.com/product.php?productIndex=3013762') # 구매하기 3차 skip
            #driver.get('https://rounz.com/product.php?productIndex=3013624') # headless 테스트 과정에서 다중 제품 선택 창 이슈
            print(selected_url, "제품 선택 성공")
            time.sleep(random.uniform(1, 5))
            driver.save_screenshot(f'{screenshot_path}/m_ROUNZ2.png')
            
            # 원본 HTML
            html = '<div style="display: block !important;">'

            # BeautifulSoup을 사용하여 HTML 파싱
            soup = BeautifulSoup(html, 'html.parser')

            # 변경할 요소 선택
            target_div = soup.find('div', style='display: block !important;')

            # 요소가 존재하는지 확인하고 수정
            if target_div:
                # 요소의 스타일 변경
                target_div['style'] = 'display: none !important;'

                # 변경된 HTML 출력
                print(soup.prettify())
                #driver.save_screenshot(f'{screenshot_path}/m_ROUNZ2-1.png')
                time.sleep(random.uniform(1, 5))
                driver.refresh()
                time.sleep(random.uniform(1, 5))
                #driver.save_screenshot(f'{screenshot_path}/m_ROUNZ2-2.png')

            # 물품 구매 버튼 1차
            found_buy_long = False
            found_buy_noti = False
            found_buy = False

            # 'li' 태그를 가진 모든 요소를 찾기
            li_elements = driver.find_elements(By.XPATH, "//div[@class='detail_wrap']//li")

            # 각 'li' 요소의 'class' 속성 값 확인
            for li in li_elements:
                class_value = li.get_attribute("class")

                if "buy noti" in class_value:
                    print(class_value, "일시 품절 상품. 제품 재선택 시도")
                    found_buy_noti = True
                    break 
                elif "buy long" in class_value:
                    print(class_value)
                    found_buy_long = True
                    break  
                elif "buy" in class_value:
                    print(class_value)
                    found_buy = True
                    break

            if found_buy_noti:
                continue
            elif found_buy_long:
                break
            elif found_buy:
                break
            else:
                raise Exception("제품 선택 실패")

        except Exception as e:
            print("제품 선택 실패", str(e))
            driver.save_screenshot(f'{screenshot_path}/m_error.png')
            sys.exit(1)  # 실패 시 스크립트 종료

    try:
        order_first_button = driver.find_element(By.CSS_SELECTOR, "a.order")
        order_first_button.click()
        print("구매하기 1차 성공")
        time.sleep(random.uniform(1, 5))
        driver.save_screenshot(f'{screenshot_path}/m_ROUNZ3.png')
    except Exception as e:
        print("구매하기 1차 실패", str(e))
        driver.save_screenshot(f'{screenshot_path}/m_error.png')
        sys.exit(1) # 실패 시 스크립트 종료

# 물품 구매 버튼 2차
    try:
        order_second_button = driver.find_element(By.CSS_SELECTOR, "a.order")
        order_second_button.click()

        try:
            # 얼럿이 나타날 때까지 최대 5초간 대기
            alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
            # 얼럿 메시지 확인
            if "상품을 선택해주세요." in alert.text:
                time.sleep(random.uniform(1, 5))
                alert.accept()  # 얼럿 확인 버튼 클릭
                time.sleep(random.uniform(1, 5))

            try:
                # 클래스가 "detail_bottom open"인 div 내부에 있는 data-index 속성을 가진 모든 a 태그를 찾기
                elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'detail_bottom') and contains(@class, 'open')]//a[@data-index]")))
                # elements에서 class가 sold_out가 아닌 요소만 골라내기
                filtered_elements = [element for element in elements if "sold_out" not in element.get_attribute("class")]
                random_element = random.choice(filtered_elements)
                random_element.click()
                time.sleep(random.uniform(1, 5))

                order_second_button.click()
                time.sleep(random.uniform(1, 5))

            except Exception as e:
                print(f"상품 가져오는 중 오류 발생: {str(e)}")
                driver.save_screenshot(f'{screenshot_path}/m_error.png')
                sys.exit(1)
        except TimeoutException:
            # 얼럿이 나타나지 않으면 다음 프로세스로 진행
            pass
        print("구매하기 2차 성공")
        time.sleep(random.uniform(1, 5))
        driver.save_screenshot(f'{screenshot_path}/m_ROUNZ4.png')
    except Exception as e:
        print("구매하기 2차 실패", str(e))
        driver.save_screenshot(f'{screenshot_path}/m_error.png')
        sys.exit(1)  # 실패 시 스크립트 종료

    # 물품 구매 버튼 3차
    try:
        order_third_button = driver.find_element(By.XPATH, "//a[contains(text(), '구매하기(')]")
        order_third_button.click()
        print("구매하기 3차 성공")
        time.sleep(random.uniform(1, 5))
        driver.save_screenshot(f'{screenshot_path}/m_ROUNZ5.png')
    except Exception as e:
        print("구매하기 3차 실패", str(e))
        pass


def buy_option_TOSS():
    # 주문자 정보 설정
    try:
        time.sleep(random.uniform(1, 5))
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(random.uniform(1, 5))
        order_info_button = driver.find_element(By.XPATH, "//label[contains(text(), '주문자 정보와 동일')]")
        driver.execute_script("arguments[0].click();", order_info_button)
        #order_info_button.click()
        print("주문자 정보 설정 성공")
        time.sleep(random.uniform(1, 5))
        driver.save_screenshot(f'{screenshot_path}/m_TOSS1.png')
    except Exception as e:
        print("주문자 정보 설정 실패", str(e))
        driver.save_screenshot(f'{screenshot_path}/m_error.png')
        sys.exit(1)  # 실패 시 스크립트 종료

    # 페이지 아래쪽으로 스크롤
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.uniform(1, 5))
    except Exception as e:
        print("페이지 스크롤 실패", str(e))
        driver.save_screenshot(f'{screenshot_path}/m_error.png')
        sys.exit(1)  # 실패 시 스크립트 종료
    # 결제 방식 선택
    try:
        select_order_button = driver.find_element(By.ID, "pay_26")
        select_order_button.click()
        print("TOSS Pay 결제 선택 성공")
        time.sleep(random.uniform(1, 5))
        driver.save_screenshot(f'{screenshot_path}/m_TOSS2.png')
    except Exception as e:
        print("TOSS Pay 결제 선택 실패", str(e))
        driver.save_screenshot(f'{screenshot_path}/m_error.png')
        sys.exit(1)  # 실패 시 스크립트 종료

    # 구매 동의
    try:
        confirm_button = driver.find_element(By.XPATH, "//label[contains(text(), '상기 결제정보를 확인')]")
        confirm_button.click()
        print("구매 동의 체크 성공")
        time.sleep(random.uniform(1, 5))
        driver.save_screenshot(f'{screenshot_path}/m_TOSS3.png')
    except Exception as e:
        print("구매 동의 체크 실패", str(e))
        driver.save_screenshot(f'{screenshot_path}/m_error.png')
        sys.exit(1)  # 실패 시 스크립트 종료

    # 결제하기
    try:
        order_button = driver.find_element(By.CLASS_NAME, "btn_fixed_bottom")
        order_button.click()
        time.sleep(random.uniform(1, 5))
        order_2_button = driver.find_element(By.CSS_SELECTOR, ".tds-mobile-button.css-14a2ds8")
        order_2_button.click()
        print("결제하기 버튼 클릭 성공")
        time.sleep(10)
        driver.save_screenshot(f'{screenshot_path}/m_TOSS4.png')
    except Exception as e:
        print("결제하기 버튼 클릭 실패", str(e))
        driver.save_screenshot(f'{screenshot_path}/m_error.png')
        sys.exit(1)  # 실패 시 스크립트 종료


def buy_option_KCP():
    # 주문자 정보 설정
    try:
        time.sleep(random.uniform(1, 5))
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(random.uniform(1, 5))
        order_info_button = driver.find_element(By.XPATH, "//label[contains(text(), '주문자 정보와 동일')]")
        driver.execute_script("arguments[0].click();", order_info_button)
        #order_info_button.click()
        print("주문자 정보 설정 성공")
        time.sleep(random.uniform(1, 5))
        driver.save_screenshot(f'{screenshot_path}/m_KCP1.png')
    except Exception as e:
        print("주문자 정보 설정 실패", str(e))
        driver.save_screenshot(f'{screenshot_path}/m_error.png')
        sys.exit(1)  # 실패 시 스크립트 종료

    # 페이지 아래쪽으로 스크롤
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print("페이지 스크롤 성공")
        time.sleep(random.uniform(1, 5))
    except Exception as e:
        print("페이지 스크롤 실패", str(e))
        driver.save_screenshot(f'{screenshot_path}/m_error.png')
        sys.exit(1)  # 실패 시 스크립트 종료

    # 결제 방식 선택
    try:
        select_order_button = driver.find_element(By.ID, "pay_1")
        select_order_button.click()
        print("KCP 카드 결제 선택 성공")
        time.sleep(random.uniform(1, 5))
        driver.save_screenshot(f'{screenshot_path}/m_KCP2.png')
    except Exception as e:
        print("KCP 카드 결제 선택 실패", str(e))
        driver.save_screenshot(f'{screenshot_path}/m_error.png')
        sys.exit(1)  # 실패 시 스크립트 종료

    # 구매 동의
    try:
        confirm_button = driver.find_element(By.XPATH, "//label[contains(text(), '상기 결제정보를 확인')]")
        confirm_button.click()
        print("구매 동의 체크 성공")
        time.sleep(random.uniform(1, 5))
        driver.save_screenshot(f'{screenshot_path}/m_KCP3.png')
    except Exception as e:
        print("구매 동의 체크 실패", str(e))
        driver.save_screenshot(f'{screenshot_path}/m_error.png')
        sys.exit(1)  # 실패 시 스크립트 종료

    # 결제하기
    try:
        # ROUNZ 결제 금액 확인
        rounz_price_element = driver.find_element(By.ID, 'totalPayPrice2')
        rounz_price_text = rounz_price_element.text

        # , 제거 및 숫자 변환
        rounz_price_number = int(rounz_price_text.replace(',', ''))
        print(rounz_price_number)

        #결제하기 클릭
        order_button = driver.find_element(By.CLASS_NAME, "btn_fixed_bottom")
        order_button.click()
        print("결제하기 버튼 클릭 성공")
        time.sleep(random.uniform(1, 5))

        # KCP 최종 결제 금액 테스트로 변환
        KCP_price_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'p.product-price')))
        KCP_price_text = KCP_price_element.text

        # '원' 글자 제거
        KCP_price_text = KCP_price_text.replace('원', '')
        KCP_price_number = int(KCP_price_text.replace(',', ''))
        print(KCP_price_number)

        if rounz_price_number == KCP_price_number:
            print("구매 가격 일치:", rounz_price_number, KCP_price_number)
            time.sleep(random.uniform(1, 5))
            driver.save_screenshot(f'{screenshot_path}/m_KCP4.png')
            # X버튼 클릭
            close_button = driver.find_element(By.ID, "top_close")
            close_button.click()
            print("X버튼 클릭 성공")
            time.sleep(random.uniform(1, 5))

        else:
            print("구매 가격 불일치:", rounz_price_number, KCP_price_number)
            driver.save_screenshot(f'{screenshot_path}/m_error.png')
            sys.exit(1)

    except Exception as e:
        print("결제하기 버튼 클릭 실패", str(e))
        driver.save_screenshot(f'{screenshot_path}/m_error.png')
        sys.exit(1)  # 실패 시 스크립트 종료

    # 페이지 새로고침
    driver.refresh()


def buy_option_NAVER():
    # 주문자 정보 설정
    try:
        time.sleep(random.uniform(1, 5))
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(random.uniform(1, 5))
        order_info_button = driver.find_element(By.XPATH, "//label[contains(text(), '주문자 정보와 동일')]")
        driver.execute_script("arguments[0].click();", order_info_button)
        #order_info_button.click()
        print("주문자 정보 설정 성공")
        time.sleep(random.uniform(1, 5))
        driver.save_screenshot(f'{screenshot_path}/m_NAVER1.png')
    except Exception as e:
        print("주문자 정보 설정 실패", str(e))
        driver.save_screenshot(f'{screenshot_path}/m_error.png')
        sys.exit(1)  # 실패 시 스크립트 종료

    # 페이지 아래쪽으로 스크롤
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print("페이지 스크롤 성공")
        time.sleep(random.uniform(1, 5))
    except Exception as e:
        print("페이지 스크롤 실패", str(e))
        driver.save_screenshot(f'{screenshot_path}/m_error.png')
        sys.exit(1)  # 실패 시 스크립트 종료

    # 결제 방식 선택
    try:
        select_order_button = driver.find_element(By.ID, "pay_24")
        select_order_button.click()
        print("Naver Pay 결제 선택 성공")
        time.sleep(random.uniform(1, 5))
        driver.save_screenshot(f'{screenshot_path}/m_NAVER2.png')
    except Exception as e:
        print("Naver Pay 결제 선택 실패", str(e))
        driver.save_screenshot(f'{screenshot_path}/m_error.png')
        sys.exit(1)  # 실패 시 스크립트 종료

    # 구매 동의
    try:
        confirm_button = driver.find_element(By.XPATH, "//label[contains(text(), '상기 결제정보를 확인')]")
        confirm_button.click()
        print("구매 동의 체크 성공")
        time.sleep(random.uniform(1, 5))
        driver.save_screenshot(f'{screenshot_path}/m_NAVER3.png')
    except Exception as e:
        print("구매 동의 체크 실패", str(e))
        driver.save_screenshot(f'{screenshot_path}/m_error.png')
        sys.exit(1)  # 실패 시 스크립트 종료

    # 결제하기
    try:
        order_button = driver.find_element(By.CLASS_NAME, "btn_fixed_bottom")
        order_button.click()
        print("결제하기 버튼 클릭 성공")
        time.sleep(random.uniform(1, 5))

        # 네이버 로그인 팝업 창으로 전환
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(random.uniform(1, 5))
        driver.save_screenshot(f'{screenshot_path}/m_NAVER4.png')

    except Exception as e:
        print("결제하기 버튼 클릭 실패", str(e))
        driver.save_screenshot(f'{screenshot_path}/m_error.png')
        sys.exit(1)  # 실패 시 스크립트 종료


def delete_screenshot():
    # 오래된 폴더 삭제
    delete_path = f'screenshot/'
    current_time = datetime.now()
    max_age_days = 1
    # 스크린샷 폴더가 존재하는지 확인
    if os.path.exists(delete_path):
        # 디렉토리 내의 모든 하위 폴더 순회
        for subdir in os.listdir(delete_path):
            subdir_path = os.path.join(delete_path, subdir)
            # 하위 폴더가 실제로 폴더인지 확인
            if os.path.isdir(subdir_path):
                # 폴더의 마지막 수정 시간 가져오기
                subdir_modified_time = datetime.fromtimestamp(os.path.getmtime(subdir_path))
                # 설정한 기간보다 오래된 폴더인지 확인
                if current_time - subdir_modified_time > timedelta(days=max_age_days):
                    try:
                        shutil.rmtree(subdir_path)  # 폴더 삭제
                        print(f"오래된 폴더 삭제: {subdir_path}")  # 로그 기록
                    except Exception as e:
                        print(f"오래된 폴더 삭제 실패 {subdir_path}: {e}")  # 에러 로깅


if __name__ == "__main__":
    pc_login() # 로그인
    pc_order() # 제품 선택 및 Rounz 결제 시도
    buy_option_KCP() # KCP 카드 결제 시도
    buy_option_TOSS() # 토스pay 결제 시도
    #buy_option_NAVER() # 네이버pay(카드) 결제 시도
    delete_screenshot() # 오래된 스크린샷 파일 삭제
    driver.quit() # 브라우저 종료
