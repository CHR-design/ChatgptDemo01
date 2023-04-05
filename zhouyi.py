import openai

import streamlit as st


# 设置OpenAI API的访问密钥

openai.api_key = st.secrets["openai"]["api_key"]


# 创建 Streamlit 应用程序

def main():

    st.title("周易算命")

    # 添加用户输入框

    name = st.text_input("请输入您的姓名")

    birth_date = st.text_input("请输入您的生辰八字")

    question = st.text_input("请输入您的问题[如，我的婚姻；我明天期末考试如何；(具体问题：人+时间+地点+事件)]")

    # 添加“提交”按钮

    if st.button("提交"):

        # 调用 OpenAI API 进行自然语言处理

        response = openai.Completion.create(

            engine="text-davinci-003",

            prompt=f"用周易帮我算{question}，本人姓名：{name}\n生辰八字：{birth_date}\n",

            temperature=0.7,

            max_tokens=2048,

            n=1,

            stop=None,

        )

        # 显示 OpenAI API 的响应

        st.write(response.choices[0].text)

if __name__ == "__main__":

    main()
