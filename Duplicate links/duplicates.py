import pandas as pd

# File paths
new_links_path = r"Scraper\articles\filtered_new_links.xlsx"
old_links_path = r"Scraper\articles\all_bulletin_links.xlsx"

# Read the new links
new_links = pd.read_excel(new_links_path)

# Read the old links
old_links = pd.read_excel(old_links_path)

# Ensure the 'date' column is properly formatted as datetime, if it exists
if 'date' in new_links.columns:
    new_links['date'] = pd.to_datetime(new_links['date'], errors='coerce')

if 'date' in old_links.columns:
    old_links['date'] = pd.to_datetime(old_links['date'], errors='coerce')

# Remove trailing slashes from the 'url' column in both dataframes
old_links['url'] = old_links['url'].str.rstrip('/')
new_links['url'] = new_links['url'].str.rstrip('/')

# Find entries in new_links that are also in old_links based on 'url' column
removed_links = new_links[new_links['url'].isin(old_links['url'])]

# Remove entries from new_links that are already in old_links based on 'url' column
filtered_new_links = new_links[~new_links['url'].isin(old_links['url'])].copy()

# Ensure 'date' column is converted to string format before saving, if it exists
if 'date' in filtered_new_links.columns:
    filtered_new_links['date'] = filtered_new_links['date'].dt.strftime('%Y-%m-%d')

# Save the filtered dataframe to a new Excel file with clickable links
output_path = r"Scraper\articles\filtered_new_links.xlsx"
with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
    filtered_new_links.to_excel(writer, index=False, sheet_name='Filtered Links')
    workbook = writer.book
    worksheet = writer.sheets['Filtered Links']
    
    # Make 'url' and 'image' columns clickable if they exist
    for col_name in ['url', 'image']:
        if col_name in filtered_new_links.columns:
            col_idx = filtered_new_links.columns.get_loc(col_name)  # Get the column index
            for row, link in enumerate(filtered_new_links[col_name], start=1):  # Start from row 1 to skip header
                if pd.notna(link):  # Check if the link is not NaN
                    worksheet.write_url(row, col_idx, link)

# Print the removed links
print(f"Filtered links saved to 'filtered_new_links.xlsx'. Number of entries after filtering: {len(filtered_new_links)}")

if not removed_links.empty:
    print(f"\nThe following {len(removed_links)} links were removed:\n")
    
    # Ensure the URLs are printed in full
    pd.set_option('display.max_colwidth', None)
    print(removed_links['url'].to_string(index=False))
else:
    print("\nNo links were removed.")




