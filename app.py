# Bring deps
import os
from apikey import apikey

import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain


os.environ['OPENAI_API_KEY'] = apikey
verbose = True

# App framework
st.title('🦜️🔗 Createur de scripts Youtube')
prompt = st.text_input('Saisissez le sujet de votre vidéo Youtube ici')

# Prompt templates
title_template = PromptTemplate(
    input_variables=['topic'],
    template="ecris-moi le titre d'une video Youtube au sujet de {topic}"
)

script_template = PromptTemplate(
    input_variables=['title'],
    template="ecris-moi le script d'une video Youtube basé sur ce titre {title}"
)


# Llms
llm = OpenAI(temperature=0.9)
title_chain = LLMChain(llm=llm, prompt=title_template,
                       verbose=verbose, output_key='title')
script_chain = LLMChain(llm=llm, prompt=script_template,
                        verbose=verbose, output_key='script')
sequential_chain = SequentialChain(chains=[title_chain, script_chain], input_variables=[
                                   'topic'], output_variables=['title', 'script'], verbose=verbose)


# show stuff to the screen if there is a prompt
if prompt:
    response = sequential_chain({'topic':prompt})
    st.write(response['title'])
    st.write(response['script'])
