# 📝 Jupyter Notebook Helper

Hi! Welcome to my Jupyter Notebook Helper project.  
As I often work with Jupyter notebooks, I created this project to leverage LLMs to help with some repetitive tasks I frequently encounter (after experimenting with ChatGPT). For instance:  

- 🗂️ **Summarizing** the content of a notebook  
- 🧹 **Cleaning** a notebook: if a notebook is messy, generate a draft of a cleaned-up version  
- 🛠️ **Modularizing**: when it makes sense, convert a notebook into a draft of a structured Python project  

## 🚀 Project Description

The Jupyter Notebook Helper is built around a modular Python backend that leverages OpenAI’s GPT models to process notebooks. Notebooks are parsed into markdown and code cells, converted into text for AI processing, and then transformed based on the selected task.  

Processed notebooks can be regenerated as cleaned notebooks or structured Python projects. Modularized projects are created from a dictionary mapping file paths to content, with directories and files automatically generated and packaged as a zip.  

The Gradio frontend provides an interactive web interface for uploading notebooks, running processing functions, and downloading results. The code is designed for clarity, modularity, and easy extension for additional notebook-related tasks.


## ⚙️ Running the project

### 1️⃣ Clone the Repository
```
git clone https://github.com/your-username/jupyter-processor.git  
cd jupyter-processor
```

### 2️⃣ Install Dependencies
`pip install -r requirements.txt`

### 3️⃣ Set Up OpenAI API Key
Create a .env file in the project root and add your API key:  
`API_KEY=your_openai_api_key_here`

## ▶️ Usage

Run the Gradio Web App:  
`python src/main.py`

Then click on the link to use the app in your browser 🌐.  
