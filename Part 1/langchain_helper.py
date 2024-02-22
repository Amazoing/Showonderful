import os

import boto3
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import io
import fitz
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def create_pdf(output_data):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    Story = []
    styles = getSampleStyleSheet()
    lines = output_data.split('\n')
    for line in lines:
        Story.append(Paragraph(line, styles['Normal']))
        Story.append(Spacer(1, 12))
    doc.build(Story)
    buffer.seek(0)

    return buffer


load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# AWS S3 configuration
aws_access_key_id = os.getenv("AWS_ACCESS_KEY")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
region_name = "us-east-1"
bucket_name = 'pdfstorageids515'
embeddings = OpenAIEmbeddings()
vector_db = ""

s3 = boto3.client('s3',
                  aws_access_key_id=aws_access_key_id,
                  aws_secret_access_key=aws_secret_access_key,
                  region_name=region_name)


def upload_to_s3(file):
    """
    Upload a file to AWS S3.
    """
    s3.upload_fileobj(file, bucket_name, file.name)


def create_chunks_from_s3_pdfs() -> FAISS:
    all_chunks = []
    for obj in s3.list_objects_v2(Bucket=bucket_name).get('Contents', []):
        # Get the object key (file name)
        object_key = obj['Key']

        # Get the object content
        response = s3.get_object(Bucket=bucket_name, Key=object_key)

        # Read the content using PyMuPDF
        pdf_content = response['Body'].read()

        # Create a BytesIO object
        pdf_file = BytesIO(pdf_content)

        # Create a PDF document object
        doc = fitz.open(stream=pdf_file, filetype="pdf")

        # Extract text from each page
        extracted_text = "".join([doc[page_number].get_text() for page_number in range(doc.page_count)])

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_text(text=extracted_text)
        all_chunks.extend(chunks)
    return all_chunks


def create_chunks_from_uploaded_docs(uploaded_files):
    all_chunks = []
    for uploaded_file in uploaded_files:
        if uploaded_file:
            # upload_to_s3(uploaded_file)
            pdf_file = BytesIO(uploaded_file.read())
            doc = fitz.open(stream=pdf_file, filetype="pdf")
            extracted_text = "".join([doc[page_number].get_text() for page_number in range(doc.page_count)])
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            chunks = text_splitter.split_text(text=extracted_text)
            all_chunks.extend(chunks)
    return all_chunks


def create_db_from_chunks(chunks) -> FAISS:
    db = FAISS.from_texts(chunks, embeddings)
    return db


def get_response_from_query(db, Role, Your_Firm, Supplier_Firm, What_it_does, What_does_the_supplier_do,
                            Scope_of_work_with_no_of_deliverables, Giveproductdetails,
                            datesofdelivery, termsofdelivery, place, add_unit_cost_of_product,
                            Delay_agreements, Mention_Your_Advance_Discounts_Policy,
                            Mention_Supplier_Responsibilities, Add_Payment_Details,
                            mention_dispute_resolution_procedure, Termination_details,
                            k=4):
    """
    text-davinci-003 can handle up to 4097 tokens. Setting the chunksize to 1000 and k to 4 maximizes
    the number of tokens to analyze.
    """

    docs = db.similarity_search(
        f'{Role} {What_it_does} {What_does_the_supplier_do} {Scope_of_work_with_no_of_deliverables} {Giveproductdetails}',
        k=k)
    docs_page_content = " ".join([d.page_content for d in docs])

    chat = ChatOpenAI()

    prompt2 = ChatPromptTemplate.from_template("using the example of {docs_page_content} how purchase contracts are built. build purchase contract using the following data not the example I am the {Role} of the company. Generate a purchase contract between {"
                 "Your_Firm} and it manufactures {What_it_does} and {Supplier_Firm} and the supplier manufactures{What_does_the_supplier_do}. The scope of work includes {"
                 "Scope_of_work_with_no_of_deliverables}.The product {Giveproductdetails} and the job of your supplier is to "
                 "deliver the products within a date of delivery are {datesofdelivery} and terms of delivery are {termsofdelivery}. Please calculate the price "
                 "with tax of {place} accordingly and the  cost per unit is {add_unit_cost_of_product}.  Please add "
                 "the delay agreements where the delay agreements are {Delay_agreements} and advance discounts which are {"
                 "Mention_Your_Advance_Discounts_Policy}  too with comprehensive details according to your estimates. "
                 "Please write the Supplier's responsibility which are {Mention_Supplier_Responsibilities} in "
                 "comprehensive manner along with the firm's responsibility of the payment in detail which are {"
                 "Add_Payment_Details}. Please give a comprehensive documentation on dispute resolution which are {"
                 "mention_dispute_resolution_procedure} and add the termination of clause in details which are {"
                 "Termination_details}. create a very detailed contract and carry out all the necessary details and the calculation.")

    print(prompt2)

    prompt2_text = prompt2.format_messages(Role=Role, Your_Firm=Your_Firm, What_it_does=What_it_does, Supplier_Firm=Supplier_Firm,
                         What_does_the_supplier_do=What_does_the_supplier_do,
                         Scope_of_work_with_no_of_deliverables=Scope_of_work_with_no_of_deliverables,
                         Giveproductdetails=Giveproductdetails, datesofdelivery=datesofdelivery,
                         termsofdelivery=termsofdelivery, place=place,
                         add_unit_cost_of_product=add_unit_cost_of_product,
                         Delay_agreements=Delay_agreements,
                         Mention_Your_Advance_Discounts_Policy=Mention_Your_Advance_Discounts_Policy,
                         Mention_Supplier_Responsibilities=Mention_Supplier_Responsibilities,
                         Add_Payment_Details=Add_Payment_Details,
                         mention_dispute_resolution_procedure=mention_dispute_resolution_procedure,
                         Termination_details=Termination_details, docs_page_content=docs_page_content)


    response = chat(prompt2_text)

    # llm = OpenAI(temperature=0.7, max_tokens = 3500, openai_api_key=openai_api_key)
    #
    #
    #
    #
    # prompt = PromptTemplate(
    #     input_variables=['Role', 'Your_Firm', 'Supplier_Firm', 'What_it_does', 'What_does_the_supplier_do',
    #                      'Scope_of_work_with_no_of_deliverables', 'Giveproductdetails', 'datesofdelivery',
    #                      'termsofdelivery', 'add_unit_cost_of_product', 'Delay_agreements',
    #                      'Mention_Your_Advance_Discounts_Policy', 'Mention_Supplier_Responsibilities',
    #                      'Add_Payment_Details', 'mention_dispute_resolution_procedure', 'Termination_details',
    #                      'docs_page_content'],
    #     template="I am the {Role} of the company. Generate a purchase contract between {"
    #              "Your_Firm} and it manufactures {What_it_does} and {Supplier_Firm} and the supplier manufactures{What_does_the_supplier_do}. The scope of work includes {"
    #              "Scope_of_work_with_no_of_deliverables}.The product {Giveproductdetails} and the job of your supplier is to "
    #              "deliver the products within a date of delivery are {datesofdelivery} and terms of delivery are {termsofdelivery}. Please calculate the price "
    #              "with tax of {place} accordingly and the  cost per unit is {add_unit_cost_of_product}.  Please add "
    #              "the delay agreements where the delay agreements are {Delay_agreements} and advance discounts which are {"
    #              "Mention_Your_Advance_Discounts_Policy}  too with comprehensive details according to your estimates. "
    #              "Please write the Supplier's responsibility which are {Mention_Supplier_Responsibilities} in "
    #              "comprehensive manner along with the firm's responsibility of the payment in detail which are {"
    #              "Add_Payment_Details}. Please give a comprehensive documentation on dispute resolution which are {"
    #              "mention_dispute_resolution_procedure} and add the termination of clause in details which are {"
    #              "Termination_details}. create a very detailed contract and carry out all the necessary details and the calculation"
    # )
    #
    # chain = LLMChain(llm=llm, prompt=prompt)
    #
    # response = chain.run(Role=Role, Your_Firm=Your_Firm, What_it_does=What_it_does, Supplier_Firm=Supplier_Firm,
    #                      What_does_the_supplier_do=What_does_the_supplier_do,
    #                      Scope_of_work_with_no_of_deliverables=Scope_of_work_with_no_of_deliverables,
    #                      Giveproductdetails=Giveproductdetails, datesofdelivery=datesofdelivery,
    #                      termsofdelivery=termsofdelivery, place=place,
    #                      add_unit_cost_of_product=add_unit_cost_of_product,
    #                      Delay_agreements=Delay_agreements,
    #                      Mention_Your_Advance_Discounts_Policy=Mention_Your_Advance_Discounts_Policy,
    #                      Mention_Supplier_Responsibilities=Mention_Supplier_Responsibilities,
    #                      Add_Payment_Details=Add_Payment_Details,
    #                      mention_dispute_resolution_procedure=mention_dispute_resolution_procedure,
    #                      Termination_details=Termination_details, docs_page_content=docs_page_content)
    # response = response.replace("Document(page_content=", "")
    # response = response.replace("),", ",")
    pdf_buffer = create_pdf(response.content)
    return response, pdf_buffer
