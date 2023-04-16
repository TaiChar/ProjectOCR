import streamlit as st
import numpy as np
import pytesseract 
import re
import cv2 as cv
from PIL import Image 
import pandas as pd

#def extract_total_amount_due(output):
#    pattern = r'Total\s+amount\s+due\s+\(USD\)\s+([\d.]+)'
#    match = re.search(pattern, output)
#    if match:
#        total_amount_due = float(match.group(1))
#        return total_amount_due
#    else:
#        return None

def to_grayscale(img):
    return cv.cvtColor(np.array(img), cv.COLOR_RGB2GRAY)

def find_amounts(text):
    amounts = re.findall(r'\d+\.\d{2}\b', text)
    floats = [float(amount) for amount in amounts]
    unique = list(set(floats))
    return unique
    
def extract_company_name(text):
    pattern = r"\b[A-Z].*? Ltd\b"
    match = re.search(pattern, text)
    if match:
        return match.group(0)
    else:
        return "Company name not found"

def extract_invoice_number(text):
    invoice_no_pattern = r"Tax Invoice No\s*:\s*([^\s]+)"
    match1 = re.search(invoice_no_pattern, text)
    if match1:
        return match1.group(1)
    
    invoice_number_pattern = re.compile(r"Invoice no\.:.*?(\d+)", re.DOTALL) 
    match2 = invoice_number_pattern.search(text)
    if match2:
        return match2.group(1)
    
    return "Invoice number not found in text"


def extract_purchase_order_number(text):
    pattern = r'PORQ\d{9}'
    match = re.search(pattern, text)
    if match:
        return match.group(0)
    else:
        return "Purchase order number not found"



pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

st.title("An Invoice OCR APP")
st.text("Step 1 : Upload Invoice which contains English Text")
st.text("Step 2 : Press Extract")

upload_image=st.sidebar.file_uploader('Choose Invoice input for convertion',type=["jpg","png","jpeg"])
if upload_image is not None:
    img=Image.open(upload_image)
    #st.image(upload_image)
    with st.expander("Original", expanded=True):
         st.image(img, use_column_width=True)
    
    grayscale = st.checkbox("Convert to Grayscale")
    if grayscale:
        img = to_grayscale(img)
        img = Image.fromarray(img)
        st.image(img)

    
    if st.button("Extract Text"):
        st.write("Extracted Text")
        output_text=pytesseract.image_to_string(img)
        invoice_number = extract_invoice_number(output_text)
        poreq = extract_purchase_order_number(output_text)
        st.write(f"Purchase Order No.: {poreq}")
        st.write(f"Invoice No.: {invoice_number}")
        company = extract_company_name(output_text)
        st.write(f"Vendor Name: {company}")
        amounts = find_amounts(output_text)
        st.write(f"Total amount due (USD): {max(amounts)} USD")


        # show the image
        #with st.expander("🖼  Artwork", expanded=True):
        #st.image(img, use_column_width=True)
