import runtime_CLI
from sswitch_runtime import SimpleSwitch
from sswitch_runtime.ttypes import *
import struct
import nnpy
import socket
import os.path
import ipaddress
import math
from jpt_algo_evaluation.jpt_algo import calculate_complex_voltage, jpt_algo, phase_angle_and_magnitude_from_complex_voltage, calculate_approximation_error, calculate_angle_error
from statistics import mean, stdev
import threading

counter = 0
buffer = []
class SimpleSwitchAPI(runtime_CLI.RuntimeAPI):
    @staticmethod
    def get_thrift_services():
        return [("simple_switch", SimpleSwitch.Client)]

    def __init__(self, pre_type, standard_client, mc_client, sswitch_client):
        runtime_CLI.RuntimeAPI.__init__(self, pre_type,
                                        standard_client, mc_client)
        self.sswitch_client = sswitch_client


def main():
    args = runtime_CLI.get_parser().parse_args()

    args.pre = runtime_CLI.PreType.SimplePreLAG

    services = runtime_CLI.RuntimeAPI.get_thrift_services(args.pre)
    services.extend(SimpleSwitchAPI.get_thrift_services())

    standard_client, mc_client, sswitch_client = runtime_CLI.thrift_connect(
        args.thrift_ip, args.thrift_port, services
    )

    runtime_CLI.load_json_config(standard_client, args.json)
    runtime_api = SimpleSwitchAPI(
        args.pre, standard_client, mc_client, sswitch_client)

    ######### Call the function listen_for_digest below #########
    listen_for_digests(runtime_api)

def listen_for_digests(controller):
    sub = nnpy.Socket(nnpy.AF_SP, nnpy.SUB)
    socket = controller.client.bm_mgmt_get_info().notifications_socket
    #s1 = Pair0()
    #s1.listen(socket)
    print("socket is : " + str(socket))
    sub.connect(socket)
    sub.setsockopt(nnpy.SUB, nnpy.SUB_SUBSCRIBE, '')
    #### Define the controller logic below ###
    while True:
        message = sub.recv()
        #print(message)
        on_message_recv(message, controller)

def parse_phasors(phasor_data, settings={"num_phasors": 1, "pmu_measurement_bytes": 8}):
    phasor = {
        "magnitude": struct.unpack('>f', phasor_data[0:int(settings["pmu_measurement_bytes"]/2)])[0],
        "angle": math.degrees(struct.unpack('>f', phasor_data[int(settings["pmu_measurement_bytes"]/2) : settings["pmu_measurement_bytes"]])[0]),
    }
    return [phasor]

def pmu_packet_parser(data, settings={"pmu_measurement_bytes": 8, "num_phasors": 1, "freq_bytes": 4, "dfreq_bytes": 4}):
    freq_start_byte = 16 + settings["num_phasors"] * settings["pmu_measurement_bytes"]
    dfreq_start_byte = freq_start_byte + settings["freq_bytes"]
    analog_start_byte = dfreq_start_byte + settings["dfreq_bytes"]
    digital_start_byte = analog_start_byte + 4

    # convert each field to correct data type
    pmu_packet = {
        "sync": data[0:2],
        "frame_size": int.from_bytes(data[2:4], byteorder="big"),
        "id_code": int.from_bytes(data[4:6], byteorder="big"),
        "soc": int.from_bytes(data[6:10], byteorder="big"),
        "frac_sec": int.from_bytes(data[10:14], byteorder="big"),
        "stat": int.from_bytes(data[14:16], byteorder="big"),
        "phasors": parse_phasors(data[16:16 + settings["pmu_measurement_bytes"]], {"num_phasors": settings["num_phasors"], "pmu_measurement_bytes": settings["pmu_measurement_bytes"]}),
        "freq": struct.unpack('>f', data[freq_start_byte:dfreq_start_byte]),
        "dfreq": struct.unpack('>f', data[dfreq_start_byte:analog_start_byte]),
        "analog": data[analog_start_byte:digital_start_byte],
        "digital": data[digital_start_byte:],
    }

    return pmu_packet
"""
def run_nnpy_thread(q, sock):
    # Create the thread
    nnpy_thread = Thread(target=fetch_traffic, args=([q], [sock]))

    # Start the thread and set as daemon (kills the thread once main thread ends)
    nnpy_thread.daemon = True
    nnpy_thread.start()

def listen_for_events(q, controller):
    while True:
        event_data = q.get()
        on_message_recv(event_data)
        q.task_done()

def fetch_traffic(q, sock):
    q = q[0]
    sock = sock[0]

    # Listen for incoming datagrams
    while(True):
        # Receive traffic from socket
        data = sock.recv(bufferSize)


        # Update the queue with the message
        q.put(data)
"""

mag_approx_errors = []
angle_approx_errors = []
def on_message_recv(msg, controller):
    _, _, ctx_id, list_id, buffer_id, num = struct.unpack("<iQiiQi", msg[:32])
    ### Insert the receiving logic below ###
    msg = msg[32:]
    #pmu_packet = pmu_packet_parser(msg)
    #offset = 36
    controller_phasor_info_packet_length = 16
    controller_phasor_info_packet_count = 3
    offset = controller_phasor_info_packet_length * controller_phasor_info_packet_count
    # For listening the next digest
    for m in range(num):
        global counter
        global buffer
        global mag_approx_errors
        global angle_approx_errors

        jpt_pmus = []
        msg_copy = msg[0:]
        for j in range(controller_phasor_info_packet_count):
            frac = int.from_bytes(msg_copy[4:8], byteorder="big")
            soc = int.from_bytes(msg_copy[0:4], byteorder="big")
            phasor = parse_phasors(msg_copy[8:controller_phasor_info_packet_length])

            print("frac: " + str(frac))
            print("soc: " + str(soc))
            print("mag: " + str(phasor[0]["magnitude"]))
            print("phase: " + str(phasor[0]["angle"]))
            #move to next jpt_phasor in triplet of
            msg_copy = msg_copy[controller_phasor_info_packet_length:]


        msg = msg[offset:]
main()
