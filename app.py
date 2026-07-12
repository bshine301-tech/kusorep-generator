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

if not st.button("生成する"):
    st.stop()

# 命令文をさらに極限まで厳しく「セリフのみ」に固定
if mode == "年上上司":
    sys_p = "あなたはウザい昭和の上司です。部下の言葉に対して、理不尽な精神論の説教を【日本語のセリフのみ】で返せ。思考プロセス、解説、英語は一切禁止。"
else:
    sys_p = "あなたはウザい熱血マンです。部下の言葉に対して、ピンチを大チャンスだと全肯定する熱いセリフを【日本語のセリフのみ】で返せ。思考プロセス、解説、英語は一切禁止。"

payload = {
    "contents": [{"parts": [{"text": f"ルール: セリフのみ出力せよ。解説禁止。英語禁止。指示: {sys_p} 相手の言葉: {user_input} 返答:"}]}]
}

with st.spinner("練っています..."):
    list_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    models_data = requests.get(list_url).json()
    
    reply_text = None
    for m in models_data.get("models", []):
        if "generateContent" in m.get("supportedGenerationMethods", []):
            gen_url = f"https://generativelanguage.googleapis.com/v1beta/{m['name']}:generateContent?key={api_key}"
            res = requests.post(gen_url, headers={'Content-Type': 'application/json'}, json=payload)
            if res.status_code == 200:
                reply_text = res.json()['candidates'][0]['content']['parts'][0]['text']
                break

    if reply_text:
        st.info(reply_text)
        share_text = f"【クソリプ】\n{reply_text}"
        share_url = "https://twitter.com/intent/tweet?text=" + urllib.parse.quote(share_text)
        st.markdown(f'<a href="{share_url}" target="_blank">𝕏 でシェアする</a>', unsafe_allow_html=True)
    else:
        st.error("エラーです。")
