import sys
import pandas as pd
import numpy as np
sys.path.append('../../')
from utilities.pmu_csv_parser import parse_csv_data
import matplotlib.pyplot as plt
from jpt_algo_evaluation.jpt_algo import calculate_complex_voltage, jpt_algo, phase_angle_and_magnitude_from_complex_voltage, calculate_approximation_error_statistics, calculate_angle_statistics
from statistics import mean, stdev
trial_count = 4

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
    average_magnitude_errors = []
    average_angle_errors = []
    average_magnitude_std_dev = []
    average_angle_std_dev = []
    for av in range(0, 10):
        average_magnitude_errors.append([])
        average_angle_errors.append([])
        average_magnitude_std_dev.append([])
        average_angle_std_dev.append([])

    for trial_number in range(trial_count):
        percent_missing_set = []
        received_pmu_data = [] #set of pmu data for 1 - 20% missing data
        generated_data_indexes = []
        for i in range(0, 10):
            percent_missing_set.append(i+1)
            received_pmu_data.append(parse_csv_data(
                "trial-" + str(trial_number + 1) + "/received-" + str(i + 1) + "-pct.csv",
                "index",
                ["magnitude", ],
                ["phase_angle"]
            ))
            generated_data_indexes.append(extract_generated_packet_indexes("trial-" + str(trial_number + 1) + "/received-" + str(i + 1) + "-pct.csv"))
        y_truthy = truthy_pmu_csv_data["magnitudes"][0]
        ang_truthy = truthy_pmu_csv_data["phase_angles"][0]
        
        complex_truthy = []
        for x in range(len(y_truthy)):
            complex_truthy.append(calculate_complex_voltage(y_truthy[x], ang_truthy[x]))

        avg_error_set = []
        avg_angle_error_set = []
        std_dev_angle_set = []
        for i in range(len(percent_missing_set)):
            y_received = received_pmu_data[i]["magnitudes"][0]
            complex_received = []
            for j in range(len(y_received)):
                complex_received.append(calculate_complex_voltage(y_received[j], received_pmu_data[i]["phase_angles"][0][j]))
            average, std_dev, max_error = calculate_approximation_error_statistics(y_truthy, y_received, generated_data_indexes[i])
            average_magnitude_errors[i].append(average)
            average_magnitude_std_dev[i].append(std_dev)
            #avg_error_set.append(average)
            avg_ang, std_dev_ang, max_erro_ang = calculate_angle_statistics(complex_truthy, complex_received, generated_data_indexes[i])
            print(i)
            print(avg_ang)
            #avg_angle_error_set.append(avg_ang)
            average_angle_errors[i].append(avg_ang)
            average_angle_std_dev[i].append(std_dev_ang)
            #std_dev_angle_set.append(std_dev_ang)


    fig, ax = plt.subplots(1, 1, figsize=(10,3.5))
    plt.yticks(fontsize=15)
    plt.xticks(fontsize=15)
    
    

    
    average_magnitude_errors = list(map(lambda error_set: mean(error_set), average_magnitude_errors))
    average_angle_errors = list(map(lambda error_set: mean(error_set), average_angle_errors))
    average_magnitude_std_dev = list(map(lambda error_set: mean(error_set), average_magnitude_std_dev))
    average_angle_std_dev = list(map(lambda error_set: mean(error_set), average_angle_std_dev))

    #print(average_magnitude_std_dev)
    #print(average_angle_std_dev)    

    plt.grid()
    plt.tight_layout()
    plt.subplots_adjust(left=0.1, bottom=.15)
    
    #print(average_angle_std_dev)
    #ax.errorbar(percent_missing_set, average_magnitude_errors, yerr=average_magnitude_std_dev, color="g", label="actual", fmt='o', ecolor='g', capthick=2)
    
    """
    ax.plot(percent_missing_set, average_magnitude_errors, color="g", label="actual")
    ax.scatter(percent_missing_set, average_magnitude_errors, color="b", s=30)

    #a, b = np.polyfit(percent_missing_set, avg_error_set, 1)
    #ax[0].plot(percent_missing_set, a*np.array(percent_missing_set) + b, color="r", label="linear fit")

    ax.set_xlabel("Missing Data Rate (%)", fontsize=15)
    ax.set_ylabel("Magnitude MAPE (%)", fontsize=15)
    plt.savefig('../figures/aggregate-accuracy-magnitude.pdf',format = 'pdf')
    """
    
    
    
    
    #ax[1].errorbar(percent_missing_set, average_angle_errors, yerr=average_angle_std_dev, color="g", label="actual", fmt='o', ecolor='g', capthick=2)
    ax.plot(percent_missing_set, average_angle_errors, color="g", label="actual")
    ax.scatter(percent_missing_set, average_angle_errors, color="b", s=30)

    #a, b = np.polyfit(percent_missing_set, avg_angle_error_set, 1)
    #ax[1].plot(percent_missing_set, a*np.array(percent_missing_set) + b, color="r", label="linear fit")
    ax.set_xlabel("Missing Data Rate (%)", fontsize=15)
    ax.set_ylabel("Phase Angle Error (Degrees)", fontsize=15)
    plt.savefig('../figures/aggregate-accuracy-angle.pdf',format = 'pdf')
    
    

    plt.show()
    



