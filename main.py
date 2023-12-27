import streamlit as st
from streamlit_qrcode_scanner import qrcode_scanner
import csv
from datetime import datetime
import hashlib

scanned_codes = {}

def encrypt_data(data):
    hash_object = hashlib.md5(data.encode())
    encrypted_code = hash_object.hexdigest()
    return encrypted_code

def save_to_csv(data):
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M")
    fields = data.split(",")

    name = fields[0] if len(fields) > 0 else ""
    age = fields[1] if len(fields) > 1 else ""
    gender = fields[2] if len(fields) > 2 else ""
    city = fields[3] if len(fields) > 3 else ""

    encrypted_code = encrypt_data(data)  # Generate encrypted code from scanned data

    if encrypted_code in scanned_codes:
        # Update only the out_time for the matching encrypted code
        scanned_codes[encrypted_code]["out_time"] = current_time
    else:
        # For the first scan of the QR code, add it to scanned_codes with in_time
        scanned_codes[encrypted_code] = {"in_time": current_time, "out_time": ""}

    # Read existing CSV data
    rows = []
    try:
        with open('scanned_data.csv', mode='r') as file:
            csv_reader = csv.reader(file)
            rows = list(csv_reader)
    except FileNotFoundError:
        pass

    # Update the CSV file with the updated out_time
    with open('scanned_data.csv', mode='w', newline='') as file:
        csv_writer = csv.writer(file)
        for row in rows:
            if row and row[0] == encrypted_code:  # Check if the encrypted code matches
                row[6] = current_time  # Update the out_time in the row
            csv_writer.writerow(row)
        if not any(row and row[0] == encrypted_code for row in rows):  # If code not found, add a new row
            row_data = [encrypted_code, name, age, gender, city, current_time, ""]
            csv_writer.writerow(row_data)

st.title("QR Code Scanner")

qr_code = qrcode_scanner()

if qr_code:
    st.write("Scanned Data:", qr_code)
    save_to_csv(qr_code)
    st.success("Data saved to CSV!")
