import streamlit as st
import requests

# Set up secrets
app_id = "wx183821d67d234031"
app_secret = "c9b80ffdacb2f6bdbfc08b1b1ffdfe22"
wechat_endpoint = "https://api.weixin.qq.com"
access_token = None
remaining_operations = 10

def get_access_token():
    global access_token
    if access_token is None:
        url = f"{wechat_endpoint}/cgi-bin/token?grant_type=client_credential&appid={app_id}&secret={app_secret}"
        response = requests.get(url)
        response_json = response.json()
        access_token = response_json["access_token"]
    return access_token

def login():
    global remaining_operations
    st.write("请用微信扫描下方二维码以登录")
    st.image(f"{wechat_endpoint}/cgi-bin/wxaapp/qrcode?access_token={get_access_token()}", width=300)
    if st.button("已完成微信登录"):
        remaining_operations -= 1
        st.session_state.logged_in = True
        st.success("登录成功！")
        st.write(f"您还可以进行 {remaining_operations} 次操作。")
        return True
    return False

def register():
    st.write("暂不支持注册。")

def home():
    global remaining_operations
    st.write("欢迎使用本程序！")
    if not st.session_state.get("logged_in"):
        st.warning("请先登录。")
        if login():
            return home()
    else:
        menu = ["个人简历", "代码编写", "检查Bug", "作业解答", "医生看病"]
        choice = st.sidebar.selectbox("请选择一个选项", menu)
        if choice == "个人简历":
            st.write("这是个人简历页面。")
            remaining_operations -= 1
        elif choice == "代码编写":
            st.write("这是代码编写页面。")
            remaining_operations -= 1
        elif choice == "检查Bug":
            st.write("这是检查Bug页面。")
            remaining_operations -= 1
        elif choice == "作业解答":
            st.write("这是作业解答页面。")
            remaining_operations -= 1
        elif choice == "医生看病":
            st.write("这是医生看病页面。")
            remaining_operations -= 1
        st.write(f"您还可以进行 {remaining_operations} 次操作。")

def login_register():
    menu = ["登录", "注册"]
    choice = st.sidebar.selectbox("请选择一个选项", menu)
    if choice == "登录":
        login()
    elif choice == "注册":
        register()

def main():
    st.title("欢迎使用本程序！")
    menu = ["主页", "登录/注册"]
    choice = st.sidebar.selectbox("请选择一个选项", menu)
    if choice == "主页":
        home()
    elif choice == "登录/注册":
        login_register()

if __name__ == "__main__":
    main()
