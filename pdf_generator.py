import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
import qrcode

# Assuming your DataFrame is stored in a variable called 'df'
# And the column with the values is called 'value_column'

df = pd.read_csv("C:/Users/edoua/Desktop/manu.csv")

values = df['dbgi_code'].tolist()

# Splitting the values into groups of 80
value_groups = [values[i:i + 80] for i in range(0, len(values), 80)]

# Set up the PDF canvas
pdf = canvas.Canvas("output.pdf", pagesize=A4)

# Set the font size and line height
font_size = 12
line_height = 1.2 * font_size

# Set the dimensions of the labels in centimeters
label_width_cm = 3.56 * cm
label_height_cm = 1.69 * cm

# Set the spacing between labels
x_spacing = label_width_cm + 0.1 * cm # Add 0.1 cm spacing between labels horizontally
y_spacing = label_height_cm + 0.1 * cm # Add 0.1 cm spacing between labels vertically

# Set the initial position for drawing
x_start = 0.5 * cm
y_start = A4[1] - 0.5 * cm

# Iterate over the value groups
for group in value_groups:
    # Calculate the number of rows and columns needed for this group
    num_rows = (len(group) - 1) // 5 + 1
    num_cols = min(len(group), 5)

    # Calculate the total width and height needed for this group
    total_width = num_cols * x_spacing
    total_height = num_rows * y_spacing

    # Calculate the starting position for this group
    x = x_start + (A4[0] - total_width) / 2
    y = y_start - total_height

    # Iterate over the values in the group
    for i, value in enumerate(group):
        # Calculate the position for drawing the value and QR code
        pos_x = x + (i % 5) * x_spacing
        pos_y = y + (i // 5) * y_spacing

        # Draw the label text
        pdf.setFont("Helvetica", font_size)
        pdf.drawString(pos_x + 0.2 * cm, pos_y + 1.3 * cm, value[:8])
        pdf.setFont("Helvetica", font_size - 2)  # Reduce font size for the second line
        pdf.drawString(pos_x + 0.2 * cm, pos_y + 0.8 * cm, value[8:])

        # Draw the QR code
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(value)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")

        # Calculate the position for drawing the QR code
        qr_pos_x = pos_x + 0.7 * cm
        qr_pos_y = pos_y + 0.3 * cm

        # Draw the QR code
        qr_img_path = "qr_code.png"
        qr_img.save(qr_img_path)
        pdf.drawInlineImage(qr_img_path, qr_pos_x, qr_pos_y, width=1.5 * cm, height=1.5 * cm)

    # Move to the next page
    pdf.showPage()

# Save and close the PDF file
pdf.save()
