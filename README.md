# EduPayAudit: Higher Education Payroll Compliance & Reconciliation System

A comprehensive Python-based system designed for higher education institutions to perform detailed payroll reconciliation and compliance auditing. This tool helps ensure accuracy between HR and Payroll systems while maintaining audit compliance standards.

## Key Features

- **Data Validation**: Enforces required fields and data format consistency
- **Comprehensive Reconciliation**: 
  - Identifies pay discrepancies between HR and Payroll systems
  - Tracks missing records in both systems
  - Performs department-level analysis
- **Audit Trail**: 
  - Maintains detailed logging of all operations
  - Timestamps all reports and analyses
  - Generates audit-ready documentation
- **Detailed Reporting**:
  - Excel reports with multiple worksheets for different types of discrepancies
  - Department-wise analysis
  - JSON summary reports for data integration
  - Floating-point precision handling for accurate financial comparisons
- **Visual Analytics**:
  - Bar charts showing discrepancies by employee category
  - Department comparison charts for HR vs. Payroll systems
  - Pie charts displaying the distribution of issues found
  - All charts saved as PNG files for easy inclusion in reports and presentations
- **Interactive Analysis**:
  - Jupyter notebook for interactive data exploration
  - Custom analysis capabilities
  - Visual report display and interpretation

## Requirements

- Python 3.x
- Required packages listed in `requirements.txt`

## Installation

### Option 1: Using Conda (Recommended)

1. Clone this repository
2. Create and activate the Conda environment:
```bash
conda env create -f environment.yml
conda activate edupayaudit
```

### Option 2: Using pip

1. Clone this repository
2. Install required packages:
```bash
pip install -r requirements.txt
```

## Input Files

The tool requires two CSV files in the same directory:
- `hr_system_data.csv`: HR system data
- `payroll_system_data.csv`: Payroll system data

### Required CSV Columns
- EmployeeID
- Pay
- Position
- Department
- PayPeriodEnd

## Sample Data

The repository includes sample data files that demonstrate various scenarios:

### Included Test Scenarios:
- Pay discrepancies between systems
- Missing records in HR/Payroll
- Department-level variations
- Different employee categories (Faculty, Staff, Adjunct)
- Various academic departments

Sample files:
- `hr_system_data.csv`: 15 sample HR records
- `payroll_system_data.csv`: 15 sample Payroll records

The sample data includes intentional discrepancies to demonstrate the tool's capabilities:
1. Salary mismatches (e.g., ADJ001, STF003, FAC006)
2. Missing records (e.g., ADJ002 in HR only, TEMP001 in Payroll only)
3. Various departments and positions for comprehensive testing

## Usage

Run the main reconciliation script:
```bash
python payroll_reconciliation.py
```

Generate visual reports from the latest audit:
```bash
python visual_report_generator.py
```

Interactive exploration with Jupyter notebook:
```bash
jupyter notebook EduPayAudit.ipynb
```

## Output

The tool generates two types of output files in the `output` directory:

1. Excel Report (`payroll_reconciliation_report_TIMESTAMP.xlsx`):
   - Mismatched Records
   - Records Missing in HR
   - Records Missing in Payroll
   - Department Analysis

2. JSON Summary (`audit_summary_TIMESTAMP.json`):
   - Audit timestamp
   - Statistical summary
   - Department-level discrepancy counts

3. Visual Reports (PNG files):
   - Bar charts, department comparison charts, and pie charts saved in the `output` directory

## Audit Compliance

This tool is designed to meet educational institution audit requirements:
- Maintains detailed audit trails
- Implements data validation checks
- Provides comprehensive reconciliation reports
- Supports department-level analysis
- Ensures accurate financial calculations

## Best Practices

- Run reconciliation reports regularly (recommended: bi-weekly)
- Review all discrepancies promptly
- Maintain audit logs for compliance purposes
- Document any manual adjustments
- Regular backup of reconciliation reports

## License and Attribution

This project is licensed under the MIT License with an attribution requirement - see the [LICENSE](LICENSE) file for details.

> **Note**: This version (v1.0) is released under MIT License for demonstration and portfolio purposes. Future versions may be released under different licensing terms.

### Attribution Requirements

When using this software or substantial portions of it, you must include the following attribution:

> Created by Nicole LeGuern (CodeQueenie). Original repository: https://github.com/CodeQueenie/HigherEd_PayrollAudit_System

This attribution may be included in:
- Documentation
- "About" section of your application
- Code comments
- Credits file that ships with your software

### Author

**Nicole LeGuern** (GitHub: [CodeQueenie](https://github.com/CodeQueenie))
