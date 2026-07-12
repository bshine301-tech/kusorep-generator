import streamlit as st
import urllib.parse
import requests

st.set_page_config(page_title="クソリプジェネレーター", page_icon="💩")
st.title("💩 クソリプジェネレーター")

try:
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    st.error("設定エラー: APIキーがありません")
    st.stop()

mode = st.radio("モード", ("老害上司", "熱血マン"))
user_input = st.text_area("本音を入力")

if st.button("生成する") and user_input:
    # 役割定義
    role = "ウザい昭和の老害上司。精神論で説教。日本語のセリフのみ50文字以内。" if mode == "老害上司" else "ウザい熱血マン。全てを大チャンスと全肯定。日本語のセリフのみ50文字以内。"
    
    # 1段目：生成
    prompt = f"指示: {role}。\n部下の言葉: {user_input}\nセリフのみ出力せよ。"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    gen_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    res = requests.post(gen_url, json=payload).json()
    raw_text = res['candidates'][0]['content']['parts'][0]['text']
    
    # 2段目：自己監視（AIに検閲させる）
    # もしAIが英語を出したり解説を出していたら、この検閲工程で「修正」される
    verify_prompt = f"指示: 前の回答が『解説』や『英語』を含んでいないか検閲せよ。含んでいるなら修正し、セリフのみにせよ。\n回答: {raw_text}"
    verify_payload = {"contents": [{"parts": [{"text": verify_prompt}]}]}
    
    final_res = requests.post(gen_url, json=verify_payload).json()
    final_text = final_res['candidates'][0]['content']['parts'][0]['text']
    
    # 表示
    st.info(final_text)
    share_url = "https://twitter.com/intent/tweet?text=" + urllib.parse.quote(f"【クソリプ】\n{final_text}")
    st.markdown(f'<a href="{share_url}" target="_blank">𝕏 でシェアする</a>', unsafe_allow_html=True)
