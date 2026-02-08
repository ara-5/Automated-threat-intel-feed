# 🛡️ Automated Threat Intelligence Feed

A fully automated, “set-it-and-forget-it” cybersecurity threat intelligence pipeline that collects, filters, summarizes, and distributes high-risk security news daily — without human intervention.

## 🚀 What This Project Does

- Automatically fetches cybersecurity news from trusted RSS feeds:
  - The Hacker News
  - BleepingComputer
  - Dark Reading
- Filters articles related to critical threats such as:
  - Zero-day vulnerabilities
  - Ransomware attacks
  - Breaches and exploits
- Uses a lightweight Large Language Model (LLM) to generate a concise daily threat summary
- Automatically delivers the report to a Discord channel
- Runs on a daily schedule using GitHub Actions (cloud-native cron)

## 🧠 Why This Matters

Security teams are overwhelmed with information. This project demonstrates how automation and AI can reduce noise, surface high-impact threats, and save operational time — a core requirement in modern cybersecurity operations.

## 🏗️ Architecture
GitHub Actions (Daily Cron)
↓
Python Automation Script
├─ RSS Ingestion
├─ Keyword-Based Threat Filtering
├─ AI Summarization (LLM)
├─ Resilience & Fallback Logic
└─ Automated Distribution (Discord)


## 🛠️ Tech Stack

- **Python 3.11**
- **GitHub Actions** (CI/CD & scheduling)
- **OpenAI API** (LLM summarization)
- **RSS Feeds** (Threat intelligence sources)
- **Discord Webhooks** (Automated reporting)

## 🔐 Security & Reliability Features

- Secrets managed securely using GitHub Actions secrets
- Graceful degradation when LLM API is unavailable
- No hardcoded credentials
- Fully unattended execution

## 📦 How to Run Locally

```bash
pip install -r requirements.txt
python threat_intel.py

Environment variables required:

OPENAI_API_KEY

DISCORD_WEBHOOK

🎯 Use Cases

SOC daily threat briefings

Cybersecurity awareness automation

AI-powered security operations tooling

Demonstration of workflow orchestration and reliability

📌 Future Enhancements

Severity scoring using MITRE ATT&CK

Multi-channel notifications (Email, Slack)

Historical storage and trend analysis

SaaS-ready deployment

