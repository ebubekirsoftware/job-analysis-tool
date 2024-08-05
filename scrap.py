import time
import re
import random
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


class Scraper:
    def __init__(self, driver_path):
        self.driver_path = driver_path
        self.driver = self._initialize_driver()

    def _initialize_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
        service = Service(self.driver_path)
        return webdriver.Chrome(service=service, options=chrome_options)

    def random_sleep(self, min_seconds=1, max_seconds=5):
        time.sleep(random.uniform(min_seconds, max_seconds))

    def scroll_to_top(self):
        self.driver.execute_script("window.scrollTo(0, 0);")

    def scroll_to_bottom(self):
        time.sleep(2)
        prev_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == prev_height:
                break
            prev_height = new_height

    def open_linkedin_jobs_page(self):
        self.driver.get("https://tr.linkedin.com/")
        self.random_sleep()

    def search_jobs(self, title, country):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "İş İlanları"))
        ).click()
        self.random_sleep()

        search_job = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//input[@aria-label="İş unvanlarını veya şirketleri arayın"]'))
        )
        search_job.send_keys(title)
        print("Title Seçildi.")
        self.random_sleep()

        search_location = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'job-search-bar-location'))
        )
        search_location.clear()
        search_location.send_keys(country)
        self.random_sleep(3, 6)
        search_location.send_keys(Keys.ENTER)
        print("Ülke Seçildi.")
        print("Bekleyin..")
        self.random_sleep()

    def apply_filters(self):
        experience_level_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(@aria-label, "Deneyim düzeyi filtresi")]'))
        )
        experience_level_button.click()
        print("Deneyim düzeyi filtresi seçiliyor.")
        self.random_sleep()

        entry_level_option = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//label[contains(@for, "f_E-1")]'))
        )
        entry_level_option.click()
        self.random_sleep()

        mid_senior_level_option = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//label[contains(@for, "f_E-3")]'))
        )
        mid_senior_level_option.click()
        self.random_sleep()

        done_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//button[@class="filter__submit-button" and @type="submit"]'))
        )
        self.driver.execute_script("arguments[0].click();", done_button)
        print("Deneyim düzeyi filtresi seçildi.")
        print("Bekleyin..")
        self.random_sleep(5, 10)

        any_time_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(@aria-label, "Yayınlandığı tarih filtresi. Herhangi bir zaman")]'))
        )
        any_time_button.click()
        print("Tarih filtresi ayarlanıyor.")
        print("Bekleyin..")
        self.random_sleep()

        past_week_option = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//label[contains(@for, "f_TPR-0")]'))
        )
        past_week_option.click()
        self.random_sleep()

        number_element = self.driver.find_element(By.XPATH, '//label[@for="f_TPR-0"]')
        number_text = number_element.text
        match = re.search(r'\(([\d.]+)\)', number_text)
        number = int(match.group(1).replace('.', ''))

        done_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//button[@class="filter__submit-button" and @type="submit"]'))
        )
        self.driver.execute_script("arguments[0].click();", done_button)
        print("Tarih filtresi ayarlandı.")
        print("Bekleyin..")
        self.random_sleep()


    def get_job_listings(self, title, country, number_of_jobs):
        self.open_linkedin_jobs_page()
        self.search_jobs(title, country)
        self.apply_filters()

        job_listings_data = []
        spam_companies = ["Turing", "Crossover"]
        unique_job_links = set()

        while len(job_listings_data) < number_of_jobs:
            self.scroll_to_top()
            self.scroll_to_bottom()
            print("İlanlar aranıyor..")
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, '//button[contains(@aria-label, "Daha fazla iş ilanı göster")]')
                    )
                ).click()
                self.random_sleep()
                self.scroll_to_bottom()

                job_listings = self.driver.find_elements(By.XPATH, '//*[@id="main-content"]/section[2]/ul/li')
                for listing in job_listings[len(job_listings_data):]:
                    company_name = listing.find_element(By.CLASS_NAME, "base-search-card__subtitle").text
                    job_title = (listing.find_element(By.CLASS_NAME, 'sr-only').text).upper()
                    address = listing.find_element(By.CLASS_NAME, 'base-search-card__metadata').text
                    job_link = listing.find_element(By.CLASS_NAME, 'base-card__full-link').get_attribute('href')

                    if job_link not in unique_job_links and company_name not in spam_companies:
                        job_listings_data.append({
                            "Company Name": company_name,
                            "Job Title": job_title,
                            "Address": address,
                            "Job Link": job_link
                        })
                        unique_job_links.add(job_link)
            except:
                break

        print(f"{len(job_listings_data)} adet ilgili ilan bulundu ve kaydedildi. ")
        self.driver.quit()
        return pd.DataFrame(job_listings_data[:number_of_jobs])

    def get_job_descriptions(self, jobs_df):
        self.driver = self._initialize_driver()

        description_list = []
        for index, link in enumerate(jobs_df['Job Link']):
            try:
                self.driver.get(link)
                self.random_sleep(3, 8)

                description_element = self.driver.find_element(By.CLASS_NAME, 'show-more-less-html__markup')
                text_content = description_element.get_attribute('innerHTML')
                print(f"Description kaydedildi.--{index + 1}")
            except Exception as e:
                text_content = None
                print(f"Error occurred for link {link} at index {index}: {e}")

            description_list.append(text_content)
            self.random_sleep()

        self.driver.quit()
        return description_list

    def clean_html(self, html_list):
        clean_text_list = []
        for html in html_list:
            if html:
                soup = BeautifulSoup(html, 'html.parser')
                text_content = soup.get_text(separator='\n', strip=True)
            else:
                text_content = ''
            clean_text_list.append(text_content)
        return clean_text_list

def main():
    title = (input("Analiz etmek istediğiniz title nedir?")).upper()
    country = (input("Hangi ülkedeki ilanları analiz etmek istiyorsunuz?")).upper()
    number_of_jobs = int(input("Kaç tane iş ilanını baz alalım? (Sayı Giriniz!)"))
    driver_path = "chromedriver.exe"

    scraper = Scraper(driver_path)
    jobs_df = scraper.get_job_listings(title, country, number_of_jobs)
    descriptions = scraper.get_job_descriptions(jobs_df)
    clean_descriptions = scraper.clean_html(descriptions)
    jobs_df['Job Description'] = clean_descriptions
    jobs_df.to_csv('jobs.csv', index=False)


if __name__ == "__main__":
    main()
