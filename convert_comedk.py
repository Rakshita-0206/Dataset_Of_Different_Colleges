import pandas as pd
import re

def main():
    # Read the raw scraped data
    df = pd.read_csv('COMEDK_2025_All_Data.csv')
    
    # Filter for Engineering Cutoff Ranks (ignoring Architecture for now, as backend ignores it anyway)
    ranks = df[(df['Section'] == 'Cutoff Rank') & (df['ExamType'] != 'Architecture')].copy()
    
    # Extract Institute and Branch from Name_Description
    ranks[['Institute', 'Branch']] = ranks['Name_Description'].str.split(r'\s*\|\s*', expand=True)
    
    # Append degree to Branch so backend _clean_branch works correctly
    ranks['Academic Program Name'] = ranks['Branch'] + " (4 Years, Bachelor of Technology)"
    
    # Extract numeric Rank from Status
    def extract_rank(status_str):
        if pd.isna(status_str):
            return None
        m = re.search(r'\d+', str(status_str))
        if m:
            return int(m.group(0))
        return None
        
    ranks['Numeric_Rank'] = ranks['Status'].apply(extract_rank)
    ranks = ranks.dropna(subset=['Numeric_Rank'])
    
    # Map COMEDK categories to Quota
    ranks['Quota'] = ranks['Category']
    
    # Hardcode Seat Type and Gender
    ranks['Seat Type'] = 'OPEN'
    ranks['Gender'] = 'Neutral'
    
    grouped = ranks.groupby(['Institute', 'Academic Program Name', 'Quota', 'Seat Type', 'Gender'])
    
    records = []
    for keys, group in grouped:
        record = {
            'Institute': keys[0],
            'Academic Program Name': keys[1],
            'Quota': keys[2],
            'Seat Type': keys[3],
            'Gender': keys[4]
        }
        
        # We will just find the final (maximum) cutoff rank across all rounds 
        # and store it in Opening_R1 and Closing_R1.
        # Note: The Disha project requires the column to be named 'Closing_R1'
        max_rank = group['Numeric_Rank'].max()
        
        if pd.notna(max_rank):
            record['Opening_R1'] = max_rank
            record['Closing_R1'] = max_rank
            records.append(record)
            
    out_df = pd.DataFrame(records)
    
    out_path = 'comedk_2025.csv'
    out_df.to_csv(out_path, index=False)
    print(f"Successfully converted data into {out_path} with only a single cutoff round!")

if __name__ == '__main__':
    main()
