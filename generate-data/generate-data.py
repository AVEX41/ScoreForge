import pandas as pd
import random


def generate_data(num_rows):
    data = {
        "id": range(1, num_rows + 1),
        "shot": [round(random.uniform(7.1, 10.9), 1) for _ in range(num_rows)],
    }

    # Correct the 'inner' column reference
    data["inner"] = [True if x >= 10.5 else False for x in data["shot"]]

    df = pd.DataFrame(data)
    return df


# Set the number of rows
num_rows = 30  # You can change this to your desired number of rows

# Generate the DataFrame
df = generate_data(num_rows)

# Save to Excel file with formatting as a table
output_file = "output_60_1.xlsx"
with pd.ExcelWriter(output_file, engine="xlsxwriter") as writer:
    df.to_excel(writer, sheet_name="Sheet1", index=False, header=True)

    # Get the xlsxwriter workbook and worksheet objects
    workbook = writer.book
    worksheet = writer.sheets["Sheet1"]

    # Get the dimensions of the DataFrame
    num_rows, num_cols = df.shape

    # Create a list of column headers to use in add_table()
    column_settings = [{"header": column} for column in df.columns]

    # Add the Excel table structure. Pandas will add the data automatically
    worksheet.add_table(0, 0, num_rows, num_cols - 1, {"columns": column_settings})

print(f"Excel file '{output_file}' generated with {num_rows} rows.")
