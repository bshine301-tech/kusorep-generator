import streamlit as st
import urllib.parse
import requests

st.set_page_config(page_title="クソリプジェネレーター", page_icon="💩")
st.title("💩 クソリプジェネレーター")

try:
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    st.error("APIキーが裏側に設定されていません。SettingsのSecretsを確認してください。")
    st.stop()

mode = st.radio("モード", ("年上上司", "熱血マン"))
user_input = st.text_area("本音を入力")

if not st.button("生成する"):
    st.stop()

if not user_input:
    st.warning("本音を入力してください")
    st.stop()

# モードごとの設定と会話例
if mode == "年上上司":
    sys_p = "あなたはウザい昭和の上司です。部下の言葉に対して、理不尽な精神論（気合、根性など）で説教するセリフのみを日本語で返してください。思考プロセスや解説は絶対に出力しないでください。"
    ex_in = "疲れた"
    ex_out = "なんだその弱音は！理屈じゃない、気合と根性で乗り切れ！"
else:
    sys_p = "あなたはウザい熱血マンです。部下の言葉に対して、ピンチを大チャンスだと全肯定する暑苦しいセリフのみを日本語で返してください。思考プロセスや解説は絶対に出力しないでください。"
    ex_in = "疲れた"
    ex_out = "素晴らしい！限界を超えて成長する特大のチャンスだね！"

# 箱を明確に分けて、AIに「分析」ではなく「会話」だと思い込ませる
payload = {
    "systemInstruction": {
        "parts": [{"text": sys_p}]
    },
    "contents": [
        {"role": "user", "parts": [{"text": ex_in}]},
        {"role": "model", "parts": [{"text": ex_out}]},
        {"role": "user", "parts": [{"text": user_input}]}
    ]
}

with st.spinner("AIがクソリプを練っています..."):
    list_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    models_data = requests.get(list_url).json()

    if "error" in models_data:
        st.error("APIキーが無効です。裏側の設定を確認してください。")
        st.stop()

    reply_text = None

    for m in models_data.get("models", []):
        if "generateContent" in m.get("supportedGenerationMethods", []):
            gen_url = f"https://generativelanguage.googleapis.com/v1beta/{m['name']}:generateContent?key={api_key}"
            res = requests.post(gen_url, headers={'Content-Type': 'application/json'}, json=payload)
            
            if res.status_code == 200:
                reply_text = res.json()['candidates'][0]['content']['parts'][0]['text']
                break

    if reply_text:
        st.success("クソリプが届きました！")
        st.info(reply_text)
        
        share_text = f"【私の本音】\n{user_input}\n\n【クソリプ】\n{reply_text}\n\n#クソリプジェネ"
        share_url = "https://twitter.com/intent/tweet?text=" + urllib.parse.quote(share_text)
        st.markdown(f'<a href="{share_url}" target="_blank" style="background-color:black;color:white;padding:10px;border-radius:10px;text-decoration:none;">𝕏 でシェアする</a>', unsafe_allow_html=True)
    else:
        st.error("AIの機嫌が悪いようです。時間をおいて試してください。")
