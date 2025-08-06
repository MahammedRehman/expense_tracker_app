# 💰 MoneyMapp

![MoneyMapp Banner](/Assests/image.png) <!-- Optional banner, replace with your image -->

**MoneyMapp** is your personal finance tracker that turns your PhonePe transaction history PDFs into clear, beautiful insights.

MoneyMapp Link : <a href="https://moneymapp.streamlit.app/">Click Me</a> , and I will take you there.

📂 Upload → 🔍 Analyze → 📊 Understand → 💡 Spend better

---

## 🚀 Features

- 📥 Upload multiple **PhonePe** transaction PDFs
- 🔎 Automatically extract and analyze **Credit** & **Debit** data
- 📈 Visual Insights:
  - 💸 Total Spent vs 💰 Total Received
  - 📉 Top 3 Highest Spendings
  - 📅 Daily Spending Overview
  - 💥 Biggest Spending Day
  - 🔄 Debit vs Credit Count (Pie Chart)
- 📆 Filter by Date
- 🧮 Average Daily & Monthly Spend
- 📤 Download insights as a **PDF report**

---

## 📂 How It Works

1. Upload one or more PhonePe transaction PDFs
2. MoneyMap reads and extracts the data
3. It analyzes and visualizes your financial behavior
4. Download the charts and summary in a click

---

## 🛠️ Tech Stack

- `Python`
- `Streamlit`
- `pytesseract` (OCR)
- `pdfplumber`, `pdf2image`, `Pillow`
- `matplotlib`, `pandas`, `reportlab`

---

## 🧪 Local Setup

```bash
git clone https://github.com/yourusername/moneymap.git
cd moneymap
pip install -r requirements.txt
streamlit run app.py 
```

### 🎉 Check Out My Other Fun Project
👉 [Excel Chat Bot](https://github.com/MahammedRehman/excel-chatbot-no-code.git) : 
I built an Excel chatbot using AI — without writing a single line of code!
