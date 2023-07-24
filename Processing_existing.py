import os
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
import qrcode

#Variables of the second window (from existing)
number_ext = os.environ.get("number_ext")
number_inj = os.environ.get("number_inj")
parambig2 = os.environ.get("parambig2")
paramsmall12 = os.environ.get("paramsmall12")
paramsmall22 = os.environ.get("paramsmall22")
file_path = os.environ.get("file_path")
if file_path:
    df = pd.read_csv(file_path, header=None)

    #values = ['dbgi_{:06d}'.format(first_number + i) for i in range(number)]

    # Write the values to a dataframe
    #df = pd.DataFrame({'dbgi_codes': values})

    values = df.tolist()

    # Splitting the values into groups of 80
    value_groups = [values[i:i + 80] for i in range(0, len(values), 80)]

    # Set up the PDF canvas
    pdf = canvas.Canvas("big_labels_generated.pdf", pagesize=A4)

    # Set the font size and line height
    font_size = 12
    line_height = 1.2 * font_size

    # Set the dimensions of the labels in centimeters
    label_width_cm = 3.56 * cm
    label_height_cm = 1.69 * cm

    # Set the spacing between labels
    x_spacing = label_width_cm + 0.27 * cm
    y_spacing = label_height_cm

    # Set the initial position for drawing
    x_start = 0.2  * cm
    y_start = A4[1] - 1.33 * cm

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
            pdf.drawString(pos_x + 0.55 * cm, pos_y + 0.9 * cm, value[:5])
            pdf.setFont("Helvetica", font_size)  # Reduce font size for the second line
            pdf.drawString(pos_x + 0.3 * cm, pos_y + 0.4 * cm, value[5:])

            # Draw the QR code
            qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=13.5, border=0 )
            qr.add_data(value)
            qr.make(fit=True)
            qr_img = qr.make_image(fill_color="black", back_color="white")

            # Calculate the position for drawing the QR code
            qr_pos_x = pos_x + 1.9 * cm
            qr_pos_y = pos_y + 0.2 * cm

            # Draw the QR code
            qr_img_path = "qr_code.png"
            qr_img.save(qr_img_path)
            pdf.drawInlineImage(qr_img_path, qr_pos_x, qr_pos_y, width=1.35 * cm, height=1.35 * cm)

        # Move to the next page
        pdf.showPage()

    # Save and close the PDF file
    pdf.save()

else:
    print("file_path is empty or not set. Unable to load the file.")