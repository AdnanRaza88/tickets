# Support Ticket Classifier

AI-powered support ticket classifier using Llama 3.1 on Groq with a glassmorphism UI.

## Run Locally
1. pip install -r requirements.txt
2. Create `.streamlit/secrets.toml` and add `GROQ_API_KEY = "sk-..."`
3. streamlit run app.py

## Deploy
Add `GROQ_API_KEY` in Streamlit Cloud > Settings > Secrets