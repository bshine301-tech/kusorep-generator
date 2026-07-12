import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="クソリプジェネレーター", page_icon="💩")
st.title("💩 クソリプジェネレーター")

api_key = st.sidebar.text_input("Gemini APIキー", type="password")
mode = st.radio("モード", ("年上上司", "熱血マン"))
user_input = st.text_area("本音を入力")

if st.button("生成する"):
    try:
        genai.configure(api_key=api_key)
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        model = genai.GenerativeModel(models[0])
        
        sys_p = "あなたはウザい昭和の上司です。精神論で説教して。" if mode == "年上上司" else "あなたはウザい熱血マンです。大チャンスと全肯定して。"
        prompt = f"設定: {sys_p}\n入力: {user_input}"
        
        response = model.generate_content(prompt)
        st.success("クソリプが届きました！")
        st.info(response.text)
    except Exception as e:
        st.error("エラー！APIキーが間違っているか未入力です。")
