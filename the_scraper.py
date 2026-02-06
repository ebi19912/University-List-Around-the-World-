from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time

# مسیر کروم‌درایور
CHROMEDRIVER_PATH = "./chromedriver.exe"  # ← اگر روی ویندوزی

# تنظیمات مرورگر
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")

# راه‌اندازی درایور
driver = webdriver.Chrome(service=Service(CHROMEDRIVER_PATH), options=options)
driver.get("https://www.timeshighereducation.com/world-university-rankings/latest/world-ranking#!/length/-1/sort_by/rank/sort_order/asc/cols/scores")

# صبر برای لود اولیه
time.sleep(10)

# لود کردن همه ردیف‌ها
while True:
    try:
        load_more = driver.find_element(By.CLASS_NAME, "show-more")
        driver.execute_script("arguments[0].click();", load_more)
        time.sleep(3)
    except:
        break

# صبر برای اطمینان
time.sleep(5)

# استخراج داده‌ها
rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")

data = []
for row in rows:
    cols = row.find_elements(By.TAG_NAME, "td")
    if len(cols) >= 6:
        rank = cols[0].text.strip()
        name = cols[1].text.strip()
        country = cols[2].text.strip()
        overall_score = cols[3].text.strip()
        teaching = cols[4].text.strip()
        research = cols[5].text.strip()
        citations = cols[6].text.strip() if len(cols) > 6 else ""
        industry_income = cols[7].text.strip() if len(cols) > 7 else ""
        international_outlook = cols[8].text.strip() if len(cols) > 8 else ""
        
        data.append({
            "Rank": rank,
            "University": name,
            "Country": country,
            "Overall Score": overall_score,
            "Teaching": teaching,
            "Research": research,
            "Citations": citations,
            "Industry Income": industry_income,
            "International Outlook": international_outlook
        })

driver.quit()

# ذخیره در Excel
df = pd.DataFrame(data)
df.to_excel("THE_University_Rankings.xlsx", index=False)

print("✅ داده‌ها ذخیره شدند در فایل: THE_University_Rankings.xlsx")
