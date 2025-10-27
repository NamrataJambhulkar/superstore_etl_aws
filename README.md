# Superstore AWS ETL Project

## Project Overview
This is an end-to-end **AWS Data Engineering project** using the Superstore dataset.  
The pipeline demonstrates:  
- Raw CSV ingestion to S3  
- ETL using AWS Glue (PySpark)  
- Partitioned Parquet storage in S3  
- Querying using Amazon Athena with efficient partition pruning  

**Tools & Services Used:**  
- Amazon S3  
- AWS Glue (Crawlers & Jobs)  
- Amazon Athena   

---

## Folder Structure

- `glue-scripts/` → PySpark ETL script  
- `screenshots/` → Screenshots of architecture flow, tables, queries, and results  

---

## ETL Pipeline

**Step 1: Raw Data Ingestion**  
CSV uploaded to S3 → `raw/Sample - Superstore.csv`  

**Step 2: Glue Crawler on Raw Data**  
Glue automatically creates a **raw table** with schema inferred.  

**Step 3: Glue ETL Job**  
- Reads CSV  
- Converts `Order Date` to timestamp  
- Adds `year`, `month`, `day` columns  
- Writes **Parquet** to `processed/` partitioned by `year/month/day`  

**Step 4: Glue Crawler on Processed Data**  
- Crawls processed Parquet files  
- Creates `processed` table in Glue  
- Detects partitions automatically  

**Step 5: Athena Queries**  
Athena queries run on processed table with **partition pruning** for efficient analytics.  

---

## Screenshots

### 1️⃣ Raw Glue Table
![Raw Table](screenshots/glue_raw_table/Glue Raw Table Screenshot.png)  
*Shows columns of raw CSV and Glue schema detection.*

### 2️⃣ Processed Glue Table
![Processed Table](screenshots/glue_processed_table/Glue Processed Table Screenshot1.png)
(screenshots/glue_processed_table/Glue Processed Table Screenshot2.png)  
*Shows processed Parquet table with `year/month/day` partitions.*

### 3️⃣ Athena Query – Aggregate Total Sales by Year
![Total Sales by Year](screenshots/total_sales_per_year/Total sales per year.png)  
*Demonstrates that the processed table is queryable.*

### 4️⃣ Athena Query – Partition Filter (Year, Month, Day)
![Month Filter Query](screenshots/filtering_query_by_year_month_day/Athena query filtering by year,month,day.png)  
*Shows Athena querying specific year, month, day using partition pruning.*

---

## Key Learnings
- Efficient ETL on AWS using Glue and PySpark  
- Partitioned Parquet storage reduces data scanned in Athena  
- Serverless analytics with Athena for big datasets  
- End-to-end AWS Data Engineering pipeline  

---

## Notes

- Partitioning helps **query only necessary data**, improving both speed and cost-efficiency.  
- Converting data from **CSV to Parquet** reduces storage size and accelerates Athena queries.  
- AWS Glue Crawlers automatically **infer schema** and create tables in the Data Catalog.  
- The **ETL Job (PySpark)** handles data cleaning, transformation, and Parquet conversion.  
- Using **S3 as a Data Lake** separates raw and processed layers, maintaining clean data organization.  
- **Athena** enables direct SQL querying on S3 data without managing any servers or databases.  
- Proper **IAM roles and permissions** are essential for Glue and Athena to access S3 securely.