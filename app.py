import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="মাস্টারমাইন্ড খাতা", layout="wide")
st.title("📔 ডিজিটাল হিসাবের খাতা")

# গুগল শিটের সাথে কানেকশন
conn = st.connection("gsheets", type=GSheetsConnection)

# ১. ইনপুট সেকশন
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("নতুন হিসাব যোগ করুন")
    with st.form("entry_form", clear_on_submit=True):
        date = st.date_input("তারিখ")
        desc = st.text_input("বিবরণ")
        amount = st.number_input("পরিমাণ (টাকা)", min_value=0)
        category = st.selectbox("ধরন", ["আয়", "খরচ"])
        submit = st.form_submit_with_button("খাতায় তুলুন")

        if submit and desc:
            existing_data = conn.read(worksheet="Sheet1")
            new_data = pd.DataFrame([{
                "Date": str(date),
                "Description": desc,
                "Amount": amount,
                "Type": category
            }])
            updated_df = pd.concat([existing_data, new_data], ignore_index=True)
            conn.update(worksheet="Sheet1", data=updated_df)
            st.success("হিসাব সফলভাবে সেভ হয়েছে!")

# ২. ডিসপ্লে সেকশন
with col2:
    st.subheader("হিসাব তালিকা ও সারাংশ")
    try:
        df = conn.read(worksheet="Sheet1")
        if not df.empty:
            st.dataframe(df, use_container_width=True)
            income = df[df['Type'] == 'আয়']['Amount'].sum()
            expense = df[df['Type'] == 'খরচ']['Amount'].sum()
            
            c1, c2, c3 = st.columns(3)
            c1.metric("মোট আয়", f"{income} টাকা")
            c2.metric("মোট খরচ", f"{expense} টাকা")
            c3.metric("অবশিষ্ট", f"{income - expense} টাকা")
    except:
        st.info("খাতা এখন খালি। নতুন এন্ট্রি দিন।")
