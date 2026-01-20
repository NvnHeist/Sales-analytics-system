import os
from utils.file_handler import read_sales_data
from utils.data_processor import (
    parse_transactions, validate_and_filter,
    calculate_total_revenue, region_wise_sales,
    daily_sales_trend, find_peak_sales_day,
    top_selling_products
)


def main():
    base_path = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(base_path, 'data', 'sales_data.txt')

    # 1. Load and Parse (Task 1.1 & 1.2)
    raw_lines = read_sales_data(input_file)
    if not raw_lines: return
    all_transactions = parse_transactions(raw_lines)

    # 2. Filter Display (Task 1.3 Requirements)
    # Print available regions and amount range before the final cleaning
    regions_found = sorted(list(set(t['Region'] for t in all_transactions)))
    print(f"\n[SYSTEM] Available Regions for Filtering: {', '.join(regions_found)}")

    # 3. Clean and Validate
    valid_data, _, summary = validate_and_filter(all_transactions)

    # 4. Run Analytics (Task 2.1 - 2.3)
    total_rev = calculate_total_revenue(valid_data)
    reg_stats = region_wise_sales(valid_data)
    peak_date, peak_rev, peak_count = find_peak_sales_day(valid_data)
    top_5 = top_selling_products(valid_data, n=5)

    # --- FINAL COMPREHENSIVE REPORT ---
    print("\n" + "=" * 55)
    print(f"{'SALES PERFORMANCE EXECUTIVE SUMMARY':^55}")
    print("=" * 55)
    print(f"Total Revenue:            ${total_rev:,.2f}")
    print(f"Peak Sales Date:          {peak_date} (${peak_rev:,.2f})")
    print(f"Peak Transaction Count:   {peak_count}")
    print("-" * 55)

    # Regional Table (Task 2.1b)
    print(f"{'Region':<15} | {'Sales':<12} | {'Transactions':<12} | {'%':<5}")
    print("-" * 55)
    for reg, data in reg_stats.items():
        print(f"{reg:<15} | ${data['total_sales']:<11,.2f} | {data['transaction_count']:<12} | {data['percentage']}%")

    # Top Products Table (Task 2.3c)
    print("\n" + "-" * 55)
    print(f"{'TOP 5 PRODUCTS BY QUANTITY':^55}")
    print("-" * 55)
    print(f"{'Product Name':<20} | {'Qty Sold':<10} | {'Total Revenue':<15}")
    for name, qty, rev in top_5:
        print(f"{name:<20} | {qty:<10} | ${rev:<14,.2f}")
    print("=" * 55)


if __name__ == "__main__":
    main()