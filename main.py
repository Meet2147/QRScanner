import streamlit as st
import requests
import base64

def generate_qr_code(text):
    base_url = "https://quickchart.io/qr"
    params = {"text": text}
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        return response.content

    return None

def main():
    st.title('User Details QR Code Generator')

    name = st.text_input('Enter your name:')
    age = st.number_input('Enter your age:', min_value=0, max_value=150, value=0)
    phone_number = st.text_input('Enter your phone number:')
    address = st.text_area('Enter your address:')
    dob = st.date_input('Enter your date of birth:')
    financial_planning = st.radio('Have you done financial planning?', ('Yes', 'No'))

    user_details = f"Name: {name}\nAge: {age}\nPhone Number: {phone_number}\nAddress: {address}\nDate of Birth: {dob}\nFinancial Planning: {financial_planning}"

    if st.button('Generate QR Code'):
        qr_image = generate_qr_code(user_details)

        if qr_image:
            st.image(qr_image, caption='Generated QR Code', use_column_width=False)
            st.markdown(get_binary_file_downloader_html(qr_image, 'QR_Code.png', 'Download QR Code'), unsafe_allow_html=True)
        else:
            st.warning("Failed to generate QR code. Please check your input and try again.")

def get_binary_file_downloader_html(bin_file, file_label='File', button_label='Download'):
    bin_file_b64 = base64.b64encode(bin_file).decode()
    return f'<a href="data:image/png;base64,{bin_file_b64}" download="{file_label}">{button_label}</a>'

if __name__ == '__main__':
    main()
