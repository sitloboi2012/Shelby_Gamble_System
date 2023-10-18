# Front-end

## Setup
To setup the front-end locally, follow these steps:
```
conda create --name shelby-project python=3.11
conda activate shelby-project

pip install -r app/requirements-dev.txt

pre-commit install
pre-commit run --all-files

streamlit run client/src/homepage.py
```
