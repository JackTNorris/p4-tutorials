
import runtime_CLI
from sswitch_runtime import SimpleSwitch 
from sswitch_runtime.ttypes import *
import struct
import nnpy
import ipaddress
class SimpleSwitchAPI(runtime_CLI.RuntimeAPI):
    @staticmethod
    def get_thrift_services():
        return [("simple_switch", SimpleSwitch.Client)]
    
    def __init__(self, pre_type, standard_client, mc_client, sswitch_client):
        runtime_CLI.RuntimeAPI.__init__(self, pre_type, standard_client, mc_client)
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
    runtime_api = SimpleSwitchAPI(args.pre, standard_client, mc_client, sswitch_client)
    listen_for_digests(runtime_api)

def listen_for_digests(controller):
    sub = nnpy.Socket(nnpy.AF_SP, nnpy.SUB)
    socket = controller.clietn.bm_mgmt_get_info().notifications_socket
    sub.connect(socket)
    sub.setsockopt(nnpy.SUB, nnpy.SUB_SUBSCRIBE, '')
    while True:
        message = sub.recv()
        on_message_recv(message, controller)

def on_message_recv(msg, controller):
    _, _, ctx_id, list_id, buffer_id, num = struct.unpack("<iQiiQi", msg[:32])
    msg = msg[32:]
    offset = 8

main()
