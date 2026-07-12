import streamlit as st
import urllib.parse
import requests

st.set_page_config(page_title="クソリプジェネレーター", page_icon="💩")
st.title("💩 クソリプジェネレーター")

api_key = st.sidebar.text_input("Gemini APIキー", type="password")
mode = st.radio("モード", ("年上上司", "熱血マン"))
user_input = st.text_area("本音を入力")

if not st.button("生成する"):
    st.stop()

if not api_key:
    st.error("APIキーを入力してください")
    st.stop()

if not user_input:
    st.warning("本音を入力してください")
    st.stop()

sys_prompt = "あなたはウザい昭和の上司です。精神論で説教して。"
if mode == "熱血マン":
    sys_prompt = "あなたはウザい熱血マンです。大チャンスと全肯定して。"

prompt = f"設定: {sys_prompt}\n入力: {user_input}"
url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=" + api_key
data = {"contents": [{"parts": [{"text": prompt}]}]}

res = requests.post(url, headers={'Content-Type': 'application/json'}, json=data)
res_data = res.json()

if res.status_code != 200:
    st.error(f"エラー発生: {res_data}")
    st.stop()

kuso_reply = res_data['candidates'][0]['content']['parts'][0]['text']
st.success("クソリプが届きました！")
st.info(kuso_reply)

share_text = f"【私の本音】\n{user_input}\n\n【クソリプ】\n{kuso_reply}\n\n#クソリプジェネ"
share_url = "https://twitter.com/intent/tweet?text=" + urllib.parse.quote(share_text)
st.markdown(f'<a href="{share_url}" target="_blank" style="background-color:black;color:white;padding:10px;border-radius:10px;text-decoration:none;">𝕏 でシェアする</a>', unsafe_allow_html=True)
