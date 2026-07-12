import streamlit as st
import requests

st.set_page_config(page_title="クソリプジェネレーター", page_icon="💩")
st.title("💩 クソリプジェネレーター")

api_key = st.sidebar.text_input("Gemini APIキー", type="password")
mode = st.radio("モード", ("年上上司", "熱血マン"))
user_input = st.text_area("本音を入力")

if not st.button("生成する"):
    st.stop()

if not api_key or not user_input:
    st.error("APIキーと本音を入力してください")
    st.stop()

sys_p = "あなたはウザい昭和の上司です。精神論で説教して。" if mode == "年上上司" else "あなたはウザい熱血マンです。大チャンスと全肯定して。"
prompt = f"設定: {sys_p}\n入力: {user_input}"

with st.spinner("起きてるAIを探しています..."):
    list_url = "https://generativelanguage.googleapis.com/v1beta/models?key=" + api_key
    models_data = requests.get(list_url).json()

    if "error" in models_data:
        st.error(f"APIキーエラー: {models_data}")
        st.stop()

    reply_text = None
    used_model = ""

    # トラップを回避するため、返事があるまで全モデルを順番に試す
    for m in models_data.get("models", []):
        if "generateContent" in m.get("supportedGenerationMethods", []):
            m_name = m["name"]
            gen_url = f"https://generativelanguage.googleapis.com/v1beta/{m_name}:generateContent?key={api_key}"
            res = requests.post(gen_url, headers={'Content-Type': 'application/json'}, json={"contents": [{"parts": [{"text": prompt}]}]})
            
            if res.status_code == 200:
                reply_text = res.json()['candidates'][0]['content']['parts'][0]['text']
                used_model = m_name
                break # 成功したらループを抜ける

    if reply_text:
        st.success(f"成功！(動いたAI: {used_model})")
        st.info(reply_text)
    else:
        st.error("全AIに無視されました。Googleの機嫌が悪いようです。")
