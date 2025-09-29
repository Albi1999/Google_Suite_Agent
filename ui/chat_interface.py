import streamlit as st
import uuid

class ChatInterface:
    def __init__(self, agent, email):
        self.agent = agent
        self.email = email
        st.set_page_config(
            page_title="Agente Google Workspace",
            page_icon="🤖",
            layout="wide"
        )

    def initialize_session_state(self):
        """Initialize Streamlit session state."""
        if "messages" not in st.session_state:
            st.session_state.messages = []
            welcome_message = f"👋 Ciao! Sono il tuo assistente AI per Google Workspace. Ho accesso alla tua email **{self.email}** e posso aiutarti con Gmail, Calendar, Drive e altri servizi Google. Come posso aiutarti oggi?"
            st.session_state.messages.append({
                "role": "assistant",
                "content": welcome_message
            })
        
        if "session_id" not in st.session_state:
            st.session_state.session_id = f"session_{int(uuid.uuid4().hex[:8], 16)}"

    def display_sidebar_info(self):
        """Display useful information in the sidebar."""
        with st.sidebar:
            st.header("ℹ️ Info Sessione")
            st.write(f"**Session ID:** `{st.session_state.session_id}`")
            st.write(f"**Email:** {self.email}")
            st.divider()
            
            st.header("🛠️ Servizi Disponibili")
            services = [
                "📧 Gmail - Cerca e gestisci email",
                "📅 Calendar - Eventi e appuntamenti", 
                "📁 Drive - File e cartelle",
                "📄 Docs - Documenti Google",
                "📊 Sheets - Fogli di calcolo",
                "📋 Tasks - Lista attività",
                "💬 Chat - Google Chat",
                "🔍 Search - Ricerca web"
            ]
            for service in services:
                st.write(service)
            
            st.divider()
            
            if st.button("🚪 Termina Sessione", type="secondary"):
                st.session_state.clear()
                st.rerun()

    def display_chat_history(self):
        """Display the chat history."""
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    def display_examples(self):
        """Display example queries if no messages yet."""
        if len(st.session_state.messages) <= 1:
            st.subheader("💡 Esempi di cosa posso fare:")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.info("**📧 Gmail**\n- Qual è la mia ultima email?\n- Cerca email da Mario\n- Invia email a colleghi")
                st.info("**📅 Calendar**\n- Che impegni ho oggi?\n- Crea evento riunione\n- Eventi della settimana")
            
            with col2:
                st.info("**📁 Drive**\n- Cerca file 'report'\n- Mostra file condivisi\n- Crea nuovo documento")
                st.info("**📊 Sheets/Docs**\n- Leggi foglio vendite\n- Modifica documento\n- Crea presentazione")
    
    def run(self):
        """Run the chat interface and handle user input."""
        self.initialize_session_state()
        
        st.title("🤖 Agente Google Workspace")
        st.caption(f"Assistente AI per la gestione della tua suite Google - Connesso con {self.email}")
        
        self.display_sidebar_info()
        
        self.display_examples()
        
        chat_container = st.container()
        with chat_container:
            self.display_chat_history()

        if prompt := st.chat_input("Scrivi qui la tua richiesta (es: 'Mostrami le ultime 3 email')..."):

            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("🤔 Sto elaborando la tua richiesta..."):
                    try:
                        session_id = st.session_state.session_id
                        response = self.agent.execute_turn(session_id, prompt)
                        
                        if not response or response.strip() == "":
                            response = "❌ Mi scuso, non sono riuscito a generare una risposta. Puoi riprovare con una richiesta diversa?"
                        
                        st.markdown(response)
                        
                    except Exception as e:
                        error_msg = f"❌ **Errore durante l'elaborazione:**\n\n```\n{str(e)}\n```\n\nRiprova con una richiesta diversa."
                        st.markdown(error_msg)
                        response = error_msg
            
            st.session_state.messages.append({"role": "assistant", "content": response})