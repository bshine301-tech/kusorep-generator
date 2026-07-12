import streamlit as st
import urllib.parse
import google.generativeai as genai

st.set_page_config(page_title="クソリプジェネレーター", page_icon="💩")

st.title("💩 クソリプジェネレーター")
st.write("あなたの本音や愚痴に、AIが最高にイラッとする（または的外れな）クソリプを返します。")

# サイドバーでAPIキーを取得
st.sidebar.header("設定")
api_key = st.sidebar.text_input("Gemini APIキーを入力", type="password", help="Google AI Studioから無料で取得できます")
st.sidebar.markdown("[APIキーの取得はこちら](https://aistudio.google.com/app/apikey)")

# モード選択
mode = st.radio(
    "クソリプのモードを選んでください：",
    ("年上上司からのクソリプ", "熱血ポジティブクソリプ")
)

# ユーザー入力
user_input = st.text_area("あなたの本音・愚痴を入力してください", placeholder="例：この定例会議、報告だけで完全に無駄なので自動化すべき。")

if st.button("クソリプを生成する", type="primary"):
    if not api_key:
        st.error("👈 左のサイドバーからAPIキーを入力してください！")
    elif not user_input:
        st.warning("本音を入力してください！")
    else:
        try:
            # Gemini APIの設定
            genai.configure(api_key=api_key)
            
            # 使えるモデルを自動検索して設定するコード
            available_models = [m for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            model = genai.GenerativeModel(available_models[0].name)

            # システムプロンプトの設定
            if mode == "年上上司からのクソリプ":
                system_prompt = '''あなたは「最高にイラッとする昭和気質の年上上司」です。
ユーザーの入力に対して、以下のルールでクソリプを返してください。
1. 結論や解決策は一切出さない。
2. 必ず「うーん、君の言うことも一理あるんだけどね」など、一旦受け入れるフリをしてから論点をすり替える。
3. ITツールや効率化を軽視し、「泥臭さ」「汗をかく」「気持ち」などの精神論を押し付ける。
4. 「僕の若い頃はね…」から始まる隙あらば自分語り・武勇伝を必ず1つ入れる。
5. 最後は「君の成長に期待してるからさ！」など、無責任に丸投げして締める。
文字数は200文字程度としてください。'''
            else:
                system_prompt = '''あなたは「的外れでウザいほど超前向きな熱血マン」です。
ユーザーの入力に対して、以下のルールでクソリプを返してください。
1. どんな不幸や怒りも、必ず「素晴らしい気づきですね！」「大チャンスを引き当てましたね！」と全肯定から入る。
2. 相手の怒りや悲しみに一切共感せず、すべてを「次への貴重なデータ」「限界突破のバネ」と勝手に解釈する。
3. 語尾には「！」を多用し、圧倒的な熱量とポジティブなエネルギーを持たせる。
4. 「さあ、ワクワクしてきましたね！」などと無理やりテンションを上げさせて締める。
文字数は200文字程度としてください。'''

            # AIへ送信する最終プロンプト
            prompt = f"【設定】\n{system_prompt}\n\n【ユーザーの入力】\n{user_input}\n\n【あなたの回答】"
            
            with st.spinner("AIがクソリプを練っています..."):
                response = model.generate_content(prompt)
                kuso_reply = response.text
                
            st.success("クソリプが届きました！")
            
            # 吹き出し風デザインで表示
            st.info(kuso_reply)
            
            # X（旧Twitter）シェア用のURL生成
            share_text = f"【私の本音】\n{user_input}\n\n【{mode}】\n{kuso_reply}\n\n#クソリプジェネ\n"
            encoded_text = urllib.parse.quote(share_text)
            twitter_url = f"https://twitter.com/intent/tweet?text={encoded_text}"
            
            # シェアボタンの表示
            st.markdown(f'''
            <a href="{twitter_url}" target="_blank" style="text-decoration: none;">
                <div style="background-color: #000000; color: white; padding: 10px 20px; border-radius: 30px; text-align: center; font-weight: bold; width: 250px; margin: 20px auto;">
                    𝕏 でシェアして浄化する
                </div>
            </a>
            ''', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"エラーが発生しました。APIキーが正しいか確認してください。詳細: {e}")
