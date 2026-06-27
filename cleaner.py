import pandas as pd
import os

def run_automated_landlord_pipeline(input_csv_path):
    print("⚡ [Stratum Analytics Engine] Initializing Raw Spreadsheet Ingestion...")
    
    # 1. Simulating an investor's raw, messy ledger data containing errors and unorganized text
    messy_data = {
        'Raw_Date': ['01/15/2026', '02/10/26', '2026-03-01', '03/12/2026'],
        'Description': ['RENT PAYMENT RECEIVED', 'Plumbing bill - leak in bathroom', 'RENT', 'Property Tax Payment - County office'],
        'Raw_Amount': ['$2,500.00', '-$350.00', '2500', '-1200.00'],
        'Tax_Status': ['Unclassified', 'Unclassified', 'Unclassified', 'Unclassified']
    }
    
    # Load into a data frame
    df = pd.DataFrame(messy_data)
    print("📋 Raw Investor Input Ingested successfully. Beginning cleaning matrix...")
    
    # 2. Automated Step: Strip out messy currency formatting text symbols ($ commas) and convert to clean decimals
    df['Cleaned_Amount'] = df['Raw_Amount'].astype(str).str.replace('$', '').str.replace(',', '')
    df['Cleaned_Amount'] = pd.to_numeric(df['Cleaned_Amount'])
    
    # 3. Automated Step: Run programmatic logic mapping rules to sort expenditures into Schedule E Tax Categories automatically
    for index, row in df.iterrows():
        desc = row['Description'].lower()
        if 'rent' in desc:
            df.at[index, 'Tax_Status'] = 'Schedule E: Gross Rents Received'
        elif 'plumbing' in desc or 'repair' in desc or 'leak' in desc:
            df.at[index, 'Tax_Status'] = 'Schedule E: Expenses - Repairs'
        elif 'tax' in desc:
            df.at[index, 'Tax_Status'] = 'Schedule E: Expenses - Taxes'
        else:
            df.at[index, 'Tax_Status'] = 'Schedule E: General Operational Overhead'
            
    # 4. Export the perfectly structured tax ready sheet back to the investor
    output_filename = "Tax_Ready_Portfolio_Ledger.csv"
    df.to_csv(output_filename, index=False)
    
    print("---")
    print("✅ [Stratum Analytics Engine] Operational Script Execution Complete!")
    print(f"📦 Messy records parsed and exported into clean corporate matrix: '{output_filename}'")
    print("---")
    print(df[['Raw_Date', 'Description', 'Cleaned_Amount', 'Tax_Status']])

if __name__ == "__main__":
    # Execute the workflow script directly
    run_automated_landlord_pipeline(input_csv_path=None)
