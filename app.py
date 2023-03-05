import openai
import streamlit as st

# 设置OpenAI API的访问密钥
openai.api_key = st.secrets["openai"]["api_key"]

# 定义一个函数，使用GPT-3生成代码
def generate_code(prompt, language):
    model_engine = "text-davinci-003"
    completions = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=0.7
    )
    message = completions.choices[0].text
    return message

def app():
    st.title("OpenAI GPT-3 代码生成器")
    st.write("请输入您的需求内容和编程语言，让GPT-3帮助您生成代码！")

    # 获取用户输入
    prompt = st.text_input("输入您的需求内容")
    language = st.selectbox("编程语言", ["Python", "JavaScript", "Java"])

    # 按下按钮以生成代码
    if st.button("生成代码"):
        # 调用 generate_code() 函数
        code = generate_code(language,prompt)
        st.code(code, language=language.lower())

if __name__ == '__main__':
    app()
    

