import socket
import struct
import math
import sys

sys.path.append('../')

from jpt_algo_evaluation.jpt_algo import calculate_complex_voltage, jpt_algo, phase_angle_and_magnitude_from_complex_voltage, calculate_approximation_error

UDP_IP_ADDRESS = "0.0.0.0"  # listen on all available interfaces
UDP_PORT_NO = 4712  # PMU data port number

# create a UDP socket object
serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# bind the socket to the specified IP address and port number
serverSock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))

def parse_phasors(phasor_data, settings={"num_phasors": 1, "pmu_measurement_bytes": 8}):
    phasor = {
        "magnitude": struct.unpack('>f', phasor_data[0:4])[0],
        "angle": math.degrees(struct.unpack('>f', phasor_data[4 : 8])[0]),
    }
    return [phasor]

def pmu_packet_parser(data, settings={"pmu_measurement_bytes": 8}):
    # convert each field to correct data type
    pmu_packet = {
        "sync": data[0:2],
        "frame_size": int.from_bytes(data[2:4], byteorder="big"),
        "id_code": int.from_bytes(data[4:6], byteorder="big"),
        "soc": (data[6:10]),
        "frac_sec": (data[10:14]),
        "stat": int.from_bytes(data[14:16], byteorder="big"),
        "phasors": parse_phasors(data[16:16 + 2 * settings["pmu_measurement_bytes"]], {"num_phasors": 1, "pmu_measurement_bytes": settings["pmu_measurement_bytes"]}),
        "freq": data[16 + 2 * settings["pmu_measurement_bytes"]:18 + 2 * settings["pmu_measurement_bytes"]],
        "dfreq": data[18 + 2 * settings["pmu_measurement_bytes"]:20 + 2 * settings["pmu_measurement_bytes"]],
        "analog": data[20 + 2 * settings["pmu_measurement_bytes"]:24 + 2 * settings["pmu_measurement_bytes"]],
        "digital": data[24 + 2 * settings["pmu_measurement_bytes"]:26 + 2 * settings["pmu_measurement_bytes"]],
    }
    return pmu_packet

# wait for incoming PMU packets
if __name__ == "__main__":
    counter = 0
    buffer = []
    predicted_magnitude = 0
    predicted_pa = 0
    while True:
        data, addr = serverSock.recvfrom(1500)  # receive up to 1500 bytes of data
        counter += 1
        # print float value of pmu_packet_parser(data)["frame_size"]
        pmu_data = pmu_packet_parser(data)
        print("Magnitude: ", pmu_data["phasors"][0]["magnitude"])
        print("Angle: ", pmu_data["phasors"][0]["angle"])
        buffer.append(calculate_complex_voltage(pmu_data["phasors"][0]["magnitude"], pmu_data["phasors"][0]["angle"]))
        if counter % 3 == 0 and counter != 0:
            complex_voltage_estimate = jpt_algo(buffer[2], buffer[1], buffer[0])
            mag, pa = phase_angle_and_magnitude_from_complex_voltage(complex_voltage_estimate)
            buffer = []
            print("Next predicted magnitude: ", mag)
            predicted_magnitude = mag
            print("Next predicted phase angle: ", pa)
            predicted_pa = pa
        if counter % 4 == 0 and counter != 0:
            print("Approximation error for magnitude: ", calculate_approximation_error(pmu_data["phasors"][0]["magnitude"] , predicted_magnitude))
            print("Approximation error for angle: ", calculate_approximation_error(pmu_data["phasors"][0]["angle"], predicted_pa))
        print("\n")