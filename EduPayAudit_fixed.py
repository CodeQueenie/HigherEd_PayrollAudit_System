#!/usr/bin/env python
# coding: utf-8

"""
EduPayAudit: Higher Education Payroll Compliance & Reconciliation System
Copyright (c) 2025 Nicole LeGuern (CodeQueenie)
MIT License with Attribution Requirement

When using this software or substantial portions of it, you must include the following attribution:
"Created by Nicole LeGuern (CodeQueenie). Original repository: https://github.com/CodeQueenie/HigherEd_PayrollAudit_System"

See the LICENSE file for full details.
"""

# # EduPayAudit: Higher Education Payroll Compliance & Reconciliation System
# 
# This notebook demonstrates the key features of the EduPayAudit system, a comprehensive solution designed for higher education institutions to ensure payroll compliance and reconciliation.
# 
# ## Overview
# 
# EduPayAudit helps higher education institutions identify and resolve discrepancies between HR and Payroll systems, ensuring accurate compensation, regulatory compliance, and financial integrity.
# 
# In this notebook, we'll walk through:
# 1. Loading and exploring HR and Payroll data
# 2. Running the reconciliation process
# 3. Analyzing discrepancies
# 4. Generating visual reports
# 5. Exporting results for further action

# ## 1. Setup and Imports
# 
# First, let's import the necessary modules and set up our environment.

# Import standard libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import json
from datetime import datetime
import os

# Import EduPayAudit modules
from payroll_reconciliation import PayrollAuditor
from visual_report_generator import VisualReportGenerator

# Set up plotting style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("deep")
plt.rcParams['figure.figsize'] = (12, 8)

# Create output directory if it doesn't exist
output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

# ## 2. Load and Explore HR and Payroll Data
# 
# Let's load the sample HR and Payroll data provided with the system and explore its structure.

# Define file paths
hr_data_path = "hr_system_data.csv"
payroll_data_path = "payroll_system_data.csv"

# Load data directly with pandas for exploration
hr_data = pd.read_csv(hr_data_path)
payroll_data = pd.read_csv(payroll_data_path)

# Display the first few rows of each dataset
print("HR System Data:")
display(hr_data.head())

print("\nPayroll System Data:")
display(payroll_data.head())

# Get basic statistics about the datasets
print("HR Data Summary:")
print(f"Number of records: {len(hr_data)}")
print(f"Departments: {hr_data['Department'].unique()}")
print(f"Employment statuses: {hr_data['EmploymentStatus'].unique()}")

print("\nPayroll Data Summary:")
print(f"Number of records: {len(payroll_data)}")
print(f"Payroll statuses: {payroll_data['PayrollStatus'].unique()}")

# ## 3. Run Payroll Reconciliation
# 
# Now, let's run the payroll reconciliation process to identify discrepancies between the HR and Payroll systems.

# Initialize the PayrollAuditor class
auditor = PayrollAuditor(
    hr_file=hr_data_path,
    payroll_file=payroll_data_path
)

# Load and validate data
auditor.load_and_validate_data()

# Run reconciliation
auditor.perform_reconciliation()

# Generate reports
auditor.generate_reports()

# Get the report paths
excel_report_path = auditor.output_dir / f"payroll_reconciliation_report_{auditor.audit_timestamp}.xlsx"
json_summary_path = auditor.output_dir / f"audit_summary_{auditor.audit_timestamp}.json"

print(f"Excel report generated: {excel_report_path}")
print(f"JSON summary generated: {json_summary_path}")

# ## 4. Analyze Discrepancies
# 
# Let's analyze the discrepancies identified during the reconciliation process.

# Load the reconciliation results
mismatched_records = auditor.mismatches
missing_in_hr = auditor.missing_in_hr
missing_in_payroll = auditor.missing_in_payroll

# Display summary of discrepancies
print("Reconciliation Summary:")
print(f"Total records processed: {auditor.stats['total_records']}")
print(f"Mismatched records: {auditor.stats['mismatches']}")
print(f"Records in Payroll but missing in HR: {auditor.stats['missing_in_hr']}")
print(f"Records in HR but missing in Payroll: {auditor.stats['missing_in_payroll']}")
print(f"Total discrepancy amount: ${auditor.stats['total_discrepancy_amount']:.2f}")

# Examine mismatched records
if len(mismatched_records) > 0:
    print("\nMismatched Records:")
    display(mismatched_records)
else:
    print("\nNo mismatched records found.")

# Examine records missing in HR
if len(missing_in_hr) > 0:
    print("\nRecords in Payroll but missing in HR:")
    display(missing_in_hr)
else:
    print("\nNo records found in Payroll that are missing in HR.")

# Examine records missing in Payroll
if len(missing_in_payroll) > 0:
    print("\nRecords in HR but missing in Payroll:")
    display(missing_in_payroll)
else:
    print("\nNo records found in HR that are missing in Payroll.")

# Examine department analysis
print("\nDepartment Analysis:")
display(auditor.dept_analysis)

# ## 5. Generate Visual Reports
# 
# Now, let's generate visual reports to better understand the discrepancies.

# Initialize the VisualReportGenerator
visual_generator = VisualReportGenerator(
    excel_report_path=excel_report_path,
    json_summary_path=json_summary_path
)

# Load data
visual_generator.load_data()

# Set style
visual_generator.set_style()

# Generate visual reports
discrepancy_chart_path = visual_generator.generate_discrepancy_bar_chart()
department_chart_path = visual_generator.generate_department_comparison_chart()
summary_pie_chart_path = visual_generator.generate_summary_pie_chart()

print(f"Discrepancy bar chart generated: {discrepancy_chart_path}")
print(f"Department comparison chart generated: {department_chart_path}")
print(f"Summary pie chart generated: {summary_pie_chart_path}")

# ## 6. Display Visual Reports
# 
# Let's display the generated visual reports.

# Display the discrepancy bar chart
if discrepancy_chart_path:
    from IPython.display import Image
    display(Image(filename=discrepancy_chart_path))
else:
    print("Discrepancy bar chart not generated.")

# Display the department comparison chart
if department_chart_path:
    from IPython.display import Image
    display(Image(filename=department_chart_path))
else:
    print("Department comparison chart not generated.")

# Display the summary pie chart
if summary_pie_chart_path:
    from IPython.display import Image
    display(Image(filename=summary_pie_chart_path))
else:
    print("Summary pie chart not generated.")

# ## 7. Custom Analysis: Pay Discrepancies by Department
# 
# Let's perform a custom analysis to examine pay discrepancies by department.

# Create a bar chart of department discrepancies
plt.figure(figsize=(12, 6))
sns.barplot(x='Department_HR', y='Discrepancy', data=auditor.dept_analysis)
plt.title('Total Pay Discrepancy by Department', fontsize=16)
plt.xlabel('Department', fontsize=14)
plt.ylabel('Total Pay Discrepancy ($)', fontsize=14)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Calculate relative discrepancy percentage
dept_analysis_pct = auditor.dept_analysis.copy()
dept_analysis_pct['Discrepancy_Percentage'] = (dept_analysis_pct['Discrepancy'] / dept_analysis_pct['Pay_HR']) * 100

# Create a bar chart of department discrepancy percentages
plt.figure(figsize=(12, 6))
sns.barplot(x='Department_HR', y='Discrepancy_Percentage', data=dept_analysis_pct)
plt.title('Discrepancy Percentage by Department', fontsize=16)
plt.xlabel('Department', fontsize=14)
plt.ylabel('Discrepancy Percentage (%)', fontsize=14)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# ## 8. Custom Analysis: Employment Status vs. Payroll Status
# 
# Let's analyze the relationship between employment status and payroll status.

# Merge HR and Payroll data on EmployeeID
merged_data = pd.merge(hr_data, payroll_data, on='EmployeeID', how='inner', suffixes=('_HR', '_Payroll'))

# Create a crosstab of employment status vs. payroll status
status_crosstab = pd.crosstab(merged_data['EmploymentStatus'], merged_data['PayrollStatus'])

# Display the crosstab
print("Employment Status vs. Payroll Status:")
display(status_crosstab)

# Create a heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(status_crosstab, annot=True, cmap='YlGnBu', fmt='d')
plt.title('Employment Status vs. Payroll Status', fontsize=16)
plt.xlabel('Payroll Status', fontsize=14)
plt.ylabel('Employment Status', fontsize=14)
plt.tight_layout()
plt.show()

# ## 9. Recommendations Based on Analysis
# 
# Based on the reconciliation results, let's provide some recommendations for addressing the identified issues.

# Calculate the percentage of records with issues
total_records = auditor.stats['total_records']
total_issues = auditor.stats['mismatches'] + auditor.stats['missing_in_hr'] + auditor.stats['missing_in_payroll']
issue_percentage = (total_issues / total_records) * 100 if total_records > 0 else 0

print("## Recommendations Based on Analysis")
print(f"\nOverall Issue Rate: {issue_percentage:.2f}% of records have some kind of discrepancy")

# Generate recommendations based on the analysis
print("\nRecommendations:")

if auditor.stats['mismatches'] > 0:
    print("1. Address Pay Discrepancies:")
    print("   - Review all mismatched records, focusing on departments with the highest discrepancy percentages")
    print("   - Establish a reconciliation process for regular pay period checks")
    print("   - Implement validation rules in both HR and Payroll systems")

if auditor.stats['missing_in_hr'] > 0:
    print("\n2. Resolve Missing HR Records:")
    print("   - Investigate why records exist in Payroll but not in HR")
    print("   - Establish procedures for employee onboarding to ensure consistent data entry")
    print("   - Implement system integrations to automatically sync employee records")

if auditor.stats['missing_in_payroll'] > 0:
    print("\n3. Address Missing Payroll Records:")
    print("   - Review HR records that are not in the Payroll system")
    print("   - Verify employment status and ensure proper payroll processing")
    print("   - Create alerts for HR records that don't have corresponding payroll entries")

# Department-specific recommendations
if len(auditor.dept_analysis) > 0:
    # Find department with highest discrepancy
    worst_dept = auditor.dept_analysis.loc[auditor.dept_analysis['Discrepancy'].idxmax()]
    print(f"\n4. Department-Specific Focus:")
    print(f"   - Prioritize review of the {worst_dept['Department_HR']} department, which has the highest absolute discrepancy")
    print("   - Conduct training for department administrators on proper payroll procedures")
    print("   - Establish department-level reconciliation checkpoints")

print("\n5. System Improvements:")
print("   - Implement automated data validation between HR and Payroll systems")
print("   - Schedule regular reconciliation reports to proactively identify issues")
print("   - Create dashboards for department heads to monitor payroll accuracy")

# ## 10. Conclusion
# 
# The EduPayAudit system has successfully identified discrepancies between the HR and Payroll systems, providing valuable insights for improving payroll accuracy and compliance.
# 
# Key outcomes from this analysis:
# 
# 1. Identified specific records with pay discrepancies
# 2. Highlighted departments with the highest discrepancy rates
# 3. Provided actionable recommendations for addressing the issues
# 4. Generated visual reports for easy communication of findings
# 
# By regularly using the EduPayAudit system, higher education institutions can ensure accurate compensation, maintain regulatory compliance, and improve financial integrity.
