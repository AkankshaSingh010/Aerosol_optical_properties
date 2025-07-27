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
    'AEAZ': {'Latitude': 24.4539, 'Longitude': 54.3773},
    'AUMN': {'Latitude': -37.81, 'Longitude': 144.96},
    'ARCB': {'Latitude': -34.6036, 'Longitude': -58.3814},  # Converted from 34°36′13″S 58°22′53″W
    'BDDU': {'Latitude': 23.7098, 'Longitude': 90.4070},   # Converted from 23°42'35" N 90°24'25" E
    'BIBU': {'Latitude': -3.3760, 'Longitude': 29.3600},   # Converted from 3°22'33.60" S 29°21'36.00" E
    'CADO': {'Latitude': 43.78, 'Longitude': -79.47},
    'CAHA': {'Latitude': 44.65, 'Longitude': -63.57},
    'CAKE': {'Latitude': 49.8831, 'Longitude': -119.4857}, # Converted from 49° 52' 59.05" N 119° 29' 8.45" W
    'CALE': {'Latitude': 49.7, 'Longitude': -112.833},
    'CASH': {'Latitude': 45.41, 'Longitude': -71.88},      # Converted from 45°24′36.00″ N 71°52′48.00″ W
    'CHTS': {'Latitude': 39.9042, 'Longitude': 116.4074},
    'CODC': {'Latitude': 3.5379, 'Longitude': -76.2972},
    'CLST': {'Latitude': -33.4375, 'Longitude': -70.65},   # Converted from 33°26′15″S 70°39′00″W
    'ETAD': {'Latitude': 9.03, 'Longitude': 38.74},       # Converted from 9°01'48" N 38°44'24" E
    'IDBD': {'Latitude': -6.9167, 'Longitude': 107.6},    # Converted from 6°55′S 107°36′E
    'ILHA': {'Latitude': 32.7940, 'Longitude': 34.9896},
    'ILNZ': {'Latitude': 31.892773, 'Longitude': 34.811272},
    'INDH': {'Latitude': 28.7041, 'Longitude': 77.1025},  # Corrected Delhi coordinates (the provided ones were same as ILNZ)
    'INKA': {'Latitude': 26.449923, 'Longitude': 80.331874},
    'KRSE': {'Latitude': 37.5667, 'Longitude': 126.9667}, # Converted from 37°34' N 126°58' E
    'KRUL': {'Latitude': 35.5372, 'Longitude': 129.3167}, # Converted from 35°32'13.99"N, 129°19'0.01"E
    'MXMC': {'Latitude': 19.4326, 'Longitude': -99.1332},
    'NGIL': {'Latitude': 8.5000, 'Longitude': 4.5500},
    'PHMO': {'Latitude': 14.6042, 'Longitude': 120.9822},
    'PRFJ': {'Latitude': 18.33, 'Longitude': -65.66},
    'SGSU': {'Latitude': 1.3521, 'Longitude': 103.8198},
    'TWKA': {'Latitude': 22.61626, 'Longitude': 120.31333},
    'TWTA': {'Latitude': 25.0478, 'Longitude': 121.5319}, # Converted from 25°2'51.94"N, 121°31'54.66"E
    'USBA': {'Latitude': 39.29, 'Longitude': -76.61},
    'USMC': {'Latitude': 37.1869, 'Longitude': -86.1011}, # Converted from 37°11′13″N 86°06′04″W
    'USPA': {'Latitude': 34.1478, 'Longitude': -118.1445},
    'VNHN': {'Latitude': 21.0278, 'Longitude': 105.8342},
    'ZAJB': {'Latitude': -26.11, 'Longitude': 28.058},     # Converted from 26°06′36.00″ S 28°03′28.80″ E
    'ZAPR': {'Latitude': -25.75, 'Longitude': 28.2167},
    'USNO': {'Latitude': 35.2216, 'Longitude': -97.4446} # 35.2216° N, 97.4446° W
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
