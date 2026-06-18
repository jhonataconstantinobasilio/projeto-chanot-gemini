import streamlit as st
from google import genai
from google.genai import types

MODELO= "gemini-2.5-flash"
persona = open("homem_aranha_persona.txt","r",encoding="utf-8")
INSTRUCAO_DE_SISTEMA = persona.read()
persona.close()


def converter_para_gemini(historico):
    mensagens_gemini = []


    for mensagem in historico:
        papel = mensagem["role"]
        conteudo = mensagem["content"]


        if papel == "assistant":
            papel_gemini = "model"
        else:
            papel_gemini = "user"


        mensagens_gemini.append(
            types.Content(
                role=papel_gemini,
                parts=[types.Part.from_text(text=conteudo)]
            )
        )


    return mensagens_gemini


def gerar_resposta():
    resposta = cliente.models.generate_content(
        model=MODELO,
        contents=converter_para_gemini(st.session_state.historico),
        config=types.GenerateContentConfig(
            system_instruction=INSTRUCAO_DE_SISTEMA,
            temperature=0.4,
        )
    )


    return resposta.text





st.set_page_config("Chatbot com Gemini","🐦")
st.title("Chatbot Homem aranha  🕷️🕸️")

chave_api = st.sidebar.text_input("Digigte sua chave API", type="password")


if not chave_api:
    st.warning("É preciso inserir uma chave de API")
    st.stop()

cliente = genai.Client(api_key= chave_api)

if "historico" not in st.session_state:
    st.session_state.historico= []

for mensagem in st.session_state.historico:  #Percorre o historico
    with st.chat_message(mensagem["role"]):  # Mostra no chat o usuario e a pergunta/resposta
        st.markdown(mensagem["content"])


entrada_usuario= st.chat_input("Digite a sua pergunta: ") 

if entrada_usuario:
    st.session_state.historico.append({
        "role":"user",
        "content":entrada_usuario
        
        })

    with st.chat_message("user"):
        st.markdown(entrada_usuario)   

    with st.chat_message("assistant"):
        resposta_ia = gerar_resposta()
        st.markdown(resposta_ia)

    st.session_state.historico.append({
        "role":"assistant",
        "content":resposta_ia
    })    