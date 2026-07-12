import streamlit as st
import urllib.parse
import requests

st.set_page_config(page_title="クソリプジェネレーター", page_icon="💩")
st.title("💩 クソリプジェネレーター")

try:
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    st.error("APIキー設定エラー")
    st.stop()

mode = st.radio("モード", ("年上上司", "熱血マン"))
user_input = st.text_area("本音を入力")

if st.button("生成する"):
    if not user_input:
        st.warning("本音を入力してください")
    else:
        # キャラ設定を「システム側」に固定（systemInstructionで固定）
        role = "あなたはウザい昭和の上司。部下の言葉に対し、理不尽な精神論（気合、根性、魂）だけで説教するセリフのみを返せ。解説・分析・英語は絶対禁止。" if mode == "年上上司" else "あなたはウザい熱血マン。部下の言葉に対し、全肯定で暑苦しく励ますセリフのみを返せ。解説・分析・英語は絶対禁止。"
        
        payload = {
            "systemInstruction": {"parts": [{"text": role}]},
            "contents": [{"parts": [{"text": user_input}]}]
        }
        
        gen_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        res = requests.post(gen_url, headers={'Content-Type': 'application/json'}, json=payload).json()
        
        if "candidates" in res:
            reply = res['candidates'][0]['content']['parts'][0]['text']
            st.info(reply)
            share_url = "https://twitter.com/intent/tweet?text=" + urllib.parse.quote(reply)
            st.markdown(f'<a href="{share_url}" target="_blank">𝕏 でシェアする</a>', unsafe_allow_html=True)
        else:
            st.error(f"エラー発生: {res}")
