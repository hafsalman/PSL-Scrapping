from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import json
import time
import os

CATEGORY_URL = "https://psl.org.pk/dictionary/76-automobile"

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

print("Saving JSON to:", os.getcwd())

driver.get(CATEGORY_URL)
time.sleep(5)

results = []

cards = driver.find_elements(
    By.XPATH, "//a[contains(@href, '/dictionary/76-automobile/')]"
)

card_links = list(set(c.get_attribute("href") for c in cards))
print(f"Found {len(card_links)} cards")

wait = WebDriverWait(driver, 15)

for i, link in enumerate(card_links, start=1):
    print(f"[{i}/{len(card_links)}] Visiting:", link)
    driver.get(link)

    try:
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "video")))

        word = driver.find_element(
            By.XPATH, "//h3[contains(@class,'font-poppins')]"
        ).text.strip()

        video = driver.find_element(By.TAG_NAME, "video")
        source = video.find_element(By.TAG_NAME, "source")
        video_url = source.get_attribute("src")

        results.append({
            "word": word,
            "videoUrl": video_url
        })

        print("Saved:", word)

    except Exception as e:
        print("Skipped:", link, "|", e)

    driver.back()
    time.sleep(2)

with open("education.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

driver.quit()

print("DONE!")
print("Total records saved:", len(results))
print("File: name.json")