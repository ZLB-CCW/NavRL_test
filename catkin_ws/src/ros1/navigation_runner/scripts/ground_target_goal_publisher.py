#!/usr/bin/env python3

import rospy
from gazebo_msgs.msg import ModelStates
from geometry_msgs.msg import PoseStamped, Quaternion


class GroundTargetGoalPublisher:
    def __init__(self):
        self.target_prefix = rospy.get_param("~target_prefix", "target_car")
        self.goal_topic = rospy.get_param("~goal_topic", "/move_base_simple/goal")
        self.goal_frame = rospy.get_param("~goal_frame", "map")
        self.goal_height = rospy.get_param("~goal_height", 1.0)
        self.lead_time = rospy.get_param("~lead_time", 0.0)
        self.publish_rate = rospy.get_param("~publish_rate", 10.0)

        self.target_name = None
        self.target_pose = None
        self.target_twist = None

        self.goal_pub = rospy.Publisher(self.goal_topic, PoseStamped, queue_size=1)
        self.model_sub = rospy.Subscriber("/gazebo/model_states", ModelStates, self.model_states_cb)

    def model_states_cb(self, msg):
        target_idx = None
        for idx, name in enumerate(msg.name):
            if name.startswith(self.target_prefix):
                target_idx = idx
                self.target_name = name
                break

        if target_idx is None:
            return

        self.target_pose = msg.pose[target_idx]
        self.target_twist = msg.twist[target_idx]

    def spin(self):
        rate = rospy.Rate(self.publish_rate)
        while not rospy.is_shutdown():
            if self.target_pose is None:
                rospy.logwarn_throttle(2.0, "Waiting for Gazebo model starting with '%s'.", self.target_prefix)
                rate.sleep()
                continue

            goal = PoseStamped()
            goal.header.stamp = rospy.Time.now()
            goal.header.frame_id = self.goal_frame
            goal.pose.position.x = self.target_pose.position.x + self.lead_time * self.target_twist.linear.x
            goal.pose.position.y = self.target_pose.position.y + self.lead_time * self.target_twist.linear.y
            goal.pose.position.z = self.goal_height
            goal.pose.orientation = Quaternion(w=1.0)
            self.goal_pub.publish(goal)
            rate.sleep()


if __name__ == "__main__":
    rospy.init_node("ground_target_goal_publisher")
    GroundTargetGoalPublisher().spin()
