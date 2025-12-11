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

## 8. Pink Morsel Sales Visualiser — Dash Application

The goal was to help Soul Foods answer a key commercial question:

“Were sales higher before or after the Pink Morsel price increase on 15 January 2021?”

⸻

🎯 Objectives of This Task

✔ Load and visualise the cleaned dataset generated in Task 1
✔ Build an interactive time-series plot using Plotly Dash
✔ Display trends clearly enough that the answer is visually obvious
✔ Style the interface so it is professional, readable, and business-friendly

⸻

🛠 Tools & Libraries Used
	•	Dash (web framework)
	•	Plotly Express (graphing & visualisation)
	•	Pandas (data manipulation)
	•	Flask (embedded within Dash)

⸻

🔧 How the Application Works
	1.	pink_morsel_sales.csv is loaded from the processed/ directory
	2.	Sales are grouped per date and sorted chronologically
	3.	A line chart is displayed showing revenue progression
	4.	A vertical marker on 15 January 2021 highlights the price change
	5.	Before/after periods are visually shaded for comparison
	6.	Hover tooltips show exact sales values for each date
	7.	A styled page layout makes the insight clear and accessible

  ✔ Hosted locally via Dash web server at
➡ http://127.0.0.1:8050/

Insight Delivered

From the visualisation:

Sales were higher before the price increase on 15 January 2021.
After the change, revenue trends decline, suggesting the higher price negatively impacted demand.




