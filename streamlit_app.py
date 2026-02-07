import streamlit as st
import requests
from PIL import Image

# Page Configuration
st.set_page_config(page_title="Agentic Guard | Trust Command Center", layout="wide")

# Custom CSS for a professional look
st.markdown("""
    <style>
    .reportview-container { background: #f0f2f6; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; border: 1px solid #e6e9ef; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: SECURITY SCOREBOARD ---
st.sidebar.title("🛡️ Agentic Guard")
active_order = st.sidebar.selectbox("Select Active Order", ["ORD-101", "ORD-102"])

# Fetch current status for the sidebar
try:
    status_res = requests.get(f"http://localhost:8000/order/{active_order}")
    if status_res.status_code == 200:
        order_data = status_res.json()
        st.sidebar.markdown("---")
        st.sidebar.subheader("Order Status")
        
        # Color-coded status
        status_color = "🟢" if order_data['status'] == "verified" else "🔴" if order_data['status'] == "flagged" else "🟡"
        st.sidebar.metric("Current State", f"{status_color} {order_data['status'].upper()}")
        st.sidebar.progress(order_data['risk_score'] / 100)
        st.sidebar.write(f"**Buyer:** {order_data['buyer_name']}")
        st.sidebar.write(f"**Amount:** {order_data['amount']} {order_data['currency']}")
except:
    st.sidebar.error("Backend Offline")

# --- MAIN INTERFACE ---
tab1, tab2 = st.tabs(["💬 Chat Monitor", "📄 Evidence Vault"])

# --- TAB 1: CHAT MONITOR ---
with tab1:
    st.header("Real-time Chat Analysis")
    st.info("Paste the P2P chat log below to scan for policy violations.")
    chat_input = st.text_area("Chat History", placeholder="User: Let's chat on WhatsApp...", height=150)
    
    if st.button("Analyze Chat"):
        if not chat_input:
            st.warning("Please paste a chat log first.")
        else:
            with st.spinner("Agentic Guard is cross-referencing Deriv Policies..."):
                res = requests.post(f"http://localhost:8000/analyze-trade/{active_order}")
                if res.status_code == 200:
                    data = res.json()
                    
                    # CLEANED OUTPUT: Extract only the 'raw' report string
                    report = data['analysis']['raw']
                    
                    st.subheader("🛡️ Guardian Risk Report")
                    if "flagged" in data['current_status']['status']:
                        st.error(report) # Red box for violations
                    else:
                        st.success(report) # Green box for safe trades
                else:
                    st.error("Failed to reach the AI Backend.")

# --- TAB 2: EVIDENCE VAULT ---
with tab2:
    st.header("Receipt Verification")
    st.write("Upload the bank transfer screenshot provided by the buyer.")
    uploaded_file = st.file_uploader("Upload Receipt (PNG/JPG)", type=["png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        col1, col2 = st.columns(2)
        with col1:
            st.image(uploaded_file, caption="Uploaded Evidence", use_container_width=True)
        
        with col2:
            if st.button("Verify Evidence"):
                with st.spinner("Checking name and amount matches..."):
                    files = {"file": uploaded_file.getvalue()}
                    res = requests.post(f"http://localhost:8000/verify-evidence/{active_order}", files=files)
                    
                    if res.status_code == 200:
                        data = res.json()
                        st.markdown("### AI Decision")
                        if data['updated_order']['status'] == "verified":
                            st.success(data['ai_findings'])
                        else:
                            st.error(data['ai_findings'])
                        
                        with st.expander("View Raw JSON Data"):
                            st.json(data['updated_order'])
                    else:
                        st.error(f"Error: {res.status_code}")