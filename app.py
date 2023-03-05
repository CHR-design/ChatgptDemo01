# 引入所需的库
import streamlit as st
import requests
import json

# 定义API密钥和API URL
OPENAI_API_KEY = "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"
OPENAI_API_URL = "https://api.openai.com/v1/engines/davinci-codex/completions"

# 定义Streamlit应用程序
def app():
    # 设置应用程序标题
    st.title("Code Generation")

    # 添加用户输入框
    language = st.text_input("Programming Language", "")
    content = st.text_input("Content", "")

    # 添加“生成代码”按钮
    if st.button("Generate Code"):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_API_KEY}",
        }
        data = {
            "prompt": f"Generate code in {language} for \"{content}\"",
            "temperature": 0.7,
            "max_tokens": 2048,
            "n": 1,
            "stop": "###",
        }
        response = requests.post(OPENAI_API_URL, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            response_data = json.loads(response.text)
            choices = response_data["choices"][0]["text"]
            code = choices[: choices.index("\n")]
            st.write(code)
        else:
            st.write("Failed to generate code. Please try again later.")


# 运行Streamlit应用程序
if __name__ == "__main__":
    app()
