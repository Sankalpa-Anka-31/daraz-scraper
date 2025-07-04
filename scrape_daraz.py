from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

# Path to your chromedriver.exe
service = Service("C:/Users/user/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe")

options = Options()
# options.add_argument("--headless")  # Uncomment if you want to run in background without opening the browser
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(service=service, options=options)

products = []

for page_num in range(1, 11):
    url = f"https://www.daraz.com.bd/catalog/?q=electronics+accessories&page={page_num}"
    print(f"Scraping page {page_num}...")
    driver.get(url)

    # Scroll several times to trigger dynamic loading
    for i in range(5):
        driver.execute_script("window.scrollBy(0, 1000);")
        time.sleep(1)

    time.sleep(8)   # slightly longer wait

    product_cards = driver.find_elements(By.CSS_SELECTOR, 'div.buTCk')
    for card in product_cards:
        try:
            title = card.find_element(By.CSS_SELECTOR, 'div.RfADt a').text.strip()
        except:
            title = ''
        try:
            price = card.find_element(By.CSS_SELECTOR, 'div.aBrP0 span.ooOxS').text.strip()
        except:
            price = ''
        try:
            location = card.find_element(By.CSS_SELECTOR, 'div._6uN7R span.oa6ri').text.strip()
        except:
            location = ''
        try:
            raw_link = card.find_element(By.CSS_SELECTOR, 'div.RfADt a').get_attribute("href")
            if raw_link and raw_link.startswith("//"):
                link = "https:" + raw_link
            else:
                link = raw_link if raw_link else ''
        except:
            link = ''

        # Save only rows where critical fields exist
        if title and price and link:
            products.append({
                "Product Name": title,
                "Price": price,
                "Location": location,
                "Link": link
            })
            # print each record for verification
            print(f"→ {title} | {price} | {location} | {link}")

driver.quit()

# Create DataFrame and save to CSV
df = pd.DataFrame(products)
df.to_csv("daraz_products.csv", index=False, encoding="utf-8-sig")

print(f"Scraping complete. Total rows scraped: {len(df)}")
print(df.head())




# ========== CLEANING START ==========
# Remove duplicates (based on Product Name + Price)
df = df.drop_duplicates(subset=['Product Name', 'Price'])

# Fix price format: remove '৳' and commas, then convert to float
df['Price_Numeric'] = df['Price'].str.replace("৳", "", regex=False).str.replace(",", "").astype(float)

# Optional: truncate overly long product names for upload purposes
df['Product Name Short'] = df['Product Name'].str.slice(0, 80)

# Save cleaned version
df.to_csv("daraz_products_cleaned.csv", index=False, encoding="utf-8-sig")

print("\n✅ Cleaned Data Preview:")
print(df[['Product Name Short', 'Price_Numeric', 'Location', 'Link']].head())
print(f"\n✅ Total Cleaned Rows: {len(df)}")


# ========== ANALYSIS START ==========

print("\n📊 Price Summary:")
print(df['Price_Numeric'].describe())

# Most expensive product
top_product = df.sort_values(by='Price_Numeric', ascending=False).iloc[0]
print("\n💸 Most Expensive Product:")
print(top_product[['Product Name', 'Price_Numeric', 'Location', 'Link']])

# Cheapest product
cheap_product = df.sort_values(by='Price_Numeric', ascending=True).iloc[0]
print("\n🧾 Cheapest Product:")
print(cheap_product[['Product Name', 'Price_Numeric', 'Location', 'Link']])

# Count by location
print("\n📍 Products per Location:")
print(df['Location'].value_counts())

# Plot price distribution (if you want to see graph)
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 5))
df['Price_Numeric'].hist(bins=30, color='skyblue', edgecolor='black')
plt.title("Price Distribution of Electronics Accessories on Daraz")
plt.xlabel("Price (BDT)")
plt.ylabel("Number of Products")
plt.grid(True)
plt.savefig("price_distribution.png")  # Save as image
plt.show()


df[['Product Name Short', 'Price_Numeric', 'Location', 'Link']].to_csv("daraz_upload_ready.csv", index=False, encoding="utf-8-sig")
