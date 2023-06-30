import argparse
import pandas as pd
from datetime import datetime, timedelta
from statistics import mean, stdev
import matplotlib.pyplot as plt
import numpy as np


sleep_time_seconds = 0.017

trials = 4

def parse_receive_file(file_path):
    data = pd.read_csv(file_path)
    received_at_times = list(map(lambda t: datetime.strptime(t, "%Y-%m-%d %H:%M:%S.%f"), data["received_at"].values))
    return received_at_times

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

def calculate_packet_end_to_end(sent_at_times, received_at_times, generated_indexes, generated_only = True):
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

def extract_avg_and_range_times(sent_file, received_file):
    end_to_end_times = calculate_packet_end_to_end(parse_send_file(sent_file), parse_receive_file(received_file), extract_generated_packet_indexes(received_file))
    return mean(end_to_end_times), stdev(end_to_end_times), min(end_to_end_times), max(end_to_end_times)

if __name__ == "__main__":
    fig, ax = plt.subplots(1, 1, figsize=(10,3.5))

    x = []
    for z in range(20):
        x.append(z)
    all_average_speeds = []
    all_average_errors = []
    for trial in range(trials):
        for i in x:
            y = []
            errors = []
            avg, sd, mn, mx = extract_avg_and_range_times("trial-" + str(trial + 1) + "/sent-" + str(i + 1) + "-pct.csv", "trial-" + str(trial + 1) + "/received-" + str(i + 1) + "-pct.csv")
            y.append(avg)
            errors.append(sd)
            print("Average for " + str(i + 1) + "%: " + str(avg))
            print("Std dev for " + str(i + 1) + "%: " + str(sd))
            print("Min for " + str(i + 1) + "%: " + str(mn))
            print("Max for " + str(i + 1) + "%: " + str(mx))

    plt.yticks(fontsize=15)
    plt.xticks(fontsize=15)
    ax.errorbar(x, y, yerr=errors, fmt='o')
    ax.set_title("Average End-to-End Time vs. Packet Loss Rate")
    ax.set_xlabel("Packet Loss Rate (%)")
    ax.set_ylabel("Average End-to-End Time (s)")
    plt.show()


