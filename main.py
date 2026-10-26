import streamlit as st
from dotenv import load_dotenv
load_dotenv()
import weave
from src.cust_assist.database.create_tables import CreateTables
from src.cust_assist.database.insert_tables import InsertTables

weave.init(project_name="cust_assist_warranty")
from src.cust_assist.agents import Warranty


@st.cache_resource
def initialize_database():
    table=CreateTables()
    table.create()
    insert=InsertTables()
    insert.get_tables_csv()
    insert.insert_tables()

initialize_database()


st.header("Warranty Claim Assistant")
name = st.text_input("Name:", value="seema")
phone = st.text_input("Phone:", value="+91 9945166436")
email = st.text_input("Email:", value="seemaj46@gmail.com")
product_name = st.text_input("Product Name:", value="Jabra Elite 8 Active")
serial_number = st.text_input("Serial Number:", value="JAB260003917VQT")
uploaded_file = st.file_uploader("Upload Image of the product:", type=['png', 'jpg', 'jpeg'])
text_area = st.text_area("Describe Your Issue:", value="earphone not working")

if st.button("Submit"):
    obj = Warranty()

    image_path = None

    if uploaded_file:
        image_path = f"uploads/{uploaded_file.name}"

        with open(image_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
    
    inputs = {
        "name": name,
        "product_name": product_name, 
        "email": email, 
        "phone": phone, 
        "serial_number": serial_number, 
        "description": text_area,
        "image_path" : image_path
    }
    
    with st.spinner("Working on your issue..."):
        result = obj.crew().kickoff(inputs=inputs)
        
    st.success("Claim processed successfully!")
    st.markdown(result.raw)
