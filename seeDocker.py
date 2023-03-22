import openai
import streamlit as st

openai.api_key = st.secrets["openai"]["api_key"]

# 定义 generate_prescription 函数
def generate_prescription(symptoms):
    prompt = "生成一个中医和西医药方，用于治疗以下症状：" + symptoms + "。"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )
    prescription = response.choices[0].text
    return prescription

# Streamlit 应用程序

st.title("药方生成器")
symptoms = st.text_input("请描述您的症状：")
if st.button("生成药方"):
    prescription = generate_prescription(symptoms)
    st.write(prescription)
