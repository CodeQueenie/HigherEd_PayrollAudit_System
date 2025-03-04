import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import json
import logging
from datetime import datetime

class VisualReportGenerator:
    """
    Generate visual reports and charts based on the payroll audit data.
    
    This class provides functionality to create visual representations of payroll audit results,
    including discrepancy charts, department comparisons, and summary visualizations.
    """
    
    def __init__(self, excel_report_path=None, json_summary_path=None, output_dir="output"):
        """
        Initialize the VisualReportGenerator with paths to audit data files.
        
        Args:
            excel_report_path (str): Path to the Excel report file containing audit data
            json_summary_path (str): Path to the JSON summary file containing audit statistics
            output_dir (str): Directory where visual reports will be saved
        """
        self.excel_report_path = excel_report_path
        self.json_summary_path = json_summary_path
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Initialize the data structures
        self.mismatches = None
        self.missing_in_hr = None
        self.missing_in_payroll = None
        self.dept_analysis = None
        self.summary_data = None
        
    def load_data(self):
        """
        Load data from the Excel report and JSON summary.
        
        Returns:
            bool: True if data loading was successful, False otherwise
        """
        try:
            if self.excel_report_path:
                # Load various sheets from the Excel file
                self.mismatches = pd.read_excel(self.excel_report_path, sheet_name="Mismatched Records")
                self.missing_in_hr = pd.read_excel(self.excel_report_path, sheet_name="Missing in HR")
                self.missing_in_payroll = pd.read_excel(self.excel_report_path, sheet_name="Missing in Payroll")
                self.dept_analysis = pd.read_excel(self.excel_report_path, sheet_name="Department Analysis")
                
            if self.json_summary_path:
                # Load the JSON summary data
                with open(self.json_summary_path, "r") as f:
                    self.summary_data = json.load(f)
                    
            logging.info("Visual report data loaded successfully")
            return True
            
        except Exception as e:
            logging.error(f"Error loading data for visual reporting: {str(e)}")
            return False
            
    def set_style(self):
        """
        Set the visual style for the charts.
        
        Configures the seaborn and matplotlib styling for consistent visualization appearance.
        """
        try:
            sns.set(style="whitegrid")
            plt.rcParams.update({
                "font.size": 12,
                "axes.labelsize": 14,
                "axes.titlesize": 16,
                "xtick.labelsize": 12,
                "ytick.labelsize": 12,
                "legend.fontsize": 12,
                "figure.titlesize": 20
            })
        except Exception as e:
            logging.error(f"Error setting chart style: {str(e)}")
    
    def generate_discrepancy_bar_chart(self):
        """
        Generate a bar chart showing discrepancies by employee category.
        
        Creates a visual representation of pay discrepancies grouped by employee categories
        (Faculty, Adjunct, Staff).
        
        Returns:
            bool: True if chart generation was successful, False otherwise
        """
        if self.mismatches is None:
            logging.warning("No mismatch data available for bar chart")
            return False
            
        try:
            # Extract position information for categorization
            self.mismatches["Category"] = self.mismatches["Position_HR"].apply(
                lambda x: "Faculty" if "Professor" in str(x) and "Adjunct" not in str(x)
                          else "Adjunct" if "Adjunct" in str(x)
                          else "Staff"
            )
            
            # Calculate discrepancy amounts
            self.mismatches["Discrepancy"] = abs(self.mismatches["Pay_HR"] - self.mismatches["Pay_Payroll"])
            
            # Group by category
            category_discrepancies = self.mismatches.groupby("Category")["Discrepancy"].sum().reset_index()
            
            # Create the bar chart
            plt.figure(figsize=(10, 6))
            ax = sns.barplot(x="Category", y="Discrepancy", data=category_discrepancies, palette="viridis")
            
            # Add value labels on top of each bar
            for p in ax.patches:
                ax.annotate(f"${p.get_height():,.2f}", 
                            (p.get_x() + p.get_width() / 2., p.get_height()),
                            ha="center", va="bottom", fontsize=12)
            
            plt.title("Total Pay Discrepancies by Employee Category")
            plt.xlabel("Employee Category")
            plt.ylabel("Total Discrepancy Amount ($)")
            plt.tight_layout()
            
            # Save the chart
            output_path = self.output_dir / f"discrepancy_by_category_{self.timestamp}.png"
            plt.savefig(output_path)
            plt.close()
            
            logging.info(f"Discrepancy bar chart generated: {output_path}")
            return True
            
        except Exception as e:
            logging.error(f"Error generating discrepancy bar chart: {str(e)}")
            return False
    
    def generate_department_comparison_chart(self):
        """
        Generate a chart comparing HR and Payroll totals by department.
        
        Creates a grouped bar chart showing the differences between HR and Payroll
        system totals for each department, focusing on the top discrepancies.
        
        Returns:
            bool: True if chart generation was successful, False otherwise
        """
        if self.dept_analysis is None:
            logging.warning("No department analysis data available for comparison chart")
            return False
            
        try:
            # Select top departments by discrepancy for better readability
            top_depts = self.dept_analysis.nlargest(5, "Discrepancy")
            
            # Prepare data for plotting
            melted_data = pd.melt(
                top_depts,
                id_vars=["Department_HR"],
                value_vars=["Pay_HR", "Pay_Payroll"],
                var_name="System",
                value_name="Total Pay"
            )
            
            # Clean up system names for display
            melted_data["System"] = melted_data["System"].apply(lambda x: x.replace("Pay_", ""))
            
            # Create the grouped bar chart
            plt.figure(figsize=(12, 7))
            ax = sns.barplot(x="Department_HR", y="Total Pay", hue="System", data=melted_data, palette="Set2")
            
            # Add formatting
            plt.title("HR vs Payroll System Totals by Department (Top 5 Discrepancies)")
            plt.xlabel("Department")
            plt.ylabel("Total Pay Amount ($)")
            plt.xticks(rotation=30, ha="right")
            plt.legend(title="System")
            
            # Format y-axis as currency
            import matplotlib.ticker as mtick
            ax.yaxis.set_major_formatter(mtick.StrMethodFormatter("${x:,.0f}"))
            
            plt.tight_layout()
            
            # Save the chart
            output_path = self.output_dir / f"department_comparison_{self.timestamp}.png"
            plt.savefig(output_path)
            plt.close()
            
            logging.info(f"Department comparison chart generated: {output_path}")
            return True
            
        except Exception as e:
            logging.error(f"Error generating department comparison chart: {str(e)}")
            return False
    
    def generate_summary_pie_chart(self):
        """
        Generate a pie chart showing the distribution of issues found.
        
        Creates a visual representation of the proportion of different issues identified
        during the audit (mismatches, missing records in HR, missing records in Payroll).
        
        Returns:
            bool: True if chart generation was successful, False otherwise
        """
        if self.summary_data is None:
            logging.warning("No summary data available for pie chart")
            return False
            
        try:
            # Extract data from summary
            stats = self.summary_data["statistics"]
            
            # Create data for pie chart
            labels = ["Mismatched Records", "Missing in HR", "Missing in Payroll"]
            values = [stats["mismatches"], stats["missing_in_hr"], stats["missing_in_payroll"]]
            
            # Create a colorful pie chart
            plt.figure(figsize=(10, 8))
            plt.pie(values, labels=labels, autopct="%1.1f%%", startangle=90, 
                   colors=["#ff9999","#66b3ff","#99ff99"])
            plt.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle
            
            # Add title
            plt.title("Distribution of Issues in Payroll Audit")
            
            # Add a legend
            plt.legend(loc="best")
            
            # Save the chart
            output_path = self.output_dir / f"issues_distribution_{self.timestamp}.png"
            plt.savefig(output_path)
            plt.close()
            
            logging.info(f"Summary pie chart generated: {output_path}")
            return True
            
        except Exception as e:
            logging.error(f"Error generating summary pie chart: {str(e)}")
            return False
    
    def generate_all_charts(self):
        """
        Generate all available visual reports.
        
        Executes all chart generation methods and tracks their success.
        
        Returns:
            dict: Dictionary containing the success status of each chart generation
        """
        try:
            self.set_style()
            
            # Track success of each chart generation
            results = {
                "discrepancy_bar_chart": self.generate_discrepancy_bar_chart(),
                "department_comparison_chart": self.generate_department_comparison_chart(),
                "summary_pie_chart": self.generate_summary_pie_chart()
            }
            
            # Count successful charts
            success_count = sum(1 for result in results.values() if result)
            logging.info(f"Generated {success_count} out of {len(results)} visual reports")
            
            return results
        except Exception as e:
            logging.error(f"Error generating charts: {str(e)}")
            return {"error": str(e)}


def main():
    """
    Main function to demonstrate the visual report generator.
    
    Finds the most recent audit report files and generates visual reports based on them.
    """
    import glob
    
    try:
        # Find most recent report files
        excel_files = sorted(glob.glob("output/payroll_reconciliation_report_*.xlsx"), reverse=True)
        json_files = sorted(glob.glob("output/audit_summary_*.json"), reverse=True)
        
        if not excel_files or not json_files:
            print("No audit report files found. Please run payroll_reconciliation.py first.")
            return
            
        # Use the most recent files
        excel_report = excel_files[0]
        json_summary = json_files[0]
        
        print(f"Generating visual reports from:\n- {excel_report}\n- {json_summary}")
        
        # Create and run the visual report generator
        generator = VisualReportGenerator(excel_report, json_summary)
        if not generator.load_data():
            print("Failed to load audit data.")
            return
            
        results = generator.generate_all_charts()
        
        # Report results
        print("\nVisual Report Generation Results:")
        for chart_name, success in results.items():
            status = " Success" if success else " Failed"
            print(f"- {chart_name.replace('_', ' ').title()}: {status}")
            
        if any(results.values()):
            print(f"\nCharts saved to: {generator.output_dir}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
