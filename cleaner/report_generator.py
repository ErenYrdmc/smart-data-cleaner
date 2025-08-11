from fpdf import FPDF
import pandas as pd
import tempfile
import os

class PDFReport(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "Smart Data Cleaner - Cleaning Report", ln=True, align="C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 10)
        self.cell(0, 10, f'Page {self.page_no()}', align="C")

    def add_missing_data_table(self, missing_df: pd.DataFrame):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Missing Data Summary:", ln=True)
        self.set_font("Arial", "", 10)

        if missing_df.empty:
            self.cell(0, 10, "No missing data found.", ln=True)
        else:
            col_width = self.w / 3
            self.cell(col_width, 8, "Column", border=1)
            self.cell(col_width, 8, "Missing Count", border=1)
            self.cell(col_width, 8, "Missing %", border=1)
            self.ln()

            for index, row in missing_df.iterrows():
                self.cell(col_width, 8, str(index), border=1)
                self.cell(col_width, 8, str(int(row['Missing Count'])), border=1)
                self.cell(col_width, 8, f"{row['Missing %']:.1f}%", border=1)
                self.ln()

def generate_pdf_report(missing_df: pd.DataFrame) -> bytes:
    pdf = PDFReport()
    pdf.add_page()
    pdf.add_missing_data_table(missing_df)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp_path = tmp.name
        pdf.output(tmp_path)

    with open(tmp_path, "rb") as f:
        content = f.read()

    os.unlink(tmp_path)
    return content
