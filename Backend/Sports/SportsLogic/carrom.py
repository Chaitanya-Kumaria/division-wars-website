import pandas as pd
import os

def load_carrom_data_from_excel(excel_path, output_dir):
    """
    Load carrom data from Excel file and convert to CSV format.
    
    Args:
        excel_path: Path to carrom.xlsx file
        output_dir: Directory where CSV files should be saved
    """
    if not os.path.exists(excel_path):
        print(f"Excel file not found: {excel_path}")
        return
    
    try:
        # Read Excel file - assuming it has multiple sheets
        excel_file = pd.ExcelFile(excel_path)
        
        # Get sheet names
        sheet_names = excel_file.sheet_names
        print(f"Found sheets: {sheet_names}")
        
        # Try to map sheets to CSV files
        # Common sheet names might be: Fixtures, Results, Points, etc.
        for sheet_name in sheet_names:
            df = pd.read_excel(excel_path, sheet_name=sheet_name)
            
            # Determine output file based on sheet name
            sheet_lower = sheet_name.lower()
            if 'fixture' in sheet_lower:
                output_path = os.path.join(output_dir, 'carrom_fixtures.csv')
            elif 'result' in sheet_lower:
                output_path = os.path.join(output_dir, 'carrom_results.csv')
            elif 'point' in sheet_lower:
                output_path = os.path.join(output_dir, 'carrom_points.csv')
            else:
                # If sheet name doesn't match, save with sheet name
                output_path = os.path.join(output_dir, f'carrom_{sheet_lower}.csv')
            
            # Save to CSV
            df.to_csv(output_path, index=False)
            print(f"Converted {sheet_name} to {output_path}")
    
    except Exception as e:
        print(f"Error reading Excel file: {e}")

if __name__ == "__main__":
    # Example usage
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sports_data_dir = os.path.join(base_dir, 'Sports', 'SportsData')
    excel_path = os.path.join(sports_data_dir, 'carrom.xlsx')
    
    load_carrom_data_from_excel(excel_path, sports_data_dir)

