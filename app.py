import openai
import streamlit as st

# 设置OpenAI API密钥
openai.api_key = "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"

# 定义一个函数，使用OpenAI GPT-3生成代码
def generate_code(prompt, language):
    model_engine = "text-davinci-002"
    completions = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=0.7,
    )
    message = completions.choices[0].text
    return message

# Streamlit 应用程序主体
def app():
    st.title("OpenAI GPT-3 代码生成器")
    st.write("请输入您的需求内容和编程语言，让GPT-3帮助您生成代码！")

    # 获取用户输入
    prompt = st.text_input("输入您的需求内容")
    language = st.text_input("输入编程语言")

    # 按下按钮以生成代码
    if st.button("生成代码"):
        # 调用 generate_code() 函数
        code = generate_code(prompt, language)
        st.code(code, language=language)

if __name__ == '__main__':
    app()
