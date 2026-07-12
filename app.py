import streamlit as st
import urllib.parse
import requests

st.set_page_config(page_title="クソリプジェネレーター", page_icon="💩")
st.title("💩 クソリプジェネレーター")

# サイドバーで入力
api_key = st.sidebar.text_input("Gemini APIキー (AQ...)", type="password")
mode = st.radio("モード", ("年上上司", "熱血マン"))
user_input = st.text_area("本音を入力")

if st.button("生成する"):
    if not api_key:
        st.error("👈 サイドバーにAPIキーを入力してください")
    elif not user_input:
        st.warning("本音を入力してください")
    else:
        sys_p = "あなたはウザい昭和の上司です。精神論で説教して。" if mode == "年上上司" else "あなたはウザい熱血マンです。大チャンスと全肯定して。"
        prompt_text = f"設定: {sys_p}\n入力: {user_input}"
        
        # 古いライブラリを捨てて、直接GoogleのAPIを叩く
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        headers = {'Content-Type': 'application/json'}
        data = {
            "contents": [{"parts": [{"text": prompt_text}]}]
        }
        
        with st.spinner("AIがクソリプを練っています..."):
            try:
                res = requests.post(url, headers=headers, json=data)
                res_json = res.json()
                
                if res.status_code == 200:
                    kuso_reply = res_json['candidates'][0]['content']['parts'][0]['text']
                    st.success("クソリプが届きました！")
                    st.info(kuso_reply)
                    
                    # Xシェアボタン
                    share_text = f"【私の本音】\n{user_input}\n\n【クソリプ】\n{kuso_reply}\n\n#クソリプジェネ"
                    share_url = "https://twitter.com/intent/tweet?text=" + urllib.parse.quote(share_text)
                    st.markdown(f'<a href="{share_url}" target="_blank" style="background-color:black;color:white;padding:10px;border-radius:10px;text-decoration:none;">𝕏 でシェアする</a>', unsafe_allow_html=True)
                else:
                    st.error(f"Googleからのエラー: {res_json.get('error', {}).get('message', '不明なエラー')}")
            except Exception as e:
                st.error(f"通信エラー: {e}")
