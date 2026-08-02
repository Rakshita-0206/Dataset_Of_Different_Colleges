# College Cutoff Data and Parsers

This repository contains raw data, cleaned datasets, and Python scripts for parsing and processing engineering college cutoff data (like KCET and COMEDK). 

## Contents

- **`kcet.py`**: A Python script to extract and parse KCET engineering cutoff data from the official PDF documents.
- **`parse_comedk.py`**: A Python script to parse COMEDK cutoff data.
- **`kcet_2025_round1_cutoffs_cleaned.csv`**: The parsed and cleaned dataset of KCET 2025 Round 1 cutoffs.
- **`comedk_2025_cutoffs_cleaned.csv`**: The parsed and cleaned dataset of COMEDK 2025 cutoffs.
- **Raw PDFs**:
  - `PROF_CODE_E_R_R1english.pdf`: The official KCET cutoff document.
  - `comedk.pdf`: The official COMEDK cutoff document.

## How to run the parsers

Make sure you have the required dependencies (like `pdfplumber` and `pandas`) installed, then you can run the scripts via:

```bash
python kcet.py
python parse_comedk.py
```
