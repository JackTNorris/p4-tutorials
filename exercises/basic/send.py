#!/usr/bin/env python3

import socket
import datetime
import math
import struct
import pandas as pd
import sys
import time
sys.path.append('../')
from utilities.pmu_csv_parser import parse_csv_data


def generate_packet(time, voltage, angle, settings={"pmu_measurement_bytes": 8, "destination_ip": "192.168.0.100", "destination_port": 4712}):
    # Define the PMU packet as a byte string
    datetime_str = str(time)[:26]

    try:
        dt = datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S.%f')
    except ValueError:
        dt = datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')

    # 2 byte
    sync = b'\xAA\x01'

    # 2 byte, 44 for 32 bit values of PMU, 40 for 16 bit values of PMU
    # 36 - 8 + 8 * number of PMUs || 36 - 8 + 4 * number PMUs
    frame_size = b'\x00\x24'

    # 2 byte, 12 for this
    id_code = b'\x00\x0C'

    # 4 byte
    soc = int(dt.strftime("%s")).to_bytes(4, 'big')

    # 4 byte
    frac_sec = dt.microsecond.to_bytes(4, 'big')

    # 2 byte (no errors)
    stat = b'\x00\x00'

    # 4 or 8 byte x number of phasors (see doc, 8 is for float)
    voltage_bytes = struct.pack('>f', voltage)
    angle_bytes = struct.pack('>f', math.radians(angle))
    phasors = voltage_bytes + angle_bytes

    # 2 byte, assumed 60
    freq = b'\x09\xC4'

    # 2 byte
    dfreq = b'\x00\x00'

    # 4 byte
    analog = b'\x42\xC8\x00\x00'

    # 2 byte
    digital = b'\x3C\x12'

    # 2 byte
    chk = b'\xD4\x3F'

    pmu_packet = sync + frame_size + id_code + soc + frac_sec + \
        stat + phasors + freq + dfreq + analog + digital + chk

    # Set the destination IP address and port number
    destination_ip = settings["destination_ip"]
    destination_port = 4712

    # Create a UDP socket
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Send the PMU packet to the destination IP address and port number
    udp_socket.sendto(pmu_packet, (destination_ip, destination_port))

    # Close the UDP socket
    udp_socket.close()


if __name__ == "__main__":
    pmu_data = parse_csv_data(
        "./pmu12.csv",
        "TimeTag",
        ["Magnitude01", "Magnitude02", "Magnitude03"],
        ["Angle01", "Angle02", "Angle03"]
    )
    settings_obj = {}
    if len(sys.argv) > 1 and sys.argv[1]:
        settings_obj["destination_ip"] = sys.argv[1]
        if len(sys.argv) > 2 and sys.argv[2]:
            settings_obj["destination_port"] = sys.argv[1]

    #first 3 packets exists in switch
    for i in range(3, 103):
        print(str(i - 2) + " | " + "Magnitude: " + str(pmu_data["magnitudes"][0][i]) + " | Phase_angle: " + str(pmu_data["phase_angles"][0][i]))
        time.sleep(0.017)
        generate_packet(pmu_data["times"][i], pmu_data["magnitudes"][0][i], pmu_data["phase_angles"][0][i], settings_obj)

    # generate_packets()
