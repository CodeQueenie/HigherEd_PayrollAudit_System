"""
EduPayAudit: Higher Education Payroll Compliance & Reconciliation System
Copyright (c) 2025 Nicole LeGuern (CodeQueenie)
MIT License with Attribution Requirement

When using this software or substantial portions of it, you must include the following attribution:
"Created by Nicole LeGuern (CodeQueenie). Original repository: https://github.com/CodeQueenie/HigherEd_PayrollAudit_System"

See the LICENSE file for full details.
"""

import pandas as pd
import sys
from datetime import datetime
import logging
from pathlib import Path
import json

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("payroll_audit.log"),
        logging.StreamHandler()
    ]
)

class PayrollAuditor:
    """
    PayrollAuditor performs detailed reconciliation between HR and Payroll systems.
    
    This class provides functionality to load, validate, and analyze payroll data from
    HR and Payroll systems, identifying discrepancies and generating comprehensive reports.
    """
    
    def __init__(self, hr_file, payroll_file, output_dir="output"):
        """
        Initialize PayrollAuditor with input files and output directory.
        
        Args:
            hr_file (str): Path to the HR system data CSV file
            payroll_file (str): Path to the Payroll system data CSV file
            output_dir (str): Directory where output reports will be saved
        """
        self.hr_file = hr_file
        self.payroll_file = payroll_file
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.audit_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def load_and_validate_data(self):
        """
        Load CSV files and perform initial data validation.
        
        Validates that all required columns are present and converts date fields
        to the appropriate format.
        
        Returns:
            bool: True if data loading and validation was successful, False otherwise
        """
        try:
            self.hr_data = pd.read_csv(self.hr_file)
            self.payroll_data = pd.read_csv(self.payroll_file)
            
            # Validate required columns
            required_columns = ["EmployeeID", "Pay", "Position", "Department", "PayPeriodEnd"]
            for df, name in [(self.hr_data, "HR"), (self.payroll_data, "Payroll")]:
                missing_cols = [col for col in required_columns if col not in df.columns]
                if missing_cols:
                    raise ValueError(f"Missing required columns in {name} data: {missing_cols}")
                    
            # Convert PayPeriodEnd to datetime
            for df in [self.hr_data, self.payroll_data]:
                df["PayPeriodEnd"] = pd.to_datetime(df["PayPeriodEnd"])
                
            logging.info("Data loaded and validated successfully")
            return True
            
        except Exception as e:
            logging.error(f"Error loading data: {str(e)}")
            return False

    def perform_reconciliation(self):
        """
        Perform comprehensive payroll reconciliation with detailed analysis.
        
        Merges HR and Payroll data to identify discrepancies, missing records,
        and perform department-level analysis.
        
        Returns:
            bool: True if reconciliation was successful, False otherwise
        """
        try:
            # Merge datasets
            merged_data = pd.merge(
                self.hr_data,
                self.payroll_data,
                on="EmployeeID",
                how="outer",
                suffixes=("_HR", "_Payroll")
            )

            # Identify discrepancies
            self.mismatches = merged_data[
                (merged_data["Pay_HR"].notna()) &
                (merged_data["Pay_Payroll"].notna()) &
                (abs(merged_data["Pay_HR"] - merged_data["Pay_Payroll"]) > 0.01)  # Account for floating point differences
            ]

            # Identify missing records
            self.missing_in_payroll = merged_data[merged_data["Pay_Payroll"].isna()]
            self.missing_in_hr = merged_data[merged_data["Pay_HR"].isna()]

            # Calculate statistics
            self.stats = {
                "total_records": len(merged_data),
                "mismatches": len(self.mismatches),
                "missing_in_payroll": len(self.missing_in_payroll),
                "missing_in_hr": len(self.missing_in_hr),
                "total_discrepancy_amount": abs(self.mismatches["Pay_HR"] - self.mismatches["Pay_Payroll"]).sum()
            }

            # Department-wise analysis
            self.dept_analysis = merged_data[merged_data["Department_HR"].notna()].groupby("Department_HR").agg({
                "EmployeeID": "count",
                "Pay_HR": "sum",
                "Pay_Payroll": "sum"
            }).reset_index()
            
            self.dept_analysis["Discrepancy"] = abs(self.dept_analysis["Pay_HR"] - self.dept_analysis["Pay_Payroll"])
            
            logging.info("Reconciliation completed successfully")
            return True

        except Exception as e:
            logging.error(f"Error during reconciliation: {str(e)}")
            return False

    def generate_reports(self):
        """
        Generate comprehensive audit reports.
        
        Creates Excel reports with multiple worksheets for different types of discrepancies
        and a JSON summary file with key statistics.
        
        Returns:
            bool: True if report generation was successful, False otherwise
        """
        try:
            output_file = self.output_dir / f"payroll_reconciliation_report_{self.audit_timestamp}.xlsx"
            
            with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
                # Mismatched Records
                self.mismatches.to_excel(
                    writer,
                    sheet_name="Mismatched Records",
                    index=False
                )
                
                # Missing Records
                self.missing_in_hr.to_excel(
                    writer,
                    sheet_name="Missing in HR",
                    index=False
                )
                self.missing_in_payroll.to_excel(
                    writer,
                    sheet_name="Missing in Payroll",
                    index=False
                )
                
                # Department Analysis
                self.dept_analysis.to_excel(
                    writer,
                    sheet_name="Department Analysis",
                    index=False
                )

            # Generate JSON summary
            summary_file = self.output_dir / f"audit_summary_{self.audit_timestamp}.json"
            with open(summary_file, "w") as f:
                json.dump({
                    "audit_date": self.audit_timestamp,
                    "statistics": self.stats,
                    "departments_with_discrepancies": len(self.dept_analysis[self.dept_analysis["Discrepancy"] > 0])
                }, f, indent=4)

            logging.info(f"Reports generated successfully: {output_file}")
            return True

        except Exception as e:
            logging.error(f"Error generating reports: {str(e)}")
            return False

def main():
    """
    Main function to execute the payroll reconciliation process.
    
    Initializes the PayrollAuditor, loads and validates data, performs reconciliation,
    generates reports, and displays a summary of the results.
    """
    try:
        # File paths
        hr_file = "hr_system_data.csv"
        payroll_file = "payroll_system_data.csv"
        
        # Initialize auditor
        auditor = PayrollAuditor(hr_file, payroll_file)
        
        # Execute reconciliation process
        if not auditor.load_and_validate_data():
            sys.exit(1)
            
        if not auditor.perform_reconciliation():
            sys.exit(1)
            
        if not auditor.generate_reports():
            sys.exit(1)
            
        print("\nPayroll Reconciliation Audit Summary:")
        print(f"Total Records Analyzed: {auditor.stats['total_records']}")
        print(f"Mismatched Records: {auditor.stats['mismatches']}")
        print(f"Records Missing in HR: {auditor.stats['missing_in_hr']}")
        print(f"Records Missing in Payroll: {auditor.stats['missing_in_payroll']}")
        print(f"Total Discrepancy Amount: ${auditor.stats['total_discrepancy_amount']:,.2f}")
        
    except Exception as e:
        logging.error(f"An error occurred during reconciliation: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
