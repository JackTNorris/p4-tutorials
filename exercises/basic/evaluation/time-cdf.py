import sys
sys.path.append('../')
from utilities.pmu_csv_parser import parse_csv_data
import pandas as pd
import matplotlib.pyplot as plt
from jpt_algo_evaluation.jpt_algo import calculate_complex_voltage, calculate_angle_statistics, calculate_approximation_error_statistics
import numpy as np
from datetime import datetime, timedelta
sleep_time_seconds = 0.017

def calculate_packet_end_to_end(sent_at_times, received_at_times, generated_indexes, generated_only = False, non_generated_only = False):
    #function to account for sleep time included for generated packets
    end_to_end_times = []
    for i in range(len(sent_at_times)):
        end_to_end_time = timedelta.total_seconds(received_at_times[i] - sent_at_times[i])
        if i in generated_indexes:
            end_to_end_time -= sleep_time_seconds
            if generated_only:
                end_to_end_times.append(end_to_end_time)
        if not generated_only:
            end_to_end_times.append(end_to_end_time)
    return end_to_end_times

def calculate_packet_end_to_end_non_generated_only(sent_at_times, received_at_times, generated_indexes, non_generated_only = False):
    #function to account for sleep time included for generated packets
    end_to_end_times = []
    for i in range(len(sent_at_times)):
        end_to_end_time = timedelta.total_seconds(received_at_times[i] - sent_at_times[i])
        if i in generated_indexes:
            print('in generated')
        else:
            end_to_end_times.append(end_to_end_time)
    return end_to_end_times

def extract_generated_packet_indexes(received_data_file_path):
    data = pd.read_csv(received_data_file_path)
    is_predicted_list = list(data["is_predicted"].values)
    generated_indexes = []
    for i in range(len(is_predicted_list)):
        if is_predicted_list[i]:
            generated_indexes.append(i)
    return generated_indexes

def parse_send_file(file_path):
    data = pd.read_csv(file_path)
    sent_at_times = list(map(lambda t: datetime.strptime(t, "%Y-%m-%d %H:%M:%S.%f"), data["sent_at"].values))
    return sent_at_times

def parse_receive_file(file_path):
    data = pd.read_csv(file_path)
    received_at_times = list(map(lambda t: datetime.strptime(t, "%Y-%m-%d %H:%M:%S.%f"), data["received_at"].values))
    return received_at_times

if __name__ == "__main__":
    end_to_end_1_pct = calculate_packet_end_to_end(parse_send_file('new-1ms-5k/sent-1-pct.csv'), parse_receive_file('new-1ms-5k/received-1-pct.csv'), extract_generated_packet_indexes('new-1ms-5k/received-1-pct.csv'))
    end_to_end_5_pct = calculate_packet_end_to_end(parse_send_file('new-1ms-5k/sent-5-pct.csv'), parse_receive_file('new-1ms-5k/received-5-pct.csv'), extract_generated_packet_indexes('new-1ms-5k/received-5-pct.csv'))
    end_to_end_10_pct = calculate_packet_end_to_end(parse_send_file('new-1ms-5k/sent-10-pct.csv'), parse_receive_file('new-1ms-5k/received-10-pct.csv'), extract_generated_packet_indexes('new-1ms-5k/received-10-pct.csv'))
    end_to_end_0_pct = calculate_packet_end_to_end_non_generated_only(parse_send_file('new-1ms-5k/sent-1-pct.csv'), parse_receive_file('new-1ms-5k/received-1-pct.csv'), extract_generated_packet_indexes('new-1ms-5k/received-1-pct.csv'))

    end_to_end_0_pct = list(map(lambda x: x * 1000, end_to_end_0_pct))
    end_to_end_1_pct = list(map(lambda x: x * 1000, end_to_end_1_pct))
    end_to_end_5_pct = list(map(lambda x: x * 1000, end_to_end_5_pct))
    end_to_end_10_pct = list(map(lambda x: x * 1000, end_to_end_10_pct))


    plt.figure(figsize=(10,5))

    plt.plot(np.sort(end_to_end_0_pct), np.linspace(0, 1, len(end_to_end_0_pct)), '--k', color='black', label='0% Missing')
    plt.plot(np.sort(end_to_end_1_pct), np.linspace(0, 1, len(end_to_end_1_pct)), '--k', color='red', label='1% Missing')
    plt.plot(np.sort(end_to_end_5_pct), np.linspace(0, 1, len(end_to_end_5_pct)), '--k', color='green', label='5% Missing')
    plt.plot(np.sort(end_to_end_10_pct), np.linspace(0, 1, len(end_to_end_10_pct)), '--k', color='blue', label='10% Missing')
    plt.plot(np.sort(end_to_end_0_pct), np.linspace(0, 1, len(end_to_end_0_pct)), '--k', color='black')


    plt.xlabel('End to end time (ms)', fontsize=15)
    plt.ylabel('Cumulative Probability', fontsize=15)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.tight_layout()
    #plt.subplots_adjust(left=0.1, bottom=0.15)
    # Show the legend
    plt.legend(fontsize="15")

    # Display the plot
    plt.grid()
    plt.savefig('./figures/times_cdf.pdf', format='pdf')
    plt.show()
    
    






