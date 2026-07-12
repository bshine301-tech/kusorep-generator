import streamlit as st
import urllib.parse
import requests

st.set_page_config(page_title="クソリプジェネレーター", page_icon="💩")
st.title("💩 クソリプジェネレーター")

try:
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    st.error("Secrets設定エラー")
    st.stop()

mode = st.radio("モード", ("老害上司", "熱血マン"))
user_input = st.text_area("本音を入力")

if st.button("生成する") and user_input:
    role = "老害上司。説教。セリフのみ日本語50文字以内。" if mode == "老害上司" else "熱血マン。全肯定励まし。セリフのみ日本語50文字以内。"
    
    # 1. 使えるモデルを自動で探しに行く（ここで絶対エラーを回避する）
    models_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    models_resp = requests.get(models_url).json()
    model_name = "models/gemini-1.5-flash" # 基本値
    if "models" in models_resp:
        for m in models_resp["models"]:
            if "generateContent" in m.get("supportedGenerationMethods", []):
                model_name = m["name"]
                break

    # 2. 生成と修正を統合した関数
    def get_reply(prompt):
        url = f"https://generativelanguage.googleapis.com/v1beta/{model_name}:generateContent?key={api_key}"
        res = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}).json()
        if "candidates" in res:
            return res["candidates"][0]["content"]["parts"][0]["text"]
        return None

    # 3. 実行
    raw = get_reply(f"指示:{role}。部下の言葉:{user_input}。セリフのみ出力。")
    if raw:
        final = get_reply(f"以下を日本語セリフのみに修正せよ: {raw}") or raw
        st.info(final)
        st.markdown(f'[𝕏 でシェア](https://twitter.com/intent/tweet?text={urllib.parse.quote("【クソリプ】\n" + final)})')
    else:
        st.error("AIからの通信が拒否されました。APIキーの権限を確認してください。")
