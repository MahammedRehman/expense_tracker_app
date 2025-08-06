import pdfplumber
import pandas as pd
import re
from datetime import datetime

# 1. Extract raw text from the PDF
def extract_text_from_pdf(file_path):
    all_text = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                all_text.append(text)
    return "\n".join(all_text)

# 2. Parse structured transactions from raw text
def extract_transactions_from_text(text):
    lines = text.splitlines()
    transactions = []

    for i in range(len(lines) - 1):
        line = lines[i].strip()

        # Match lines like: Aug 06, 2025 Paid to X DEBIT ₹360
        match = re.match(
            r"^([A-Za-z]{3,9} \d{1,2}, \d{4}) (Paid to|Received from) (.+?) (DEBIT|CREDIT) ₹([\d,]+)",
            line
        )

        if match:
            date_str = match.group(1)
            direction = match.group(2)
            name = match.group(3).strip()
            txn_type = match.group(4)
            amount_str = match.group(5).replace(",", "")

            try:
                amount = float(amount_str)
                # Get time from next line
                time_line = lines[i + 1].strip()
                time_match = re.match(r"^(\d{1,2}:\d{2}) ?(am|pm)$", time_line, re.IGNORECASE)
                if time_match:
                    time_str = f"{time_match.group(1)} {time_match.group(2)}"
                else:
                    time_str = "12:00 am"  # fallback

                # Combine date and time
                dt = datetime.strptime(f"{date_str} {time_str}", "%b %d, %Y %I:%M %p")

                transactions.append({
                    "Date": dt.date(),
                    "Time": dt.time(),
                    "Description": name,
                    "Debit": amount if txn_type == "DEBIT" else 0,
                    "Credit": amount if txn_type == "CREDIT" else 0
                })

            except Exception as e:
                print(f"⚠️ Failed to parse: {e}")
                continue

    return pd.DataFrame(transactions) if transactions else None

# 3. Entry point for app.py
def parse_pdf(file_path):
    raw_text = extract_text_from_pdf(file_path)

    # 👇 DEBUG print full raw text
    print("\n🧾 RAW EXTRACTED TEXT START =================")
    print(raw_text[:3000])  # print first 3000 characters
    print("\n🧾 RAW EXTRACTED TEXT END ===================")

    result = extract_transactions_from_text(raw_text)
    print(f"📦 Returned result type: {type(result)}")
    return result
