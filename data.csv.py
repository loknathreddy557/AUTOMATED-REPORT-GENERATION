import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# Load CSV data
def load_data(file_path):
    return pd.read_csv(file_path)

# Generate summary statistics
def analyze_data(df):
    return df.describe()

# Create PDF report
def generate_pdf(dataframe, summary_stats, filename="report.pdf"):
    doc = SimpleDocTemplate(filename, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    # Title
    title = Paragraph("Automated Report", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 12))

    # Original Data Table
    elements.append(Paragraph("Original Data", styles['Heading2']))
    data = [list(dataframe.columns)] + dataframe.values.tolist()
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(table)
    elements.append(Spacer(1, 12))

    # Summary Stats Table
    elements.append(Paragraph("Summary Statistics", styles['Heading2']))
    summary_data = [list(summary_stats.columns.insert(0, 'Metric'))]
    for idx in summary_stats.index:
        row = [idx] + summary_stats.loc[idx].tolist()
        summary_data.append(row)
    summary_table = Table(summary_data)
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(summary_table)

    # Build PDF
    doc.build(elements)
    print(f"PDF report '{filename}' generated successfully.")

# Main driver
if _name_ == "_main_":
    df = load_data("data.csv")
    summary = analyze_data(df.select_dtypes(include=['number']))  # only numeric columns
    generate_pdf(df, summary)
