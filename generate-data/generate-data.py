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
num_rows = 20  # You can change this to your desired number of rows

# Generate the DataFrame
df = generate_data(num_rows)

# Save to Excel file
df.to_excel("output_file.xlsx", index=False)

print(f"Excel file 'output_file.xlsx' generated with {num_rows} rows.")
