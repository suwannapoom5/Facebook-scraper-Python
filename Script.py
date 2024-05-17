import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

def scrape_facebook_posts(page_url, desired_post_count):
    chrome_driver_path = "C:/Users/suwan/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe"
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service)

    try:
        driver.get(page_url)

        SCROLL_PAUSE_TIME = 5
        last_height = driver.execute_script("return document.body.scrollHeight")

        posts_count = 0 

        while posts_count < desired_post_count:  
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

            # เพิ่มรหัสที่คลิกปุ่ม "ดูเพิ่มเติม" ก่อนที่จะดึงข้อมูลโพสต์
            try:
                element_to_click = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="x92rtbv x10l6tqk x1tk7jg1 x1vjfegm"]')))
                element_to_click.click()
            except NoSuchElementException:
                print("Element 'ดูเพิ่มเติม' ไม่พบในโพสต์นี้")
                continue

            new_posts = driver.find_elements(By.XPATH, "//div[@role='article']")
            for post in new_posts:
                try:
                    message_element = post.find_element(By.XPATH, ".//div[@data-ad-comet-preview='message' or @data-ad-preview='message']")
                    text = message_element.text.strip() if message_element else None

                    image_elements = post.find_elements(By.XPATH, ".//img[@src]")
                    image_urls = [image_element.get_attribute("src") for image_element in image_elements]

                    print("===============================================")
                    print("Message:", text)
                    print("Images:", image_urls)
                    print("===============================================")

                    posts_count += 1  

                    if posts_count >= desired_post_count:
                        break
                except NoSuchElementException:
                    print("Element 'message' หรือ 'img[src]' ไม่พบ")
                    continue
                except Exception as e:
                    print("An error occurred while processing post:", e)

            if posts_count >= desired_post_count:
                break  

    except Exception as e:
        print("An error occurred:", e)

    finally:
        driver.quit()

page_url = "https://www.facebook.com/Wing23.rtaf"
desired_post_count = 5
scrape_facebook_posts(page_url, desired_post_count)
