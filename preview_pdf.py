import pdfplumber
import pandas as pd
import json

def preview_pdf():
    pdf_path = r"c:\Users\2613r\Downloads\Comedk_data\COMEDK_2025_Complete_Data.pdf"
    try:
        with pdfplumber.open(pdf_path) as pdf:
            page = pdf.pages[0]
            tables = page.extract_tables()
            if tables:
                print(f"Found {len(tables)} tables on page 1")
                # Print first 5 rows of the first table
                for i, row in enumerate(tables[0][:5]):
                    print(f"Row {i}: {row}")
            else:
                print("No tables found on page 1")
                text = page.extract_text()
                print("Text snippet:", text[:500])
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    preview_pdf()
