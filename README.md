# Build a RAG to Brag About - PyCon Ireland 2024

## Description
This repository contains code and notebooks for the RAGBRAG project presented at PyCon Ireland 24. The project describes how to set up a LllamIndex RAG pipeline over a dataset of documents and various methods on how to improve its performance.

## Presentation
To run the reveal.js presentation, follow these steps:

1. Ensure you have [Node.js](https://nodejs.org/) installed on your machine.
2. Navigate to the `reveal.js/` directory:
    ```bash
    cd reveal.js
    ```
3. Install the necessary dependencies using npm:
    ```bash
    npm install
    ```
4. Start the presentation server:
    ```bash
    npm start
    ```
5. Open your web browser and go to `http://localhost:8000` to view the presentation.

## Data
Documents used for this project are UK political parties manifestos for the 2024 UK general election.

## Structure
- `notebooks/`: Contains Jupyter notebooks and utils functions for running RAG pipelines.
- `data/`: Datasets used in the project.

## Installation
To install the necessary dependencies, run(it is recommended to use a virtual environment tool such as venv):
```bash
pip install -r requirements.txt
```

## Usage
If you do not already have an OPENAI API account, you can set one up here: [OPENAI API](https://platform.openai.com/)
Create a `.env` file in this repository and add your OPENAI API key:
```
OPENAI_API_KEY=<YOUR KEY HERE>
```

To run the notebooks start Jupyter:
```bash
jupyter notebook
```

## Contact
For any questions or inquiries feel free to reach out on GitHub.
