import base64

import streamlit as st

import langchain_helper

def displayPDF(file):
    # Opening file from file path
    with open(file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')

    # Embedding PDF in HTML
    pdf_display =  f"""<embed
    class="pdfobject"
    type="application/pdf"
    title="Embedded PDF"
    src="data:application/pdf;base64,{base64_pdf}"
    style="overflow: auto; width: 100%; height: 100%;">"""

    # Displaying File
    st.markdown(pdf_display, unsafe_allow_html=True)

st.title("LawChain: The Future of Faster and Efficient Supplier Contracts")
option = st.radio("Choose an option:", ("Upload Files", "Use Files from S3"))
all_chunks = []

if option == "Upload Files":
    uploaded_files = st.file_uploader("Upload your PDFs", type='pdf', accept_multiple_files=True)
    if uploaded_files:
        all_chunks = langchain_helper.create_chunks_from_uploaded_docs(uploaded_files)

elif option == "Use Files from S3":
    all_chunks = langchain_helper.create_chunks_from_s3_pdfs()

if all_chunks:
    st.write(f'Processing combined text from all PDFs')
    db = langchain_helper.create_db_from_chunks(all_chunks)
    st.success("All PDFs processed")

    with st.form(key='my_form'):
        st.write("Enter details for legal contract generation:")
        Role = st.text_input("Role")
        Your_Firm = st.text_input(" Your_Firm")
        Supplier_Firm = st.text_input("Supplier_Firm")
        What_it_does = st.text_input("What_it_does")
        What_does_the_supplier_do = st.text_input("What_does_the_supplier_do")
        Scope_of_work_with_no_of_deliverables = st.text_input("Scope_of_work_with_no_of_deliverables")
        Giveproductdetails = st.text_input("Giveproductdetails")
        datesofdelivery = st.text_input("datesofdelivery")
        termsofdelivery = st.text_input("termsofdelivery")
        place = st.text_input("place")
        add_unit_cost_of_product = st.text_input("add_unit_cost_of_product")
        Delay_agreements = st.text_input("Delay_agreements")
        Mention_Your_Advance_Discounts_Policy = st.text_input("Mention_Your_Advance_Discounts_Policy")
        Mention_Supplier_Responsibilities = st.text_input("Mention_Supplier_Responsibilities")
        Add_Payment_Details = st.text_input("Add_Payment_Details")
        mention_dispute_resolution_procedure = st.text_input("mention_dispute_resolution_procedure")
        Termination_details = st.text_input("Termination_Details")

        submit_button = st.form_submit_button(label='Submit')

    if (Role and Your_Firm and Supplier_Firm and What_it_does and What_does_the_supplier_do and
            Scope_of_work_with_no_of_deliverables and Giveproductdetails and
            datesofdelivery and termsofdelivery and place and add_unit_cost_of_product and
            Delay_agreements and Mention_Your_Advance_Discounts_Policy and
            Mention_Supplier_Responsibilities and Add_Payment_Details and
            mention_dispute_resolution_procedure and Termination_details):
        response, pdf_buffer = langchain_helper.get_response_from_query(db, Role, Your_Firm, Supplier_Firm, What_it_does,
                                                            What_does_the_supplier_do,
                                                            Scope_of_work_with_no_of_deliverables, Giveproductdetails,
                                                            datesofdelivery, termsofdelivery, place,
                                                            add_unit_cost_of_product,
                                                            Delay_agreements, Mention_Your_Advance_Discounts_Policy,
                                                            Mention_Supplier_Responsibilities, Add_Payment_Details,
                                                            mention_dispute_resolution_procedure, Termination_details)
        st.text(response)
        with open('output.pdf', 'wb') as f:
            f.write(pdf_buffer.read())
        displayPDF('output.pdf')

