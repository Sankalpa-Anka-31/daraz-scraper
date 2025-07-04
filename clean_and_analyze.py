import pandas as pd
import matplotlib.pyplot as plt

# ✅ STEP 1 — LOAD YOUR SCRAPED CSV
df = pd.read_csv("daraz_products.csv", encoding="utf-8-sig")

# ========== CLEANING START ==========

# Remove duplicates (based on Product Name + Price)
df = df.drop_duplicates(subset=['Product Name', 'Price'])

# Fix price format: remove '৳' and commas, then convert to float
df['Price_Numeric'] = (
    df['Price']
    .str.replace("৳", "", regex=False)
    .str.replace(",", "")
    .astype(float)
)

# Optional: truncate overly long product names for upload purposes
df['Product Name Short'] = df['Product Name'].str.slice(0, 80)

# ✅ RENAME COLUMNS FOR PROFESSIONAL PORTFOLIO
df.rename(columns={
    'Product Name': 'Product_Name',
    'Product Name Short': 'Product_Name_Short',
    'Price': 'Price_BDT',
    'Price_Numeric': 'Price_Numeric',
    'Location': 'Location',
    'Link': 'Product_Link'
}, inplace=True)

# Save cleaned CSV
df.to_csv("daraz_products_cleaned.csv", index=False, encoding="utf-8-sig")

print("\n✅ Cleaned Data Preview:")
print(df[['Product_Name_Short', 'Price_Numeric', 'Location', 'Product_Link']].head())
print(f"\n✅ Total Cleaned Rows: {len(df)}")

# ========== ANALYSIS START ==========

print("\n📊 Price Summary:")
print(df['Price_Numeric'].describe())

# Most expensive product
top_product = df.sort_values(by='Price_Numeric', ascending=False).iloc[0]
print("\n💸 Most Expensive Product:")
print(top_product[['Product_Name', 'Price_Numeric', 'Location', 'Product_Link']])

# Cheapest product
cheap_product = df.sort_values(by='Price_Numeric', ascending=True).iloc[0]
print("\n🧾 Cheapest Product:")
print(cheap_product[['Product_Name', 'Price_Numeric', 'Location', 'Product_Link']])

# Count by location
print("\n📍 Products per Location:")
print(df['Location'].value_counts())

# Plot price distribution
plt.figure(figsize=(10, 5))
df['Price_Numeric'].hist(bins=30, color='skyblue', edgecolor='black')
plt.title("Price Distribution of Electronics Accessories on Daraz")
plt.xlabel("Price (BDT)")
plt.ylabel("Number of Products")
plt.grid(True)
plt.savefig("price_distribution.png")  # Save as image
plt.show()

# Save upload-ready CSV
df[['Product_Name_Short', 'Price_Numeric', 'Location', 'Product_Link']].to_csv(
    "daraz_upload_ready.csv", index=False, encoding="utf-8-sig"
)

print("\n✅ Upload-ready CSV saved as daraz_upload_ready.csv")
