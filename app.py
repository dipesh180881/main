import streamlit as st
import sqlite3
import os
from datetime import datetime

# Ensure the "uploads" directory exists
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# Initialize database connection
conn = sqlite3.connect('ethos_contributions.db')
c = conn.cursor()

# Create table if it doesn't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS contributions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        whatsapp_number TEXT,
        gmail_id TEXT,
        building TEXT,
        flat_no TEXT,
        amount_paid REAL,
        transaction_details TEXT,
        image_path TEXT
    )
''')
conn.commit()

# List of buildings
buildings = ["Yukon", "Amazon", "Nile", "Sutlez", "Mississippi", "Thames", "Rhine"]

# Streamlit App Interface
st.title("Nyati Ethos Contribution Form 2024-25")

# Collect user input
name = st.text_input("Name")
whatsapp_number = st.text_input("WhatsApp Number")
gmail_id = st.text_input("Gmail ID")

# Building selection
building = st.selectbox("Building", buildings)

flat_no = st.text_input("Flat No")
amount_paid = st.number_input("Amount Paid", step=0.01)
transaction_details = st.text_input("Transaction Details")
image = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

# Submission button
if st.button("Submit"):
    # Handle image upload and save the path
    if image:
        # Generate a unique file name using current timestamp
        image_name = f"{name}_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
        image_path = os.path.join("uploads", image_name)
        
        # Save the uploaded image to the "uploads" directory
        with open(image_path, "wb") as f:
            f.write(image.getbuffer())

        # Insert data into the database
        c.execute('''
            INSERT INTO contributions (name, whatsapp_number, gmail_id, building, flat_no, amount_paid, transaction_details, image_path)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, whatsapp_number, gmail_id, building, flat_no, amount_paid, transaction_details, image_path))
        conn.commit()
        st.success("Data submitted successfully!")
    else:
        st.warning("Please upload an image.")

# Display the data
st.header("View Contributions")
results = c.execute("SELECT * FROM contributions").fetchall()
for row in results:
    st.write(row)
