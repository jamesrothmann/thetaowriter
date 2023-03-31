import openai
import streamlit as st
from streamlit_chat import message
import requests

# Set up the OpenAI API key
openai.api_key = st.secrets["api_secret"]

#Creating the chatbot interface
st.title("MungerGPT - Think like Uncle Charlie")

response = requests.get("https://raw.githubusercontent.com/jamesrothmann/askunclecharlie/main/unclecharlieprompt.txt")
prompt_text = response.text.strip()


# Storing the chat
if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

# Define the chatbot function
def chatbot(input_text):
    messages = [
        {"role": "system", "content": prompt_text},
#        {"role": "user", "content": "Give me an overview of mental models"},
#       {"role": "assistant", "content": prompt_text},
        {"role": "user", "content": input_text}
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0301",
  #      model="gpt-4",
        messages=messages,
        temperature=0.7,
        max_tokens=500,
        n=1,
        stop=None,
        frequency_penalty=0,
        presence_penalty=0
    )
    answer = response.choices[0].message['content'].strip()
    return answer

# We will get the user's input by calling the get_text function
def get_text():
    input_text = st.text_input("You: ","Hello, how are you?", key="input")
    return input_text

user_input = get_text()

if user_input:
    output = chatbot(user_input)
    # store the output 
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)

if st.session_state['generated']:
    
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        st.write("Assistant: " + st.session_state["generated"][i])
        st.write("You: " + st.session_state['past'][i])
