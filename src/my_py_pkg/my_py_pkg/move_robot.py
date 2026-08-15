#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import String
import string
 
 
class RobotMove(Node): 
    def __init__(self):
        super().__init__("robot_move") 
        self.command_= ""
        self.text_subscribe = self.create_subscription(String,"speech_text",self.callback_sub,10)
        self.move_publish = self.create_publisher(Twist, "cmd_vel" , 10)
        self.timer_ = self.create_timer(1.0,self.timer_callback)
        self.get_logger().info("Publishing has started")


    def callback_sub(self, msg:String):
        self.command_ = msg.data.strip().lower()
        self.command_ = self.command_.translate(str.maketrans("","",string.punctuation))


    def timer_callback(self):

        msg = Twist()

        if self.command_ == "forward":
            msg.linear.x = 0.2
            msg.angular.z = 0.0
            self.move_publish.publish(msg)

        elif self.command_ == "back":
            msg.linear.x = -0.2
            msg.angular.z = 0.0
            self.move_publish.publish(msg)

        elif self.command_ == "left":
            msg.linear.x = 0.0
            msg.angular.z = -1.0
            self.move_publish.publish(msg)

        elif self.command_ == "right":
            msg.linear.x = 0.0
            msg.angular.z = 1.0
            self.move_publish.publish(msg)

        elif self.command_ == "stop":
            msg.linear.x = 0.0
            msg.angular.z = 0.0
            self.move_publish.publish(msg)

        
        else:
            self.get_logger().warn("Unrecognised Command")
            msg.linear.x = 0.0
            msg.angular.z = 0.0
            self.move_publish.publish(msg)



 
def main(args=None):
    rclpy.init(args=args)
    node = RobotMove() 
    rclpy.spin(node)
    rclpy.shutdown()
 
 
if __name__ == "__main__":
    main()