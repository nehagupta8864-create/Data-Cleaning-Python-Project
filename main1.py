import pandas as pd

# Load CSV
df = pd.read_csv("Customer_raw_data.csv")

# Save original copy
raw_df = df.copy()

# Fix column names
df.columns = df.columns.str.strip().str.lower()

print("Total rows:", len(df))


# Remove duplicates
df = df.drop_duplicates()


# Clean name
df["name"] = df["name"].astype(str).str.strip().str.title()


# Clean email
df["email"] = df["email"].astype(str).str.strip().str.lower()

df = df[df["email"].str.contains("@", na=False)]
df = df[df["email"].str.contains(".com", na=False)]


# Clean phone
df["phone"] = df["phone"].astype(str).str.strip()

df = df[df["phone"].str.isnumeric()]
df = df[df["phone"].str.len() == 10]


# Clean city
df["city"] = df["city"].astype(str).str.strip().str.title()

df["city"] = df["city"].replace("Unknown", "Not Provided")


# Remove missing
df = df.dropna()


# Save clean data
df.to_csv("clean_customer_data3.csv", index=False)


# Invalid rows detect
invalid = raw_df[~raw_df.index.isin(df.index)]

invalid.to_csv("invalid_customer_data3.csv", index=False)

# ---------------- REPORT GENERATION ---------------- #

report = {}

# Total records
report["Total Records"] = len(raw_df)

# Clean records
report["Clean Records"] = len(df)

# Invalid records
report["Invalid Records"] = len(invalid)

# Duplicates removed
report["Duplicates Removed"] = len(raw_df) - len(raw_df.drop_duplicates())

# Unique cities
report["Unique Cities"] = df["city"].nunique()

# Top cities
top_cities = df["city"].value_counts().head(5)

# Convert report dict to dataframe
report_df = pd.DataFrame(list(report.items()), columns=["Metric", "Value"])

# Save main report
report_df.to_csv("report_summary1.csv", index=False)

# Save top cities separately
top_cities.to_csv("top_cities_report.csv")

print("\nReport Generated Successfully")

# ---------------- EXCEL REPORT (ALL IN ONE) ---------------- #

with pd.ExcelWriter("customer_report.xlsx", engine="openpyxl") as writer:
    
    # Clean data
    df.to_excel(writer, sheet_name="Clean Data", index=False)
    
    # Invalid data
    invalid.to_excel(writer, sheet_name="Invalid Data", index=False)
    
    # Summary report
    report_df.to_excel(writer, sheet_name="Summary", index=False)
    
    # Top cities
    top_cities_df = top_cities.reset_index()
    top_cities_df.columns = ["City", "Count"]
    top_cities_df.to_excel(writer, sheet_name="Top Cities", index=False)

print("Excel Report Generated Successfully")

print("Cleaning completed")
print("Clean rows:", len(df))
print("Invalid rows:", len(invalid))