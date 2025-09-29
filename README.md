# Google Suite Agent

</div>

<p>
  <img alt="Python" src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white&style=for-the-badge" height="25"/>
  <img alt="Visual Studio Code" src="https://img.shields.io/badge/Visual Studio Code-007ACC?logo=VisualStudioCode&logoColor=white&style=for-the-badge" height="25"/>
  <img alt="MCP" src="https://img.shields.io/badge/MCP%20-000000?style=for-the-badge&logo=modelcontextprotocol&logoColor=white" height="25"/>
  <img alt="Gemini" src="https://img.shields.io/badge/Gemini%20-8E75B2?style=for-the-badge&logo=googlegemini&logoColor=white" height="25"/>
  <img alt="Docker" src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white&logoSize=auto" height="25"/>
  <img alt="Streamlit" src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white&logoSize=auto" height="25"/>
  <img alt="Google Cloud" src="https://img.shields.io/badge/GoogleCloud-4285F4?style=for-the-badge&logo=googlecloud&logoColor=white&logoSize=auto" height="25"/>
  <img alt="Git" src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white&logoSize=auto" height="25"/>
  <img alt="GitHub" src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white&logoSize=auto" height="25"/>
<p>


This repository contains a Docker Compose setup for running a Google Suite Agent application. The application consists of two main services: an MCP server and a Streamlit interface with an AI Agent.

## Quickstart
To quickly run the demo, you can use Docker. Make sure you have Docker installed on your machine.

### Prerequisites
- Docker installed
- An API key for Gemini models from Google Cloud

## Running the demo

> [!IMPORTANT]
> Check the [Google Workspace MCP Reporsitory](https://github.com/taylorwilsdon/google_workspace_mcp.git) to correctly setup the MCP Server.


1. Clone this repository to your local machine.
```bash
git clone ...
```
2. Clone the [google_workspace_mcp](https://github.com/taylorwilsdon/google_workspace_mcp.git) repository into the parent directory.
```bash
git clone https://github.com/taylorwilsdon/google_workspace_mcp.git
```
3. Set your Google API key, Client ID and Client Secret in the `docker-compose.yml` file or as an environment variable.
4. Navigate to the directory containing the `docker-compose.yml` file.
5. Build and run the Docker containers using Docker Compose:
```bash
docker compose up --build
```
