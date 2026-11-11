# SimpleMail AI ✉️

AI-powered Thai Email Writing Assistant using OpenThaiGPT.

## About the Project

SimpleMail AI is an AI-powered application that helps users generate Thai emails from short descriptions.

Users can provide a brief message, select the email type and choose the language tone. The system then generates a complete email.

## Features

- Generate Thai emails from short descriptions
- Support formal, semi-formal and informal tones
- Support multiple email types
- Download generated emails as text files

## Technologies

- Python
- OpenThaiGPT 8B
- Hugging Face Transformers
- FastAPI
- Streamlit
- PyTorch

## System Architecture

User
  ↓
Streamlit Frontend
  ↓
FastAPI Backend
  ↓
OpenThaiGPT 8B
  ↓
Generated Email

## Project Structure

SimpleMail-AI/
- backend/
  - main.py
  - requirements.txt
- frontend/
  - app.py
  - requirements.txt
- .gitignore
- README.md

## Deployment

- Frontend: Streamlit Community Cloud
- Backend: RunPod GPU

## Developer

Created as an AI / NLP portfolio project.
