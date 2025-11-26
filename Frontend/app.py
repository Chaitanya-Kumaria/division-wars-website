import streamlit as st
import pandas as pd
import os

# Set page config
st.set_page_config(page_title="Division Wars", layout="wide")

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
