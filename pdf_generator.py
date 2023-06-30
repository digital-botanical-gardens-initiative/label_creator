import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Spacer
from reportlab.lib import colors
import qrcode
from io import BytesIO

# Generate the values (as shown in the previous example)
start_value = 'dbgi_000001'
n = 80  # 5 boxes horizontally * 16 boxes vertically = 80 boxes
start_number = int(start_value.split('_')[1])
values = ['dbgi_{:06d}'.format(start_number + i) for i in range(n)]

# Write the values to a CSV file
df = pd.DataFrame({'Column': values})
df.to_csv('codes.csv', index=False)

# Generate the PDF with labels
doc = SimpleDocTemplate("labels.pdf", pagesize=letter)

# Create a list to store table data
data = []

# Generate QR codes for each value and add them to the data list
for value in values:
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(value)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_buffer = BytesIO()
    qr_img.save(qr_buffer, format='PNG')
    qr_image = Image(qr_buffer)
    qr_image.drawHeight = 2.54 * cm  # 1 inch = 2.54 centimeters
    qr_image.drawWidth = 2.54 * cm  # 1 inch = 2.54 centimeters
    data.append([value, qr_image])

# Set table style
table_style = TableStyle([
    ('BACKGROUND', (0, 0), (-1, -1), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, -1), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 0), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
])

# Calculate the number of boxes horizontally and vertically
num_boxes_horizontal = 5
num_boxes_vertical = 16

# Create table and apply style
table_data = [data[i * num_boxes_horizontal:(i + 1) * num_boxes_horizontal] for i in range(num_boxes_vertical)]
table = Table(table_data, colWidths=[3.81 * cm] * num_boxes_horizontal, rowHeights=[4.06 * cm] * num_boxes_vertical)  # 1.5 inches = 3.81 centimeters, 1.6 inches = 4.06 centimeters
table.setStyle(table_style)

# Build the PDF
elements = [table]
doc.build(elements)