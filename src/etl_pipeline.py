import json
import logging
from pathlib import Path

import pandas as pd


# Load configuration
CONFIG_FILE = Path("config/config.json")

with open(CONFIG_FILE, "r") as file:
    config = json.load(file)


# Configure logging
Path("logs").mkdir(exist_ok=True)

logging.basicConfig(
    filename="logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def extract():
    """Read raw data from the configured input file."""
    input_file = config["input_file"]

    df = pd.read_csv(input_file)

    logging.info("Extract stage completed. Records extracted: %d", len(df))

    return df


def transform(df):
    """Clean and transform the dataset."""
    df = df.copy()

    # Remove extra spaces from column names
    df.columns = df.columns.str.strip()

    # Remove extra spaces from text values
    for column in ["product", "category"]:
        df[column] = df[column].astype(str).str.strip()

    # Convert numeric columns
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["price"] = pd.to_numeric(df["price"], errors="coerce")

    # Create derived column
    df["total_amount"] = df["quantity"] * df["price"]

    output_file = config["transformed_file"]

    Path(output_file).parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(output_file, index=False)

    logging.info("Transform stage completed. Records transformed: %d", len(df))

    return df


def validate(df):
    """Validate records using rules from configuration."""
    validation = config["validation"]

    required_columns = validation["required_columns"]
    quantity_min = validation["quantity_min"]
    price_min = validation["price_min"]

    # Check required columns
    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    # Apply validation rules
    valid_records = df[
        df["product"].notna()
        & df["category"].notna()
        & df["quantity"].notna()
        & df["price"].notna()
        & (df["quantity"] >= quantity_min)
        & (df["price"] >= price_min)
    ].copy()

    invalid_count = len(df) - len(valid_records)

    logging.info(
        "Validation completed. Valid records: %d, Invalid records: %d",
        len(valid_records),
        invalid_count
    )

    return valid_records


def load(df):
    """Save validated records to the configured output file."""
    output_file = config["output_file"]

    Path(output_file).parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(output_file, index=False)

    logging.info(
        "Load stage completed. Final records loaded: %d",
        len(df)
    )


def main():
    """Run the complete ETL pipeline."""
    logging.info("ETL Pipeline Started")

    try:
        raw_data = extract()

        transformed_data = transform(raw_data)

        valid_data = validate(transformed_data)

        load(valid_data)

        logging.info("ETL Pipeline Completed Successfully")

        print("ETL Pipeline completed successfully!")
        print(f"Records extracted: {len(raw_data)}")
        print(f"Records transformed: {len(transformed_data)}")
        print(f"Valid records: {len(valid_data)}")
        print(f"Invalid records: {len(transformed_data) - len(valid_data)}")

    except Exception as error:
        logging.exception("ETL Pipeline Failed: %s", error)
        print(f"ETL Pipeline failed: {error}")


if __name__ == "__main__":
    main()