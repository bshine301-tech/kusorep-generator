import streamlit as st
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

# 1. 決め打ちをやめ、あなたのキーで使えるモデルを自動で取得する
list_url = "https://generativelanguage.googleapis.com/v1beta/models?key=" + api_key
models_data = requests.get(list_url).json()

if "error" in models_data:
    st.error(f"APIキーが無効です: {models_data}")
    st.stop()

use_model = ""
for m in models_data.get("models", []):
    if "generateContent" in m.get("supportedGenerationMethods", []):
        use_model = m["name"]
        break

if not use_model:
    st.error("このキーで使えるAIがありません")
    st.stop()

# 2. 見つけたモデルを使ってクソリプを生成する
sys_p = "あなたはウザい昭和の上司です。精神論で説教して。" if mode == "年上上司" else "あなたはウザい熱血マンです。大チャンスと全肯定して。"
prompt = f"設定: {sys_p}\n入力: {user_input}"
gen_url = f"https://generativelanguage.googleapis.com/v1beta/{use_model}:generateContent?key={api_key}"

res = requests.post(gen_url, headers={'Content-Type': 'application/json'}, json={"contents": [{"parts": [{"text": prompt}]}]})
res_data = res.json()

if res.status_code != 200:
    st.error(f"生成エラー: {res_data}")
    st.stop()

reply = res_data['candidates'][0]['content']['parts'][0]['text']
st.success(f"成功！(使用AI: {use_model})")
st.info(reply)
