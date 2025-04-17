
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from fpdf import FPDF
import random

# ---------------------------
# Simulated Data for Testing
# ---------------------------
def simulate_inventory(product_name):
    return pd.DataFrame({
        'Process': ['Raw material extraction', 'Manufacturing', 'Transport', 'Use phase', 'End-of-life'],
        'Energy (MJ)': [random.uniform(10, 100) for _ in range(5)],
        'GHG Emissions (kg CO2-eq)': [random.uniform(1, 10) for _ in range(5)],
        'Water Use (L)': [random.uniform(5, 50) for _ in range(5)]
    })

# ---------------------------
# Generate PDF Report
# ---------------------------
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'ISO-Compliant LCA Report', 0, 1, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(2)

    def chapter_body(self, text):
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 10, text)
        self.ln()

    def add_chart(self, fig):
        fig.savefig("chart.png")
        self.image("chart.png", w=180)

# ---------------------------
# Streamlit UI
# ---------------------------
st.set_page_config(page_title="LCA Bot", layout="centered")
st.title("🔍 ISO-Compliant LCA Bot")
st.markdown("This bot performs a full cradle-to-grave LCA using test data.")

product_name = st.text_input("Enter the product name:", "Generic Product")

if st.button("Run LCA"):
    st.subheader("Goal & Scope Definition")
    st.markdown(f"**Goal:** Assess environmental impacts of {product_name} over its full life cycle.")
    st.markdown("**System boundary:** Cradle-to-grave")

    st.subheader("Life Cycle Inventory (LCI)")
    inventory = simulate_inventory(product_name)
    st.dataframe(inventory)

    st.subheader("Life Cycle Impact Assessment (LCIA)")
    ghg_total = inventory['GHG Emissions (kg CO2-eq)'].sum()
    water_total = inventory['Water Use (L)'].sum()
    energy_total = inventory['Energy (MJ)'].sum()

    st.metric("Total GHG Emissions (kg CO2-eq)", f"{ghg_total:.2f}")
    st.metric("Total Energy Use (MJ)", f"{energy_total:.2f}")
    st.metric("Total Water Use (L)", f"{water_total:.2f}")

    st.subheader("Charts")
    fig, ax = plt.subplots()
    inventory.plot(x='Process', y='GHG Emissions (kg CO2-eq)', kind='bar', ax=ax)
    st.pyplot(fig)

    st.subheader("Interpretation")
    top_process = inventory.loc[inventory['GHG Emissions (kg CO2-eq)'].idxmax(), 'Process']
    st.markdown(f"Greatest GHG contributor: **{top_process}**")

    # Generate PDF
    pdf = PDF()
    pdf.add_page()
    pdf.chapter_title("1. Goal & Scope")
    pdf.chapter_body(f"Goal: Assess environmental impacts of {product_name} over its full life cycle.\nSystem boundary: Cradle-to-grave.")
    pdf.chapter_title("2. Inventory")
    for idx, row in inventory.iterrows():
        pdf.chapter_body(f"{row['Process']}: {row['Energy (MJ)']:.2f} MJ, {row['GHG Emissions (kg CO2-eq)']:.2f} kg CO2-eq, {row['Water Use (L)']:.2f} L")
    pdf.chapter_title("3. Impact Assessment")
    pdf.chapter_body(f"Total GHG: {ghg_total:.2f} kg CO2-eq\nTotal Energy: {energy_total:.2f} MJ\nTotal Water: {water_total:.2f} L")
    pdf.chapter_title("4. Interpretation")
    pdf.chapter_body(f"Most impactful process: {top_process}")
    pdf.add_chart(fig)
    pdf.output("lca_report.pdf")

    with open("lca_report.pdf", "rb") as file:
        st.download_button("📄 Download Full PDF Report", file, file_name="lca_report.pdf")
