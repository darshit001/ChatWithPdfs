
# File Chat System with Multiple AI Models

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
│── main.py                      # Main script to run the Streamlit app.
│── README.md                    # Project documentation.
│── .env                          # Stores API keys and environment variables.
```

🛠️ **Technologies Used**
- **Python**: Programming language for the project.
- **Streamlit**: For the interactive web interface.
- **Langchain**: For splitting text into chunks.
- **Sentence Transformers**: For creating text embeddings.
- **Chroma**: Vector store for efficient document search.
- **Hugging Face Transformers**: For model inference (e.g., Cohere, Dolly, Phi-1_5, Bloomz, DeepSeek).
- **PyPDF2**: For PDF text extraction.
- **python-docx**: For DOCX file text extraction.
- **olefile**: For DOC file text extraction.
- **Tkinter**: For folder selection dialog.

## 📥 Installation
Clone the repository:
```bash
git clone https://github.com/your-username/FileChatSystem.git
```

Navigate to the project directory:
```bash
cd FileChatSystem
```

Install the required dependencies:
```bash
pip install -r requirements.txt
```

Set up your API keys for models (e.g., Cohere):
- Create a `.env` file in the root directory and add the necessary keys:
```bash
COHERE_API_KEY=your-cohere-api-key
```

Run the app:
```bash
streamlit run main.py
```

## 📌 Usage
1. **Select Folder**: Click on "Browse Folder" to select the folder containing your files (PDF, DOCX, TXT, DOC).
2. **Process Files**: Click on "Process Files in Folder" to extract text and generate embeddings.
3. **Ask Questions**: Once the files are processed, select the AI model and input your question.
4. **View Responses**: The system will retrieve the context from the uploaded files and generate answers based on the selected model.

### 📜 Example 
**You**:Input
Click on 'Browse Folder' and select the folder that contains PDF, TXT, DOCX, or DOC files. Then, click on 'Process Files in Folder'.
![image](https://github.com/user-attachments/assets/288e71e3-9b02-4620-80d6-63d7a3a81ab7)

**Answer**: Output
Then, click on the 'Chat with File' section, select the model of your choice, and ask a question related to the PDF. After clicking 'Submit Question', you'll receive an answer in a question-and-answer format, and all your previous questions will be displayed below. However, if you ask a question not related to the PDF, the LLM will not provide a response
![image](https://github.com/user-attachments/assets/8c0ec354-72af-4fee-b6fe-05e196d19697)


## 🤝 Contributing
Feel free to fork the repository, create issues, and submit pull requests. Contributions are always welcome!

## 📄 License
This project is licensed under the MIT License.

⭐ **Star this repo if you found it useful!**

📩 For any queries, feel free to contact me.
