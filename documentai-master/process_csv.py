import pandas as pd
import os
import glob


# Function to detect relevant columns and handle renaming dynamically
def process_dynamic_csv(df):
    """
    Dynamically process the DataFrame by detecting and renaming columns,
    and handling rows safely.
    """
    # Dynamically print column names
    print("Available columns:", df.columns.tolist())

    # Drop columns dynamically if they exist
    columns_to_drop = ["Unnamed: 0", "TAX"]
    available_columns_to_drop = [col for col in columns_to_drop if col in df.columns]
    if available_columns_to_drop:
        df = df.drop(available_columns_to_drop, axis=1)

    # Dynamically rename columns if they exist
    rename_columns = {"PRICE DISCOUNT": "AMOUNT", "ITEM DESCRIPTION QTY": "ITEM DESCRIPTION"}
    available_rename_columns = {old: new for old, new in rename_columns.items() if old in df.columns}
    df.rename(columns=available_rename_columns, inplace=True)

    # Handle row operations safely
    if "ITEM DESCRIPTION" in df.columns and len(df) > 1:
        df["ITEM DESCRIPTION"].iloc[1] = df["ITEM DESCRIPTION"].iloc[0] + df["ITEM DESCRIPTION"].iloc[1]

    if "AMOUNT" in df.columns and len(df) > 1:
        df["AMOUNT"].iloc[1] = "PRICE"  # Dynamically update the "AMOUNT" column

    # Drop the first row dynamically if it exists
    if 0 in df.index:
        df = df.drop(0)

    return df


# Get the latest file in the "test" directory (or adapt this to another file as needed)
csv_files = glob.glob("test/*.csv")
latest_file = max(csv_files, key=os.path.getmtime)
print(f"Processing file: {latest_file}")

# Read the CSV file
df = pd.read_csv(latest_file)

# Process the DataFrame dynamically
df = process_dynamic_csv(df)

# Save the processed DataFrame to a new CSV file
df.to_csv("test/Invoice.csv", index=False)
print("Processed file saved as 'Invoice.csv'")

'''
import pandas as pd

df=pd.read_csv("test/page1_1.csv")
df = df.drop(["Unnamed: 0","TAX"],axis=1)
df.rename(columns={"PRICE DISCOUNT":"AMOUNT","ITEM DESCRIPTION QTY":"ITEM DESCRIPTION"},inplace=True)
df["ITEM DESCRIPTION"][1]=df["ITEM DESCRIPTION"][0]+df["ITEM DESCRIPTION"][1]
df["AMOUNT"][1]="PRICE"
df = df.drop(0)

df.to_csv("test/Invoice.csv",index=False)

'''