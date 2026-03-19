# 💰 FinCal-AI (Finova)

> A full-stack AI-powered Financial Calculator Web Application — Final Year Project

![Project Banner](https://img.shields.io/badge/Project-FinCal--AI-6C3BBF?style=for-the-badge)
![React](https://img.shields.io/badge/React-Frontend-61DAFB?style=for-the-badge&logo=react)
![Node.js](https://img.shields.io/badge/Node.js-Backend-339933?style=for-the-badge&logo=node.js)
![Python](https://img.shields.io/badge/Python-FastAPI-009688?style=for-the-badge&logo=fastapi)
![Firebase](https://img.shields.io/badge/Firebase-Database-FFCA28?style=for-the-badge&logo=firebase)
![Groq AI](https://img.shields.io/badge/Groq-AI%20API-FF4F00?style=for-the-badge)

---

## 📌 About the Project

**FinCal-AI (Finova)** is a comprehensive full-stack web application that brings together **19 financial calculators**, **interactive data visualizations**, and an **AI-powered financial assistant** — all in one platform. Whether you want to calculate your EMI, plan your investments, or simply ask a finance-related question, Finova has you covered.

The project also includes a **personal dashboard** for a quick financial overview and a **history feature** to track all your past calculations.

This project was developed as a **Final Year Project** by a team of 4 developers.

---

## ✨ Features

- 🤖 **AI Financial Assistant** — Powered by Groq API, ask any finance-related question and get instant intelligent answers
- 🧮 **19 Financial Calculators** — Covering all major finance topics like EMI, SIP, Tax, Interest, Investment, and more
- 📊 **Charts & Graphs** — Every calculator comes with interactive visualizations for better understanding
- 🗂️ **Calculation History** — View and track all your past calculations in one place
- 📋 **Dashboard** — A clean overview of your financial activity at a glance
- 🔐 **User Authentication** — Secure login and signup using Firebase
- 📧 **Email Notifications** — Gmail SMTP integration for alerts and updates
- 📥 **CSV Download** — Export your calculation data as CSV files

---

## 🧮 Calculators (19 Total)

| # | Calculator | # | Calculator |
|---|-----------|---|-----------|
| 1 | EMI Calculator | 11 | Inflation Calculator |
| 2 | SIP Calculator | 12 | Savings Goal Calculator |
| 3 | Income Tax Calculator | 13 | Budget Calculator |
| 4 | Fixed Deposit (FD) Calculator | 14 | Net Worth Calculator |
| 5 | Recurring Deposit (RD) Calculator | 15 | GST Calculator |
| 6 | Simple Interest Calculator | 16 | Currency Converter |
| 7 | Compound Interest Calculator | 17 | Mutual Fund Calculator |
| 8 | Loan Calculator | 18 | Home Loan Calculator |
| 9 | Investment Return Calculator | 19 | Car Loan Calculator |
| 10 | Retirement Calculator | | |

> *(Update this list with your actual calculator names if different)*

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React, TypeScript, Tailwind CSS |
| Backend | Node.js, Express.js |
| AI Backend | Python, FastAPI |
| Database / Auth | Firebase |
| AI Integration | Groq AI API |
| Charts & Graphs | Chart.js / Recharts |
| Email Service | Gmail SMTP (Nodemailer) |

---

## 👩‍💻 Team Members

| Name | Role | Responsibility |
|------|------|---------------|
| **Chaitrali** | Frontend Developer | React UI, Calculators, Dashboard, Charts & Visualizations |
| **Jagruti** | Backend Developer | Node.js, Express.js, REST APIs |
| **Siddhi** | Database Manager | Firebase, Data Modeling, History Feature |
| **Sakshi** | API Integration | Groq AI API, Python FastAPI, Email Service |

---

## 📁 Project Structure

```
Finova/
├── Frontend2/              # React Frontend
│   ├── src/
│   │   ├── components/     # Reusable UI components
│   │   ├── pages/          # Calculator pages, Dashboard, History
│   │   └── assets/
│   ├── package.json
│   └── tailwind.config.ts
├── Backend/                # Node.js + Python Backend
│   ├── server.js           # Node.js Express server
│   ├── routes/             # API routes
│   ├── .env                # (not pushed - contains secrets)
│   └── package.json
└── README.md
```

---

## ⚙️ Installation & Setup

### Prerequisites
- Node.js installed
- Python 3.x installed
- npm and pip installed
- Firebase account
- Groq API key

---

### 1. Clone the Repository
```bash
git clone https://github.com/chaitrali-07/FinCal-AI.git
cd FinCal-AI
```

### 2. Setup Node.js Backend
```bash
cd Backend
npm install
```

Create a `.env` file inside the `Backend` folder:
```env
GROQ_API_KEY=your_groq_api_key
GMAIL_USER=your_email@gmail.com
GMAIL_PASS=your_app_password
PORT=5000
```

Start the backend:
```bash
node server.js
```

### 3. Setup React Frontend
```bash
cd Frontend2
npm install
npm run dev
```

### 4. Open in Browser
```
http://localhost:5173
```

---

## 🔐 Environment Variables

Never push these to GitHub. Keep them only in your local `.env` file.

| Variable | Description |
|----------|-------------|
| `GROQ_API_KEY` | Your Groq AI API key |
| `GMAIL_USER` | Gmail address for email notifications |
| `GMAIL_PASS` | Gmail App Password |
| `PORT` | Backend server port (default: 5000) |

---

## 📸 Screenshots

> *(Add your project screenshots here)*

| Dashboard | Calculator | AI Assistant |
|-----------|-----------|--------------|
| ![Dashboard](screenshots/dashboard.png) | ![Calculator](screenshots/calculator.png) | ![AI](screenshots/ai.png) |

---

## 🚀 Deployment

| Part | Recommended Platform |
|------|----------|
| Frontend | Vercel / Netlify |
| Node.js Backend | Render / Railway |
| Python FastAPI | Render / Railway |
| Database | Firebase (Cloud) |

---

## 📄 License

This project is developed for educational purposes as a Final Year Project.

---

> ⭐ If you found this project helpful, don't forget to give it a star on GitHub!
