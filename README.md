## Quantium Data Analytics Project

This repository contains my work for the Quantium Data Analytics Virtual Experience Program on Forage.  
It includes environment setup, data processing, and output preparation required for Task 1.

---

## 📌 Project Overview

Soul Foods, a Quantium client, wants to understand whether **Pink Morsel** sales increased or decreased after a price change on **15 January 2021**.

To answer this, transaction-level sales data was provided across three CSV files.  
My objective for this stage was to:

✔ load and explore the datasets  
✔ clean and transform them  
✔ isolate Pink Morsel sales  
✔ generate a new formatted output dataset suitable for analysis  

---

## 📂 Repository Structure

📦 quantium-starter-repo
│
├── 📁 data
│   ├── 📄 daily_sales_data_0.csv
│   ├── 📄 daily_sales_data_1.csv
│   └── 📄 daily_sales_data_2.csv
│
├── 📁 processed
│   └── 📄 pink_morsel_sales.csv
│
├── 🐍 process_data.py
│
├── 📝 setup_complete.txt
│
└── 📘 README.md

## 🔧 Environment & Tools Used

- Python 3  
- Pandas library  
- Virtual environment (venv)  
- Visual Studio Code  
- Git & GitHub for version control  

---

## 🚀 What I Did

### ✔ 1. Forked & cloned the starter repository  
Created a local environment where I could work on the project independently.

### ✔ 2. Set up a Python virtual environment  
Installed dependencies including:

- pandas
- dash (for later visualisation tasks)

### ✔ 3. Inspected the raw data  
Each dataset contains:

- product name
- quantity sold
- price
- date of transaction
- region sold

### ✔ 4. Processed and filtered Pink Morsel transactions  
- Removed all rows that did not relate to Pink Morsels.
- Cleaned the price field (removed “$” symbol).
- Converted values into numeric types.

### ✔ 5. Created a new **sales** field  
Calculated total revenue per transaction: sales=price*quantity

### ✔ 6. Extracted only relevant fields  
Kept:

- `sales`
- `date`
- `region`

To determine whether Pink Morsel sales increased or decreased after the price change on 15 January 2021, I processed and transformed daily product-level transaction data into a structured dataset containing revenue, date and region. By isolating Pink Morsel transactions, calculating sales value per record, and comparing total revenue before and after the price change threshold, it becomes possible to quantify buying behaviour shifts. This analysis allows the business to understand whether customers continued purchasing at similar levels post-increase, reduced consumption due to price sensitivity, or whether total revenue rose despite higher prices — providing actionable commercial insight for pricing decisions.

### ✔ 7. Exported the cleaned dataset  
The transformed output is stored in: processed/pink_morsel_sales.csv

This file is now ready for downstream analysis and dashboard visualisation.

---

## 📌 process_data.py Summary

This script:

- Reads all three CSV files
- Concatenates them
- Filters Pink Morsels
- Calculates transaction sales
- Outputs a clean dataset





