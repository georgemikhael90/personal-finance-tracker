"""
CSV Import/Export Handler
"""

import csv
import pandas as pd
from datetime import datetime
from typing import List, Dict

class CSVHandler:
    """Handle CSV import and export operations"""

    @staticmethod
    def export_transactions(transactions: List[Dict], filename: str):
        """Export transactions to CSV file"""
        if not transactions:
            raise ValueError("No transactions to export")

        # Define columns to export
        fieldnames = ['date', 'account', 'category', 'type', 'amount', 'description']

        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for transaction in transactions:
                writer.writerow({
                    'date': transaction['transaction_date'],
                    'account': transaction['account_name'],
                    'category': transaction['category_name'],
                    'type': transaction['transaction_type'],
                    'amount': transaction['amount'],
                    'description': transaction['description'] or ''
                })

    @staticmethod
    def import_transactions(filename: str, account_id: int, column_mapping: Dict[str, int],
                          db_manager, category_map: Dict[str, int]) -> tuple:
        """
        Import transactions from CSV file

        Args:
            filename: Path to CSV file
            account_id: Target account ID for all imported transactions
            column_mapping: Maps field names to column indices
                           e.g., {'date': 0, 'amount': 1, 'description': 2, 'category': 3, 'type': 4}
            db_manager: Database manager instance
            category_map: Maps category names to category IDs

        Returns:
            Tuple of (success_count, error_count, errors_list)
        """
        success_count = 0
        error_count = 0
        errors = []

        try:
            # Read CSV file
            with open(filename, 'r', encoding='utf-8') as csvfile:
                # Try to detect if file has headers
                sample = csvfile.read(1024)
                csvfile.seek(0)
                sniffer = csv.Sniffer()
                has_header = sniffer.has_header(sample)

                reader = csv.reader(csvfile)

                # Skip header if present
                if has_header:
                    next(reader)

                for row_num, row in enumerate(reader, start=2 if has_header else 1):
                    try:
                        # Extract fields based on column mapping
                        date_str = row[column_mapping['date']].strip()
                        amount_str = row[column_mapping['amount']].strip()
                        description = row[column_mapping.get('description', -1)].strip() if column_mapping.get('description', -1) >= 0 else ''

                        # Parse date (try multiple formats)
                        transaction_date = CSVHandler._parse_date(date_str)
                        if not transaction_date:
                            errors.append(f"Row {row_num}: Invalid date format '{date_str}'")
                            error_count += 1
                            continue

                        # Parse amount
                        amount = CSVHandler._parse_amount(amount_str)
                        if amount is None or amount <= 0:
                            errors.append(f"Row {row_num}: Invalid amount '{amount_str}'")
                            error_count += 1
                            continue

                        # Get transaction type
                        if 'type' in column_mapping and column_mapping['type'] >= 0:
                            transaction_type = row[column_mapping['type']].strip().lower()
                            if transaction_type not in ['income', 'expense']:
                                errors.append(f"Row {row_num}: Invalid transaction type '{transaction_type}'")
                                error_count += 1
                                continue
                        else:
                            # Default to expense if not specified
                            transaction_type = 'expense'

                        # Get category
                        category_id = None
                        if 'category' in column_mapping and column_mapping['category'] >= 0:
                            category_name = row[column_mapping['category']].strip()
                            category_id = category_map.get(category_name)

                        # If no category found, use default
                        if not category_id:
                            # Try to find "Other Income" or "Other Expense" category
                            default_category_name = 'Other Income' if transaction_type == 'income' else 'Other Expense'
                            category_id = category_map.get(default_category_name)

                        if not category_id:
                            errors.append(f"Row {row_num}: No valid category found")
                            error_count += 1
                            continue

                        # Add transaction to database
                        db_manager.add_transaction(
                            account_id=account_id,
                            category_id=category_id,
                            amount=amount,
                            transaction_type=transaction_type,
                            description=description,
                            transaction_date=transaction_date
                        )

                        success_count += 1

                    except IndexError:
                        errors.append(f"Row {row_num}: Invalid row format (not enough columns)")
                        error_count += 1
                    except Exception as e:
                        errors.append(f"Row {row_num}: {str(e)}")
                        error_count += 1

        except FileNotFoundError:
            raise ValueError(f"File not found: {filename}")
        except Exception as e:
            raise ValueError(f"Error reading CSV file: {str(e)}")

        return success_count, error_count, errors

    @staticmethod
    def _parse_date(date_str: str) -> str:
        """Parse date string in various formats to YYYY-MM-DD"""
        date_formats = [
            '%Y-%m-%d',
            '%Y/%m/%d',
            '%m/%d/%Y',
            '%d/%m/%Y',
            '%m-%d-%Y',
            '%d-%m-%Y',
            '%Y%m%d',
            '%m/%d/%y',
            '%d/%m/%y',
        ]

        for fmt in date_formats:
            try:
                date_obj = datetime.strptime(date_str, fmt)
                return date_obj.strftime('%Y-%m-%d')
            except ValueError:
                continue

        return None

    @staticmethod
    def _parse_amount(amount_str: str) -> float:
        """Parse amount string to float (handles $ and commas)"""
        try:
            # Remove currency symbols, commas, and spaces
            cleaned = amount_str.replace('$', '').replace(',', '').replace(' ', '').strip()

            # Handle parentheses for negative numbers (accounting format)
            if cleaned.startswith('(') and cleaned.endswith(')'):
                cleaned = '-' + cleaned[1:-1]

            return float(cleaned)
        except (ValueError, AttributeError):
            return None

    @staticmethod
    def get_csv_preview(filename: str, num_rows: int = 5) -> List[List[str]]:
        """Get preview of first few rows of CSV file"""
        preview = []
        try:
            with open(filename, 'r', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                for i, row in enumerate(reader):
                    if i >= num_rows:
                        break
                    preview.append(row)
        except Exception as e:
            raise ValueError(f"Error reading CSV file: {str(e)}")

        return preview
