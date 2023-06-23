# Bring deps
import os
#from apikey import apikey

import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.utilities import WikipediaAPIWrapper


#os.environ['OPENAI_API_KEY'] = apikey
verbose = True

# App framework
st.title('🦜️🔗 Createur de scripts Youtube')
openai_api_key = st.sidebar.text_input("Votre clé d'API OpenAI")
prompt = st.text_input('Saisissez le sujet de votre vidéo Youtube ici')

if not openai_api_key.startswith('sk-'):
    st.warning("Veuillez entrer votre clé d'API OpenAI!", icon='⚠')
    st.warning("https://platform.openai.com/account/api-keys", icon='⚠')


# Prompt templates
title_template = PromptTemplate(
    input_variables=['topic'],
    template="ecris-moi le titre d'une video Youtube au sujet de {topic}"
)

script_template = PromptTemplate(
    input_variables=['title', 'wikipedia_research'],
    template="ecris-moi le script d'une video Youtube basé sur ce titre {title} en utilisant cette recherche Wikipedia {wikipedia_research}"
)

# Memory
title_memory = ConversationBufferMemory(
    input_key='topic', memory_key='chat_history')
script_memory = ConversationBufferMemory(
    input_key='title', memory_key='chat_history')


# Llms
llm = OpenAI(temperature=0.9, openai_api_key=openai_api_key)
title_chain = LLMChain(llm=llm, prompt=title_template,
                       verbose=verbose, output_key='title', memory=title_memory)
script_chain = LLMChain(llm=llm, prompt=script_template,
                        verbose=verbose, output_key='script', memory=script_memory)

wiki = WikipediaAPIWrapper(lang='fr')

# sequential_chain = SequentialChain(chains=[title_chain, script_chain], input_variables=[
#                                    'topic'], output_variables=['title', 'script'], verbose=verbose)


# show stuff to the screen if there is a prompt
if prompt:
    title = title_chain.run(prompt)
    wiki_research = wiki.run(prompt)
    script = script_chain.run(title=title, wikipedia_research=wiki_research)
    # response = sequential_chain({'topic': prompt})
    st.write(title)
    st.write(script)

    with st.expander('Historique des titres'):
        st.info(title_memory.buffer)

    with st.expander('Historique des messages'):
        st.info(script_memory.buffer)

    with st.expander('Historique des recherches wikipedia'):
        st.info(wiki_research)
