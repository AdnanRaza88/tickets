import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

st.set_page_config(page_title="Ticket Classifier", page_icon="🎫", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
.stApp {
    background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
    font-family: 'Inter', sans-serif;
}
.glass-card {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 16px;
}
h1, h3, p, label, div[data-testid="stMarkdownContainer"] {color: #e2e8f0 !important;}
.stTextArea textarea {
    background: rgba(255, 255, 255, 0.08) !important;
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
    color: #f8fafc !important;
    border-radius: 12px !important;
}
.stButton>button {
    background: linear-gradient(90deg, #6366f1 0%, #8b5cf6 100%);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 600;
    width: 100%;
    padding: 0.6rem;
}
.stButton>button:hover {filter: brightness(1.1);}
.badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 999px;
    font-weight: 600;
    font-size: 0.85rem;
    margin-top: 8px;
}
.billing {background: #10b981; color: #0f172a;}
.technical {background: #38bdf8; color: #0f172a;}
.account {background: #f59e0b; color: #0f172a;}
.general {background: #a855f7; color: #ffffff;}
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_llm():
    return ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0,
        api_key=st.secrets["GROQ_API_KEY"]
    )

llm = get_llm()

template = PromptTemplate(
    input_variables=["ticket"],
    template="""Classify into exactly one category. Return only the category name.
Categories: Billing, Technical Issue, Account Access, General Inquiry
Rules: Password, Login, Hacked, Suspicious Activity = Account Access
Ticket: {ticket}
Category:"""
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

BADGE_CLASS = {
    "Billing": "billing",
    "Technical Issue": "technical", 
    "Account Access": "account",
    "General Inquiry": "general"
}

st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.title("🎫 Support Ticket Classifier")
st.caption("AI-powered classification using Llama 3.1 on Groq")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="glass-card">', unsafe_allow_html=True)
user_ticket = st.text_area("Enter Ticket", placeholder="Paste your support ticket here...", height=120, label_visibility="collapsed")
if st.button("Classify Ticket", use_container_width=True, type="primary"):
    if user_ticket:
        with st.spinner("Analyzing..."):
            res = llm.invoke(template.format(ticket=user_ticket))
            cat = res.content.strip().replace("Category:", "").strip()
            st.markdown(f'<span class="badge {BADGE_CLASS.get(cat, "general")}">{cat}</span>', unsafe_allow_html=True)
    else:
        st.warning("Please enter a ticket first")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.subheader("Sample Tickets")
if st.button("Run All 10 Tests", use_container_width=True):
    for i, t in enumerate(TICKETS, 1):
        res = llm.invoke(template.format(ticket=t))
        cat = res.content.strip().replace("Category:", "").strip()
        st.markdown(f"**Ticket {i}**")
        st.markdown(f'<span class="badge {BADGE_CLASS.get(cat, "general")}">{cat}</span>', unsafe_allow_html=True)
        st.caption(t)
st.markdown('</div>', unsafe_allow_html=True)