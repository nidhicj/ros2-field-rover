import os
import time
import canopen
import binascii
from canopen import Network
import numpy as np


SERVO_SPEED:int = 70000  # counts/s
SERVO_ACCELERATION:int = 70000 # counts/s2
SERVO_DECELERATION:int = 70000 # counts/s2

# CANopen EDS file for the ZeroErr servo drivers
SERVO_EDS_PATH:str = os.environ.get('SERVO_EDS_PATH', 'ZeroErr Driver_V1.5.eds')


class ServoConfig():
    def __init__(self,network,node_id):
        # pass

        node_id_list = [1,2,3,4]
        self.network = network
        self.node_id = node_id
        
        if node_id in node_id_list:
            print(f"Found node {node_id} !")
            self.node = canopen.BaseNode402(node_id, SERVO_EDS_PATH)
            self.network.add_node(self.node)
            print(self.node.state)
        print(f"Servo {self.node_id} added to network.")
      
        self.reset_communication()
        # time.sleep(4)

        self.start_node()
        # time.sleep(1)

        self.set_profile_mode()
        # time.sleep(1)

        self.set_profile_params()
        # time.sleep(1)

        self.enable()
        # time.sleep(1)

        print(self.get_pos())
        # time.sleep(1)
    
        print(f"Node {self.node_id} Initialized")

    def state_node(self):
        status = self.node.state
        return status

    def stop_node(self):
        #Stops the servo motor motor node.
        self.node.nmt.send_command(0x2)
        # print(f"Node {self.node_id} stopped")

    def start_node(self):
        #Starts the servo motor self.node.
        self.node.nmt.send_command(0x1)
        # print(f"Node {self.node_id} started")

    def reset_communication(self):
        #Resets the communication with the servo motor node.
        self.node.nmt.send_command(0x82)
        # print(f"Node {self.node_id} communication reset")

    def move(self, delta_angle)-> None:

        self.set_profile_params()
        counts = self.angle_to_counts(delta_angle)
        self.node.sdo[0x607A].raw = counts
        self.node.sdo[0x6040].raw = 63
        # time.sleep(0.01)
        # print(f'Moving command to {delta_angle} and {counts} ')
        
    def get_pos(self):
        
        counts = self.node.sdo[0x6064].raw
        angle = np.round(((360*counts)/(524288)),2)
        return angle


    def set_profile_mode(self, mode = 1):
        if mode == 1: # profile positon mode
            self.node.sdo.download(index = 0x6060,subindex = 0x00,data = int(1).to_bytes(1, 'little'))
            time.sleep(2)
            response = self.node.sdo.upload(index = 0x6061,subindex = 0x00)

            if int.from_bytes(response, 'little') == 1:
                print(f"Node {self.node_id} profile is set to position mode")
            else:
                raise ProfileSetFailed(f"Node {self.node_id} profile setting failed")


    def set_profile_params(self)-> None:

        # set speed/velocity
        speed_data = SERVO_SPEED.to_bytes(4, 'little')
        self.node.sdo.download(index = 0x6081,subindex = 0x00,data = speed_data)
        
        # set acceleration
        acc_data = SERVO_ACCELERATION.to_bytes(4, 'little')
        self.node.sdo.download(index = 0x6083,subindex = 0x00,data = acc_data)
        
        # set deceleration
        dec_data = SERVO_DECELERATION.to_bytes(4, 'little')
        self.node.sdo.download(index = 0x6084,subindex = 0x00,data = dec_data)
        
        # clear motor error report (no idea - following seq)
        err_data = int(128).to_bytes(2, 'little')
        self.node.sdo.download(index = 0x6040,subindex = 0x00,data = err_data)


    def enable(self):
        msg = [ (0x6040, 0x00, 38), # set to 38
                (0x6040, 0x00, 39), # set to 39
                (0x6040, 0x00, 47), # set to 47
              ]
        for cmd in msg:
            if len(str(cmd[2]))==2:
                size = 2
            else:
                size = 4
            dat = int(cmd[2]).to_bytes(size, 'little')
            self.node.sdo.download(index = cmd[0],subindex = cmd[1],data = dat)

    def disable(self):
        self.node.sdo.download(
                index = 0x6040,
                subindex = 0x00,
                data = int(2).to_bytes(2, 'little')
            )
        response = self.node.sdo.upload(
                index = 0x6040,
                subindex = 0x00
            )
        time.sleep(1)
        print(self.node.state)

    def angle_to_counts(self, ang:float):
        counts = (ang/360)*(524288)
        return int(counts)


class NodeNotFound(Exception):
    pass 


class ProfileSetFailed(Exception):
    pass

# if __name__ == '__main__':
#     servo1 = ServoConfig(network0,1)
