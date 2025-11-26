import streamlit as st
import pandas as pd
import os

# Set page config
st.set_page_config(page_title="Division Wars", layout="wide")

# Paths to data
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(BASE_DIR, '..', 'Backend')
SPORTS_DATA_DIR = os.path.join(BACKEND_DIR, 'Sports', 'SportsData')
CULTURAL_DATA_DIR = os.path.join(BACKEND_DIR, 'Cultural')

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

sports_df, cultural_df = load_overall_data()

# Calculate Final Points Table
# Assuming 'Team' is the common column
if not sports_df.empty and not cultural_df.empty:
    # Rename points columns to avoid collision
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
    available_sports = ["Throwball", "Carrom"] # Add more as needed
    selected_sport = st.selectbox("Select a Sport", available_sports)
    
    if selected_sport:
        st.subheader(f"{selected_sport} Details")
        
        # Construct paths for specific sport data
        sport_key = selected_sport.lower()
        fixtures_path = os.path.join(SPORTS_DATA_DIR, f'{sport_key}_fixtures.csv')
        points_path = os.path.join(SPORTS_DATA_DIR, f'{sport_key}_points.csv')
        results_path = os.path.join(SPORTS_DATA_DIR, f'{sport_key}_results.csv')
        
        # Create 3 columns for Fixtures, Points, Results
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

with tab2:
    st.header("Cultural Overall Standings")
    st.dataframe(cultural_df, use_container_width=True)
