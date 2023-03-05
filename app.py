import openai
import streamlit as st

# 设置OpenAI API的访问密钥
openai.api_key = st.secrets["openai"]["api_key"]

# 定义一个函数，使用GPT-3生成代码
def generate_code(language, prompt):
    model_engine = "text-codex-002"
    # 设置生成代码的参数
    completions = openai.Completion.create(
        engine=model_engine,
        prompt=f"Please write a {language} code that {prompt}.",
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=0.5,
    )
    # 从生成代码的结果中提取代码
    message = completions.choices[0].text
    code = message.strip()
    return code

# 设置Streamlit应用程序的外观和布局
st.set_page_config(page_title="Generate Code", page_icon=":computer:", layout="wide")

st.title("OpenAI GPT-3 代码生成器")
st.write("请输入您的需求内容和编程语言，让GPT-3帮助您生成代码！")

# 允许用户选择编程语言和需求
language = st.selectbox("编程语言", ["Python", "JavaScript", "Java"])
prompt = st.text_input("输入您的需求内容", "generate Fibonacci sequence")

# 当用户单击按钮时，使用GPT-3生成代码
if st.button("Generate Code"):
    code = generate_code(language, prompt)
    # 显示生成的代码
    st.code(code, language=language.lower())

