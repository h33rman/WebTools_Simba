# Description:
# This file contains the Visualizer class that is used to visualize the gas data in 2D.
from  viz_tools_py import the_gaussian_kernel
import numpy as np
import matplotlib.pyplot as plt


class Visualizer:
    def __init__(self, gas_data, gas_mass, gas_hsml):
        self.gas_data = gas_data
        self.gas_mass = gas_mass
        self.gas_hsml = gas_hsml
        self.visual2d = None
        self.average_hsml = None

    def compute_simple_gauss(self, visual_size=100):  # default visual_size=100
        visual2d = np.zeros((visual_size, visual_size))
        x_range = [min(self.gas_data[0]), max(self.gas_data[0])]
        y_range = [min(self.gas_data[1]), max(self.gas_data[1])]
        x_width = x_range[1] - x_range[0]
        y_width = y_range[1] - y_range[0]

        scaler = visual_size / max(x_width, y_width)
        self.gas_hsml = self.gas_hsml * scaler # Scaling the hsml values

        self.average_hsml = np.mean(self.gas_data)

        pos_i = np.array((self.gas_data[0] - x_range[0]) / x_width * visual_size, dtype=int)
        pos_j = np.array((self.gas_data[1] - y_range[0]) / y_width * visual_size, dtype=int)

        grid_x, grid_y = the_gaussian_kernel.create_grid(_size=visual_size)

        for i in range(len(pos_i)):
            visual2d += the_gaussian_kernel.gaussian_kernel(
                pos_i[i], pos_j[i], self.gas_hsml[i], self.gas_mass[i], grid_x, grid_y)

        self.visual2d = visual2d

    def plot_visual(self, x_range, y_range):
        if self.visual2d is None:
            raise ValueError("No visualization computed! Use 'compute_simple_gauss' method first.")

        plt.figure(figsize=(10, 10))
        plt.imshow(self.visual2d.T, origin='lower', cmap='viridis',
                   extent=[x_range[0], x_range[1], y_range[0], y_range[1]])
        plt.title('Galaxy Visualization')
        plt.xlabel('X axis (kpc)')
        plt.ylabel('Y axis (kpc)')
        plt.colorbar(label='Intensity')
        plt.show()
