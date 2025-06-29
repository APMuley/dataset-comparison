import pandas as pd

# Load the CSV file
input_file = "minute_weather.csv"  # Replace with your CSV file path
df = pd.read_csv(input_file)

# Convert the 'date' column to datetime format
df['hpwren_timestamp'] = pd.to_datetime(df['hpwren_timestamp'], format="%Y-%m-%d %H:%M:%S", errors='coerce')  # Replace 'date' with your actual column name

# Drop the first two columns
df = df.iloc[:, 1:]

# Filter and save data for each year, limiting to 50 rows
for year in [2011, 2012, 2013]:
    # Filter rows where the year matches
    df_year = df[df['hpwren_timestamp'].dt.year == year]
    # Limit to the first 50 rows
    df_year = df_year.head(50)
    # Drop the 'date' column before saving
    df_year = df_year.drop(columns=['hpwren_timestamp'])
    # Save to a new file
    df_year.to_csv(f"output_{year}.csv", index=False)
