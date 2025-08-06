import streamlit as st
import pandas as pd
from pdf_parser import parse_pdf
import matplotlib.pyplot as plt

st.set_page_config(page_title="Expense Insights", layout="wide")
st.title("📄 Daily Expense Analyzer")
st.markdown("Upload a transaction PDF to get insights about your expenses and income.")

# Upload PDF
uploaded_file = st.file_uploader("Upload your transaction PDF", type=["pdf"])

if uploaded_file:
    with open("expense.pdf", "wb") as f:
        f.write(uploaded_file.read())

    with st.spinner("📊 Extracting data..."):
        result = parse_pdf("expense.pdf")

    if isinstance(result, str):
        st.subheader("🔍 Raw OCR Text")
        st.text(result)
        st.warning("The parser is returning raw text instead of structured data. Custom parsing logic needed.")

    elif isinstance(result, pd.DataFrame):
        df = result
        if df.empty:
            st.error("❌ No valid data extracted from the PDF.")
        else:
            st.success("✅ Data extracted successfully!")

            # Convert and clean
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
            df.dropna(subset=['Date'], inplace=True)
            df['Debit'] = pd.to_numeric(df['Debit'], errors='coerce').fillna(0)
            df['Credit'] = pd.to_numeric(df['Credit'], errors='coerce').fillna(0)

            # ================================
            # ✅ FILTERS
            # ================================
            st.sidebar.header("📅 Filter Transactions")

            start_date = st.sidebar.date_input("Start Date", df['Date'].min())
            end_date = st.sidebar.date_input("End Date", df['Date'].max())

            payees = df['Description'].dropna().unique()
            selected_payees = st.sidebar.multiselect("Payees", sorted(payees), default=payees)

            filtered_df = df[
                (df['Date'].dt.date >= start_date) &
                (df['Date'].dt.date <= end_date) &
                (df['Description'].isin(selected_payees))
            ]

            if filtered_df.empty:
                st.warning("⚠️ No transactions match the filters.")
                st.stop()

            # ================================
            # ✅ Table and CSV Download
            # ================================
            st.subheader("🔍 Extracted Transactions")
            st.dataframe(filtered_df)

            st.download_button(
                label="📁 Download Transactions as CSV",
                data=filtered_df.to_csv(index=False),
                file_name="transactions.csv",
                mime="text/csv"
            )

            # ================================
            # ✅ Summary Metrics
            # ================================
            total_debit = filtered_df['Debit'].sum()
            total_credit = filtered_df['Credit'].sum()

            col1, col2 = st.columns(2)
            col1.metric("💸 Total Spent", f"₹{total_debit:,.2f}")
            col2.metric("💰 Total Received", f"₹{total_credit:,.2f}")

            # ================================
            # ✅ Top 3 Spendings
            # ================================
            top_spends = filtered_df.sort_values(by='Debit', ascending=False).head(3)
            st.subheader("📉 Top 3 Highest Spendings")
            st.bar_chart(top_spends.set_index("Description")["Debit"])

            # ================================
            # ✅ Daily Spending
            # ================================
            try:
                daily_spending = filtered_df.groupby(filtered_df['Date'].dt.date)['Debit'].sum()
                st.subheader("📅 Daily Spending Overview")
                st.bar_chart(daily_spending)
            except Exception as e:
                st.warning(f"Couldn't create daily spend chart: {e}")

            # --- Additional Insights Section ---
            st.subheader("📊 Key Insights")

            # 💥 Biggest Spending Day
            if not daily_spending.empty:
                biggest_day = daily_spending.idxmax()
                biggest_amount = daily_spending.max()
                st.markdown(f"💥 **Biggest Spending Day:** {biggest_day.strftime('%b %d, %Y')} — ₹{biggest_amount:,.2f}")

            # 🔄 Debit vs Credit Count
            debit_count = df[df["Debit"] > 0].shape[0]
            credit_count = df[df["Credit"] > 0].shape[0]
            st.markdown(f"🔄 **Transactions Count:** Debit - `{debit_count}`, Credit - `{credit_count}`")

            # 📊 Pie Chart for Transaction Types
            labels = ["Debit", "Credit"]
            counts = [debit_count, credit_count]
            colors = ["#FF6B6B", "#6BCB77"]

            fig, ax = plt.subplots(figsize=(3, 3))  # Smaller figure size
            ax.pie(counts, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
            ax.axis('equal')

            # Center the chart using columns
            left, center, right = st.columns([1, 2, 1])
            with center:
                st.pyplot(fig)

            # ================================
            # ✅ Averages
            # ================================
            try:
                daily_avg = filtered_df.groupby(filtered_df['Date'].dt.date)['Debit'].sum().mean()
                monthly_avg = filtered_df.groupby(filtered_df['Date'].dt.to_period("M"))['Debit'].sum().mean()

                st.subheader("📈 Averages")
                col1, col2 = st.columns(2)
                col1.metric("📅 Average Daily Spend", f"₹{daily_avg:,.2f}")
                col2.metric("🗓️ Average Monthly Spend", f"₹{monthly_avg:,.2f}")
            except Exception as e:
                st.warning(f"Couldn't calculate averages: {e}")

            # 1. Required imports
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        import matplotlib.pyplot as plt
        import tempfile
        import os

        # 2. Paths to temporary chart images
        top_spends_chart = "top_spends_chart.png"
        daily_spend_chart = "daily_spend_chart.png"
        pie_chart = "pie_chart.png"


        # 3. Save charts with labels
        def save_charts():
            # Top 3 Spendings Bar Chart
            fig1, ax1 = plt.subplots()
            top_data = top_spends.set_index("Description")["Debit"]
            bars1 = top_data.plot(kind='bar', ax=ax1, color='#FF6B6B')
            ax1.set_title("Top 3 Highest Spendings")
            for bar in bars1.patches:
                height = bar.get_height()
                ax1.annotate(f'₹{height:.0f}', (bar.get_x() + bar.get_width() / 2, height),
                             ha='center', va='bottom', fontsize=9)
            fig1.tight_layout()
            fig1.savefig(top_spends_chart)
            plt.close(fig1)

            # Daily Spending Bar Chart
            fig2, ax2 = plt.subplots()
            bars2 = daily_spending.plot(kind='bar', ax=ax2, color='#6BCB77')
            ax2.set_title("Daily Spending Overview")
            for bar in bars2.patches:
                height = bar.get_height()
                ax2.annotate(f'₹{height:.0f}', (bar.get_x() + bar.get_width() / 2, height),
                             ha='center', va='bottom', fontsize=8)
            fig2.tight_layout()
            fig2.savefig(daily_spend_chart)
            plt.close(fig2)

            # Debit vs Credit Pie Chart
            fig3, ax3 = plt.subplots(figsize=(3, 3))
            wedges, texts, autotexts = ax3.pie(
                [debit_count, credit_count],
                labels=["Debit", "Credit"],
                autopct='%1.1f%%',
                startangle=90,
                colors=["#FF6B6B", "#6BCB77"],
                textprops={'fontsize': 9}
            )
            for autotext in autotexts:
                autotext.set_color('white')
            ax3.axis('equal')
            fig3.tight_layout()
            fig3.savefig(pie_chart)
            plt.close(fig3)


        # 4. Generate the PDF file
        def create_pdf():
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            pdf_path = temp_file.name
            c = canvas.Canvas(pdf_path, pagesize=letter)
            width, height = letter
            y = height - 50

            # Title
            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, y, "📊 Expense Insights Report")
            y -= 30

            # Text Insights
            c.setFont("Helvetica", 12)
            c.drawString(50, y, f"💥 Biggest Spending Day: {biggest_day.strftime('%b %d, %Y')} (₹{biggest_amount:,.2f})")
            y -= 20
            c.drawString(50, y, f"🔄 Debit Transactions: {debit_count}")
            y -= 20
            c.drawString(50, y, f"🔄 Credit Transactions: {credit_count}")
            y -= 40

            # Insert charts
            for chart_path, title in [
                (top_spends_chart, "Top 3 Highest Spendings"),
                (daily_spend_chart, "Daily Spending Overview"),
                (pie_chart, "Debit vs Credit Split")
            ]:
                if y < 250:
                    c.showPage()
                    y = height - 50
                c.setFont("Helvetica-Bold", 14)
                c.drawString(50, y, title)
                y -= 10
                c.drawImage(chart_path, 50, y - 250, width=500, height=250)
                y -= 270

            c.save()
            return pdf_path


        # 5. Save charts and create PDF
        save_charts()
        pdf_file_path = create_pdf()

        # 6. Add download button to Streamlit
        with open(pdf_file_path, "rb") as f:
            st.download_button(
                label="📥 Download Insights PDF",
                data=f,
                file_name="expense_insights.pdf",
                mime="application/pdf"
            )



    else:
        st.error("Unexpected output from parser. Please debug.")
