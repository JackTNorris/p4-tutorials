import sys
import pandas as pd
import numpy as np
sys.path.append('../../')
from utilities.pmu_csv_parser import parse_csv_data
import matplotlib.pyplot as plt
from jpt_algo_evaluation.jpt_algo import calculate_complex_voltage, jpt_algo, phase_angle_and_magnitude_from_complex_voltage, calculate_approximation_error, calculate_angle_error, calculate_approximation_error_statistics

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
    received_pmu_data = []
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
    avg_error_set = []
    for i in range(len(received_pmu_data)):
        y_received = received_pmu_data[i]["magnitudes"][0]
        average, std_dev, max_error = calculate_approximation_error_statistics(y_truthy, y_received, generated_data_indexes[i])
        avg_error_set.append(average)


    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    
    ax.scatter(percent_missing, avg_error_set, color="g", label="actual", s=5)
    a, b = np.polyfit(percent_missing, avg_error_set, 1)
    ax.set_title("Average error vs. percent missing data")
    ax.plot(percent_missing, a*np.array(percent_missing) + b, color="r", label="linear fit")
    ax.set_xlabel("Percent missing data")
    ax.set_ylabel("Average error")
    print('y = ' + str(a) + 'x + ' + str(b))

    plt.show()



