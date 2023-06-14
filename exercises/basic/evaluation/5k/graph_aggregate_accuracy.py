import sys
import pandas as pd
import numpy as np
sys.path.append('../../')
from utilities.pmu_csv_parser import parse_csv_data
import matplotlib.pyplot as plt
from jpt_algo_evaluation.jpt_algo import calculate_complex_voltage, jpt_algo, phase_angle_and_magnitude_from_complex_voltage, calculate_approximation_error_statistics, calculate_angle_statistics

def extract_generated_packet_indexes(received_data_file_path):
    data = pd.read_csv(received_data_file_path)
    is_predicted_list = list(data["is_predicted"].values)
    generated_indexes = []
    for i in range(len(is_predicted_list)):
        if is_predicted_list[i]:
            generated_indexes.append(i)
    return generated_indexes

if __name__ == "__main__":
    truthy_pmu_csv_data = parse_csv_data(
        '../../pmu8_5k.csv',
        "TimeTag",
        ["Magnitude01", "Magnitude02", "Magnitude03"],
        ["Angle01", "Angle02", "Angle03"]
    )
    percent_missing = []
    received_pmu_data = [] #set of pmu data for 1 - 20% missing data
    generated_data_indexes = []
    for i in range(0, 20):
        percent_missing.append(i+1)
        received_pmu_data.append(parse_csv_data(
            "received-" + str(i + 1) + "-pct.csv",
            "index",
            ["magnitude", ],
            ["phase_angle"]
        ))
        generated_data_indexes.append(extract_generated_packet_indexes("received-" + str(i + 1) + "-pct.csv"))
    y_truthy = truthy_pmu_csv_data["magnitudes"][0]
    ang_truthy = truthy_pmu_csv_data["phase_angles"][0]
    
    complex_truthy = []
    for i in range(len(y_truthy)):
        complex_truthy.append(calculate_complex_voltage(y_truthy[i], ang_truthy[i]))

    avg_error_set = []
    avg_angle_error_set = []
    
    for i in range(len(received_pmu_data)):
        y_received = received_pmu_data[i]["magnitudes"][0]
        complex_received = []
        for j in range(len(y_received)):
            complex_received.append(calculate_complex_voltage(y_received[j], received_pmu_data[i]["phase_angles"][0][j]))
        average, std_dev, max_error = calculate_approximation_error_statistics(y_truthy, y_received, generated_data_indexes[i])
        avg_error_set.append(average)
        avg_ang, std_dev_ang, max_erro_ang = calculate_angle_statistics(complex_truthy, complex_received, generated_data_indexes[i])
        avg_angle_error_set.append(avg_ang)

    fig, ax = plt.subplots(2, 1, figsize=(10, 10))
    
    
    ax[0].scatter(percent_missing, avg_error_set, color="g", label="actual", s=5)
    a, b = np.polyfit(percent_missing, avg_error_set, 1)
    ax[0].set_title("Average Approximation Error (Magnitude)  vs. % Missing Data")
    ax[0].plot(percent_missing, a*np.array(percent_missing) + b, color="r", label="linear fit")
    ax[0].set_xlabel("% Missing Data")
    ax[0].set_ylabel("Approximation Error")
    print("Magnitude Error Linear Fit:")
    print('y = ' + str(a) + 'x + ' + str(b))
    
    
    ax[1].scatter(percent_missing, avg_angle_error_set, color="g", label="actual", s=5)
    a, b = np.polyfit(percent_missing, avg_angle_error_set, 1)
    ax[1].set_title("Average Angle Error for  vs. % Missing Data")
    ax[1].plot(percent_missing, a*np.array(percent_missing) + b, color="r", label="linear fit")
    ax[1].set_xlabel("% Missing Data")
    ax[1].set_ylabel("Angle Error")
    print("Angle Error Linear Fit:")
    print('y = ' + str(a) + 'x + ' + str(b))
    
    plt.show()



