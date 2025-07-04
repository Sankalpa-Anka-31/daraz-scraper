import pandas as pd

# load cleaned data
df = pd.read_csv("daraz_products_cleaned.csv", encoding="utf-8-sig")

# export with styles
with pd.ExcelWriter("daraz_upload_ready.xlsx", engine="xlsxwriter") as writer:
    df.to_excel(writer, sheet_name='Products', index=False)

    workbook = writer.book
    worksheet = writer.sheets['Products']

    header_format = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'fg_color': '#D7E4BC',
        'border': 1
    })

    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num, value, header_format)

    worksheet.set_column('A:A', 40)
    worksheet.set_column('B:B', 15)
    worksheet.set_column('C:C', 20)
    worksheet.set_column('D:D', 80)
    worksheet.set_column('E:E', 20)   # Price_Numeric
    worksheet.set_column('F:F', 80)   # Product_Name_Short

    price_col_idx = df.columns.get_loc("Price_Numeric")
    worksheet.conditional_format(
        1, price_col_idx, len(df), price_col_idx,
        {
            'type': '3_color_scale',
            'min_color': "#63BE7B",
            'mid_color': "#FFEB84",
            'max_color': "#F8696B"
        }
    )
