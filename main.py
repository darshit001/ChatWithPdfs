
import os
import uuid 
import streamlit as st 
from PyPDF2 import PdfReader 
from docx import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter 
from sentence_transformers import SentenceTransformer 
import chromadb 
import cohere 
import tkinter as tk 
from tkinter import filedialog 
import torch 
from transformers import pipeline 
import zipfile
import olefile
from dotenv import load_dotenv
import os
load_dotenv()


client = chromadb.Client()
collection = client.get_or_create_collection(name="pdf")

def get_pdf_text(pdf_folder):
    text = ""
    pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith('.pdf')]
    for pdf_file in pdf_files:
        pdf_path = os.path.join(pdf_folder, pdf_file)
        pdf_reader = PdfReader(pdf_path)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    return text

def get_txt_text(txt_folder):
    text = ""
    txt_files = [f for f in os.listdir(txt_folder) if f.endswith('.txt')]
    for txt_file in txt_files:
        txt_path = os.path.join(txt_folder, txt_file)
        with open(txt_path, 'r', encoding='utf-8') as file:
            text += file.read()
    return text

def get_docx_text(docx_folder):
    text = ""
    docx_files = [f for f in os.listdir(docx_folder) if f.endswith('.docx')]
    for docx_file in docx_files:
        docx_path = os.path.join(docx_folder, docx_file)
        doc = Document(docx_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    return text

def get_doc_text(doc_folder):
    text = ""
    doc_files = [f for f in os.listdir(doc_folder) if f.endswith('.doc')]
    for doc_file in doc_files:
        doc_path = os.path.join(doc_folder, doc_file)
        ole = olefile.OleFileIO(doc_path)
        if ole.exists('WordDocument'):
            stream = ole.openstream('WordDocument')
            content = stream.read()
            text += content.decode('utf-8', errors='ignore')
    return text

def get_text_from_files(folder_path, file_type='pdf'):
    text = ""
    if file_type == 'pdf': 
        text = get_pdf_text(folder_path)
    elif file_type == 'txt':
        text = get_txt_text(folder_path)
    elif file_type == 'docx':
        text = get_docx_text(folder_path)
    elif file_type == 'doc':
        text = get_doc_text(folder_path)
    return text

def get_text_chunks(text, chunk_size=500, chunk_overlap=100):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    return text_splitter.split_text(text)

def generate_unique_ids(chunks):
    return [str(uuid.uuid4()) for _ in range(len(chunks))]

def create_embeddings(chunks):
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    return embedding_model.encode(chunks)

def get_vector_store(chunks):
    embeddings = create_embeddings(chunks)
    ids = generate_unique_ids(chunks)
    collection.add(
        documents=chunks,
        metadatas=[{"chunk_id": i} for i in range(len(chunks))],
        embeddings=embeddings,
        ids=ids
    )

def get_best_context_from_chroma(collection, question, n_results=2):
    results = collection.query(
        query_texts=[question],
        n_results=n_results
    )
    return results['documents'][0]

def prepare_prompt(context, question):
    prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
    provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n
    Context:\n {context}?\n
    Question: \n{question}\n
    Answer:
    """
    return prompt_template.format(context=context, question=question)

def generate_response_with_cohere(prompt):
    cohere_api_key = os.getenv("COHERE_API_KEY")
    llm = cohere.Client(api_key=cohere_api_key)
    response = llm.generate(
        model="command-xlarge",
        prompt=prompt,
        max_tokens=300,
        temperature=0.1 
    )
    return response.generations[0].text.strip()

def generate_response_with_dolly(prompt):
    generate_text = pipeline(model="databricks/dolly-v2-3b", torch_dtype=torch.bfloat16, trust_remote_code=True, device_map="cpu")
    res = generate_text(prompt)
    return res[0]["generated_text"].strip()


def generate_response_with_phi(prompt):
    pipe = pipeline("text-generation", model="microsoft/phi-1_5")
    generated_text = pipe(prompt, max_length=1000, num_return_sequences=1)
    # return str(generated_text[0]['generated_text'].strip())
    answer = generated_text[0]['generated_text']
    # return str(generated_text[0]['generated_text'].strip().split('Answer:')[-1].strip())
    # answer = answer.split('Answer:')[-1].strip()
    if "Answer:" in answer:
        answer = answer.split("Answer:")[1].strip()
    return answer

def generate_response_with_bloomz(prompt):
    # prompt = f"Answer the following question as concisely as possible:\n{question}"
    pipe = pipeline("text-generation", model="bigscience/bloomz-560m")  
    generated_text = pipe(prompt, max_length=1000, num_return_sequences=1)
    return generated_text[0]['generated_text'].strip()

def generate_response_with_deepseek(prompt):
    pipe = pipeline("text-generation", model="deepseek-ai/deepseek-coder-1.3b-base")
    generated_text = pipe(prompt, max_length=1000, num_return_sequences=1)
    answer= generated_text[0]['generated_text']
    answer = answer.split('Answer:')
    return answer


def user_input(question, collection, selected_model):
    context = get_best_context_from_chroma(collection, question)
    prompt = prepare_prompt(context, question)
    
    if selected_model == "Cohere":
        final_answer = generate_response_with_cohere(prompt)
    elif selected_model == "Dolly":
        final_answer = generate_response_with_dolly(prompt)
    elif selected_model == "Phi-1_5":
        final_answer = generate_response_with_phi(prompt)
    elif selected_model == "Bloomz":
        final_answer = generate_response_with_bloomz(prompt)
    elif selected_model == "DeepSeek": 
        final_answer = generate_response_with_deepseek(prompt)
    
    return str(final_answer)

def main():
    st.set_page_config(page_title="Chat PDF, DOCX & TXT", page_icon="💁")
    st.header("Ask PDFs, DOCX, and TXT with Multiple AI Models 🤖")

    tab1, tab2 = st.tabs(["Select Files", "Chat with Files"])

    with tab1:
        st.write("### Select Folder and Upload Files")

        root = tk.Tk()
        root.withdraw()
        root.wm_attributes('-topmost', 1)
        st.write('Please select a folder:') 
        clicked = st.button('Browse Folder')

        if clicked:
            dirname = filedialog.askdirectory(master=root)
            if dirname:
                st.session_state['folder_path'] = dirname

        if 'folder_path' in st.session_state:
            dirname = st.session_state['folder_path']
            files = [file for file in os.listdir(dirname) if file.endswith('.pdf') or file.endswith('.txt') or file.endswith('.docx') or file.endswith('.doc')]
            st.session_state['files'] = files
            st.write("Files Available:")
            for file in files:
                st.write(f"- {file}")
                
            process_button = st.button("Process Files in Folder")
            if process_button:
                with st.spinner("Processing..."):
                    for file in files:
                        if file not in st.session_state.get('processed_files', []):
                            file_extension = file.split('.')[-1].lower()
                            raw_text = get_text_from_files(dirname, file_type=file_extension)
                            text_chunks = get_text_chunks(raw_text)
                            get_vector_store(text_chunks)
                            st.session_state.setdefault('processed_files', []).append(file)
                    st.session_state['collection'] = collection
                    st.success("Processing Done!")

    with tab2:
        st.write("### Chat with Files")

        if 'collection' not in st.session_state:
            st.warning("Please upload and process the files first.")
        else:
            if 'conversation_history' not in st.session_state:
                st.session_state['conversation_history'] = []
            selected_model = st.radio("Choose Model", ("Cohere", "Dolly", "Phi-1_5", "Bloomz", "DeepSeek"), horizontal=True) 
            user_question = st.text_input("Ask a Question from the Files")

            if st.button("Submit Question"):
                if user_question:
                    answer = user_input(user_question, st.session_state['collection'], selected_model)
                    st.session_state['conversation_history'].append({'question': user_question, 'answer': answer})

            for chat in st.session_state['conversation_history']:
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.markdown(f"**You:** {chat['question']}")
                with col2:
                    st.markdown(f"**Answer:** {chat['answer']}")

if __name__ == "__main__":
    main()
