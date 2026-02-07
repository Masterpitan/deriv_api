
# 🛡️ Agentic Guard

### **Autonomous P2P Fraud Detection & Policy Enforcement**

**Agentic Guard** is an AI-powered security layer for the Deriv P2P platform. It moves beyond static filters by using **Multimodal AI Agents** and **Retrieval-Augmented Generation (RAG)** to autonomously detect social engineering, verify payment evidence, and enforce platform policies in real-time.


## 🚀 The Problem

Peer-to-Peer (P2P) trading is vulnerable to sophisticated fraud patterns:

* **Social Engineering:** Scammers lure users off-platform (WhatsApp/Telegram) to bypass security.
* **Triangulation Fraud:** Payments made via third-party bank accounts.
* **Evidence Tampering:** Fake or edited payment receipts.

Manual dispute resolution is slow, reactive, and costly.

## ✨ The Solution

Agentic Guard introduces a proactive **AI Guardian Crew** that acts as an automated compliance officer.

### **Core Features**

* **Contextual Chat Analysis:** Uses LLM agents to scan trade chats for fraud patterns by cross-referencing messages with the **official Deriv P2P Policy** via RAG.
* **Multimodal Receipt Verification:** Extracts sender names and amounts from uploaded images (PNG/JPG) to ensure they match the order details exactly.
* **Policy-as-Code:** Grounded in a dynamic knowledge base (`deriv_policy.txt`), allowing for instant policy updates without retraining models.
* **Reasoned Reporting:** Instead of binary flags, the AI provides detailed reports citing specific policy violations.

---

## 🛠️ Technical Stack

* **Engine:** Gemini 1.5 Flash (Multimodal & High-speed)
* **Framework:** CrewAI & LangChain (Agent orchestration)
* **Backend:** FastAPI (Async API)
* **Frontend:** Streamlit (Security Dashboard)

---

## 📁 Project Structure

```text
deriv-guardian/
├── app/
│   ├── agents.py        # CrewAI Agent & Task definitions
│   ├── database.py      # Mock database for P2P orders
│   └── main.py          # FastAPI endpoints
├── data/
│   └── deriv_policy.txt # Knowledge base for RAG
├── streamlit_app.py     # Frontend Dashboard
├── .env                 # API Keys (Google Gemini)
└── requirements.txt     # Dependencies

```

---

## ⚡ Quick Start

### 1. Clone the repository

### 2. Set up Environment Variables

Create a `.env` file in the root directory:

```text
GOOGLE_API_KEY=your_gemini_api_key_here

```

### 3. Install Dependencies

```bash
pip install -r requirements.txt

```

### 4. Run the Application

**Start the Backend:**

```bash
uvicorn app.main:app --reload

```

**Start the Frontend:**

```bash
streamlit run streamlit_app.py

```

---

## 📊 Comparative Advantage

| Feature | Traditional P2P Security | Agentic Guard |
| --- | --- | --- |
| **Response Time** | Minutes/Hours (Human) | **Seconds (AI)** |
| **Fraud Detection** | Keyword filters | **Agentic Reasoning** |
| **Policy Updates** | Manual training | **Instant (Edit .txt file)** |
| **Evidence Verification** | Manual visual check | **Automated OCR Match** |

---

## 🔮 Future Roadmap

* **Automated Escalation:** Integration with Deriv’s core engine to auto-freeze escrow.
* **Voice Analysis:** Fraud detection for P2P transactions involving voice calls.
* **Blacklist Sync:** Automatically updating global scammer blacklists based on AI findings.