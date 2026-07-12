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

mode = st.radio("モード", ("老害上司", "熱血マン"))
user_input = st.text_area("本音を入力")

if st.button("生成する") and user_input:
    role = "昭和の老害上司。説教。日本語のセリフのみ50文字以内。" if mode == "老害上司" else "熱血マン。大チャンスだと全肯定。日本語のセリフのみ50文字以内。"
    
    # API呼び出し用の共通関数
    def call_gemini(prompt):
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        try:
            res = requests.post(url, json=payload).json()
            # candidatesが存在するかチェック
            if "candidates" in res and len(res["candidates"]) > 0:
                return res["candidates"][0]["content"]["parts"][0]["text"]
            else:
                return None
        except:
            return None

    # 1. 生成
    raw_text = call_gemini(f"指示: {role}。部下の言葉: {user_input}。セリフのみ出力。")
    
    if raw_text:
        # 2. 検閲（ルール違反があれば修正させる）
        verify_prompt = f"前の回答が『セリフのみ』でない場合、修正せよ。解説や英語は禁止。回答: {raw_text}"
        final_text = call_gemini(verify_prompt) or raw_text
        
        # 表示
        st.info(final_text)
        share_url = "https://twitter.com/intent/tweet?text=" + urllib.parse.quote(f"【クソリプ】\n{final_text}")
        st.markdown(f'<a href="{share_url}" target="_blank">𝕏 でシェアする</a>', unsafe_allow_html=True)
    else:
        st.error("Googleの反応がありません。ボタンをもう一度押してください。")
