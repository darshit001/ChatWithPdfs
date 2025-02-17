# Chat With Multiple PDF With 5 LLMs

📌 **Project Description**  
This project is a File Chat System that allows users to interact with multiple document formats (PDF, DOCX, TXT, DOC) using AI models. Users can ask questions based on the content of these files, and the system provides answers powered by models like Cohere, Dolly, Phi-1_5, Bloomz, and DeepSeek.

## 🚀 Features
- **File Processing**: Supports PDF, DOCX, TXT, and DOC file formats.
- **Multiple AI Models**: Allows switching between various AI models like Cohere, Dolly, Phi-1_5, Bloomz, and DeepSeek.
- **Text Chunking**: Automatically splits long text into manageable chunks for efficient querying.
- **Contextual Responses**: Uses context from the uploaded documents to answer user questions.

## 📂 Project Structure
```bash
/FileChatSystem
│── /class
│   ├── text_processing.py       # Contains functions to process text from various file formats.
│   ├── embedding_model.py       # Handles embedding creation for text chunks.
│── main.py                      # Main script to run the Streamlit app.
│── README.md                    # Project documentation.
│── .env
```
                   # Stores API keys and environment variables.
🛠️ Technologies Used
Python
Streamlit: For the interactive web interface.
Langchain: For splitting text into chunks.
Sentence Transformers: For creating text embeddings.
Chroma: Vector store for efficient document search.
Hugging Face Transformers: For model inference (e.g., Cohere, Dolly, Phi-1_5, Bloomz, DeepSeek).
PyPDF2: For PDF text extraction.
python-docx: For DOCX file text extraction.
olefile: For DOC file text extraction.
Tkinter: For folder selection dialog.

📥 Installation
Clone the repository:

```bash
Copy
Edit
git clone https://github.com/your-username/FileChatSystem.git
Navigate to the project directory:
```

```bash
Copy
Edit
cd FileChatSystem
Install the required dependencies:
```
```bash
Copy
Edit
pip install -r requirements.txt
Set up your API keys for models (e.g., Cohere):
Create a .env file in the root directory and add the necessary keys:
```
```bash
Copy
Edit
COHERE_API_KEY=your-cohere-api-key
Run the app:
```
```bash
Copy
Edit
streamlit run main.py
```

📌 Usage
Select Folder: Click on "Browse Folder" to select the folder containing your files (PDF, DOCX, TXT, DOC).
Process Files: Click on "Process Files in Folder" to extract text and generate embeddings.
Ask Questions: Once the files are processed, select the AI model and input your question.
View Responses: The system will retrieve the context from the uploaded files and generate answers based on the selected model.
📜 Example Output
You: What is the summary of the document?
Answer: The document discusses the use of AI in various industries, focusing on healthcare, finance, and education. It explores both the opportunities and challenges posed by AI adoption.

🤝 Contributing
Feel free to fork the repository, create issues, and submit pull requests. Contributions are always welcome!

📄 License
This project is licensed under the MIT License.

⭐ Star this repo if you found it useful!

📩 For any queries, feel free to contact me.
