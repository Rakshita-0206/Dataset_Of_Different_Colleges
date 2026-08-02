import pdfplumber
import pandas as pd
import re

def parse_kcet_pdf(pdf_path, output_csv_path):
    print("Starting KEA KCET Round 1 PDF Parsing...")
    
    # KEA Standard Category Order (Rest of Karnataka PDF)
    CATEGORIES = [
        "1G", "1K", "1R", 
        "2AG", "2AK", "2AR", 
        "2BG", "2BK", "2BR", 
        "3AG", "3AK", "3AR", 
        "3BG", "3BK", "3BR", 
        "GM", "GMK", "GMR", 
        "SCG", "SCK", "SCR", 
        "STG", "STK", "STR"
    ]
    
    records = []
    
    with pdfplumber.open(pdf_path) as pdf:
        print(f"Total Pages detected: {len(pdf.pages)}")
        
        current_college_code = ""
        current_college_name = ""
        
        for page_num, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if not text:
                continue
                
            lines = text.split('\n')
            
            i = 0
            while i < len(lines):
                line = lines[i].strip()
                
                # 1. Detect College Header (e.g., "College: E001 Univesity of Visvesvaraya College of Engineering...")
                if "College:" in line or re.match(r'^E\d{3}\s', line):
                    match = re.search(r'(E\d{3})\s+([^,]+)', line)
                    if match:
                        current_college_code = match.group(1).strip()
                        current_college_name = match.group(2).strip()
                    i += 1
                    continue
                
                # 2. Skip Table Header line ("Course Name 1G 1K 1R 2AG...")
                if "Course Name" in line or "1G" in line and "GM" in line:
                    i += 1
                    continue
                
                # 3. Detect Rank Data Lines
                # A rank line ends with numeric rank values or '--' placeholders
                tokens = line.split()
                # Check if line contains rank numbers or dashes
                num_tokens = [t for t in tokens if t.replace('.', '').isdigit() or t == '--']
                
                if len(num_tokens) >= 5:  # Valid row with cutoffs
                    # Separate course text from rank values
                    course_words = []
                    rank_values = []
                    
                    for token in tokens:
                        if token.replace('.', '').isdigit() or token == '--':
                            rank_values.append(token)
                        else:
                            course_words.append(token)
                    
                    course_name = " ".join(course_words)
                    
                    # Look backwards up to 3 lines to capture multi-line course titles (e.g. "COMPUTER SCIENCE AND")
                    prev_lines_text = []
                    j = i - 1
                    while j >= 0 and j >= i - 3:
                        prev_line = lines[j].strip()
                        # If prev line is not a college header or category header or numeric row
                        if not any(k in prev_line for k in ["College:", "Course Name", "1G", "GM"]) and not re.search(r'\d{4,}', prev_line):
                            prev_lines_text.insert(0, prev_line)
                            j -= 1
                        else:
                            break
                    
                    full_course_name = " ".join(prev_lines_text + [course_name]).strip()
                    
                    # Map extracted ranks to category headers
                    for idx, rank in enumerate(rank_values):
                        if rank != '--' and idx < len(CATEGORIES):
                            # Clean numeric floats (e.g., 22042.5 -> 22042)
                            clean_rank = int(float(rank))
                            
                            records.append({
                                'exam_type': 'KCET',
                                'year': 2025,
                                'round': 1,
                                'college_code': current_college_code,
                                'college_name': current_college_name,
                                'course_name': full_course_name,
                                'category': CATEGORIES[idx],
                                'closing_rank': clean_rank
                            })
                i += 1

    print(f"Parsing complete! Total records collected: {len(records)}")
    
    if records:
        df = pd.DataFrame(records)
        df.to_csv(output_csv_path, index=False)
        print(f"✅ Success! Saved {len(df)} KCET cutoff records to '{output_csv_path}'")
    else:
        print("❌ Still 0 records. Let's inspect raw text lines.")

if __name__ == "__main__":
    parse_kcet_pdf("PROF_CODE_E_R_R1english.pdf", "kcet_2025_round1_cutoffs_cleaned.csv")