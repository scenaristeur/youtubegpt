
# Youtube generation de script


# install dependencies
`pip3 install streamlit langchain openai wikipedia chromadb tiktoken`

# openai api key
rename apikey_example.py in apikey.py and fill it with your aopen api key

# run 
`streamlit run app.py`


# inspiration
- tuto https://www.youtube.com/watch?v=MlK6SIjcjE8&t=1288s

# bout de code minimal pour obtenir une réponse 
`
# Bring deps
import os
from apikey import apikey

import streamlit as st
from langchain import OpenAI

os.environ['OPENAI_API_KEY'] = apikey

#App framework
st.title('🦜️🔗 Createur de scripts Youtube')
prompt = st.text_input('Saisissez votre prompt ici')

# Llms
llm = OpenAI(temperature= 0.9)

# show stuff to the screen if there is a prompt
if prompt:
    response = llm(prompt)
    st.write(response)
`

# hosting
- https://blog.streamlit.io/host-your-streamlit-app-for-free/
- https://blog.streamlit.io/langchain-tutorial-1-build-an-llm-powered-app-in-18-lines-of-code/
