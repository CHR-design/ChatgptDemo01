import openai
import streamlit as st

openai.api_key = st.secrets["openai"]["api_key"]

# 定义生成日报的函数
def generate_report(work_content):
    prompt = f"Generate a daily report for {work_content}."
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )
    report = response.choices[0].text.strip()
    return report

# 构建 Streamlit Web 界面
st.title("生成日报")
work_content = st.text_input("请写你的工作内容：")
if st.button("Generate"):
    report = generate_report(work_content)
    st.write(report)
