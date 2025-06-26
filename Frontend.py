import streamlit as st
import Backend as bk
import time

# Page configuration
st.set_page_config(
    page_title="GEN AI Project", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for dark theme with animations 
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main background with animated gradient */
    .stApp {
        background: linear-gradient(-45deg, #0f0f23, #1a1a2e, #16213e, #0f3460);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
        font-family: 'Poppins', sans-serif;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Floating particles animation */
    .particles {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 1;
    }
    
    .particle {
        position: absolute;
        width: 4px;
        height: 4px;
        background: rgba(74, 144, 226, 0.6);
        border-radius: 50%;
        animation: float 20s infinite linear;
    }
    
    @keyframes float {
        0% {
            transform: translateY(100vh) rotate(0deg);
            opacity: 0;
        }
        10% {
            opacity: 1;
        }
        90% {
            opacity: 1;
        }
        100% {
            transform: translateY(-100vh) rotate(360deg);
            opacity: 0;
        }
    }
    
    /* Main container with glassmorphism */
    .main-container {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 40px;
        margin: 20px auto;
        max-width: 800px;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);
        position: relative;
        z-index: 10;
        animation: slideUp 0.8s ease-out;
    }
    
    @keyframes slideUp {
        from {
            transform: translateY(50px);
            opacity: 0;
        }
        to {
            transform: translateY(0);
            opacity: 1;
        }
    }
    
    /* Animated title */
    .ai-title {
        font-size: 3.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 10px;
        background: linear-gradient(45deg, #4A90E2, #50C878, #FFD700, #FF6B6B);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: gradientText 4s ease-in-out infinite;
        text-shadow: 0 0 30px rgba(74, 144, 226, 0.3);
    }
    
    @keyframes gradientText {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    /* Robot emoji animation */
    .robot-emoji {
        display: inline-block;
        animation: bounce 2s infinite;
        font-size: 3.5rem;
        margin-right: 15px;
    }
    
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
        40% { transform: translateY(-10px); }
        60% { transform: translateY(-5px); }
    }
    
    /* Subtitle with typing effect */
    .subtitle {
        font-size: 1.2rem;
        color: rgba(255, 255, 255, 0.8);
        text-align: center;
        margin-bottom: 40px;
        font-weight: 300;
        animation: fadeIn 1s ease-in 0.5s both;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Input field styling */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.9) !important;
        border: 2px solid rgba(74, 144, 226, 0.5) !important;
        border-radius: 15px !important;
        color: #000000 !important;
        font-size: 1.1rem !important;
        padding: 12px 20px !important;
        transition: all 0.3s ease !important;
        backdrop-filter: blur(10px) !important;
        font-weight: 500 !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #4A90E2 !important;
        box-shadow: 0 0 20px rgba(74, 144, 226, 0.4) !important;
        transform: scale(1.02) !important;
        background: rgba(255, 255, 255, 0.95) !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: rgba(0, 0, 0, 0.6) !important;
        font-weight: 400 !important;
    }
    
    /* Input label styling */
    .stTextInput > label {
        color: rgba(255, 255, 255, 0.9) !important;
        font-size: 1.1rem !important;
        font-weight: 500 !important;
        margin-bottom: 8px !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #4A90E2, #50C878) !important;
        color: white !important;
        border: none !important;
        border-radius: 15px !important;
        padding: 12px 30px !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 8px 25px rgba(74, 144, 226, 0.3) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 12px 35px rgba(74, 144, 226, 0.4) !important;
    }
    
    .stButton > button:active {
        transform: translateY(-1px) !important;
    }
    
    /* Success message styling */
    .stSuccess {
        background: rgba(80, 200, 120, 0.15) !important;
        border: 1px solid rgba(80, 200, 120, 0.4) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(10px) !important;
        animation: slideInLeft 0.5s ease-out !important;
        color: #ffffff !important;
    }
    
    .stSuccess > div {
        color: #ffffff !important;
    }
    
    @keyframes slideInLeft {
        from { transform: translateX(-20px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    /* Warning message styling */
    .stWarning {
        background: rgba(255, 193, 7, 0.15) !important;
        border: 1px solid rgba(255, 193, 7, 0.4) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(10px) !important;
        animation: shake 0.5s ease-in-out !important;
        color: #ffffff !important;
    }
    
    .stWarning > div {
        color: #ffffff !important;
    }
    
    /* Heading (Choose Data Source) */
    h3, h4, h5, h6 {
        color: rgba(255, 255, 255, 0.95) !important;
    }

    /* Section text */
    .stMarkdown p {
        color: rgba(255, 255, 255, 0.85) !important;
    }

    /* Button text already looks good */

    
    /* Error message styling */
    .stError {
        background: rgba(220, 53, 69, 0.15) !important;
        border: 1px solid rgba(220, 53, 69, 0.4) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(10px) !important;
        color: #ffffff !important;
    }
    
    .stError > div {
        color: #ffffff !important;
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        75% { transform: translateX(5px); }
    }
    
    /* Output text styling */
    .output-container {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        margin-top: 20px;
        backdrop-filter: blur(10px);
        animation: expandIn 0.6s ease-out;
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.05rem;
        line-height: 1.6;
    }
    
    @keyframes expandIn {
        from {
            transform: scale(0.9);
            opacity: 0;
        }
        to {
            transform: scale(1);
            opacity: 1;
        }
    }
    
    /* Loading animation */
    .loading {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 20px;
    }
    
    .loading-dots {
        display: flex;
        gap: 8px;
    }
    
    .loading-dot {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background: #4A90E2;
        animation: loadingBounce 1.4s infinite ease-in-out both;
    }
    
    .loading-dot:nth-child(1) { animation-delay: -0.32s; }
    .loading-dot:nth-child(2) { animation-delay: -0.16s; }
    
    @keyframes loadingBounce {
        0%, 80%, 100% {
            transform: scale(0);
            opacity: 0.5;
        }
        40% {
            transform: scale(1);
            opacity: 1;
        }
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-container {
            margin: 10px;
            padding: 25px;
        }
        
        .ai-title {
            font-size: 2.5rem;
        }
        
        .robot-emoji {
            font-size: 2.5rem;
        }
        
        .subtitle {
            font-size: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Floating particles
st.markdown("""
<div class="particles">
    <div class="particle" style="left: 10%; animation-delay: 0s;"></div>
    <div class="particle" style="left: 20%; animation-delay: 2s;"></div>
    <div class="particle" style="left: 30%; animation-delay: 4s;"></div>
    <div class="particle" style="left: 40%; animation-delay: 6s;"></div>
    <div class="particle" style="left: 50%; animation-delay: 8s;"></div>
    <div class="particle" style="left: 60%; animation-delay: 10s;"></div>
    <div class="particle" style="left: 70%; animation-delay: 12s;"></div>
    <div class="particle" style="left: 80%; animation-delay: 14s;"></div>
    <div class="particle" style="left: 90%; animation-delay: 16s;"></div>
</div>
""", unsafe_allow_html=True)

#for excel button
st.markdown("""
<style>
/* Match file uploader to button style */
.stFileUploader > label {
    display: flex;
    justify-content: center;
    align-items: center;
    background: linear-gradient(45deg, #4A90E2, #50C878) !important;
    color: white !important;
    border-radius: 15px !important;
    padding: 12px 30px !important;
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 8px 25px rgba(74, 144, 226, 0.3) !important;
    cursor: pointer !important;
    text-align: center !important;
    height: 42px;
}

/* Hide the file name text below uploader */
.stFileUploader .uploadedFileName {
    display: none;
}
</style>
""", unsafe_allow_html=True)


# Main container
with st.container():
    st.markdown("""
        <div class="main-container">
            <h1 class="ai-title">
                <span class="robot-emoji">🤖</span>AskYourData
            </h1>
            <p class="subtitle">✨ Enter your query and let AI do the magic! ✨</p>
        </div>
    """, unsafe_allow_html=True)

    # --- Choose Data Source Section ---
    st.markdown("""
        <h3 style="color: white; margin-bottom: 10px;">🔗 Choose Data Source</h3>
        <p style="color: white; font-size: 1rem; margin-top: -10px;">Select data source:</p>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        use_db = st.button("🛢️ Use MySQL Database", use_container_width=True)
    with col2:
        use_csv = st.button("📄 Generate Sample Data (CSV)", use_container_width=True)
    with col3:
        upload_excel = st.button("📁 Upload Excel File Here", use_container_width=True)

    # Keep track of user selection
    if "data_source" not in st.session_state:
        st.session_state.data_source = None

    if use_db:
        st.session_state.data_source = "mysql"
    elif use_csv:
        st.session_state.data_source = "csv"
    elif upload_excel:
        st.session_state.data_source = "excel"


    # Show fields based on choice
    if st.session_state.data_source == "mysql":
        st.markdown("<h4 style='color:white;'>🛠️ Enter MySQL Connection Details</h4>", unsafe_allow_html=True)
        host = st.text_input("Host", value="localhost")
        port = st.text_input("Port", value="3306")
        user = st.text_input("Username")
        password = st.text_input("Password", type="password")
        database = st.text_input("Database Name")
        
        if st.button("Connect to MySQL"):
            bk.load_sales_df_from_mysql(host, port, user, password, database)
            st.success(f"✅ Connected to {database} at {host}:{port}")

        df = bk.get_loaded_df()
        if df is not None:
            st.markdown("### 📄 Preview of Loaded Data:")
            st.dataframe(df.head(10), use_container_width=True)


    elif st.session_state.data_source == "csv":
        if st.button("Generate Sample Data"):
            bk.create_sample_data()
            bk.load_sales_df_from_csv()
            st.success("✅ Sample data 'sales_dataset.csv' created!")

        df = bk.get_loaded_df()
        if df is not None:
            st.markdown("### 📄 Preview of Sample Data:")
            st.dataframe(df.head(10), use_container_width=True)

    elif st.session_state.data_source == "excel":
        uploaded_file = st.file_uploader("📤 Upload your Excel file Here", type=["xlsx", "xls"])
        
        if uploaded_file:
            bk.load_sales_df_from_excel(uploaded_file)
            st.success("✅ Excel file successfully uploaded and loaded!")

        df = bk.get_loaded_df()
        if df is not None:
            st.markdown("### 📄 Preview of Uploaded Data:")
            st.dataframe(df.head(10), use_container_width=True)


    # Input and button
    user_input = st.text_input(
        "💬 What's your question for the AI?", 
        placeholder="Ask me anything... 🚀 Type your question here!",
        key="user_query",
        help="Enter your question and press the button below to get an AI response"
    )
    
    submit = st.button("🚀 Generate Response", use_container_width=True)
    
    # Handle submission
    if submit and user_input:
        st.success(f"✅ Processing: {user_input}")
        time.sleep(1)

        try:
            # Just pass the user question to backend
            pandas_code = bk.get_text_output(user_input)

            st.markdown(f"#### 🐼 Generated pandas code:\n```python\n{pandas_code}\n```")

            # Run the code and get result
            result_df = bk.run_pandas_code(pandas_code)

            if result_df is not None:
                st.markdown("### 📊 Result:")
                st.dataframe(result_df)

                csv = result_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="⬇️ Download as CSV",
                    data=csv,
                    file_name='result.csv',
                    mime='text/csv'
                )
            else:
                st.error("⚠️ Could not run pandas code. Try again.")

        except Exception as e:
            st.error(f"⚠️ Error: {str(e)}")

    elif submit:
        st.warning("⚡ Please enter a question!")

# Footer
st.markdown("""
    <div style="text-align: center; margin-top: 50px; padding: 20px;">
        <p style="color: rgba(255, 255, 255, 0.5); font-size: 0.9rem;">
            🌟 Powered by Advanced AI Technology 🌟
        </p>
    </div>
""", unsafe_allow_html=True)