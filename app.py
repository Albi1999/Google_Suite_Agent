import os
from dotenv import load_dotenv
from datetime import datetime
import google.genai as genai
import streamlit as st

from core.agent import GoogleWorkspaceAgent
from ui.chat_interface import ChatInterface

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

SYSTEM_PROMPT = f"""
Sei un assistente AI professionale e altamente intelligente per Google Workspace dell'utente {{email}}.

La tua funzione principale è aiutare l'utente a gestire il suo spazio di lavoro digitale eseguendo strumenti per interagire con servizi come Gmail, Google Calendar, Google Drive, Docs, Sheets e altri.

REGOLE IMPORTANTI:
- L'email dell'utente è sempre: {{email}}
- Ricorda sempre le conversazioni precedenti per fornire un'esperienza fluida
- Prima di eseguire strumenti che modificano o creano contenuto (es. creare eventi, inviare email), chiedi sempre conferma all'utente
- Se l'esecuzione di uno strumento fallisce, scusati e informa chiaramente l'utente dell'errore restituendo il messaggio di errore e il body della riciesta che ha causato l'errore
- Formatta sempre le informazioni in modo chiaro usando Markdown (liste, testo in grassetto, ecc.)
- Le tue risposte devono essere sempre in italiano
- Sii cortese, conciso e utile

Data e ora corrente: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""

def main():

    if not GOOGLE_API_KEY:
        print("Error: GOOGLE_API_KEY not found in environment variables")
        return

    if "user_email" not in st.session_state:
        st.set_page_config(page_title="Login - Agente Google", layout="centered")
        st.title("🤖 Agente Google Workspace")
        st.write("Inserisci il tuo indirizzo email per iniziare la sessione.")
        
        email = st.text_input("Indirizzo Email", placeholder="es. mario.rossi@maggioli.it")
        
        if st.button("Inizia Sessione", type="primary"):
            if email and "@" in email:
                st.session_state.user_email = email
                st.rerun()
            else:
                st.error("Per favore, inserisci un indirizzo email valido.")
    else:
        user_email = st.session_state.user_email

        if "agent" not in st.session_state:
            dynamic_system_prompt = SYSTEM_PROMPT.format(email=user_email)
            
            st.session_state.agent = GoogleWorkspaceAgent(
                model_name="gemini-2.5-flash",
                system_prompt=dynamic_system_prompt
            )

        if "chat_ui" not in st.session_state:
            st.session_state.chat_ui = ChatInterface(
                agent=st.session_state.agent,
                email=user_email
            )

        st.session_state.chat_ui.run()

if __name__ == "__main__":
    main()