import sys
sys.path.append('../')
from utilities.pmu_csv_parser import parse_csv_data
import matplotlib.pyplot as plt
from jpt_algo_evaluation.jpt_algo import calculate_complex_voltage, jpt_algo, phase_angle_and_magnitude_from_complex_voltage, calculate_approximation_error, calculate_angle_error, calculate_approximation_error_statistics


if __name__ == "__main__":
    truthy_pmu_csv_data = parse_csv_data(
        '../pmu8_5k.csv',
        "TimeTag",
        ["Magnitude01", "Magnitude02", "Magnitude03"],
        ["Angle01", "Angle02", "Angle03"]
    )
    received_pmu_data = parse_csv_data(
        "5k/received-10-pct.csv",
        "index",
        ["magnitude", ],
        ["phase_angle"]
    )
    
    y_truthy = truthy_pmu_csv_data["magnitudes"][0]
    y_received = received_pmu_data["magnitudes"][0]
    index = received_pmu_data["times"]
    fig, ax = plt.subplots(3, 1, figsize=(10, 10))

    ax[0].scatter(index, y_truthy, color="g", label="actual", s=1)
    ax[1].scatter(index, y_received, color="r", label="predicted", s=1, marker="x")
    ax[2].scatter(index, y_received, color="r", label="predicted", s=1, marker="x")
    ax[2].scatter(index, y_truthy, color="g", label="actual", s=1)
    ax[0].set_title("Ground Truth Values")
    ax[1].set_title("Received Values (10% loss)")
    ax[2].set_title("Comparison of Ground Truth and Received Values (10% loss)")
    

    print(y_truthy)
    print(y_received)
    
    average, std_dev, max_error = calculate_approximation_error_statistics(y_truthy, y_received)

    print("Average error: " + str(average))
    print("Standard deviation: " + str(std_dev))
    print("Max error: " + str(max_error))

    plt.show()



