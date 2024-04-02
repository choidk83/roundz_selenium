import os

os.system('pip install --upgrade selenium')

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time, sys, shutil
from datetime import datetime, timedelta

chrome_options = Options()
#chrome_options.add_argument("--headless")  # 헤드리스 모드 활성화
chrome_options.add_argument("--no-sandbox")  # 샌드박스 모드 비활성화
chrome_options.add_argument("--disable-dev-shm-usage")  # /dev/shm 사용 안함
chrome_options.add_argument("--window-size=1920,1080")  # 해상도 설정

print(webdriver.__version__)

url = "https://rounz.com/login.php"
wish_url = "https://rounz.com/my_wish_list.php"
create_date = datetime.now().strftime("%Y%m%d_%H%M%S")
screenshot_path = f'rounz_selenium/screenshot/{create_date}'
driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(10)
driver.maximize_window()
driver.get(url)
time.sleep(3)
delete_path = f'rounz_selenium/screenshot/'
current_time = datetime.now()
max_age_days = 1

# 웹사이트 타이틀 출력
print(driver.title) 

# 스크린샷 폴더 생성
if not os.path.exists(screenshot_path):
    os.makedirs(screenshot_path)

# ID 입력
try:
    username_input = driver.find_element(By.CSS_SELECTOR, "input[name='member_id']")
    username_input.send_keys("lecarto")
    print("ID 입력 성공")
    time.sleep(5)
except Exception as e:
    print("ID 입력 실패", str(e))
    sys.exit(1)  # 실패 시 스크립트 종료

# PW 입력
try:
    password_input = driver.find_element(By.CSS_SELECTOR, "input[name='pwd']")
    password_input.send_keys("asm4admin!")
    print("PW 입력 성공")
    time.sleep(5)
except Exception as e:
    print("PW 입력 실패", str(e))
    sys.exit(1)  # 실패 시 스크립트 종료

# LOGIN 버튼 클릭
try:
    login_button = driver.find_element(By.ID, "btnRounzLogin")
    login_button.click()
    print("로그인 성공")
    time.sleep(30)
    driver.save_screenshot(f'{screenshot_path}/page_screenshot1.png')
except Exception as e:
    print("로그인 실패", str(e))
    sys.exit(1)  # 실패 시 스크립트 종료

# 찜 목록 전환
try:
    driver.get(wish_url)
    print("찜 목록 호출 성공")
    time.sleep(5)
    driver.save_screenshot(f'{screenshot_path}/page_screenshot2.png')
except Exception as e:
    print("찜 목록 호출 실패", str(e))
    sys.exit(1)  # 실패 시 스크립트 종료

# 찜 물품 선택
try:
    my_wish_list_button = driver.find_element(By.ID, "wish_thumbnails")
    my_wish_list_button.click()
    print("찜 물품 선택 성공")
    time.sleep(5)
    driver.save_screenshot(f'{screenshot_path}/page_screenshot3.png')
except Exception as e:
    print("찜 물품 선택 실패", str(e))
    sys.exit(1)  # 실패 시 스크립트 종료

# 물품 구매 버튼 1차
try:
    order_first_button = driver.find_element(By.CLASS_NAME, "order")
    order_first_button.click()
    print("구매하기 1차 성공")
    time.sleep(5)
    driver.save_screenshot(f'{screenshot_path}/page_screenshot4.png')
except Exception as e:
    print("구매하기 1차 실패", str(e))
    sys.exit(1)  # 실패 시 스크립트 종료

# 물품 구매 버튼 2차
try:
    order_second_button = driver.find_element(By.CLASS_NAME, "order")
    order_second_button.click()
    print("구매하기 2차 성공")
    time.sleep(5)
    driver.save_screenshot(f'{screenshot_path}/page_screenshot5.png')
except Exception as e:
    print("구매하기 2차 실패", str(e))
    sys.exit(1)  # 실패 시 스크립트 종료

# 물품 구매 버튼 3차
try:
    order_third_button = driver.find_element(By.XPATH, "//a[contains(text(), '구매하기(')]")
    order_third_button.click()
    print("구매하기 3차 성공")
    time.sleep(5)
    driver.save_screenshot(f'{screenshot_path}/page_screenshot6.png')
except Exception as e:
    print("구매하기 3차 실패", str(e))
    sys.exit(1)  # 실패 시 스크립트 종료

# 주문자 정보 설정
try:
    order_info_button = driver.find_element(By.XPATH, "//label[contains(text(), '주문자 정보와 동일')]")
    order_info_button.click()
    print("주문자 정보 설정 성공")
    time.sleep(5)
    driver.save_screenshot(f'{screenshot_path}/page_screenshot7.png')
except Exception as e:
    print("주문자 정보 설정 실패", str(e))
    sys.exit(1)  # 실패 시 스크립트 종료

# 페이지 아래쪽으로 스크롤
try:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    print("페이지 스크롤 성공")
    time.sleep(5)
except Exception as e:
    print("페이지 스크롤 실패", str(e))
    sys.exit(1)  # 실패 시 스크립트 종료

# 결제 방식 선택
try:
    select_order_button = driver.find_element(By.ID, "pay_1")
    select_order_button.click()
    print("결제 방식 선택 성공")
    time.sleep(5)
    driver.save_screenshot(f'{screenshot_path}/page_screenshot8.png')
except Exception as e:
    print("결제 방식 선택 실패", str(e))
    sys.exit(1)  # 실패 시 스크립트 종료

# 구매 동의
try:
    confirm_button = driver.find_element(By.XPATH, "//label[contains(text(), '상기 결제정보를 확인')]")
    confirm_button.click()
    print("구매 동의 체크 성공")
    time.sleep(5)
    driver.save_screenshot(f'{screenshot_path}/page_screenshot9.png')
except Exception as e:
    print("구매 동의 체크 실패", str(e))
    sys.exit(1)  # 실패 시 스크립트 종료

# 결제하기
try:
    order_button = driver.find_element(By.CLASS_NAME, "btn_fixed_bottom")
    order_button.click()
    print("결제하기 버튼 클릭 성공")
    time.sleep(5)
    driver.save_screenshot(f'{screenshot_path}/page_screenshot10.png')
except Exception as e:
    print("결제하기 버튼 클릭 실패", str(e))
    sys.exit(1)  # 실패 시 스크립트 종료

# 오래된 폴더 삭제
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
                    sys.exit(1)  # 실패 시 스크립트 종료

# 브라우저 종료
driver.quit()