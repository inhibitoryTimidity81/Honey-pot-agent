🕵️‍♂️ Honeypot AI Agent"Turning the tables on scammers, one confused message at a time."📖 OverviewThe Honeypot AI Agent is an autonomous cybersecurity tool designed to waste scammers' time and extract actionable intelligence. It features "Ram Lal", an AI persona simulating a confused, non-tech-savvy elderly victim.While the scammer tries to "help" Ram Lal transfer money, the system silently:Engages the scammer in endless, frustrating loops.Extracts UPI IDs, Bank Account numbers, Phone numbers, and Phishing links.Logs everything to a secure local database.Visualizes live data on a "Command Center" dashboard.🚀 Key Features🤖 AI Persona ("Ram Lal"): A Generative AI model prompted to act fearful, confused, and slow, maximizing the scammer's time investment.🛡️ Intel Extraction: Automatically identifies and captures financial details (UPI, Bank Accounts) and contact info from chat logs.📊 Live Command Center: A WhatsApp-style Streamlit dashboard to monitor conversations in real-time.⏳ Time Wasting Metrics: Tracks exactly how much of the scammer's time has been wasted per session.💾 Persistant Logging: Uses SQLite to store chat history and intelligence, ensuring data survives server restarts.🛠️ Tech StackBackend: Python, FastAPI, UvicornAI Engine: Google Gemini API (Generative AI)Dashboard: Streamlit, PandasDatabase: SQLite (Embedded)Utilities: Regex for pattern matching📂 Project StructureBashhoneypot-agent/
├── app/
│   ├── api/             # API Routes
│   ├── core/            # Config & Settings
│   ├── models/          # Pydantic Schemas
│   ├── services/        # AI Logic & Intel Extraction
│   ├── database.py      # SQLite Connection
│   └── main.py          # FastAPI Entry Point
├── .env                 # API Keys (Not shared)
├── dashboard.py         # Streamlit Command Center
├── honeypot_logs.db     # Local Database (Auto-generated)
├── requirements.txt     # Python Dependencies
└── README.md            # Documentation
⚙️ Installation & Setup1. Clone the RepositoryBashgit clone https://github.com/yourusername/honeypot-agent.git
cd honeypot-agent
2. Create Virtual EnvironmentBashpython -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
3. Install DependenciesBashpip install -r requirements.txt
4. Configure EnvironmentCreate a file named .env in the root folder and add your API keys:Ini, TOMLGEMINI_API_KEY=your_google_gemini_key_here
YOUR_SECRET_API_KEY=my_secret_key_123
GUVI_CALLBACK_URL=https://example.com/report
🏃‍♂️ How to RunYou need to run the Backend and the Dashboard in two separate terminals.Terminal 1: Start the Backend (Brain)Bash# Run from the root folder
python -m app.main
You should see: Uvicorn running on http://0.0.0.0:8000Terminal 2: Start the Dashboard (UI)Bash# Run from the root folder
streamlit run dashboard.py
This will open the dashboard in your browser at http://localhost:8501🧪 Testing the AgentSince the agent is an API, you can trigger it using Postman or cURL.Endpoint: POST http://localhost:8000/api/v1/chatHeaders:x-api-key: (The key from your .env file)Content-Type: application/jsonSample Payload (Start a Scam):JSON{
  "sessionId": "live_demo_1",
  "message": {
    "sender": "Scammer",
    "text": "Hello sir, your electricity will be cut tonight. Call 9876543210 immediately.",
    "timestamp": "2026-02-02T10:00:00Z"
  },
  "conversationHistory": []
}
📸 ScreenshotsLive DashboardExtracted IntelligenceReal-time chat monitoringAuto-captured UPIs & Links(Note: Replace these placeholder links with your actual screenshots)⚠️ DisclaimerThis tool is created for educational and research purposes only.Do not use this tool to harass innocent individuals.The extraction of data is for reporting to relevant authorities (Cyber Cell/Bank).The developers are not responsible for misuse of this software.🤝 ContributionFork the ProjectCreate your Feature Branch (git checkout -b feature/AmazingFeature)Commit your Changes (git commit -m 'Add some AmazingFeature')Push to the Branch (git push origin feature/AmazingFeature)Open a Pull Request📄 LicenseDistributed under the MIT License. See LICENSE for more information.📦 Bonus: requirements.txtCreate a file named requirements.txt and paste this inside so users can install everything easily:Plaintextfastapi
uvicorn
streamlit
google-generativeai
python-dotenv
pandas
requests
pydantic
pydantic-settings
watchdog
