import os
import asyncio
import threading
from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams

class GoogleWorkspaceAgent:
    def __init__(self, model_name: str, system_prompt: str):
        if not os.environ.get("GOOGLE_API_KEY"):
            raise ValueError("GOOGLE_API_KEY required.")

        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=self._run_event_loop, daemon=True)
        self.thread.start()

        future = asyncio.run_coroutine_threadsafe(self._async_init(model_name, system_prompt), self.loop)
        future.result()

    def _run_event_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    async def _async_init(self, model_name: str, system_prompt: str):
        agent_definition = LlmAgent(
            model=model_name,
            name='google_workspace_assistant_agent',
            instruction=system_prompt,
            tools=[
                MCPToolset(
                    connection_params=StreamableHTTPConnectionParams(
                        url="http://mcp_server:8000/mcp"
                    )
                )
            ],
        )
        self.session_service = InMemorySessionService()
        self.runner = Runner(
            app_name='google_workspace_agent_app',
            agent=agent_definition,
            session_service=self.session_service,
        )
        self.sessions = {}
        print("[Agent] Async initialization completed.")

    def execute_turn(self, session_id: str, user_prompt: str) -> str:
        if not hasattr(self, 'runner'):
            return "Error: Agent not initialized correctly."
            
        future = asyncio.run_coroutine_threadsafe(
            self.async_execute_turn(session_id, user_prompt), self.loop
        )
        return future.result()

    async def async_execute_turn(self, session_id: str, user_prompt: str) -> str:
        if session_id not in self.sessions:
            print(f"Creating a new ADK session with ID: {session_id}")
            self.sessions[session_id] = await self.session_service.create_session(
                app_name=self.runner.app_name, user_id=session_id, session_id=session_id
            )
        
        session = self.sessions[session_id]
        user_content = Content(role='user', parts=[Part(text=user_prompt)])
        final_response = ""

        try:
            events_async = self.runner.run_async(
                session_id=session.id, user_id=session.user_id, new_message=user_content
            )
            async for event in events_async:
                if event.is_final_response() and event.content:
                    for part in event.content.parts:
                        if part.text:
                            final_response += part.text
            
            return final_response if final_response else "Action completed"

        except Exception as e:
            print(f"Error during execution of ADK Agent: {e}")
            return f"Error: {str(e)}"