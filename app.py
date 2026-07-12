import streamlit as st
import google.generativeai as genai

st.title("APIキー 最終テスト")
api_key = st.text_input("AQから始まるAPIキーを貼り付け", type="password")

if st.button("通信テスト"):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("テスト")
        st.success(f"大成功！AIからの返事：{response.text}")
    except Exception as e:
        st.error(f"本当のエラー原因はこちらです：{e}")
