\# Configuration-Driven ETL Pipeline



\## Overview



This project implements a configuration-driven ETL (Extract, Transform, Load) pipeline using Python and Pandas.



The pipeline reads data from a CSV file, applies configurable transformation and validation rules, and generates a validated final dataset.



The input source, transformed output location, final output location, and validation rules are maintained separately in a JSON configuration file.



\## Objectives



\- Build a practical ETL pipeline using Python.

\- Separate configuration from application code.

\- Perform data extraction, transformation, validation, and loading.

\- Apply configurable validation rules.

\- Generate raw, transformed, and final datasets.

\- Maintain pipeline logs with record counts at each stage.



\## Technologies Used



\- Python

\- Pandas

\- JSON

\- CSV

\- Logging



\## Project Structure



```text

task26-configuration-driven-etl/

│

├── config/

│   └── config.json

│

├── data/

│   ├── raw/

│   │   └── sales\_raw.csv

│   ├── transformed/

│   │   └── sales\_transformed.csv

│   └── final/

│       └── sales\_final.csv

│

├── logs/

│   └── pipeline.log

│

├── src/

│   └── etl\_pipeline.py

│

├── requirements.txt

└── README.md
ETL Workflow
Raw CSV
   ↓
Extract
   ↓
Transform
   ↓
Validate
   ↓
Load
   ↓
Final CSV
Pipeline Stages
1. Extract

The pipeline reads the raw sales CSV file specified in the configuration file.

Input:

data/raw/sales_raw.csv

Records extracted:

10
2. Transform

The transformation stage:

Cleans column names.
Removes unnecessary spaces from text values.
Converts quantity and price into numeric values.
Creates a total_amount column.

Records transformed:

10
3. Validate

Validation rules are loaded from config.json.

The pipeline checks:

Required columns exist.
Quantity is at least 1.
Price is not negative.
Required values are not missing.

Validation result:

Valid records: 8
Invalid records: 2
4. Load

The validated records are saved to:

data/final/sales_final.csv

Final records loaded:

8
Configuration

The pipeline behavior is controlled using:

config/config.json

Example:

{
    "input_file": "data/raw/sales_raw.csv",
    "transformed_file": "data/transformed/sales_transformed.csv",
    "output_file": "data/final/sales_final.csv",
    "validation": {
        "required_columns": [
            "product",
            "category",
            "quantity",
            "price"
        ],
        "quantity_min": 1,
        "price_min": 0
    }
}

This allows paths and validation rules to be changed without modifying the Python source code.

Logging

Pipeline execution is recorded in:

logs/pipeline.log

Example execution summary:

ETL Pipeline Started
Extract stage completed. Records extracted: 10
Transform stage completed. Records transformed: 10
Validation completed. Valid records: 8, Invalid records: 2
Load stage completed. Final records loaded: 8
ETL Pipeline Completed Successfully
How to Run
1. Create a virtual environment
python -m venv venv
2. Activate the environment
.\venv\Scripts\Activate.ps1
3. Install dependencies
pip install -r requirements.txt
4. Run the pipeline
python src\etl_pipeline.py
Output

The pipeline generates:

Raw dataset
Transformed dataset
Validated final dataset
Pipeline execution logs
Result

The configuration-driven ETL pipeline successfully processed 10 input records.

Extracted: 10
Transformed: 10
Valid: 8
Invalid: 2
Loaded: 8
Key Learning Outcomes
ETL pipeline design
Configuration-driven programming
Data cleaning and transformation
Data validation
CSV processing
Pandas
JSON configuration
Python logging
Modular pipeline development
