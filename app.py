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


from streamlit.components.v1 import html

button = """
<script type="text/javascript"
 src="https://cdnjs.buymeacoffee.com/1.0.0/button.prod.min.js" 
 data-name="bmc-button" data-slug="SqdOnMgfw" data-color="#FFDD00" data-emoji="" 
   data-font="Cookie" data-text="Offre-nous un thé !" data-outline-color="#000000" data-font-color="#000000" data-coffee-color="#ffffff" ></script>
"""

html(button, height=70, width=220)

st.markdown(
    """
    <style>
        iframe[width="220"] {
            position: fixed;
            bottom: 60px;
            right: 40px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


openai_api_key = st.sidebar.text_input("Votre clé d'API OpenAI")
prompt = st.text_input('Saisissez le sujet de votre vidéo Youtube ici')




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
if not openai_api_key.startswith('sk-'):
    st.warning("Veuillez entrer votre clé d'API OpenAI et la copier dans la sidebar à gauche. Elle est disponible sur https://platform.openai.com/account/api-keys.", icon='⚠')
else:
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

st.info("N'oubliez pas de nous soutenir en nous offrant un thé ou un livre en cliquant sur le bouton jaune en bas à droite !)")
st.info("Idées et suggestions https://github.com/scenaristeur/youtubegpt/issues")

st.video('https://youtu.be/25dbMirBY04')
