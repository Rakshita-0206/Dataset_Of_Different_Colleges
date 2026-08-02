import pdfplumber
import pandas as pd
import re

def convert_comedk_pdf_to_csv(pdf_path, output_csv_path):
    print("Starting page-by-page matrix parsing...")
    
    all_extracted_records = []
    
    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        print(f"Total pages detected: {total_pages}")
        
        for page_idx, page in enumerate(pdf.pages, start=1):
            table = page.extract_table()
            if not table or len(table) < 2:
                continue
            
            # Find the header row on THIS specific page
            header_row = None
            data_start_idx = 0
            
            for idx, row in enumerate(table):
                cleaned_row = [re.sub(r'\s+', ' ', str(cell)).strip() if cell is not None else '' for cell in row]
                # Header row contains 'College Code' or 'College Name'
                if any('College' in cell for cell in cleaned_row):
                    header_row = cleaned_row
                    data_start_idx = idx + 1
                    break
            
            if not header_row:
                continue

            # Process data rows for this page
            for row in table[data_start_idx:]:
                if not row:
                    continue
                
                cleaned_row = [re.sub(r'\s+', ' ', str(cell)).strip() if cell is not None else '' for cell in row]
                
                # Verify row starts with a College Code (e.g., E001, E027)
                if len(cleaned_row) >= 4 and re.match(r'^E\d{3}$', cleaned_row[0]):
                    college_code = cleaned_row[0]
                    college_name = cleaned_row[1]
                    category = cleaned_row[2]
                    
                    # Loop through all branch columns on this page
                    for col_idx in range(3, min(len(cleaned_row), len(header_row))):
                        branch_header = header_row[col_idx]
                        rank_val = cleaned_row[col_idx]
                        
                        # Only keep valid numeric cutoff ranks
                        if rank_val and rank_val.isdigit() and branch_header:
                            # Extract short branch code (e.g., 'AD' from 'AD-Artificial Intelligence')
                            branch_code = branch_header.split('-')[0].strip() if '-' in branch_header else branch_header[:4].strip()
                            
                            all_extracted_records.append({
                                'exam_type': 'COMEDK',
                                'year': 2025,
                                'college_code': college_code,
                                'college_name': college_name,
                                'category': category,
                                'branch_code': branch_code,
                                'branch_full_name': branch_header,
                                'closing_rank': int(rank_val)
                            })

    print(f"Extraction complete! Total records collected: {len(all_extracted_records)}")
    
    if all_extracted_records:
        df = pd.DataFrame(all_extracted_records)
        df.to_csv(output_csv_path, index=False)
        print(f"✅ Success! Saved {len(df)} clean cutoff records with exact branch names to '{output_csv_path}'")
    else:
        print("❌ No records extracted. Check PDF structure.")

if __name__ == "__main__":
    pdf_file = "comedk.pdf"
    csv_file = "comedk_2025_cutoffs_cleaned.csv"
    convert_comedk_pdf_to_csv(pdf_file, csv_file)