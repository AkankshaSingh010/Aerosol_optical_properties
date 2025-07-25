import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Set page config
st.set_page_config(
    page_title="Aerosol Optical Parameters",
    page_icon="🌍",
    layout="wide"
)

# Load and prepare the data
@st.cache_data
def load_and_prepare_data():
    # CSV file
    try:
        df = pd.read_csv('season_avg.csv')
    except FileNotFoundError:
        st.error("Error: season_avg.csv file not found. Please ensure it's uploaded.")
        return pd.DataFrame()
    
    # Add latitude and longitude coordinates for each site
    site_coordinates = {
        'AEAZ': {'Latitude': 31.0, 'Longitude': 2.0},  # Algeria
        'AUMN': {'Latitude': -35.0, 'Longitude': 149.0},  # Australia
        'BDDU': {'Latitude': 23.0, 'Longitude': 90.0},  # Bangladesh
        'BIBU': {'Latitude': 4.0, 'Longitude': 114.0},  # Brunei
        'CAHA': {'Latitude': 49.0, 'Longitude': -125.0},  # Canada
        'CASH': {'Latitude': 49.5, 'Longitude': -125.5},  # Canada
        'CHTS': {'Latitude': 39.9, 'Longitude': 116.4},  # China
        'CLST': {'Latitude': -33.9, 'Longitude': 18.4},  # South Africa
        'ETAD': {'Latitude': 9.0, 'Longitude': 40.0},  # Ethiopia
        'IDBD': {'Latitude': -6.2, 'Longitude': 106.8},  # Indonesia
        'ILHA': {'Latitude': 32.6, 'Longitude': -16.9},  # Portugal (Madeira)
        'ILNZ': {'Latitude': -36.8, 'Longitude': 174.7},  # New Zealand
        'INDH': {'Latitude': 28.6, 'Longitude': 77.2},  # India
        'INKA': {'Latitude': 28.7, 'Longitude': 77.1},  # India
        'KRSE': {'Latitude': 37.5, 'Longitude': 127.0},  # South Korea
        'KRUL': {'Latitude': 56.0, 'Longitude': 93.0},  # Russia
        'MXMC': {'Latitude': 19.4, 'Longitude': -99.1},  # Mexico
        'NGIL': {'Latitude': 9.0, 'Longitude': 8.0},  # Nigeria
        'PRFJ': {'Latitude': -22.9, 'Longitude': -43.2},  # Brazil
        'TWKA': {'Latitude': 25.0, 'Longitude': 121.5},  # Taiwan
        'TWTA': {'Latitude': 24.8, 'Longitude': 120.9},  # Taiwan
        'USNO': {'Latitude': 40.7, 'Longitude': -74.0},  # USA
        'USPA': {'Latitude': 39.9, 'Longitude': -75.2},  # USA
        'ZAJB': {'Latitude': -26.2, 'Longitude': 28.0},  # South Africa
        'ZAPR': {'Latitude': -25.7, 'Longitude': 28.2},  # South Africa
    }
    
    # Add coordinates to dataframe
    df['Latitude'] = df['Site'].map(lambda x: site_coordinates.get(x, {}).get('Latitude', 0))
    df['Longitude'] = df['Site'].map(lambda x: site_coordinates.get(x, {}).get('Longitude', 0))
    
    return df

# Load the data
df = load_and_prepare_data()

# Define optical parameters mapping
optical_parameters = {
    'b_abs_lambda': 'Absorption Coefficient (b_abs_lambda)',
    'MAC_lambda': 'MAC Lambda',
    'f_mass_EC': 'f_mass_EC',
    'Black_carbon_mass': 'Black Carbon Mass',
    'Non_Black_carbon_mass': 'Non-Black Carbon Mass',
    'b_abs_BC@550': 'b_abs_BC@550',
    'b_abs_BrC@550': 'b_abs_BrC@550'
}

# Main app
def main():
    st.title("🌍 Aerosol Optical Parameters Data Visualization")
    st.markdown("---")
    
    if df.empty:
        st.error("No data loaded. Please check your CSV file.")
        return
    
    # Create three columns for the dropdowns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("📍 Select Site")
        site_options = ['All Sites'] + sorted(df['location'].unique().tolist())
        selected_site = st.selectbox(
            "Choose a site:",
            site_options,
            key="site_selector"
        )
    
    with col2:
        st.subheader("🌤️ Select Season")
        season_options = ['All Seasons'] + sorted(df['Season'].unique().tolist())
        selected_season = st.selectbox(
            "Choose a season:",
            season_options,
            key="season_selector"
        )
    
    with col3:
        st.subheader("🔬 Select Parameter")
        selected_parameter = st.selectbox(
            "Choose an optical parameter:",
            list(optical_parameters.keys()),
            format_func=lambda x: optical_parameters[x],
            key="parameter_selector"
        )
    
    st.markdown("---")
    
    # Filter the dataframe based on selections
    filtered_df = df.copy()
    
    # Filter by site
    if selected_site != 'All Sites':
        filtered_df = filtered_df[filtered_df['location'] == selected_site]
    
    # Filter by season
    if selected_season != 'All Seasons':
        filtered_df = filtered_df[filtered_df['Season'] == selected_season]
    
    # Remove rows with missing coordinates or parameter values
    filtered_df = filtered_df.dropna(subset=['Latitude', 'Longitude', selected_parameter])
    
    # Create the map
    if len(filtered_df) > 0:
        # Handle size values (ensure positive)
        param_values = filtered_df[selected_parameter].copy()
        if param_values.min() <= 0:
            size_values = param_values - param_values.min() + 0.1
        else:
            size_values = param_values
        
        # Create the scatter mapbox
        fig = px.scatter_mapbox(
            filtered_df,
            lat="Latitude",
            lon="Longitude",
            color=selected_parameter,
            size=size_values,
            hover_name="location",
            hover_data={
                'Hemisphere': True,
                'Season': True,
                selected_parameter: ':.3f'
            },
            color_continuous_scale=px.colors.sequential.Viridis,
            size_max=15,
            zoom=1,
            title=f"{optical_parameters[selected_parameter]} - {len(filtered_df)} samples",
            mapbox_style="open-street-map",
            height=600
        )
        
        fig.update_layout(
            margin={"r": 0, "t": 50, "l": 0, "b": 0}
        )
        
        # Display the map
        st.plotly_chart(fig, use_container_width=True)
        
        # Summary statistics
        st.markdown("---")
        st.subheader("📊 Summary Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        parameter_values = filtered_df[selected_parameter]
        
        with col1:
            st.metric("Total Samples", len(filtered_df))
        
        with col2:
            st.metric(
                f"Average {optical_parameters[selected_parameter]}", 
                f"{parameter_values.mean():.3f}"
            )
        
        with col3:
            st.metric(
                f"Minimum {optical_parameters[selected_parameter]}", 
                f"{parameter_values.min():.3f}"
            )
        
        with col4:
            st.metric(
                f"Maximum {optical_parameters[selected_parameter]}", 
                f"{parameter_values.max():.3f}"
            )
        
        # Optional: Show filtered data table
        with st.expander("📋 View Filtered Data"):
            st.dataframe(
                filtered_df[['location', 'Hemisphere', 'Season', selected_parameter]].round(3),
                use_container_width=True
            )
    
    else:
        st.warning("⚠️ No data available for selected filters")
        st.info("Try selecting different options from the dropdowns above.")

# Run the app
if __name__ == "__main__":
    main()