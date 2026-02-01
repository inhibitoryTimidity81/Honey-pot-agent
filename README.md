# 🕵️‍♂️ Honeypot AI Agent

> **"Turning the tables on scammers, one confused message at a time."**

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B.svg)
![AI](https://img.shields.io/badge/Powered%20by-Gemini%20Pro-8E24AA.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 📖 Overview

The **Honeypot AI Agent** is an autonomous cybersecurity tool designed to waste scammers' time and extract actionable intelligence. It features **"Ram Lal"**, an AI persona simulating a confused, non-tech-savvy elderly victim.

While the scammer tries to "help" Ram Lal transfer money, the system silently:
1.  **Engages** the scammer in endless, frustrating loops.
2.  **Extracts** UPI IDs, Bank Account numbers, Phone numbers, and Phishing links.
3.  **Logs** everything to a secure local database.
4.  **Visualizes** live data on a "Command Center" dashboard.

---

## 🚀 Key Features

* **🤖 AI Persona ("Ram Lal"):** A Generative AI model prompted to act fearful, confused, and slow, maximizing the scammer's time investment.
* **🛡️ Intel Extraction:** Automatically identifies and captures financial details (UPI, Bank Accounts) and contact info from chat logs.
* **📊 Live Command Center:** A WhatsApp-style Streamlit dashboard to monitor conversations in real-time.
* **⏳ Time Wasting Metrics:** Tracks exactly how much of the scammer's time has been wasted per session.
* **💾 Persistent Logging:** Uses SQLite to store chat history and intelligence, ensuring data survives server restarts.

---

## 🛠️ Tech Stack

* **Backend:** Python, FastAPI, Uvicorn
* **AI Engine:** Google Gemini API (Generative AI)
* **Dashboard:** Streamlit, Pandas
* **Database:** SQLite (Embedded)
* **Utilities:** Regex for pattern matching

---

## 📂 Project Structure

```bash
honeypot-agent/
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
