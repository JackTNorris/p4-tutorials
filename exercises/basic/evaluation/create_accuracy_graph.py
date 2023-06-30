import sys
sys.path.append('../')
from utilities.pmu_csv_parser import parse_csv_data
import pandas as pd
import matplotlib.pyplot as plt
from jpt_algo_evaluation.jpt_algo import calculate_complex_voltage, calculate_angle_statistics, calculate_approximation_error_statistics
from statistics import mean, stdev, median

pct_missing = 5
trial = 1
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
    fig, ax = plt.subplots(1, 1, figsize=(10,3.5))
    plt.tight_layout()
    plt.subplots_adjust(left=0.1, bottom=0.15)
    
    """
    ax.plot(index, magnitude_received, color="r", label="Recovered Data")
    ax.plot(index, magnitude_truthy, color="g", label="Actual Measurement")
    ax.set_xlabel("Packet Index", fontsize=15)
    ax.set_ylabel("Magnitude (Volts)", fontsize=15)
    plt.yticks(fontsize=15)
    plt.xticks(fontsize=15)
    ax.legend(fontsize=15)
    plt.grid()
    plt.savefig('figures/' + str(pct_missing) + '-pct-accuracy-magnitude.pdf', format='pdf')
    plt.show()
    """

    
    average_mag_error, std_dev_mag, max_mag_error = calculate_approximation_error_statistics(magnitude_truthy, magnitude_received, generated_indexes=extract_generated_packet_indexes("5k/trial-" + str(trial) + "/received-" + str(pct_missing) + "-pct.csv"))
    x = []
    for i in range(len(magnitude_truthy)):
        x.append(magnitude_truthy[i]- magnitude_received[i])
        if magnitude_truthy[i]- magnitude_received[i] > 1000:
            print(i)
    angle_truthy = truthy_pmu_csv_data["phase_angles"][0]
    angle_received = received_pmu_data["phase_angles"][0]

    plt.yticks(fontsize=15)
    plt.xticks(fontsize=15)
    ax.plot(index, angle_received, color="r", label="Recovered Data")
    ax.plot(index, angle_truthy, color="g", label="Actual Measurement", linestyle='dashed', dashes=(10, 10))
    ax.set_xlabel("Packet Index", fontsize=15)
    ax.set_ylabel("Phase Angle (Degrees)", fontsize=15)
    ax.legend(fontsize=15)
    

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
    

    plt.ylim(-180, 180)
    plt.yticks([-180, -135, -90, -45, 0, 45, 90, 135, 180])
    plt.grid()
    plt.savefig('figures/' + str(pct_missing) + '-pct-accuracy-angle.pdf', format='pdf')
    plt.show()
    





