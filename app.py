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

# お手本（例）を示すことで、AIに英語や解説を書く隙を与えない最強の命令
if mode == "年上上司":
    sys_p = "ウザい昭和の上司として、精神論で説教してください。"
    ex_in = "疲れた"
    ex_out = "なんだその弱音は！理屈じゃない、気合と根性で乗り切れ！"
else:
    sys_p = "ウザい熱血マンとして、大チャンスだと全肯定してください。"
    ex_in = "疲れた"
    ex_out = "素晴らしい！限界を超えて成長する特大のチャンスだね！"

prompt = f"""あなたは役者です。思考プロセスや英語での解説は【一切出力せず】、日本語のセリフのみを直接出力してください。

【設定】
{sys_p}

【例】
相手: {ex_in}
あなた: {ex_out}

【本番】
相手: {user_input}
あなた:"""

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
            res = requests.post(gen_url, headers={'Content-Type': 'application/json'}, json={"contents": [{"parts": [{"text": prompt}]}]})
            
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
