"""
compute_sales.py - Computes total sales from JSON input files.
"""

import json
import sys
import time


def load_json_file(file_path):
    """Loads a JSON file and returns its content."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in file {file_path}.")
        sys.exit(1)


def compute_total_sales(catalogue, sales):
    """Computes the total sales revenue based on the price catalogue."""
    product_prices = {
        item["title"]: item["price"]
        for item in catalogue
    }
    sales_total = 0.0
    errors = []

    for sale in sales:
        product_name = sale["Product"]
        quantity = sale["Quantity"]

        if product_name in product_prices:
            sales_total += product_prices[product_name] * quantity
        else:
            errors.append(
                "Warning: Product '"
                + product_name
                + "' not found in price catalogue."
            )

    return sales_total, errors


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(
            "Usage: python computeSales.py "
            "priceCatalogue.json salesRecord.json"
        )
        sys.exit(1)

    # Read JSON files from command-line arguments
    price_catalogue_path = sys.argv[1]
    sales_record_path = sys.argv[2]

    # Load data
    price_catalogue = load_json_file(price_catalogue_path)
    sales_record = load_json_file(sales_record_path)

    # Ensure data is loaded before using it
    if not price_catalogue or not sales_record:
        print("Error: One or both input files are empty or invalid.")
        sys.exit(1)

    # Start sales computation
    start_time = time.time()
    total_sales, warnings = compute_total_sales(price_catalogue, sales_record)
    end_time = time.time()
    execution_time = end_time - start_time

    # Print results to console
    print("\n--- Sales Report ---")
    print(f"Total Sales: ${total_sales:.2f}")
    print(f"Execution Time: {execution_time:.4f} seconds")

    if warnings:
        print("\nWarnings:")
        for warning in warnings:
            print(warning)

    # Write results to SalesResults.txt
    with open("SalesResults.txt", "w", encoding="utf-8") as result_file:
        result_file.write("--- Sales Report ---\n")
        result_file.write(f"Total Sales: ${total_sales:.2f}\n")
        result_file.write(f"Execution Time: {execution_time:.4f} seconds\n")

        if warnings:
            result_file.write("\nWarnings:\n")
            for warning in warnings:
                result_file.write(f"{warning}\n")

    print("\nSalesResults.txt has been generated successfully.")
