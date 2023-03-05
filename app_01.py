import streamlit as st
import openai

# Set OpenAI API key
openai.api_key = st.secrets["openai"]["api_key"]








# Define app
def app_01():
    # Initialize session state
    session_state = st.session_state.get(logged_in=False)

    # Define homepage layout
def home_page():
    st.title("解惑学院")
    st.write("欢迎来到解惑学院！")

    # Add navigation options
    st.write("导航：")
    if st.button("个人简历"):
        st.experimental_set_query_params(page="resume")
    if st.button("代码编写"):
        st.experimental_set_query_params(page="code")
    if st.button("检查代码Bug"):
        st.experimental_set_query_params(page="bug")
    if st.button("作业解答"):
        st.experimental_set_query_params(page="homework")
    if st.button("看医生"):
        st.experimental_set_query_params(page="doctor")
        
    # Define login page layout
    def login_page():
        st.title("Login")
        # Add login form
        with st.form(key="login_form"):
            username = st.text_input("用户名")
            password = st.text_input("密码", type="password")
            submit = st.form_submit_button("Login")

            # Verify user credentials and set session state
            if submit:
                if username == "admin" and password == "admin":
                    session_state.logged_in = True
                    st.experimental_set_query_params(page="home")
                
    # not logged in
    if st.experimental_get_query_params().get("page") == "login":
        login_page()
    else:
        home_page()

    # Update page if user logs in
    if session_state.logged_in:
        st.experimental_set_query_params(page="home")
        home_page()
if __name__ == '__main__':
    app_01()
