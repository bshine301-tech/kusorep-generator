import streamlit as st
import urllib.parse
import requests

st.set_page_config(page_title="クソリプジェネレーター", page_icon="💩")
st.title("💩 クソリプジェネレーター")

# 秘密の金庫からAPIキーを自動で読み込む
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

# AIへの命令を「絶対になりきる」ように超強化
sys_p = "あなたはウザい昭和の上司です。精神論で説教してください。" if mode == "年上上司" else "あなたはウザい熱血マンです。大チャンスだと全肯定してください。"
prompt = f"【厳守】\n以下の設定に完全になりきって、返信のセリフ「のみ」を日本語で出力してください。設定の分析や英語での解説は一切不要です。\n\n【設定】\n{sys_p}\n\n【相手の本音】\n{user_input}\n\n【あなたのクソリプ】:"

with st.spinner("AIがクソリプを練っています..."):
    list_url = "https://generativelanguage.googleapis.com/v1beta/models?key=" + api_key
    models_data = requests.get(list_url).json()

    if "error" in models_data:
        st.error("APIキーが無効です。裏側の設定を確認してください。")
        st.stop()

    reply_text = None

    # 動くAIを探して生成
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
        
        # Xシェアボタン
        share_text = f"【私の本音】\n{user_input}\n\n【クソリプ】\n{reply_text}\n\n#クソリプジェネ"
        share_url = "https://twitter.com/intent/tweet?text=" + urllib.parse.quote(share_text)
        st.markdown(f'<a href="{share_url}" target="_blank" style="background-color:black;color:white;padding:10px;border-radius:10px;text-decoration:none;">𝕏 でシェアする</a>', unsafe_allow_html=True)
    else:
        st.error("AIの機嫌が悪いようです。時間をおいて試してください。")
