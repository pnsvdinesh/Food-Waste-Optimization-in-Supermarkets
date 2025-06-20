# -*- coding: utf-8 -*-
"""
Created on Thu Jun 19 12:24:43 2025

@author: ASUS
"""

import pandas as pd
 
food_data = pd.read_csv(r"C:\Users\ASUS\Desktop\Dinesh project files\Dinesh DACT Training Files\PROJECT FILES\Gigaversity project files\Food_Waste_Optimization_Supermarkets.csv")
food_data.info()

# Display the first 5 rows if the DataFrame was loaded successfully
food_data.head(5)
food_data.describe()

# identify duplicate rows
duplicate= food_data.duplicated()
sum(duplicate)

duplicate_rows = food_data[food_data.duplicated()]

# Removing Duplicate rows
food_data2 = food_data.drop_duplicates()
food_data.shape
food_data2.shape

# Drop rows where Item_Name column and Category column are nan
food_data3= food_data2.dropna(subset=['Item_Name','Category'], how = 'all')
food_data2.shape
food_data3.shape


# fill values of Item_Name based on the Item_Name and Category match in food_data3

# Identify rows with missing 'Item_Name'
missing_item_name_rows = food_data3[food_data3['Item_Name'].isnull()]

if not missing_item_name_rows.empty:
    print("\nRows with missing 'Item_Name' before filling:")
    print(missing_item_name_rows.head().to_markdown(index=False))
else:
    print("\nNo rows with missing 'Item_Name' found.")
    
# Create a mapping from Category and a non-null Item_Name to the corresponding Item_Name
# We'll group by 'Category' and 'Item_Name', then take the first valid 'Item_Name' for each group.
# This helps in case there are multiple non-null Item_Names for the same Category (though ideally there should be one canonical name).
item_name_mapping = food_data3.dropna(subset=['Item_Name']).groupby('Category')['Item_Name'].first().to_dict()

# Fill missing 'Item_Name' values based on the mapping
# We use apply and a lambda function to look up the Item_Name based on the 'Category'
food_data3['Item_Name'] = food_data3.apply(
    lambda row: item_name_mapping.get(row['Category'], row['Item_Name'])
    if pd.isnull(row['Item_Name']) else row['Item_Name'],
    axis=1
)

# Verify that missing 'Item_Name' values have been filled
missing_item_name_rows_after = food_data3[food_data3['Item_Name'].isnull()]

if not missing_item_name_rows_after.empty:
    print("\nRows with missing 'Item_Name' after filling:")
    print(missing_item_name_rows_after.head().to_markdown(index=False))
else:
    print("\nNo rows with missing 'Item_Name' found after filling.")

# Display the first few rows to show the changes
print("\nFirst 30 rows of the DataFrame after filling missing 'Item_Name':")
print(food_data3.head(30).to_markdown(index=False))



import pandas as pd
# Identify rows with missing 'Category'
missing_category_rows = food_data3[food_data3['Category'].isnull()]

if not missing_category_rows.empty:
    print("\nRows with missing 'Category' before filling:")
    print(missing_category_rows.head().to_markdown(index=False))
else:
    print("\nNo rows with missing 'Category' found.")

# Create a mapping from Item_Name to the corresponding Category
# We'll group by 'Item_Name' and take the first non-null 'Category' for each item.
category_mapping = food_data3.dropna(subset=['Category']).groupby('Item_Name')['Category'].first().to_dict()

# Fill missing 'Category' values based on the mapping
food_data3['Category'] = food_data3.apply(
    lambda row: category_mapping.get(row['Item_Name'], row['Category'])
    if pd.isnull(row['Category']) else row['Category'],
    axis=1
)

# Verify that missing 'Category' values have been filled
missing_category_rows_after = food_data3[food_data3['Category'].isnull()]

if not missing_category_rows_after.empty:
    print("\nRows with missing 'Category' after filling:")
    print(missing_category_rows_after.head().to_markdown(index=False))
else:
    print("\nNo rows with missing 'Category' found after filling.")

# Display the first few rows to show the changes
print("\nFirst 30 rows of the DataFrame after filling missing 'Category':")
print(food_data3.head(30).to_markdown(index=False))


#print Stock_Quantity null values 20  food_data3

# Identify rows with missing 'Stock_Quantity'
missing_stock_quantity_rows = food_data3[food_data3['Stock_Quantity'].isnull()]


if not missing_stock_quantity_rows.empty:
    print("\nRows with missing 'Stock_Quantity' (first 20):")
    print(missing_stock_quantity_rows.head(20).to_markdown(index=False))
else:
    print("\nNo rows with missing 'Stock_Quantity' found.")
    
    
#fill Stock_Quantity and convert negative valuesinto positive in df_cleaned by adding Waste_Quantity + Sold_Quantity in Stock_Quantity nan place if Waste_Quantity and Sold_Quantity are not nan

import pandas as pd
# Before filling 'Stock_Quantity' NaN values
print("\nShape before filling 'Stock_Quantity' NaNs:", food_data3.shape)

# Fill NaN values in 'Stock_Quantity'
# Apply the function only to rows where 'Stock_Quantity' is NaN
nan_stock_mask = food_data3['Stock_Quantity'].isnull()

# For rows where Stock_Quantity is NaN, if Waste_Quantity and Sold_Quantity are not NaN, sum them
food_data3.loc[nan_stock_mask, 'Stock_Quantity'] = food_data3.loc[nan_stock_mask].apply(
    lambda row: row['Waste_Quantity'] + row['Sold_Quantity']
    if pd.notnull(row['Waste_Quantity']) and pd.notnull(row['Sold_Quantity'])
    else row['Stock_Quantity'], # Keep the original NaN if Waste_Quantity or Sold_Quantity is NaN
    axis=1
)

# Convert negative values in 'Stock_Quantity' to positive
food_data3['Stock_Quantity'] = food_data3['Stock_Quantity'].abs()


# After filling 'Stock_Quantity' NaN values and converting negative to positive
print("Shape after filling 'Stock_Quantity' NaNs and converting negative to positive:", food_data3.shape)

# Verify that missing 'Stock_Quantity' values have been filled and negative values are now positive
missing_stock_quantity_rows_after = food_data3[food_data3['Stock_Quantity'].isnull()]

if not missing_stock_quantity_rows_after.empty:
    print("\nRows with missing 'Stock_Quantity' after filling (first 20):")
    print(missing_stock_quantity_rows_after.head(20).to_markdown(index=False))
else:
    print("\nNo rows with missing 'Stock_Quantity' found after filling.")

# Display the first few rows to show the changes
print("\nFirst 30 rows of the DataFrame after filling and correcting 'Stock_Quantity':")
print(food_data3.head(30).to_markdown(index=False))

# Check for any remaining negative values in 'Stock_Quantity'
negative_stock_values = food_data3[food_data3['Stock_Quantity'] < 0]

if not negative_stock_values.empty:
    print("\nRows with negative 'Stock_Quantity' after correction:")
    print(negative_stock_values.head().to_markdown(index=False))
else:
    print("\nNo negative 'Stock_Quantity' values found after correction.")  
    
    
#print rows count from df_cleaned where Stock_Quantity and Waste_Quantity are nan and print rows also

# Filter rows where both 'Stock_Quantity' and 'Waste_Quantity' are NaN
nan_stock_waste_rows = food_data3[food_data3['Stock_Quantity'].isnull() & food_data3['Waste_Quantity'].isnull()]

# Print the count of such rows
print(f"\nNumber of rows where 'Stock_Quantity' and 'Waste_Quantity' are NaN: {len(nan_stock_waste_rows)}")

# Print the rows themselves
if not nan_stock_waste_rows.empty:
    print("\nRows where 'Stock_Quantity' and 'Waste_Quantity' are NaN:")
    print(nan_stock_waste_rows.to_markdown(index=False))
else:
    print("\nNo rows found where both 'Stock_Quantity' and 'Waste_Quantity' are NaN.")
    


# F delete rows count from food_data3 where Stock_Quantity and Waste_Quantity are nan and print rows also.print shape befoer and after

# Print shape before deletion
print("Shape before deleting rows with NaN in 'Stock_Quantity' and 'Waste_Quantity':", food_data3.shape)

# Delete rows where both 'Stock_Quantity' and 'Waste_Quantity' are NaN
food_data4 = food_data3.dropna(subset=['Stock_Quantity', 'Waste_Quantity'], how='all')

# Print shape after deletion
print("Shape after deleting rows with NaN in 'Stock_Quantity' and 'Waste_Quantity':", food_data4.shape)

# Verify that these rows have been deleted
nan_stock_waste_rows_after = food_data4[food_data4['Stock_Quantity'].isnull() & food_data4['Waste_Quantity'].isnull()]

if not nan_stock_waste_rows_after.empty:
    print("\nRows where 'Stock_Quantity' and 'Waste_Quantity' are still NaN after deletion:")
    print(nan_stock_waste_rows_after.to_markdown(index=False))
else:
    print("\nNo rows found where both 'Stock_Quantity' and 'Waste_Quantity' are NaN after deletion.")

# Display the first few rows of the cleaned DataFrame
print("\nFirst 30 rows of the DataFrame after deleting rows with NaN in 'Stock_Quantity' and 'Waste_Quantity':")
print(food_data4.head(30).to_markdown(index=False))



# : if 4th column and 6th column are nan then fill with 0. or if 6 th column is 0 and 4th and 5th are not 0 then fill 6th column = 4thcolumn - 5thcolumn and convrt it to positive value .
# print row count where both 4th column and 5th column are nan before and after filling

import pandas as pd
# Before filling NaN and performing calculations
initial_nan_stock_sold = food_data4[food_data4['Stock_Quantity'].isnull() & food_data4['Sold_Quantity'].isnull()]
print(f"\nInitial count of rows where 'Stock_Quantity' and 'Sold_Quantity' are NaN: {len(initial_nan_stock_sold)}")


# Apply the filling and calculation logic
def fill_and_calculate_quantities(row):
    # Fill NaN in 'Stock_Quantity' and 'Sold_Quantity' with 0 if both are NaN
    if pd.isnull(row['Stock_Quantity']) and pd.isnull(row['Sold_Quantity']):
        row['Stock_Quantity'] = 0
        row['Sold_Quantity'] = 0

    # If 'Sold_Quantity' is 0 and 'Stock_Quantity' and 'Waste_Quantity' are not 0,
    # calculate 'Sold_Quantity' and convert to positive
    if row['Sold_Quantity'] == 0 and pd.notnull(row['Stock_Quantity']) and pd.notnull(row['Waste_Quantity']):
        row['Sold_Quantity'] = abs(row['Stock_Quantity'] - row['Waste_Quantity'])

    return row

# Apply the function row-wise
food_data4 = food_data4.apply(fill_and_calculate_quantities, axis=1)

# After filling and performing calculations
final_nan_stock_sold = food_data4[food_data4['Stock_Quantity'].isnull() & food_data4['Sold_Quantity'].isnull()]
print(f"Final count of rows where 'Stock_Quantity' and 'Sold_Quantity' are NaN: {len(final_nan_stock_sold)}")

# Display the first few rows to show the changes
print("\nFirst 30 rows of the DataFrame after filling and calculating quantities:")
print(food_data4.head(30).to_markdown(index=False))

print(food_data4.shape)


# : fill Sold_Quantity in food_data4 where Sold_Quantity is nan or 0  .fill by Sold_Quantity = Waste_Quantity - Stock_Quantity . make all values of Sold_Quantity positive

import pandas as pd
# Identify rows where 'Sold_Quantity' is NaN or 0
sold_quantity_mask = food_data4['Sold_Quantity'].isnull() | (food_data4['Sold_Quantity'] == 0)

# Apply the formula only to rows where 'Sold_Quantity' is NaN or 0
# Ensure 'Waste_Quantity' and 'Stock_Quantity' are not NaN for calculation
food_data4.loc[sold_quantity_mask, 'Sold_Quantity'] = food_data4.loc[sold_quantity_mask].apply(
    lambda row: row['Waste_Quantity'] - row['Stock_Quantity']
    if pd.notnull(row['Waste_Quantity']) and pd.notnull(row['Stock_Quantity'])
    else row['Sold_Quantity'], # Keep the original value (NaN or 0) if components are NaN
    axis=1
)

# Make all values in 'Sold_Quantity' positive by taking the absolute value
food_data4['Sold_Quantity'] = food_data4['Sold_Quantity'].abs()

# Display the first few rows to show the changes
print("\nFirst 30 rows of the DataFrame after filling and correcting 'Sold_Quantity':")
print(food_data4.head(30).to_markdown(index=False))

# Check for any remaining NaN values in 'Sold_Quantity' in the original mask locations
remaining_nan_sold_quantity = food_data4.loc[sold_quantity_mask, 'Sold_Quantity'].isnull()

if remaining_nan_sold_quantity.any():
    print("\nRows with remaining NaN 'Sold_Quantity' after filling:")
    print(food_data4.loc[sold_quantity_mask & remaining_nan_sold_quantity].to_markdown(index=False))
else:
    print("\nNo remaining NaN 'Sold_Quantity' values in the locations that were initially NaN or 0.")

# Check for any negative values in 'Sold_Quantity' after correction
negative_sold_values = food_data4[food_data4['Sold_Quantity'] < 0]

if not negative_sold_values.empty:
    print("\nRows with negative 'Sold_Quantity' after correction:")
    print(negative_sold_values.head().to_markdown(index=False))
else:
    print("\nNo negative 'Sold_Quantity' values found after correction.")
    
    
# : count rows where 5 and 6th column are nan

# Check if columns with index 5 and 6 exist (0-based indexing)
if food_data4.shape[1] > 6:
  # Count rows where both the 5th and 6th columns are NaN
  # We need to get the column names corresponding to index 5 and 6
  col_name_5 = food_data4.columns[4]
  col_name_6 = food_data4.columns[5]

  nan_count_col5_col6 = food_data4[food_data4[col_name_5].isnull() & food_data4[col_name_6].isnull()].shape[0]

  print(f"\nNumber of rows where both column '{col_name_5}' and column '{col_name_6}' (indices 4 and 5) are NaN: {nan_count_col5_col6}")
else:
  print("\nDataFrame does not have columns at index 4 and 5.")
  
  
# : delete rows where 5 and 6th column are nan

# Identify rows where both the 5th and 6th columns are NaN (using 0-based indexing)
# We need to ensure the DataFrame has enough columns first.
if food_data4.shape[1] > 5: # Check if column index 5 exists (which is the 6th column)
  # Get the names of the 5th and 6th columns
  col_index_4_name = food_data4.columns[4] # 5th column
  col_index_5_name = food_data4.columns[5] # 6th column

  # Before dropping rows
  print(f"\nShape before dropping rows where both '{col_index_4_name}' and '{col_index_5_name}' are NaN:", food_data4.shape)

  # Drop rows where both the 5th and 6th columns are NaN
  food_data4 = food_data4.dropna(subset=[col_index_4_name, col_index_5_name], how='all')

  # After dropping rows
  print(f"Shape after dropping rows where both '{col_index_4_name}' and '{col_index_5_name}' are NaN:", food_data4.shape)

  # Display the first few rows to verify
  print(f"\nFirst 30 rows of the DataFrame after removing rows with NaN in both '{col_index_4_name}' and '{col_index_5_name}':")
  print(food_data4.head(30).to_markdown(index=False))
else:
  print("\nDataFrame does not have at least 6 columns, cannot check columns at index 4 and 5.")
  
  

# : fill Waste_Quantity in df_cleaned where Waste_Quantity is nan by Stock_Quantity - Sold_Quantity

# Identify rows where Waste_Quantity is NaN and both Stock_Quantity and Sold_Quantity are not NaN
mask_waste_quantity = food_data4['Waste_Quantity'].isnull() & food_data4['Stock_Quantity'].notnull() & food_data4['Sold_Quantity'].notnull()

# Fill the NaN values in Waste_Quantity for the rows identified by the mask
# Ensure the values are treated as numbers before subtraction
food_data4.loc[mask_waste_quantity, 'Waste_Quantity'] = food_data4.loc[mask_waste_quantity, 'Stock_Quantity'].astype(float) - food_data4.loc[mask_waste_quantity, 'Sold_Quantity'].astype(float)

# Ensure Waste_Quantity is not negative (assuming quantity wasted cannot be negative)
food_data4.loc[mask_waste_quantity & (food_data4['Waste_Quantity'] < 0), 'Waste_Quantity'] = 0


# Verify that missing 'Waste_Quantity' values have been filled where possible
missing_waste_quantity_rows_after = food_data4[food_data4['Waste_Quantity'].isnull()]

if not missing_waste_quantity_rows_after.empty:
    print("\nRows with missing 'Waste_Quantity' after filling (first 20):")
    print(missing_waste_quantity_rows_after.head(20).to_markdown(index=False))
else:
    print("\nNo rows with missing 'Waste_Quantity' found after filling based on the calculation.")

# Display the first few rows to show the changes
print("\nFirst 30 rows of the DataFrame after filling missing 'Waste_Quantity':")
print(food_data4.head(300).to_markdown(index=False))


# : delete rows where 5 and 6 columns are nan

# Get the names of columns at index 5 and 6
col5_name = food_data4.columns[4]
col6_name = food_data4.columns[5]

print(f"\nColumns at index 5 ('{col5_name}') and 6 ('{col6_name}').")

# Before dropping rows where both columns 5 and 6 are NaN
print("Shape before dropping rows with NaN in both columns 5 and 6:", food_data4.shape)

# Drop rows where both column at index 5 and column at index 6 are NaN
# We need to use the actual column names for this
food_data4 = food_data4.dropna(subset=[col5_name, col6_name], how='all')

# After dropping rows
print("Shape after dropping rows with NaN in both columns 5 and 6:", food_data4.shape)

# Display the first few rows of the cleaned DataFrame to verify
print("\nFirst 30 rows of the DataFrame after removing rows with NaN in both columns 5 and 6:")
print(food_data4.head(30).to_markdown(index=False))


# : count rows if 4th column and 5th column are nan

# Get the names of the 4th and 5th columns (0-based index 3 and 4)
col4_name = food_data4.columns[3]
col5_name = food_data4.columns[4]

# Count rows where both the 4th and 5th columns are NaN
nan_count_col4_col5 = food_data4[food_data4[col4_name].isnull() & food_data4[col5_name].isnull()].shape[0]

print(f"\nNumber of rows where both column '{col4_name}' and column '{col5_name}' (indices 3 and 4) are NaN: {nan_count_col4_col5}")



# : fill 7th column nan values by other matching the other column values that occured already

import pandas as pd
# Assuming 'Selling_Price' is the 7th column (index 6)
seventh_column_name = food_data4.columns[6] # Get the name of the 7th column

# Identify rows where the 7th column is NaN
nan_seventh_column_mask = food_data4[seventh_column_name].isnull()

# Identify columns to use for matching. Let's assume 'Item_Name' and 'Category'
# are good identifiers for matching.
matching_columns = ['Item_Name', 'Category']

# Create a mapping from the unique combinations of matching_columns
# to the first non-null value in the 7th column for that combination.
# We drop rows where the 7th column is NaN before creating the mapping
seventh_column_mapping = food_data4.dropna(subset=[seventh_column_name]).groupby(matching_columns)[seventh_column_name].first().to_dict()

# Before filling
print(f"\nNumber of NaN values in '{seventh_column_name}' before filling: {food_data4[seventh_column_name].isnull().sum()}")

# Fill NaN values in the 7th column based on the mapping
# We iterate through the rows where the 7th column is NaN
for index, row in food_data4[nan_seventh_column_mask].iterrows():
  # Create a key for the mapping from the values in matching_columns
  # Ensure the values are hashable (convert lists/arrays if necessary, though pandas series values usually are)
  # Handle potential NaN values in matching_columns by converting them to a string representation or skipping
  matching_key_parts = [str(row[col]) if pd.notnull(row[col]) else 'NaN' for col in matching_columns]
  matching_key = tuple(matching_key_parts)

  # Look up the corresponding value in the mapping
  if matching_key in seventh_column_mapping:
    # Fill the NaN value in the original DataFrame
    food_data4.loc[index, seventh_column_name] = seventh_column_mapping[matching_key]

# After filling
print(f"Number of NaN values in '{seventh_column_name}' after filling by matching: {food_data4[seventh_column_name].isnull().sum()}")

# Display the first few rows to show the changes
print(f"\nFirst 30 rows of the DataFrame after filling missing '{seventh_column_name}':")
print(food_data4.head(30).to_markdown(index=False))


# : fill 4th column if 4th column is 0 by adding 5th column and 6th column

import pandas as pd
# Assuming the 4th column is at index 3 (0-based indexing)
col_index_to_fill = 3

# Assuming the 5th column is at index 4
col_index_add1 = 4

# Assuming the 6th column is at index 5
col_index_add2 = 5

# Get the names of the relevant columns
col_to_fill_name = food_data4.columns[col_index_to_fill]
col_add1_name = food_data4.columns[col_index_add1]
col_add2_name = food_data4.columns[col_index_add2]

print(f"\nFilling column '{col_to_fill_name}' (index {col_index_to_fill}) if its value is 0, by adding columns '{col_add1_name}' (index {col_index_add1}) and '{col_add2_name}' (index {col_index_add2}).")

# Ensure the columns to be added are numeric. Coerce errors to NaN.
food_data4[col_add1_name] = pd.to_numeric(food_data4[col_add1_name], errors='coerce')
food_data4[col_add2_name] = pd.to_numeric(food_data4[col_add2_name], errors='coerce')

# Identify rows where the 4th column is 0
mask_fill_zeros = food_data4[col_to_fill_name] == 0

# Apply the fill logic only to the rows identified by the mask
# We use .loc to assign values based on the mask and index
# We ensure that the columns being added are not NaN before adding them
food_data4.loc[mask_fill_zeros, col_to_fill_name] = food_data4.loc[mask_fill_zeros].apply(
    lambda row: row[col_add1_name] + row[col_add2_name]
    if pd.notnull(row[col_add1_name]) and pd.notnull(row[col_add2_name])
    else row[col_to_fill_name], # Keep the original 0 if components are NaN
    axis=1
)

# Display the first few rows to show the changes
print(f"\nFirst 30 rows of the DataFrame after filling 0s in column '{col_to_fill_name}':")
print(food_data4.head(900).to_markdown(index=False))


# : shape

food_data4.shape


# : in 7th column make all values as positive numbers and delete rows if 7th column is 0

# Make all values in the 7th column positive
food_data4[seventh_column_name] = food_data4[seventh_column_name].abs()

# Before dropping rows where the 7th column is 0
print(f"\nShape before dropping rows where '{seventh_column_name}' is 0: {food_data4.shape}")

# Drop rows where the 7th column is 0
food_data4 = food_data4[food_data4[seventh_column_name] != 0]

# After dropping rows
print(f"Shape after dropping rows where '{seventh_column_name}' is 0: {food_data4.shape}")

# Display the first few rows to verify
print(f"\nFirst 30 rows of the DataFrame after making '{seventh_column_name}' positive and dropping rows where it's 0:")
print(food_data4.head(30).to_markdown(index=False))

# Check if there are any non-positive values in the 7th column (should only be positive now)
non_positive_seventh_column = food_data4[food_data4[seventh_column_name] <= 0]

if not non_positive_seventh_column.empty:
    print(f"\nRows with non-positive values in '{seventh_column_name}' after processing:")
    print(non_positive_seventh_column.head().to_markdown(index=False))
else:
    print(f"\nNo non-positive values found in '{seventh_column_name}' after processing.")
    

# : fill Manufacture_Date  whre Manufacture_Date   is nan Manufacture_Date   = Expiry_Date - Manufacture_Date by for same Item_Name and Category    .dont print time

import pandas as pd
# Convert 'Manufacture_Date' and 'Expiry_Date' to datetime objects
food_data4['Manufacture_Date'] = pd.to_datetime(food_data4['Manufacture_Date'], errors='coerce')
food_data4['Expiry_Date'] = pd.to_datetime(food_data4['Expiry_Date'], errors='coerce')

# Identify rows where 'Manufacture_Date' is NaN
nan_manufacture_date_mask = food_data4['Manufacture_Date'].isnull()

# Iterate through the rows where 'Manufacture_Date' is NaN
for index in food_data4[nan_manufacture_date_mask].index:
    item_name = food_data4.loc[index, 'Item_Name']
    category = food_data4.loc[index, 'Category']
    expiry_date = food_data4.loc[index, 'Expiry_Date']

# Check if Expiry_Date is not NaN for this row
if pd.notnull(expiry_date):
 # Find rows with the same Item_Name and Category where Manufacture_Date is NOT NaN
      matching_rows = food_data4[
            (food_data4['Item_Name'] == item_name) &
            (food_data4['Category'] == category) &
            food_data4['Manufacture_Date'].notnull() &
            food_data4['Expiry_Date'].notnull() # Ensure Expiry_Date is also not null for calculation
        ]

if not matching_rows.empty:
 # Calculate the time difference for the matching rows
 # We can take the average difference or the first difference found
 time_difference = (matching_rows['Expiry_Date'] - matching_rows['Manufacture_Date']).mean()

 # Fill the NaN Manufacture_Date for the current row
 # Subtract the calculated time difference from the Expiry_Date
 food_data4.loc[index, 'Manufacture_Date'] = expiry_date - time_difference

# Convert the dates back to string format without the time component if desired,
# or keep them as datetime objects and format later for display.
# To remove time:
food_data4['Manufacture_Date'] = food_data4['Manufacture_Date'].dt.date
food_data4['Expiry_Date'] = food_data4['Expiry_Date'].dt.date



# Verify if there are still missing 'Manufacture_Date' values
remaining_nan_manufacture = food_data4[food_data4['Manufacture_Date'].isnull()]

if not remaining_nan_manufacture.empty:
    print("\nRows with remaining missing 'Manufacture_Date' after filling:")
    print(remaining_nan_manufacture.head().to_markdown(index=False))
else:
    print("\nAll possible 'Manufacture_Date' values have been filled.")
    

# : delete rows where Manufacture_Date   and Expiry_Date is NaT

# Before dropping rows where 'Manufacture_Date' and 'Expiry_Date' are both NaT
print("\nShape before dropping rows where 'Manufacture_Date' and 'Expiry_Date' are both NaT:", food_data4.shape)

# Drop rows where both 'Manufacture_Date' and 'Expiry_Date' are NaT
food_data4 = food_data4.dropna(subset=['Manufacture_Date', 'Expiry_Date'], how='all')

# After dropping rows
print("Shape after dropping rows where 'Manufacture_Date' and 'Expiry_Date' are both NaT:", food_data4.shape)

# Display the first few rows of the cleaned DataFrame to verify
print("\nFirst 30 rows of the DataFrame after removing rows with NaT in both 'Manufacture_Date' and 'Expiry_Date':")
print(food_data4.head(127).to_markdown(index=False))

food_data4.shape


# : delete rows where 4th and 5th column are nan

# Identify the column names for the 4th and 5th columns (0-indexed)
col4_name = food_data4.columns[3]
col5_name = food_data4.columns[4]

print(f"\nColumns at index 4 ('{col4_name}') and 5 ('{col5_name}').")

# Before dropping rows where both columns 4 and 5 are NaN
print("Shape before dropping rows with NaN in both columns 4 and 5:", food_data4.shape)

# Drop rows where both column at index 4 and column at index 5 are NaN
# We need to use the actual column names for this
food_data4 = food_data4.dropna(subset=[col4_name, col5_name], how='all')

# After dropping rows
print("Shape after dropping rows with NaN in both columns 4 and 5:", food_data4.shape)

# Display the first few rows of the cleaned DataFrame to verify
print("\nFirst 30 rows of the DataFrame after removing rows with NaN in both columns 4 and 5:")
print(food_data4.head(30).to_markdown(index=False))

food_data4.shape


# : fill   Expiry_Date is nan     Expiry_Date = Expiry_Date - Manufacture_Date by for same Item_Name and Category    .dont print time

import pandas as pd
# Convert 'Manufacture_Date' and 'Expiry_Date' to datetime objects if they are not already
# This step is important if previous operations converted them to string or date objects
food_data4['Manufacture_Date'] = pd.to_datetime(food_data4['Manufacture_Date'], errors='coerce')
food_data4['Expiry_Date'] = pd.to_datetime(food_data4['Expiry_Date'], errors='coerce')

# Identify rows where 'Expiry_Date' is NaN (or NaT after conversion)
nan_expiry_date_mask = food_data4['Expiry_Date'].isnull()

# Iterate through the rows where 'Expiry_Date' is NaN
for index in food_data4[nan_expiry_date_mask].index:
    item_name = food_data4.loc[index, 'Item_Name']
    category = food_data4.loc[index, 'Category']
    manufacture_date = food_data4.loc[index, 'Manufacture_Date']

 # Check if Manufacture_Date is not NaN for this row
   if pd.notnull(manufacture_date):
 # Find rows with the same Item_Name and Category where Expiry_Date is NOT NaN
        matching_rows = food_data4[
            (food_data4['Item_Name'] == item_name) &
            (food_data4['Category'] == category) &
            food_data4['Expiry_Date'].notnull() &
            food_data4['Manufacture_Date'].notnull() # Ensure Manufacture_Date is also not null for calculation
        ]

        if not matching_rows.empty:
            # Calculate the time difference (Shelf Life) for the matching rows
            # We can take the average difference or the first difference found
            # Ensure subtraction results in Timedelta
            time_difference = (matching_rows['Expiry_Date'] - matching_rows['Manufacture_Date']).mean()

            # Fill the NaN Expiry_Date for the current row
            # Add the calculated time difference to the Manufacture_Date
            food_data4.loc[index, 'Expiry_Date'] = manufacture_date + time_difference

# Convert the dates to date objects to remove the time component
food_data4['Manufacture_Date'] = food_data4['Manufacture_Date'].dt.date
food_data4['Expiry_Date'] = food_data4['Expiry_Date'].dt.date

# Verify if there are still missing 'Expiry_Date' values in the rows we attempted to fill
remaining_nan_expiry = food_data4.loc[nan_expiry_date_mask][food_data4.loc[nan_expiry_date_mask, 'Expiry_Date'].isnull()]

if not remaining_nan_expiry.empty:
    print("\nRows with remaining missing 'Expiry_Date' after filling:")
    print(remaining_nan_expiry.head().to_markdown(index=False))
else:
    print("\nAll possible 'Expiry_Date' values have been filled.")

# Display the first 30 rows to show the changes
print("\nFirst 30 rows of the DataFrame after filling missing 'Expiry_Date':")
print(food_data4.head(37).to_markdown(index=False))

food_data4.shape


# : print rows if 1 to 10 coluns are nan or blank or 0

# Select columns from index 0 to 9 (inclusive, which are the first 10 columns)
cols_to_check = food_data4.columns[0:10]

# Create a mask where ALL of the selected columns are NaN, blank, or 0
# Use .isin(['', 0]) for blank strings and 0, and .isnull() for NaN
# Combine these conditions with | (OR) within each column check
condition_nan_blank_0 = food_data4[cols_to_check].apply(
    lambda col: col.isnull() | col.isin(['', 0])
).all(axis=1)

# Filter the DataFrame to get the rows that satisfy the condition
rows_to_print = food_data4[condition_nan_blank_0]

# Print the shape of the filtered DataFrame
print(f"\nShape of rows where columns 1 to 10 are NaN, blank, or 0: {rows_to_print.shape}")

# Print the rows
if not rows_to_print.empty:
    print("\nRows where columns 1 to 10 are NaN, blank, or 0:")
    print(rows_to_print.to_markdown(index=False))
else:
    print("\nNo rows found where columns 1 to 10 are all NaN, blank, or 0.")
    

# : print 300 rows

print("\nFirst 300 rows of the DataFrame after filling missing 'Waste_Quantity':")
print(food_data4.head(300).to_markdown(index=False))


# : count  the 10th column nan values

# Get the name of the 10th column (0-based index 9)
if food_data4.shape[1] > 9:
  col10_name = food_data4.columns[9]

# Count the number of NaN values in the 10th column
 nan_count_col10 = food_data4[col10_name].isnull().sum()

  print(f"\nNumber of NaN values in the 10th column ('{col10_name}'): {nan_count_col10}")
else:
  print("\nDataFrame does not have a 10th column.")
  
  

# : fill 10th column nan values by other matching the other column values that occured already

import pandas as pd
# Ensure the DataFrame has at least 10 columns (index 9)
if food_data4.shape[1] > 9:
  col10_name = food_data4.columns[9] # The 10th column (index 9)

# Identify rows where the 10th column is NaN
 nan_col10_mask = food_data4[col10_name].isnull()

# Create a mapping from 'Item_Name' to the first non-null value found in the 10th column
# This assumes 'Item_Name' is the relevant column to match on. Adjust if needed.
# Filter out rows where the 10th column is NaN before creating the mapping
col10_mapping = food_data4[food_data4[col10_name].notnull()].groupby('Item_Name')[col10_name].first().to_dict()

# Fill NaN values in the 10th column based on the mapping
# Use apply to look up the value based on 'Item_Name' for rows where the 10th column is NaN
  food_data4.loc[nan_col10_mask, col10_name] = food_data4.loc[nan_col10_mask].apply(
      lambda row: col10_mapping.get(row['Item_Name'], row[col10_name])
      if pd.isnull(row[col10_name]) else row[col10_name],
      axis=1
  )

  # Verify if there are still missing values in the 10th column after filling
  nan_count_col10_after = food_data4[col10_name].isnull().sum()
  print(f"\nNumber of NaN values in the 10th column ('{col10_name}') after filling: {nan_count_col10_after}")

  # Display the first 30 rows to show the changes
  print("\nFirst 30 rows of the DataFrame after filling 10th column NaNs:")
  print(food_data4.head(32).to_markdown(index=False))
else:
  print("\nDataFrame does not have a 10th column (index 9) to fill.")
  
  

# : count  the 10th column nan values

# Count the number of NaN values in the 10th column (index 9)
if food_data4.shape[1] > 9:
  col10_name = food_data4.columns[9]
  nan_count_col10 = food_data4[col10_name].isnull().sum()
  print(f"\nNumber of NaN values in the 10th column ('{col10_name}'): {nan_count_col10}")
else:
  print("\nDataFrame does not have a 10th column.")
  
  

# : count  the 11th column nan values

# Check if the DataFrame has at least 11 columns (index 10)
if food_data4.shape[1] > 10:
  col11_name = food_data4.columns[10] # The 11th column (index 10)

# Count the number of NaN values in the 11th column
nan_count_col11 = food_data4[col11_name].isnull().sum()

  print(f"\nNumber of NaN values in the 11th column ('{col11_name}'): {nan_count_col11}")
else:
  print("\nDataFrame does not have an 11th column (index 10).")
  
  

# : fill 11th column nan values by other matching the other column values that occured already

import pandas as pd
# Ensure the DataFrame has at least 11 columns (index 10)
if food_data4.shape[1] > 10:
  col11_name = food_data4.columns[10] # The 11th column (index 10)

# Identify rows where the 11th column is NaN
nan_col11_mask = food_data4[col11_name].isnull()

# Create a mapping from 'Item_Name' to the first non-null value found in the 11th column
# This assumes 'Item_Name' is the relevant column to match on. Adjust if needed.
# Filter out rows where the 11th column is NaN before creating the mapping
col11_mapping = food_data4[food_data4[col11_name].notnull()].groupby('Item_Name')[col11_name].first().to_dict()

# Fill NaN values in the 11th column based on the mapping
# Use apply to look up the value based on 'Item_Name' for rows where the 11th column is NaN
  food_data4.loc[nan_col11_mask, col11_name] = food_data4.loc[nan_col11_mask].apply(
      lambda row: col11_mapping.get(row['Item_Name'], row[col11_name])
      if pd.isnull(row[col11_name]) else row[col11_name],
      axis=1
  )

  # Verify if there are still missing values in the 11th column after filling
  nan_count_col11_after = food_data4[col11_name].isnull().sum()
  print(f"\nNumber of NaN values in the 11th column ('{col11_name}') after filling: {nan_count_col11_after}")

  # Display the first 30 rows to show the changes
  print("\nFirst 30 rows of the DataFrame after filling 11th column NaNs:")
  print(food_data4.head(30).to_markdown(index=False))
else:
  print("\nDataFrame does not have an 11th column (index 10) to fill.")
  
  

# : count  the 11th column nan values

# Count the number of NaN values in the 11th column (index 10)
if food_data4.shape[1] > 10:
  col11_name = food_data4.columns[10]
  nan_count_col11 = food_data4[col11_name].isnull().sum()
  print(f"\nNumber of NaN values in the 11th column ('{col11_name}'): {nan_count_col11}")
else:
  print("\nDataFrame does not have an 11th column.")
  
  
# : print 300 rows

print("\nFirst 300 rows of the DataFrame:")
print(food_data4.head(300).to_markdown(index=False))


# : count  the 12th column nan values

# Check if the DataFrame has at least 12 columns (index 11)
if food_data4.shape[1] > 11:
  col12_name = food_data4.columns[11] # The 12th column (index 11)

# Count the number of NaN values in the 12th column
nan_count_col12 = food_data4[col12_name].isnull().sum()

  print(f"\nNumber of NaN values in the 12th column ('{col12_name}'): {nan_count_col12}")
else:
  print("\nDataFrame does not have a 12th column (index 11).")
  
  


# : fill 12th column nan values by other matching the other column values that occured already

import pandas as pd
# Check if the DataFrame has at least 12 columns (index 11)
if food_data4.shape[1] > 11:
  col12_name = food_data4.columns[11] # The 12th column (index 11)

# Count the number of NaN values in the 12th column
nan_count_col12 = food_data4[col12_name].isnull().sum()

  print(f"\nNumber of NaN values in the 12th column ('{col12_name}'): {nan_count_col12}")
else:
  print("\nDataFrame does not have a 12th column (index 11).")

# Ensure the DataFrame has at least 12 columns (index 11)
if food_data4.shape[1] > 11:
  col12_name = food_data4.columns[11] # The 12th column (index 11)

# Identify rows where the 12th column is NaN
nan_col12_mask = food_data4[col12_name].isnull()

# Create a mapping from 'Item_Name' to the first non-null value found in the 12th column
# This assumes 'Item_Name' is the relevant column to match on. Adjust if needed.
# Filter out rows where the 12th column is NaN before creating the mapping
col12_mapping = food_data4[food_data4[col12_name].notnull()].groupby('Item_Name')[col12_name].first().to_dict()

# Fill NaN values in the 12th column based on the mapping
# Use apply to look up the value based on 'Item_Name' for rows where the 12th column is NaN
food_data4.loc[nan_col12_mask, col12_name] = food_data4.loc[nan_col12_mask].apply(
      lambda row: col12_mapping.get(row['Item_Name'], row[col12_name])
      if pd.isnull(row[col12_name]) else row[col12_name],
      axis=1
  )
  
 # Verify if there are still missing values in the 12th column after filling
  nan_count_col12_after = food_data4[col12_name].isnull().sum()
  print(f"\nNumber of NaN values in the 12th column ('{col12_name}') after filling: {nan_count_col12_after}")

# Display the first 30 rows to show the changes
  print("\nFirst 30 rows of the DataFrame after filling 12th column NaNs:")
  print(food_data4.head(30).to_markdown(index=False))
else:
  print("\nDataFrame does not have a 12th column (index 11) to fill.")

# Count the number of NaN values in the 12th column (index 11) after the operation
if food_data4.shape[1] > 11:
  col12_name = food_data4.columns[11]
  nan_count_col12 = food_data4[col12_name].isnull().sum()
  print(f"\nNumber of NaN values in the 12th column ('{col12_name}') after operation: {nan_count_col12}")
else:
  print("\nDataFrame does not have a 12th column.")
  
  
  
# : count  the 12th column nan values

# Count the number of NaN values in the 12th column (index 11)
if food_data4.shape[1] > 11:
  col12_name = food_data4.columns[11] # The 12th column (index 11)

  # Count the number of NaN values in the 12th column
  nan_count_col12 = food_data4[col12_name].isnull().sum()

  print(f"\nNumber of NaN values in the 12th column ('{col12_name}'): {nan_count_col12}")
else:
  print("\nDataFrame does not have a 12th column (index 11).")
  
food_data4.shape



# : fill 13th column nan values by 10th column matching  values that occured already

# Ensure the DataFrame has at least 13 columns (index 12) and 10 columns (index 9)
if food_data4.shape[1] > 12 and food_data4.shape[1] > 9:
  col13_name = food_data4.columns[12] # The 13th column (index 12)
  col10_name = food_data4.columns[9]  # The 10th column (index 9)

# Before filling NaN values in the 13th column
 print(f"\nNumber of NaN values in the 13th column ('{col13_name}') before filling: {food_data4[col13_name].isnull().sum()}")

# Create a mapping from the 10th column to the first non-null value found in the 13th column
# This mapping is created from rows where the 13th column is NOT NaN
# We use .drop_duplicates() to handle cases where multiple rows have the same 10th column value
# but potentially different 13th column values (though .first() already handles this)
col13_mapping = food_data4.dropna(subset=[col13_name]).set_index(col10_name)[col13_name].to_dict()

# Identify rows where the 13th column is NaN
nan_col13_mask = food_data4[col13_name].isnull()

# Fill NaN values in the 13th column based on the mapping from the 10th column
# Use map to look up the value based on the 10th column for rows where the 13th column is NaN
 food_data4.loc[nan_col13_mask, col13_name] = food_data4.loc[nan_col13_mask, col10_name].map(col13_mapping)

# Verify if there are still missing values in the 13th column after filling
nan_count_col13_after = food_data4[col13_name].isnull().sum()
print(f"\nNumber of NaN values in the 13th column ('{col13_name}') after filling: {nan_count_col13_after}")

# Display the first 30 rows to show the changes
  print("\nFirst 30 rows of the DataFrame after filling 13th column NaNs:")
  print(food_data4.head(30).to_markdown(index=False))
else:
  print("\nDataFrame does not have both a 10th column (index 9) and a 13th column (index 12) to perform the filling.")

# Count the number of NaN values in the 13th column (index 12) after the operation
if food_data4.shape[1] > 12:
  col13_name = food_data4.columns[12]
  nan_count_col13 = food_data4[col13_name].isnull().sum()
  print(f"\nNumber of NaN values in the 13th column ('{col13_name}') after operation: {nan_count_col13}")
else:
  print("\nDataFrame does not have a 13th column.")
  
  

# : check print count of nan or blank values in all counts

# Check the total count of NaN values in each column
nan_counts = food_data4.isnull().sum()

# Print the count of NaN values for each column
print("\nNaN counts per column:")
nan_counts

# Optionally, check for blank values (empty strings) or zeros if they are not represented as NaN
# This depends on how blank/zero values were handled during cleaning.
# If blank strings or zeros should also be counted, you can add checks like:
# blank_counts = (food_data4 == '').sum()
# zero_counts = (food_data4 == 0).sum()
# print("\nBlank string counts per column:")
# print(blank_counts)
# print("\nZero counts per column:")
# print(zero_counts)

# You can combine these counts if needed, but be mindful of data types.
# For example, sum NaN counts with blank string counts for object type columns:
# combined_counts = nan_counts
# for col in food_data4.columns:
#     if food_data4[col].dtype == 'object':
#         combined_counts[col] += (food_data4[col] == '').sum()
# print("\nCombined NaN and blank counts per column:")
# print(combined_counts)


