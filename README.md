# Colab Test - VSCode Setup

This repository is a test setup for running Jupyter notebooks in VSCode with a Google Colab-like experience.

## Prerequisites

- [Visual Studio Code](https://code.visualstudio.com/)
- [Python](https://www.python.org/downloads/) (3.8 or higher)
- VSCode Extensions:
  - Python (ms-python.python)
  - Jupyter (ms-toolsai.jupyter)

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Markushenriksson13/colab_test.git
   cd colab_test
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Open in VSCode:**
   ```bash
   code .
   ```

## Testing the Setup

### Option 1: Run the Jupyter Notebook

1. Open `test_notebook.ipynb` in VSCode
2. Select your Python interpreter (the one from your virtual environment)
3. Run all cells using the "Run All" button or run them one by one
4. Verify that all cells execute without errors

### Option 2: Run the Python Test Script

```bash
python test_script.py
```

This will check your Python environment and verify that common libraries are installed.

## What's Included

- **test_notebook.ipynb**: A Jupyter notebook with test cells to verify the environment
- **test_script.py**: A Python script to check the environment setup
- **requirements.txt**: Python dependencies for data science work

## Troubleshooting

### Notebook Kernel Issues
If the notebook can't find a kernel:
1. Open the Command Palette (Ctrl+Shift+P / Cmd+Shift+P)
2. Select "Python: Select Interpreter"
3. Choose the Python from your virtual environment

### Missing Libraries
If you get import errors, ensure you've installed the requirements:
```bash
pip install -r requirements.txt
```

## Success Criteria

Your setup is working correctly if:
- ✓ The Jupyter notebook opens and runs in VSCode
- ✓ All cells in the notebook execute without errors
- ✓ The test script runs and shows your Python environment info
- ✓ You can add new cells and run code interactively

## Next Steps

Once your environment is working, you can:
- Create new notebooks for your projects
- Install additional packages as needed
- Share notebooks with collaborators
- Use VSCode's debugging features with notebooks

Enjoy your Colab-like experience in VSCode! 🚀