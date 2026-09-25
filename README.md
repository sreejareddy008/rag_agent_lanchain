# LangChain RAG & Multi-Agent Assistant

An intelligent multi-agent assistant built with LangChain, featuring orchestrator, calendar, Gmail, and web browsing capabilities using OpenRouter LLMs.

## 🚀 Features

- **Orchestrator Agent (`orch_agent.py`)**: Routes user requests to specialized domain agents.
- **Calendar Agent (`calender_agent.py`)**: Manages Google Calendar schedules and events.
- **Gmail Agent (`gmail_agent.py`)**: Drafts, searches, and reads emails via Gmail API.
- **Web Agent (`web_agent.py`)**: Searches the web for real-time information retrieval.

## 🛠️ Installation & Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/sreejareddy008/rag_agent_lanchain.git
   cd rag_agent_lanchain
   ```

2. **Create & Activate Virtual Environment**:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables**:
   Copy `.env.example` to `.env` and configure your API key:
   ```bash
   cp .env.example .env
   ```
   Add your `OPENROUTER_API_KEY` to the `.env` file.

## 🏃 Usage

Run the main orchestrator agent:
```bash
python orch_agent.py
```
