import streamlit as st
import urllib.parse
import requests

st.set_page_config(page_title="クソリプジェネレーター", page_icon="💩")
st.title("💩 クソリプジェネレーター")

# サイドバー
api_key = st.sidebar.text_input("Gemini APIキー (AQ...)", type="password")
mode = st.radio("モード", ("年上上司", "熱血マン"))
user_input = st.text_area("本音を入力")

# ボタンが押されていない時はここでストップ（段落を深くしないための工夫）
if not st.button("生成する"):
    st.stop()

if not api_key:
    st.error("👈 サイドバーにAPIキーを入力してください")
    st.stop()

if not user_input:
    st.warning("本音を入力してください")
    st.stop()

sys_p = "あなたはウザい昭和の上司です。精神論で説教して。" if mode == "年上上司" else "あなたはウザい熱血マンです。大チャンスと全肯定して。"
prompt_text = f"設定: {sys_p}\n入力: {user_input}"

with st.spinner("AIがクソリプを練っています..."):
    try:
        # 1. 使えるモデルを検索
        list_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
        list_res = requests.get(list_url).json()
        
        if "error" in list_res:
            st.error(f"APIキーエラー: {list_res['error']['message']}")
            st.stop()
            
        available_model = None
        for m in list_res.get("models", []):
            if "generateContent" in m.get("supportedGenerationMethods", []):
                available_model = m["name"]
                break
                
        if not available_model:
            st.error("使えるモデルがありません。")
            st.stop()

        # 2. クソリプを生成
        gen_url = f"https://generativelanguage.googleapis.com/v1beta/{available_model}:generateContent?key={api_key}"
        data = {"contents": [{"parts": [{"text": prompt_text}]}]}
        
        res = requests.post(gen_url, headers={'Content-Type': 'application/json'}, json=data)
        res_json = res.json()
        
        if res.status_code != 200:
            st.error(f"生成エラー: {res_json.get('error', {}).get('message', '不明')}")
            st.stop()

        # 結果を表示
        kuso_reply = res_json['candidates'][0]['content']['parts'][0]['text']
        st.success(f"クソリプが届きました！ (使用AI: {available_model.split('/')[1]})")
        st.info(kuso_reply)
        
        # Xシェアボタン
        share_text = f"【私の本音】\n{user_input}\n\n【クソリプ】\n{kuso_reply}\n\n#クソリプジェネ"
        share_url = "https://twitter.com/intent/tweet?text=" + urllib.parse.quote(share_text)
        st.markdown(f'<a href="{share_url}" target="_blank" style="background-color:black;color:white;padding:10px;border-radius:10px;text-decoration:none;">𝕏 でシェアする</a>', unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"エラー: {e}")
                        
                if not available_model:
                    st.error("利用可能なモデルが見つかりません。APIキーの権限を確認してください。")
                    st.stop()

                # 2. 見つけたモデルで生成リクエストを送る
                generate_url = f"https://generativelanguage.googleapis.com/v1beta/{available_model}:generateContent?key={api_key}"
                headers = {'Content-Type': 'application/json'}
                data = {
                    "contents": [{"parts": [{"text": prompt_text}]}]
                }
                
                res = requests.post(generate_url, headers=headers, json=data)
                res_json = res.json()
                
                if res.status_code == 200:
                    kuso_reply = res_json['candidates'][0]['content']['parts'][0]['text']
                    st.success(f"クソリプが届きました！ (裏側で使用したAI: {available_model.split('/')[1]})")
                    st.info(kuso_reply)
                    
                    # Xシェアボタン
                    share_text = f"【私の本音】\n{user_input}\n\n【クソリプ】\n{kuso_reply}\n\n#クソリプジェネ"
                    share_url = "https://twitter.com/intent/tweet?text=" + urllib.parse.quote(share_text)
                    st.markdown(f'<a href="{share_url}" target="_blank" style="background-color:black;color:white;padding:10px;border-radius:10px;text-decoration:none;">𝕏 でシェアする</a>', unsafe_allow_html=True)
                else:
                    st.error(f"Googleからの生成エラー: {res_json.get('error', {}).get('message', '不明なエラー')}")
            except Exception as e:
                st.error(f"通信エラー: {e}")
                    st.info(kuso_reply)
                    
                    # Xシェアボタン
                    share_text = f"【私の本音】\n{user_input}\n\n【クソリプ】\n{kuso_reply}\n\n#クソリプジェネ"
                    share_url = "https://twitter.com/intent/tweet?text=" + urllib.parse.quote(share_text)
                    st.markdown(f'<a href="{share_url}" target="_blank" style="background-color:black;color:white;padding:10px;border-radius:10px;text-decoration:none;">𝕏 でシェアする</a>', unsafe_allow_html=True)
                else:
                    st.error(f"Googleからのエラー: {res_json.get('error', {}).get('message', '不明なエラー')}")
            except Exception as e:
                st.error(f"通信エラー: {e}")
