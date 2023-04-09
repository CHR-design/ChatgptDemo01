import openai
import streamlit as st

# set up OpenAI API key
openai.api_key = st.secrets["openai"]["api_key"]

# define function to interact with OpenAI
def generate_text(prompt):
    response = openai.Completion.create(
      engine="text-davinci-003",
      prompt=prompt,
      max_tokens=1024,
      n=1,
      stop=None,
      temperature=0.5,
    )

    message = response.choices[0].text.strip()
    return message

# create Streamlit app
def main():
    st.title("GPT Chatbot")

    # create text input for user to input text
    user_input = st.text_input("You: ")

    # create button to generate response from OpenAI
    if st.button("Send"):
        response = generate_text(user_input)
        st.write("Bot: " + response)

if __name__ == "__main__":
    main()
