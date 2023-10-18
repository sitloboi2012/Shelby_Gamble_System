# Shelby Gamble System

This is the repository for LostD team for the Shelby Gamble System project. The project aims to create an AI-powered system that able to make prediction and inference about the market price and recommend user to buy or sell on a specific of time frame.

## Setup
Please refer to `app` and `client` folder for more information.

Some files you need to change and replace the info before running the code:
- Create a folder at the parent path, `.streamlit/secrets.toml` and `app/local.env`
- Check shared folder on GDrive for API KEY for specific key information like FinnHub or AWS.
- With `.streamlit/secrets.toml`, the format of the file would be `NAME = "API_KEY"`
- With `app/local.env`, the format of the file would be `NAME = API_KEY`

## Folder Structure
```
\app: folder contains the back-end api of the web-app
\client: folder contains the front-end of the web-app
.gitignore: basic .gitignore file
.pre-commit-config.yaml: the configuration of pre-commit
```
