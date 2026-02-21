import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from adafruit_servokit import ServoKit
import math

# PCA9685 kurulumu
kit = ServoKit(channels=16)

class SimpleBridge(Node):
    def __init__(self):
        super().__init__('simple_bridge')
        self.subscription = self.create_subscription(JointState, '/joint_states', self.listener_callback, 10)
        self.get_logger().info('Haberleşme Hazır! Asus üzerindeki sürgüyü (joint1) oynatın...')

    def listener_callback(self, msg):
        # Sürgüden gelen radyan değerini (yaklaşık -3.14 ile +3.14 arası) alıyoruz
        # joint1 listede 0. indekstedir
        if len(msg.position) > 0:
            angle_rad = msg.position[0]
            # Radyanı dereceye çevirip orta noktayı 90 yapıyoruz
            angle_deg = math.degrees(angle_rad) + 90 
            
            # Servoyu güvenli aralıkta tut (0-180)
            angle_deg = max(0, min(180, angle_deg))
            
            self.get_logger().info(f'Servo 0 Açısı: {angle_deg:.2f}')
            kit.servo[0].angle = angle_deg

def main():
    rclpy.init()
    node = SimpleBridge()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
