import sys
sys.path.append('../')
from utilities.pmu_csv_parser import parse_csv_data
import pandas as pd
import matplotlib.pyplot as plt
from jpt_algo_evaluation.jpt_algo import calculate_complex_voltage, calculate_angle_statistics, calculate_approximation_error_statistics
from statistics import mean, stdev, median

pct_missing = 10
trial = 2
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
        '../pmu8_5k.csv',
        "TimeTag",
        ["Magnitude01", "Magnitude02", "Magnitude03"],
        ["Angle01", "Angle02", "Angle03"]
    )
    received_pmu_data = parse_csv_data(
        "5k/trial-" + str(trial) + "/received-" + str (pct_missing) + "-pct.csv",
        "index",
        ["magnitude", ],
        ["phase_angle"]
    )
    
    magnitude_truthy = truthy_pmu_csv_data["magnitudes"][0]
    magnitude_received = received_pmu_data["magnitudes"][0]
    index = received_pmu_data["times"]
    fig, ax = plt.subplots(2, 1, figsize=(10, 10))

    ax[0].plot(index, magnitude_received, color="r", label="predicted")
    ax[0].plot(index, magnitude_truthy, color="g", label="actual")
    ax[0].set_title("Comparison of Ground Truth and Received Magnitude Values (" + str(pct_missing) + "% loss)")
    ax[0].set_xlabel("Index")
    ax[0].set_ylabel("Magnitude (Volts)")
    ax[0].legend()
    
    average_mag_error, std_dev_mag, max_mag_error = calculate_approximation_error_statistics(magnitude_truthy, magnitude_received, generated_indexes=extract_generated_packet_indexes("5k/trial-" + str(trial) + "/received-" + str(pct_missing) + "-pct.csv"))
    x = []
    for i in range(len(magnitude_truthy)):
        x.append(magnitude_truthy[i]- magnitude_received[i])
    print("Average magnitude error: " + str(mean(x)))
    print("Standard deviation: " + str(stdev(x)))
    print("Max error: " + str(max(x)))
    angle_truthy = truthy_pmu_csv_data["phase_angles"][0]
    angle_received = received_pmu_data["phase_angles"][0]

    ax[1].plot(index, angle_received, color="r", label="predicted")
    ax[1].plot(index, angle_truthy, color="g", label="actual")
    ax[1].set_title("Comparison of Ground Truth and Received Phase Angle Values (" + str(pct_missing) + "% loss)")
    ax[1].set_xlabel("Index")
    ax[1].set_ylabel("Phase Angle (Degrees)")
    ax[1].legend()


    complex_phasors_received = []
    complex_phasors_truthy = []
    for i in range(len(magnitude_received)):
        complex_phasors_received.append(calculate_complex_voltage(magnitude_received[i], angle_received[i]))    
        complex_phasors_truthy.append(calculate_complex_voltage(magnitude_truthy[i], angle_truthy[i]))

    average_ang_error, std_dev_ang, max_error_ang = calculate_angle_statistics(exact_measurements=complex_phasors_truthy, approximate_measurements=complex_phasors_received, generated_indexes=extract_generated_packet_indexes("5k/trial-" + str(trial) + "/received-" + str (pct_missing) + "-pct.csv"))


    print("---Magnitude---")
    print("Average approximation error: " + str(average_mag_error))
    print("Standard deviation: " + str(std_dev_mag))
    print("Max error: " + str(max_mag_error))

    
    print("---Angle---")
    print("Average error: " + str(average_ang_error))
    print("Standard deviation: " + str(std_dev_ang))
    print("Max error: " + str(max_error_ang))
    

    plt.grid()
    plt.savefig('figures/10-pct-accuracy.pdf', format='pdf')
    plt.show()






