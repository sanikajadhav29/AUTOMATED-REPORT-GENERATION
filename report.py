import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from fpdf import FPDF
import numpy as np

# Step 1: Read Data from CSV
def read_data(file_path):
    df = pd.read_csv(file_path)
    return df

# Step 2: Analyze Data
def analyze_data(df):
    summary = df.describe()
    return summary

# Step 3: Generate Visualization
def generate_chart(df, columns, output_path, bin_count=5):
    sns.set_style("whitegrid")  # Apply seaborn theme
    fig, axes = plt.subplots(1, len(columns), figsize=(10, 4))
    fig.suptitle("Data Distribution", fontsize=14, fontweight='bold')

    if len(columns) == 1:
        axes = [axes]  # Ensure axes is iterable

    colors = sns.color_palette("husl", len(columns))  # Use different colors for histograms

    for i, column in enumerate(columns):
        df[column].hist(ax=axes[i], bins=bin_count, edgecolor='black', color=colors[i])
        axes[i].set_title(column, fontsize=12, fontweight='bold')
        axes[i].set_xlabel(column, fontsize=10)
        axes[i].set_ylabel("Frequency", fontsize=10)
        axes[i].set_ylim(bottom=0)  # Explicitly set Y-axis limits

    plt.tight_layout()
    plt.savefig(output_path)  # Save the figure
    plt.close()

# Step 4: Generate PDF Report
def generate_pdf(summary, chart_path, output_pdf):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "Automated Data Report", ln=True, align="C")
    pdf.ln(10)

    # Summary Statistics
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, "Summary Statistics", ln=True)
    pdf.set_font("Arial", "", 10)

    for col in summary.columns:
        pdf.cell(0, 10, f"{col}: Mean={summary[col]['mean']:.2f}, Min={summary[col]['min']}, Max={summary[col]['max']}", ln=True)

    pdf.ln(10)

    # Add Chart
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, "Data Distribution Charts", ln=True)
    pdf.image(chart_path, x=10, y=None, w=180)

    pdf.output(output_pdf)

# Main Execution
if __name__ == "__main__":
    file_path = "sample_data.csv"  # Replace with actual file
    chart_path = "chart.png"
    output_pdf = "report.pdf"

    df = read_data(file_path)
    summary = analyze_data(df)

    # ✅ Pass the correct columns from your dataset
    columns_to_plot = ["Age", "Salary"]  # Adjust based on your dataset
    generate_chart(df, columns_to_plot, chart_path)  

    generate_pdf(summary, chart_path, output_pdf)
    
    print(f"Report generated: {output_pdf}")
