import streamlit as st
import os
from groq import Groq as gq
import pandas as pd

# 環境変数から API キーを取得
api_key = "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"
if not api_key:
    st.error("APIキーが設定されていません。")
    st.stop()

# Groq クライアントの初期化
client = gq(api_key=api_key)

def get_response(question):
    """ Groq API を使用してチャット応答を取得する関数 """
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": question}
        ],
        model="llama3-70b-8192",
    )
    return chat_completion.choices[0].message.content

# Streamlit UI
st.title('Groq Recipe')

# ユーザー入力
initial_text = "を使ったレシピを教えてください"

user_input = st.text_input("質問を入力してください:", value=initial_text)
if st.checkbox('アレルギー'): #食材記入したあとにチェックボックスでだす
    text_area = st.text_area('アレルギー', '食材')
    user_input += ("アレルギーは"+text_area +"なので使わないでください。")
if st.checkbox('嫌いな食べ物'):
    text_area = st.text_area('嫌いな食べ物', '食材')
    user_input += ("嫌いな食べ物は"+text_area +"なのであまり使わないでください。")
if st.checkbox('好きな食べ物'):
    text_area = st.text_area('好きな食べ物', '食材')
    user_input += ("好きな食べ物は"+text_area +"なので優先して使ってください。")



col1, col2= st.columns([4,2])

# col1にテキストを表示
with col1:
    if st.button('回答を取得'):
        with st.spinner('回答を取得中...'):
            response = get_response(user_input)
            st.write(response)

# col2にDataFrameを表示
with col2:
    st.header("参照サイト")
    # # DataFrameを表示
    # st.write("df")
    data_df = pd.DataFrame(
    {
        
        "creator": [
            "https://cookpad.com/jp",
           
        ],
    }
)

    st.dataframe(
        data_df,
        column_config={
            
            "creator": st.column_config.LinkColumn(
                "URL", 
                display_text="Open website"
            ),
        },
        hide_index=True,
    )
