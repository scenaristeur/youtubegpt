# Bring deps
import os
from apikey import apikey

import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


os.environ['OPENAI_API_KEY'] = apikey

# App framework
st.title('🦜️🔗 Createur de scripts Youtube')
prompt = st.text_input('Saisissez le sujet de votre vidéo Youtube ici')

# Prompt templates
title_template = PromptTemplate(
    input_variables=['topic'],
    template="ecris-moi le titre d'un video Youtube au sujet de {topic}"
)


# Llms
llm = OpenAI(temperature=0.9)
tittle_chain = LLMChain(llm=llm, prompt=title_template, verbose=True)


# show stuff to the screen if there is a prompt
if prompt:
    response = tittle_chain.run(topic=prompt)
    st.write(response)
