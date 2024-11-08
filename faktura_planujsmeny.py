#!/usr/bin/env python3

import sys
import pandas as pd
from dateutil.parser import parse
import datetime as dt

def main():
    if len(sys.argv) != 2:
        print("Usage: script.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]

    try:
        # Read the first table from the HTML file
        data = pd.read_html(input_file, decimal=",")[0].iloc[:-2]
    except Exception as e:
        print(f"Error reading HTML file '{input_file}': {e}")
        sys.exit(1)

    # Simplify column headers
    data.columns = data.columns.get_level_values(1)
    data = data.loc[:, ~data.columns.duplicated()]

    # Drop rows without 'Směna' information
    data.dropna(subset=['Směna'], inplace=True)

    # Extract and format dates
    current_year = dt.datetime.now().year
    data['date'] = data['Datum'].str.extract(r'(\d{1,2}\.\d{1,2}\.)')[0] + str(current_year)
    data['date'] = data['date'].apply(lambda x: parse(x, dayfirst=True))

    # Format dates as 'DD.MM.RRRR'
    data['Datum objednávky'] = data['date'].apply(lambda x: x.replace(day=1).strftime('%d.%m.%Y'))
    data['Datum vystoupení'] = data['date'].dt.strftime('%d.%m.%Y')

    # Add fixed and calculated columns
    data['Typ vystoupení / specifikace'] = '3 ceremoniály'
    data['Čas trvání min.'] = data['Délka'].str.replace(",", "").str.split().apply(
        lambda x: sum(map(float, x)) * 0.6
    )
    data['Jméno klienta'] = 'Wellness resort s.r.o.'

    # Select and rename output columns
    output_columns = [
        'Datum objednávky',
        'Datum vystoupení',
        'Typ vystoupení / specifikace',
        'Čas trvání min.',
        'Jméno klienta'
    ]
    output_data = data[output_columns]

    # Save the processed data to a CSV file
    output_filename = f"{input_file.rsplit('.', 1)[0]}.csv"
    output_data.to_csv(output_filename, index=False)
    print(f"Data successfully saved to '{output_filename}'")

if __name__ == "__main__":
    main()
