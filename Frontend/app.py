import streamlit as st
import pandas as pd
import os

# Set page config
st.set_page_config(page_title="Division Wars", layout="wide", page_icon="🏆", initial_sidebar_state="expanded")

# Custom CSS for Aggressive Tournament Theme
st.markdown("""
<style>
    /* Color Variables */
    :root {
        --primary-purple: #7B2CBF;
        --light-purple: #C77DFF;
        --primary-orange: #FF6B35;
        --light-orange: #F77F00;
        --neon-purple: #B537F2;
        --neon-orange: #FF8C42;
    }
    
    /* FORCE DARK THEME */
    .stApp {
        background: #0d0d0d !important;
        color: #ffffff !important;
    }
    
    /* Main Background */
    .main {
        background: linear-gradient(135deg, #0d0d0d 0%, #1a1a1a 50%, #0d0d0d 100%) !important;
    }
    
    /* Headers with Aggressive Neon Gradient */
    h1 {
        background: linear-gradient(90deg, var(--neon-purple) 0%, var(--neon-orange) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 900 !important;
        font-size: 4rem !important;
        text-align: center;
        padding: 1.5rem 0;
        text-transform: uppercase;
        letter-spacing: 4px;
        filter: drop-shadow(0 0 20px rgba(181, 55, 242, 0.8));
    }
    
    h2 {
        color: var(--neon-orange) !important;
        font-weight: 800 !important;
        border-bottom: 4px solid var(--neon-purple);
        padding-bottom: 0.8rem;
        margin-top: 2rem;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    h3 {
        color: var(--light-purple) !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Enforce white text everywhere */
    p, span, div, label, li {
        color: #ffffff !important;
    }
    
    /* Dataframe Styling */
    .stDataFrame {
        background: #000000 !important;
        border-radius: 8px;
        padding: 1rem;
        box-shadow: 0 0 20px rgba(255, 255, 255, 0.2);
        border: 2px solid #ffffff;
    }
    
    /* Data table cells */
    .stDataFrame table {
        background: #000000 !important;
        border-collapse: collapse;
    }
    
    .stDataFrame th {
        background: #000000 !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        border: 1px solid #555555;
    }
    
    .stDataFrame td {
        background: #000000 !important;
        color: #ffffff !important;
        border: 1px solid #555555;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background: #1a1a1a !important;
        padding: 1rem;
        border-radius: 8px;
        border: 2px solid var(--neon-purple);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: #252525;
        color: #ffffff !important;
        border-radius: 5px;
        padding: 1rem 2.5rem;
        font-weight: 800;
        border: 2px solid var(--primary-purple);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--neon-purple) 0%, var(--neon-orange) 100%) !important;
        color: #ffffff !important;
        border: 2px solid var(--neon-orange);
        box-shadow: 0 0 25px rgba(181, 55, 242, 0.8);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--neon-purple) 0%, var(--neon-orange) 100%) !important;
        color: #ffffff !important;
        font-weight: 800;
        border: 2px solid var(--neon-orange) !important;
        border-radius: 8px;
        padding: 0.8rem 2.5rem;
        box-shadow: 0 0 20px rgba(181, 55, 242, 0.6);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 0 30px rgba(181, 55, 242, 1);
    }
    
    /* Selectbox */
    .stSelectbox > div > div {
        background: #252525 !important;
        border: 2px solid var(--neon-purple) !important;
        border-radius: 8px;
        color: #ffffff !important;
    }
    
    .stSelectbox option {
        background: #252525 !important;
        color: #ffffff !important;
    }
    
    /* Text Input */
    .stTextInput > div > div > input {
        background: #252525 !important;
        border: 2px solid var(--primary-purple) !important;
        color: #ffffff !important;
        border-radius: 8px;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d0d0d 0%, #1a1a1a 100%) !important;
        border-right: 3px solid var(--neon-purple);
    }
    
    section[data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    
    /* Messages */
    .stSuccess {
        background: rgba(181, 55, 242, 0.2) !important;
        border-left: 5px solid var(--neon-purple) !important;
        color: #ffffff !important;
    }
    
    .stError {
        background: rgba(255, 107, 53, 0.2) !important;
        border-left: 5px solid var(--neon-orange) !important;
        color: #ffffff !important;
    }
    
    .stWarning, .stInfo {
        background: rgba(199, 125, 255, 0.2) !important;
        border-left: 5px solid var(--light-purple) !important;
        color: #ffffff !important;
    }
    
    /* Divider */
    hr {
        border-color: var(--neon-purple) !important;
        opacity: 0.8;
    }
    
    /* Column containers */
    [data-testid="column"] {
        background: rgba(26, 26, 26, 0.6);
        border-radius: 8px;
        padding: 1rem;
        border: 1px solid rgba(181, 55, 242, 0.3);
    }
    
    /* Markdown */
    .stMarkdown {
        color: #ffffff !important;
    }
    
    /* Fix for any remaining dark text */
    * {
        color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)




# Paths to data
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(BASE_DIR, '..', 'Backend')
SPORTS_DIR = os.path.join(BACKEND_DIR, 'Sports')
SPORTS_DATA_DIR = os.path.join(BACKEND_DIR, 'Sports', 'SportsData')
CULTURAL_DATA_DIR = os.path.join(BACKEND_DIR, 'Cultural')
RULES_DIR = os.path.join(BACKEND_DIR, 'Sports', 'Rules')
PASSWORDS_FILE = os.path.join(SPORTS_DIR, 'passwords.txt')

# Ensure directories exist
os.makedirs(RULES_DIR, exist_ok=True)

# Load passwords from file
def load_passwords():
    """Load sport passwords from passwords.txt"""
    passwords = {}
    if os.path.exists(PASSWORDS_FILE):
        with open(PASSWORDS_FILE, 'r') as f:
            for line in f:
                line = line.strip()
                if ':' in line:
                    sport, pwd = line.split(':', 1)
                    passwords[pwd] = sport.strip()
    return passwords

# Load Overall Data
@st.cache_data
def load_overall_data():
    sports_path = os.path.join(SPORTS_DATA_DIR, 'overall_table.csv')
    cultural_path = os.path.join(CULTURAL_DATA_DIR, 'overall_points_table.csv')
    
    if os.path.exists(sports_path):
        sports_df = pd.read_csv(sports_path)
    else:
        sports_df = pd.DataFrame(columns=['Team', 'Points'])
        
    if os.path.exists(cultural_path):
        cultural_df = pd.read_csv(cultural_path)
    else:
        cultural_df = pd.DataFrame(columns=['Team', 'Points'])
        
    return sports_df, cultural_df

# Authentication
def check_password():
    """Returns `True` if the user had the correct password."""
    passwords = load_passwords()

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        entered_pwd = st.session_state["password"]
        if entered_pwd in passwords:
            st.session_state["password_correct"] = True
            sport = passwords[entered_pwd]
            # Store authorized sports
            if sport == "admin":
                st.session_state["authorized_sports"] = ["Throwball", "Badminton"]  # All sports
            else:
                st.session_state["authorized_sports"] = [sport.title()]
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.sidebar.text_input(
            "Admin Login", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.sidebar.text_input(
            "Admin Login", type="password", on_change=password_entered, key="password"
        )
        st.sidebar.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        authorized = st.session_state.get("authorized_sports", [])
        st.sidebar.success(f"✅ Logged in as: {', '.join(authorized)}")
        if st.sidebar.button("Logout"):
             st.session_state["password_correct"] = False
             if "authorized_sports" in st.session_state:
                 del st.session_state["authorized_sports"]
             st.rerun()
        return True

# Admin Interface
def admin_interface():
    st.title("Admin Portal 🛠️")
    
    # Get authorized sports for this user
    authorized_sports = st.session_state.get("authorized_sports", [])
    
    if not authorized_sports:
        st.warning("No sports authorized for your account.")
        return
    
    available_sports = authorized_sports
    selected_sport = st.selectbox("Select Sport to Edit", available_sports)
    
    if selected_sport:
        sport_key = selected_sport.lower()
        
        # Tabs for editing
        tab_fixtures, tab_results, tab_points, tab_rules = st.tabs(["Fixtures", "Results", "Points", "Rules"])
        
        with tab_fixtures:
            st.subheader(f"Edit {selected_sport} Fixtures")
            fixtures_path = os.path.join(SPORTS_DATA_DIR, f'{sport_key}_fixtures.csv')
            if os.path.exists(fixtures_path):
                df = pd.read_csv(fixtures_path)
                edited_df = st.data_editor(df, num_rows="dynamic")
                if st.button("Save Fixtures"):
                    edited_df.to_csv(fixtures_path, index=False)
                    st.success("Fixtures saved!")
            else:
                st.warning(f"No fixtures file found at {fixtures_path}")

        with tab_results:
            st.subheader(f"Edit {selected_sport} Results")
            results_path = os.path.join(SPORTS_DATA_DIR, f'{sport_key}_results.csv')
            if os.path.exists(results_path):
                df = pd.read_csv(results_path)
                edited_df = st.data_editor(df, num_rows="dynamic")
                if st.button("Save Results"):
                    edited_df.to_csv(results_path, index=False)
                    st.success("Results saved!")
            else:
                st.warning(f"No results file found at {results_path}")
                
        with tab_points:
            st.subheader(f"Edit {selected_sport} Points")
            points_path = os.path.join(SPORTS_DATA_DIR, f'{sport_key}_points.csv')
            if os.path.exists(points_path):
                df = pd.read_csv(points_path)
                edited_df = st.data_editor(df, num_rows="dynamic")
                if st.button("Save Points"):
                    edited_df.to_csv(points_path, index=False)
                    st.success("Points saved!")
            else:
                st.warning(f"No points file found at {points_path}")

        with tab_rules:
            st.subheader(f"Edit {selected_sport} Rules")
            rules_path = os.path.join(RULES_DIR, f'{sport_key}_rules.txt')
            
            current_rules = ""
            if os.path.exists(rules_path):
                with open(rules_path, "r") as f:
                    current_rules = f.read()
            
            new_rules = st.text_area("Rules Content", value=current_rules, height=300)
            if st.button("Save Rules"):
                with open(rules_path, "w") as f:
                    f.write(new_rules)
                st.success("Rules saved!")

# Main App Logic
if check_password():
    admin_interface()
else:
    # User Interface
    sports_df, cultural_df = load_overall_data()

    # Calculate Final Points Table
    if not sports_df.empty and not cultural_df.empty:
        s_df = sports_df[['Team', 'Points']].rename(columns={'Points': 'Sports Points'})
        c_df = cultural_df[['Team', 'Points']].rename(columns={'Points': 'Cultural Points'})
        
        final_df = pd.merge(s_df, c_df, on='Team', how='outer').fillna(0)
        final_df['Total Points'] = final_df['Sports Points'] + final_df['Cultural Points']
        final_df = final_df.sort_values(by='Total Points', ascending=False).reset_index(drop=True)
    else:
        final_df = pd.DataFrame(columns=['Team', 'Total Points'])

    # Title
    st.title("🏆 Division Wars 2025")

    # Final Points Table
    st.subheader("Final Points Table")
    st.dataframe(final_df, use_container_width=True)

    # Tabs
    tab1, tab2 = st.tabs(["🏅 Sports", "🎭 Cultural"])

    with tab1:
        st.header("Sports Overall Standings")
        st.dataframe(sports_df, use_container_width=True)
        
        st.divider()
        
        # Sport Selection
        available_sports = ["Throwball", "Badminton", "Carrom"] 
        selected_sport = st.selectbox("Select a Sport", available_sports)
        
        if selected_sport:
            st.subheader(f"{selected_sport} Details")
            
            # Construct paths for specific sport data
            sport_key = selected_sport.lower()
            fixtures_path = os.path.join(SPORTS_DATA_DIR, f'{sport_key}_fixtures.csv')
            points_path = os.path.join(SPORTS_DATA_DIR, f'{sport_key}_points.csv')
            results_path = os.path.join(SPORTS_DATA_DIR, f'{sport_key}_results.csv')
            rules_path = os.path.join(RULES_DIR, f'{sport_key}_rules.txt')
            
            # Create columns
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("### 📅 Upcoming Fixtures")
                if os.path.exists(fixtures_path):
                    fixtures_df = pd.read_csv(fixtures_path)
                    st.dataframe(fixtures_df, hide_index=True)
                else:
                    st.info("No fixtures data available.")
                    
            with col2:
                st.markdown("### 📊 Points Table")
                if os.path.exists(points_path):
                    points_df = pd.read_csv(points_path)
                    st.dataframe(points_df, hide_index=True)
                else:
                    st.info("No points data available.")
                    
            with col3:
                st.markdown("### 🏆 Results")
                if os.path.exists(results_path):
                    results_df = pd.read_csv(results_path)
                    st.dataframe(results_df, hide_index=True)
                else:
                    st.info("No results data available.")
            
            st.divider()
            st.markdown("### 📜 Rules")
            if os.path.exists(rules_path):
                with open(rules_path, "r") as f:
                    rules_content = f.read()
                st.markdown(rules_content)
            else:
                st.info("No rules available for this sport.")

    with tab2:
        st.header("Cultural Overall Standings")
        st.dataframe(cultural_df, use_container_width=True)
