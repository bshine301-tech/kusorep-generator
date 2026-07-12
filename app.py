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

if not st.button("生成する"):
    st.stop()

# 思考プロセスを物理的に排除する、極限までシンプルな指示に変更
sys_p = "あなたはウザい昭和の上司【老害】です。部下の言葉に対して、理不尽な精神論の説教を【日本語のみ】で、セリフ【のみ】の50文字以内で返してください。" if mode == "老害上司" else "あなたはウザい熱血マンです。部下の言葉に対して、ピンチを大チャンスだと全肯定する暑苦しいセリフ【のみ】を50文字以内で日本語で返してください。"

# payloadを極限までシンプルにする
payload = {
    "contents": [{"parts": [{"text": f"ルール: 思考プロセスは禁止。解説禁止。英語禁止。以下の指示に従い、セリフのみ出力せよ。\n\n指示: {sys_p}\n部下の言葉: {user_input}\n\nあなたの返答:"}]}]
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
        share_url = "https://twitter.com/intent/tweet?text=" + urllib.parse.quote(f"【クソリプ】\n{reply_text}")
        st.markdown(f'<a href="{share_url}" target="_blank">𝕏 でシェアする</a>', unsafe_allow_html=True)
    else:
        st.error("エラーが発生しました。")
