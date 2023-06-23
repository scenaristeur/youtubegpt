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