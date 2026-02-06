import requests
import pandas as pd
import streamlit as st

# دانلود داده‌ها از GitHub
url = "https://raw.githubusercontent.com/Hipo/university-domains-list/master/world_universities_and_domains.json"
response = requests.get(url)
data = response.json()

# تبدیل به DataFrame
df = pd.DataFrame(data)

# ذخیره به فایل اکسل
excel_file = "universities_list.xlsx"
df.to_excel(excel_file, index=False)

# رابط گرافیکی با Streamlit
st.title("📚 لیست دانشگاه‌های دنیا")
st.markdown("منبع: [Hipo/university-domains-list](https://github.com/Hipo/university-domains-list)")

# فیلتر بر اساس کشور
countries = sorted(df['country'].unique())
selected_country = st.selectbox("یک کشور انتخاب کن:", ["همه کشورها"] + countries)

if selected_country != "همه کشورها":
    filtered_df = df[df['country'] == selected_country]
else:
    filtered_df = df

# جستجو
search = st.text_input("🔍 جستجو در نام دانشگاه:")

if search:
    filtered_df = filtered_df[filtered_df['name'].str.contains(search, case=False, na=False)]

# نمایش جدول
st.dataframe(filtered_df)

# لینک دانلود اکسل
with open(excel_file, "rb") as f:
    st.download_button("⬇️ دانلود فایل اکسل", f, file_name=excel_file)
