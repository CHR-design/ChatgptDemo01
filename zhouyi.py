import openai

import streamlit as st


# 设置OpenAI API的访问密钥

openai.api_key = st.secrets["openai"]["api_key"]


# 创建 Streamlit 应用程序

def main():

    st.title("周易算命")

    # 添加用户输入框

    name = st.text_input("请输入您的姓名")

    birth_date = st.text_input("请输入您的农历出生日期（格式为 YYYY年MM月DD日）")

    location = st.text_input("请输入您的居住地")

    question = st.text_input("请输入您的问题所在范围(如，婚姻、做生意等)")

    # 添加“提交”按钮

    if st.button("提交"):

        # 调用 OpenAI API 进行自然语言处理

        response = openai.Completion.create(

            engine="davinci",

            prompt=f"假设你是一名占卜师，熟读周易，现在有人向你求{question}，他的姓名叫：{name}\n农历{birth_date}出生\n出生\n住在{location}\n",

            temperature=0.7,

            max_tokens=1024,

            top_p=1,

            frequency_penalty=0,

            presence_penalty=0

        )

        # 显示 OpenAI API 的响应

        st.write(response.choices[0].text)

if __name__ == "__main__":

    main()
