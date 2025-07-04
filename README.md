# Daraz Electronics Accessories Scraper & Data Analysis

This repository contains Python scripts to **scrape product data** from Daraz Bangladesh’s Electronics Accessories category, **clean and analyze the data**, and **generate professional Excel reports** for e-commerce or data entry purposes.

---

## 🚀 Features

✅ Scrape product information:
- Product name
- Price
- Location
- Product page link

✅ Data cleaning and formatting:
- Remove duplicates
- Clean price text into numeric values
- Truncate long product names
- Export clean CSV and Excel files

✅ Data analysis:
- Price distribution graphs
- Stats on min, max, and average prices
- Count of products by location

✅ Excel output:
- Styled Excel file ready for professional use or portfolio

---

## 🛠 Technologies Used

- Python 3
- Selenium
- pandas
- matplotlib
- xlsxwriter
- Google Chrome & Chromedriver

---

## 💻 How to Run

### 1. Install dependencies

```bash
pip install selenium pandas matplotlib xlsxwriter


### 2. Run the scraping script

python scrape_daraz.py

### 3. Clean and analyze data

python clean_and_analyze.py

### 4. Export styled Excel report (optional)

python export_excel_styled.py

📊 Example Output
daraz_products.csv → Raw scraped data

daraz_products_cleaned.csv → Cleaned data

daraz_upload_ready.xlsx → Styled Excel ready for use

PNG plots of price distributions

👤 Author
Sankalpa Anka
Bachelor of Science in Computer Science & Engineering (BRAC University, Dhaka)



