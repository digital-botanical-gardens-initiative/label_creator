def main():

    import requests
    import os
    import pandas as pd
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import cm
    from reportlab.pdfgen import canvas
    import qrcode

    #Variables of the first window (generate from scratch)
    username = os.environ.get("username")
    password = os.environ.get("password")
    location = os.environ.get("location")
    storage = os.environ.get("storage")
    number = int(os.environ.get("number"))
    output_folder = os.environ.get("output_folder")

    # Check if username and password are set (not empty)
    if username and password and location and storage and number != 0 and output_folder:

        # Define the Directus base URL
        base_url = 'http://directus.dbgi.org'

        # Define the login endpoint URL
        login_url = base_url + '/auth/login'
        # Create a session object for making requests
        session = requests.Session()
        # Send a POST request to the login endpoint
        response = session.post(login_url, json={'email': username, 'password': password})
        data = response.json()['data']
        access_token = data['access_token']
        refresh_token = data['refresh_token']

        #Extract the last entry in the DBGI_SPL_ID column of the samples collection
        container_id = 'container_9x9_id'
        params = {'sort[]': f'-{container_id}'}
        collection_url = base_url + '/items/Container_9x9'
        response = session.get(collection_url, params=params)
        last_value = response.json()['data'][0][container_id]
        last_number = int(last_value.split('_')[2])

        #Define the first number of the list (last number + 1)
        first_number = last_number + 1

        # Create template dataframe to reserve labels
        row_data = {'Reserved': 'True',
                    'BG': location,
                    'box_location': storage}
        
        template = pd.DataFrame([row_data for _ in range(number)], columns=['Reserved',
                                        'BG',
                                        'box_location'])

        # Generate the container IDs
        template['container_9x9_id'] = ['container_9x9_{:06d}'.format(first_number + i) for i in range(number)]

        # Print the resulting DataFrame
        print(template)

        headers = {
                    'Content-Type': 'application/json'
        }
        
        #Create a list with the asked codes beginning with the first number
        values = ['container_9x9_{:06d}'.format(first_number + i) for i in range(number)]
        
        records = template.to_json(orient="records")
        print(records)

        #Add the codes to the database
        session.headers.update({'Authorization': f'Bearer {access_token}'})
        response = session.post(url=collection_url, headers=headers, data=records)
        print(response.json())

        # Splitting the values into groups of 80 (number of labels per page)
        value_groups = [values[i:i + 80] for i in range(0, len(values), 80)]

        # Set up the PDF canvas
        pdf_path = output_folder + "/9x9_generated.pdf"
        pdf = canvas.Canvas(pdf_path, pagesize=A4)

        # Set the font size and line height
        font_size = 7.5

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
                pdf.setFont("Helvetica-Bold", font_size)
                pdf.drawString(pos_x + 0.55 * cm, pos_y + 0.9 * cm, value[:10])
                pdf.setFont("Helvetica-Bold", font_size)  # Reduce font size for the second line
                pdf.drawString(pos_x + 0.3 * cm, pos_y + 0.4 * cm, value[10:])

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
        print("Username and/or password not set. The script will be ignored.")
    # Needs still to add the generated code on directus