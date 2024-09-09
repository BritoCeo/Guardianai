import os
import numpy as np
import pandas as pd


# Get the latest CSV file in the directory
def get_latest_csv(directory="test"):
    csv_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.csv')]
    if csv_files:
        latest_file = max(csv_files, key=os.path.getmtime)
        print(f"Processing file: {latest_file}")
        return latest_file
    else:
        print("No CSV files found in the directory.")
        return None


# Load the CSV file dynamically
latest_file = get_latest_csv()

if latest_file:
    # Read the CSV file
    df = pd.read_csv(latest_file)

    # Display a dynamic preview of the file (first 10 rows)
    print("First 10 rows of the DataFrame:")
    print(df.head(10))

    # Dynamically print the columns of the DataFrame
    print("Available columns:")
    print(df.columns.tolist())
else:
    print("No file to process.")


'''import os

import numpy as np
import pandas as pd

df=pd.read_csv("test/page1_1.csv")


print(df.head(10))
print(df.columns)'''


