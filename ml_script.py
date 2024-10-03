import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress
import os

def process_csv_and_generate_graph(csv_file_path, output_folder):
    # Read CSV file
    df = pd.read_csv(csv_file_path)

    # Clean data
    df = df.iloc[2:].reset_index(drop=True)

    # List of experiments (columns in the CSV)
    namelist = ['Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4', 'Unnamed: 5']

    # Convert values to numeric
    df['Unnamed: 0'] = pd.to_numeric(df['Unnamed: 0'], errors='coerce')
    for i in namelist:
        df[i] = pd.to_numeric(df[i], errors='coerce')

    # Track total r-values for zeroth, first, and second-order reactions
    zero_sum = 0
    first_sum = 0
    second_sum = 0

    plot_filenames = []

    # Plot for each experiment
    for idx, i in enumerate(namelist):
        # Define x and y
        x = df['Unnamed: 0']
        y = df[i]

        plt.figure(figsize=(12, 4))

        # Plot raw data
        plt.subplot(1, 3, 1)
        plt.scatter(x, y, label='Raw Data')
        plt.xlabel('Time')
        plt.ylabel('Volume')
        plt.title('Raw Data')

        # Generate regression line (zeroth order)
        slope, intercept, r_value, p_value, std_err = linregress(x, y)
        plt.plot(x, slope * x + intercept, color='red', label='Regression Line')
        zero_r = r_value
        zero_sum += zero_r

        # First-order linearization
        plt.subplot(1, 3, 2)
        plt.scatter(x, np.log(y), label='Linearized (1st Order)')
        plt.xlabel('time')
        plt.ylabel('ln(volume)')
        plt.title('Linearized (1st Order)')
        slope, intercept, r_value, p_value, std_err = linregress(x, np.log(y))
        plt.plot(x, slope * x + intercept, color='red', label='Regression Line')
        first_r = r_value
        first_sum += first_r

        # Second-order linearization
        plt.subplot(1, 3, 3)
        plt.scatter(x, 1/y, label='Linearized (2nd Order)')
        plt.xlabel('Time')
        plt.ylabel('1/volume')
        plt.title('Linearized (2nd Order)')
        slope, intercept, r_value, p_value, std_err = linregress(x, 1/y)
        plt.plot(x, slope * x + intercept, color='red', label='Regression Line')
        second_r = r_value
        second_sum += second_r

        # Adjust layout and save the figure
        plt.tight_layout()

        # Unique identifier for file naming
        plot_filename = f"{os.path.basename(csv_file_path).split('.')[0]}_Reaction_{idx + 1}_plot.png"
        plot_path = os.path.join(output_folder, plot_filename)
        
        # Save the figure to the output folder
        plt.savefig(plot_path)
        plt.close()

        plot_filenames.append(plot_filename)

    average_zero_r = zero_sum / len(namelist)
    average_first_r = first_sum / len(namelist)
    average_second_r = second_sum / len(namelist)

    return plot_filenames, (average_zero_r, average_first_r, average_second_r)
