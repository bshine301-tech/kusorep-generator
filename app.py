import streamlit as st
import urllib.parse
import requests

st.set_page_config(page_title="クソリプジェネレーター", page_icon="💩")
st.title("💩 クソリプジェネレーター")

try:
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    st.error("API設定エラー")
    st.stop()

mode = st.radio("モード", ("年上上司", "熱血マン"))
user_input = st.text_area("本音を入力")

if st.button("生成する"):
    if not user_input:
        st.warning("本音を入力してください")
    else:
        # キャラ設定を「システム側」に固定し、ユーザー入力を完全に分離する
        role = "あなたはウザい昭和の上司です。部下の言葉に対して、理不尽な精神論（気合、根性、魂）だけで説教するセリフのみを返してください。解説や英語は禁止。" if mode == "年上上司" else "あなたはウザい熱血マンです。部下の言葉に対して、ピンチを大チャンスだと全肯定する熱いセリフのみを返してください。解説や英語は禁止。"
        
        payload = {
            "system_instruction": {"parts": [{"text": role}]},
            "contents": [{"parts": [{"text": f"入力:{user_input}\nセリフ:"}]}]
        }
        
        # APIバージョンを明示的に指定して実行
        gen_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        res = requests.post(gen_url, headers={'Content-Type': 'application/json'}, json=payload).json()
        
        try:
            reply = res['candidates'][0]['content']['parts'][0]['text']
            st.info(reply)
            share_url = "https://twitter.com/intent/tweet?text=" + urllib.parse.quote(reply)
            st.markdown(f'<a href="{share_url}" target="_blank">𝕏 でシェアする</a>', unsafe_allow_html=True)
        except:
            st.error("生成失敗：設定を見直してください")
