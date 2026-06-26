import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

st.set_page_config(page_title="Ticket Classifier", page_icon="🎫", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
html, body, [class*="st-"] {font-family: 'Poppins', sans-serif;}
.stApp {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    background-attachment: fixed;
}
.glass {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    padding: 2rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
}
h1, h2, h3, p, label {color: #ffffff !important;}
.stTextArea textarea, .stTextInput input {
    background: rgba(255, 255, 255, 0.15) !important;
    border: 1px solid rgba(255, 255, 255, 0.3) !important;
    color: white !important;
    border-radius: 12px !important;
}
.stButton>button {
    background: linear-gradient(90deg, #f093fb 0%, #f5576c 100%);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.6rem 1.5rem;
    font-weight: 600;
    width: 100%;
    transition: all 0.3s ease;
}
.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(245, 87, 108, 0.4);
}
.badge {
    display: inline-block;
    padding: 0.4rem 1rem;
    border-radius: 999px;
    font-weight: 600;
    font-size: 0.9rem;
    margin-top: 0.5rem;
}
.billing {background: linear-gradient(90deg, #43e97b 0%, #38f9d7 100%); color: #0f172a;}
.technical {background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%); color: #0f172a;}
.account {background: linear-gradient(90deg, #fa709a 0%, #fee140 100%); color: #0f172a;}
.general {background: linear-gradient(90deg, #a18cd1 0%, #fbc2eb 100%); color: #0f172a;}
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

prompt_template = PromptTemplate(
    input_variables=["ticket"],
    template="""Classify into one category only. Return only the name.
Categories: Billing, Technical Issue, Account Access, General Inquiry
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

COLOR_MAP = {
    "Billing": "billing",
    "Technical Issue": "technical", 
    "Account Access": "account",
    "General Inquiry": "general"
}

st.markdown('<div class="glass">', unsafe_allow_html=True)
st.title("🎫 Support Ticket Classifier")
st.write("Classify any support ticket instantly using Llama 3.1 on Groq.")
st.markdown('</div>', unsafe_allow_html=True)

col1, col2 = st.columns([1.2, 1])

with col1:
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    user_ticket = st.text_area("Enter Ticket", height=200, placeholder="Paste your support ticket here...")
    classify = st.button("Classify Ticket")
    
    if classify:
        if user_ticket:
            with st.spinner("Analyzing..."):
                response = llm.invoke(prompt_template.format(ticket=user_ticket))
                category = response.content.strip().replace("Category:", "").strip()
                css_class = COLOR_MAP.get(category, "general")
                st.markdown(f'<div class="badge {css_class}">{category}</div>', unsafe_allow_html=True)
        else:
            st.warning("Please enter a ticket first")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.subheader("Test All 10 Samples")
    run_all = st.button("Run All Tickets")
    
    if run_all:
        for i, t in enumerate(TICKETS, 1):
            response = llm.invoke(prompt_template.format(ticket=t))
            category = response.content.strip().replace("Category:", "").strip()
            css_class = COLOR_MAP.get(category, "general")
            st.markdown(f"**Ticket {i}**")
            st.markdown(f'<div class="badge {css_class}">{category}</div>', unsafe_allow_html=True)
            st.caption(t[:70] + "...")
            st.write("")
    st.markdown('</div>', unsafe_allow_html=True)