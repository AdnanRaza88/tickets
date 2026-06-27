import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Ticket Classifier", page_icon="🎫", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
html, body, [class*="st-"] {font-family: 'Poppins', sans-serif;}
.stApp {background: #f1f5f9;}
.block-container {padding-top: 2rem; max-width: 700px;}
.main-container {
    background: #ffffff;
    border-radius: 20px;
    padding: 32px 28px;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
}
h1 {color: #1e293b !important; font-weight: 700; font-size: 1.8rem;}
.stTextArea textarea {
    background: #f8fafc !important;
    border: 1.5px solid #e2e8f0 !important;
    color: #1e293b !important;
    border-radius: 12px !important;
}
.stButton>button {
    background: #6366f1; color: white; border: none; border-radius: 12px;
    font-weight: 600; width: 100%; padding: 0.8rem; font-size: 15px;
}
.stButton>button:hover {background: #4f46e5;}
hr {margin: 24px 0; border: none; border-top: 1px solid #e2e8f0;}
.result-pill {
    display: inline-block; padding: 8px 18px; border-radius: 999px;
    font-weight: 700; font-size: 0.9rem; margin-top: 12px;
}
.billing {background: #ecfdf5; color: #065f46; border: 1px solid #a7f3d0;}
.technical {background: #eff6ff; color: #1e40af; border: 1px solid #bfdbfe;}
.account {background: #fffbeb; color: #92400e; border: 1px solid #fde68a;}
.general {background: #f5f3ff; color: #5b21b6; border: 1px solid #c4b5fd;}
.ticket-box {background: #f8fafc; border-radius: 12px; padding: 12px; margin-top: 8px; border-left: 4px solid #6366f1;}
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_llm():
    return ChatGroq(model="llama-3.1-8b-instant", temperature=0)

llm = get_llm()

template = PromptTemplate(
    input_variables=["ticket"],
    template="""You are a professional support assistant. Classify the following ticket into exactly one of these categories:
1. Billing
2. Technical Issue
3. Account Access
4. General Inquiry

Ticket: {ticket}
Category Name:"""
)

TICKETS = [
    "I was charged twice for my monthly subscription this month. Can you please refund one of the charges?",
    "My login keeps failing with an invalid password error even though I'm sure it's correct. Help!",
    "The app crashes every time I try to upload a file. It's been happening for the last week.",
    "I forgot my password and the reset link isn't working. How do I regain access to my account?",
    "What are your pricing plans for enterprise customers? I need more details.",
    "My credit card was declined when trying to renew my subscription. Please assist.",
    "The dashboard is showing incorrect data after the recent update. Can you fix this bug?",
    "I received a notification about suspicious activity on my account. Is it hacked?",
    "How do I change my email address associated with the account?",
    "I'm interested in your services but have some questions about features before signing up."
]

BADGE_MAP = {"Billing": "billing", "Technical Issue": "technical", "Account Access": "account", "General Inquiry": "general"}

st.markdown('<div class="main-container">', unsafe_allow_html=True)

st.title("🎫 Ticket Classification")

st.markdown("<hr>", unsafe_allow_html=True)

user_ticket = st.text_area("Enter Your Support Ticket", placeholder="Paste a ticket here...", height=120)
if st.button("Classify Ticket", use_container_width=True):
    if user_ticket:
        with st.spinner("Classifying..."):
            prompt = template.format(ticket=user_ticket) 
            response = llm.invoke(prompt)
            category = response.content.strip()
            st.markdown(f'<span class="result-pill {BADGE_MAP.get(category, "general")}">{category}</span>', unsafe_allow_html=True)
    else:
        st.warning("Please enter a ticket")

st.markdown("<hr>", unsafe_allow_html=True)

st.subheader("Assignment: All 10 Sample Tickets")
if st.button("Classify All 10 Tickets", use_container_width=True):
    for i, ticket_text in enumerate(TICKETS, 1): 
        prompt = template.format(ticket=ticket_text)
        response = llm.invoke(prompt)
        category = response.content.strip()
        st.markdown(f"**Sample Support Ticket {i}** <span class='result-pill {BADGE_MAP.get(category, 'general')}'>{category}</span>", unsafe_allow_html=True)
        st.markdown(f'<div class="ticket-box">{ticket_text}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
