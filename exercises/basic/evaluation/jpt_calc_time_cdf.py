import sys
sys.path.append('../')
from utilities.pmu_csv_parser import parse_csv_data
import pandas as pd
import matplotlib.pyplot as plt
from jpt_algo_evaluation.jpt_algo import calculate_complex_voltage, calculate_angle_statistics, calculate_approximation_error_statistics
import numpy as np
if __name__ == "__main__":
    with open('avg_jpt_exec_time.txt') as file:
        lines = [line.rstrip() for line in file]
        lines = list(map(lambda x: float(x.split("AVERAGE JPT TIME: ")[1]), lines))
    #plt.hist(lines, bins=20, cumulative=True, density=True, histtype='step', label='CDF')
    plt.plot(np.sort(lines), np.linspace(0, 1, len(lines)), '--k', color='red', label='Curved CDF')
    plt.xlabel('Local Controller Compuatation Time')
    plt.ylabel('Cumulative Probability')
    plt.title('Local Controller Computation Time CDF')

    # Show the legend

    # Display the plot
    plt.grid()
    plt.show()
    
    






