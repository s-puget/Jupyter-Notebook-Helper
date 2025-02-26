import nbformat
import re
import ast
import os
import shutil

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY")

from prompts import *


def load_notebook(file_path):
    """Load a Jupyter notebook from a file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return nbformat.read(f, as_version=4)


def extract_cells(notebook):
    """Extract markdown and code cells from a notebook."""
    return [(cell['cell_type'], cell['source']) for cell in notebook['cells'] if cell['cell_type'] in ['markdown', 'code']]


def cells_to_text(cells):
    """Generate a textual summary of the notebook."""
    return "\n".join(f'\n"""\n{cell[1]}\n"""\n' if cell[0] == 'markdown' else cell[1] for cell in cells)


def file_to_text(file_path):
    """Convert the notebook file into a string summary."""
    notebook = load_notebook(file_path)
    cells = extract_cells(notebook)
    return cells_to_text(cells)


def summarize(file_path):
    """Summarize the content of a Jupyter notebook."""
    notebook_code = file_to_text(file_path)
    client = OpenAI()  # Replace with a secure method to load API keys
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt_summarize},
            {"role": "user", "content": notebook_code}
        ]
    )
    return completion.choices[0].message.content


def create_notebook_from_cells(cell_list, output_filename):
    """Create a Jupyter notebook from a list of markdown and code cells."""
    nb = nbformat.v4.new_notebook()
    for cell in cell_list:
        if cell['type'] == 'markdown':
            nb.cells.append(nbformat.v4.new_markdown_cell(cell['content']))
        elif cell['type'] == 'code':
            nb.cells.append(nbformat.v4.new_code_cell(cell['content']))
    with open(output_filename, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
    print(f"File {output_filename} saved.")


def clean(file_path):
    """Clean the notebook and improve its code using AI, then return the new notebook file path."""
    print("Parsing notebook...")
    notebook_code = file_to_text(file_path)

    print("Improving code...")
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt_code_improvement},
            {"role": "user", "content": notebook_code}
        ]
    )
    improved_code = completion.choices[0].message.content

    print("Creating cells...")
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt_create_cells},
            {"role": "user", "content": improved_code}
        ]
    )
    cell_list = completion.choices[0].message.content
    cleaned_cell_list = re.sub(r'```python|```json|\n```', '', cell_list)
    final_list = ast.literal_eval(cleaned_cell_list)

    print("Creating notebook...")
    base_name = os.path.splitext(file_path)[0]
    new_file_path = f"{base_name}_updated.ipynb"
    new_file_path = f"{re.sub('.ipynb', '', file_path)}_updated.ipynb"
    create_notebook_from_cells(final_list, new_file_path)
    
    return new_file_path


def modularize(file_path):
    """Modularize the notebook into a structured Python project."""
    print("Parsing notebook...")
    notebook_code = file_to_text(file_path)
    print("Improving code...")
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt_code_improvement},
            {"role": "user", "content": notebook_code}
        ]
    )
    improved_code = completion.choices[0].message.content
    print("Modularizing code...")
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt_modularization},
            {"role": "user", "content": improved_code}
        ]
    )
    file_structure = completion.choices[0].message.content
    print("Creating folder...")
    cleaned_file_structure = re.sub(r'```python|```json|\n```', '', file_structure)
    final_file_structure = ast.literal_eval(cleaned_file_structure)
    create_project_from_dict("modularized_code", final_file_structure)
    shutil.make_archive("modularized_code", 'zip', "modularized_code")
    return "modularized_code.zip"

def create_project_from_dict(project_name, file_dict):
    """Creates a structured Python project from a dictionary."""
    if not os.path.exists(project_name):
        os.makedirs(project_name)
    for file_path, content in file_dict.items():
        full_path = os.path.join(project_name, file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
    print(f"{project_name} folder created successfully!")