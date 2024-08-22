import streamlit as st
from viz_tools_py import data_loader, galaxy_selection, visualization
import matplotlib.pyplot as plt

st.header('Galaxy Visualization Application - DATA from SIMBA')


# Cache the data loading to avoid reloading every time the parameters change
@st.cache_data()
def load_data(snap_path, catalog_path):
    loader = data_loader.DataLoader(snap_path, catalog_path)
    snapshot_data = loader.load_snapshot()
    catalog_data = loader.load_catalog()
    combined_data = {**snapshot_data, **catalog_data}
    return combined_data


# Load the data only once
snap_path = '/home/herman/Documents/AstroData/SIMBA/snap/snap_m50n512_151'
catalog_path = '/home/herman/Documents/AstroData/SIMBA/catalogs/m50n512_151.hdf5'

combined_data = load_data(snap_path, catalog_path)

# Sidebar for Galaxy selection and parameters
st.sidebar.header('Galaxy Selection and Parameters')
galaxy_id = st.sidebar.number_input('Galaxy ID', min_value=0, max_value=6921, value=27)
grid_size = st.sidebar.slider('Grid Size', min_value=80, max_value=600, value=100, step=20)

# Galaxy selection and visualization
selector = galaxy_selection.GalaxySelector(combined_data)
selector.select_galaxy(i_pos=galaxy_id)

gas_x, gas_y, gas_z = selector.particles_within()

visualizer = visualization.Visualizer(
    gas_data=(gas_x, gas_y, gas_z),
    gas_mass=combined_data['gas_mass'][selector.selected_index],
    gas_hsml=combined_data['gas_smoothing_lengths'][selector.selected_index]
)

# Compute Gaussian visualization
visualizer.compute_simple_gauss(visual_size=grid_size)

# Plot the visualization in the app
x_range = [min(gas_x), max(gas_x)]
y_range = [min(gas_y), max(gas_y)]


def plot_visual(visualizer, x_range, y_range):
    if visualizer.visual2d is None:
        raise ValueError("No visualization computed! Use 'compute_simple_gauss' method first.")

    plt.figure(figsize=(10, 10))
    plt.imshow(visualizer.visual2d.T, origin='lower', cmap='viridis',
               extent=[x_range[0], x_range[1], y_range[0], y_range[1]])
    plt.title('Galaxy Visualization')
    plt.xlabel('X axis (kpc)')
    plt.ylabel('Y axis (kpc)')
    plt.colorbar(label='Intensity')

    # Streamlit method to show the plot
    st.pyplot(plt)


# Call the function to display the visualization
plot_visual(visualizer, x_range, y_range)
