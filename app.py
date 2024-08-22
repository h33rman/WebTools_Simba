import streamlit as st
from viz_tools_py import data_loader, galaxy_selection, visualization

st.header('Galaxy Visualization Application'
          'DATA from SIMBA')
# Keep Cache
@st.cache(persist=True)

def welcome():
    return st.header('Welcome to the Galaxy Visualization App')

# Initialize DataLoader and load data
loader = data_loader.DataLoader('/home/herman/Documents/AstroData/SIMBA/snap/snap_m50n512_151',
                                '/home/herman/Documents/AstroData/SIMBA/catalogs/m50n512_151.hdf5')
snapshot_data = loader.load_snapshot()
catalog_data = loader.load_catalog()

# Combine snapshot and catalog data into a single dictionary
combined_data = {**snapshot_data, **catalog_data}

# Initialize GalaxySelector and select a galaxy
selector = galaxy_selection.GalaxySelector(combined_data)

st.sidebar.header('Galaxy Selection and Parameters')
galaxy_id = st.sidebar.number_input('Galaxy ID', min_value=0, max_value=6921, value=27)
grid_size = st.sidebar.slider('Grid Size', min_value=80, max_value= 600, value=100, step=20)

st.write(selector.select_galaxy(i_pos=galaxy_id))

gas_x, gas_y, gas_z = selector.particles_within()

# Initialize Visualizer and compute the visualization
visualizer = visualization.Visualizer(
    gas_data=(gas_x, gas_y, gas_z),
    gas_mass=snapshot_data['gas_mass'][selector.selected_index],
    gas_hsml=snapshot_data['gas_smoothing_lengths'][selector.selected_index]
)

visualizer.compute_simple_gauss(visual_size = grid_size)

# Plot the visualization
x_range = [min(gas_z), max(gas_z)]
y_range = [min(gas_y), max(gas_y)]

visualizer.plot_visual(x_range, y_range)
