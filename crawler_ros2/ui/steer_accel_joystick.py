import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Int32, Int64
import numpy as np
from crawler_libs.msg import Crawler

class Steer_Accel(Node):
    def __init__(self):
        super().__init__('steer_accel')
        self.btn_name = ''
        self.btn_magnitude = ''
        self.subscription = self.create_subscription(
            String,
            'joystick_status',
            self.listener_callback,
            1)
        self.subscription  # prevent unused variable warning
        timer_period = 0.001
        self.state_code = Crawler()
        self.crawler_velocity_pub = self.create_publisher(Crawler, 'crawler_velocity_pub', 1)
        self.timer = self.create_timer(timer_period, self.publish_custom_data)
        self.i = 0
        self.state_code.digital_voltage = 0

        self.declare_parameter("crawler_mode",0)

    def listener_callback(self, msg):
        self.btn_name = msg.data.split(',')[0]
        self.btn_magnitude = msg.data.split(',')[2]
        # state_magnitude = Int32()

        if (self.btn_name == 'BTN_SOUTH'):
            if (self.btn_magnitude == '1'):
                self.get_logger().info('Brining servos to zero positions')
                self.state_code.zero_pos = True
                # self.crawler_velocity_pub.publish(self.state_code)
            else:
                self.state_code.zero_pos = False

        if (self.btn_name == 'BTN_NORTH'):
            if (self.btn_magnitude == '0'):
                self.get_logger().info('Crawler in Mode 1 -> wheels at 30*')
                self.state_code.mode = 1
                # self.crawler_velocity_pub.publish(self.state_code)

        if (self.btn_name == 'BTN_WEST'):
            if (self.btn_magnitude == '0'):
                self.get_logger().info('Crawler in Mode 0 -> wheels at 0*')
                self.state_code.mode = 0
                # self.crawler_velocity_pub.publish(self.state_code)

        # if (self.btn_name == 'BTN_EAST'):
        #     if (self.btn_magnitude == '0'):
        #         self.get_logger().info('Crawler in Mode 2 -> container mode')
        #         self.state_code.mode = 2
        #         self.crawler_velocity_pub.publish(self.state_code)
        if ((self.btn_name == ('ABS_RY' or 'ABS_RX')) ):
            vtg_in_digital = 32767 - int(self.btn_magnitude)
            self.state_code.digital_voltage = vtg_in_digital 
            # self.crawler_velocity_pub.publish(self.state_code)
            self.get_logger().info(f"vtg_in_digital: {self.state_code.digital_voltage}")

        if (self.btn_name == 'ABS_HAT0X'):

            if (self.btn_magnitude == '1'):
                self.get_logger().info('cralwer expected to go right')
                self.state_code.direction = 1
                # self.crawler_velocity_pub.publish(self.state_code)


            if (self.btn_magnitude == '-1'):
                self.get_logger().info('cralwer expected to go left') 
                self.state_code.direction = -1
                # self.crawler_velocity_pub.publish(self.state_code)

            if (self.btn_magnitude == '0'):
                self.get_logger().info('cralwer expected to go straight')
                self.state_code.direction = 0
                # self.crawler_velocity_pub.publish(self.state_code)

        else:
            self.get_logger().info(f"Not correct input {self.btn_name}")

    def publish_custom_data(self):
        self.crawler_velocity_pub.publish(self.state_code)

def main(args=None):
    rclpy.init(args=args)
    subscriber = Steer_Accel()
    rclpy.spin(subscriber)
    subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
