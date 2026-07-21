#!/usr/bin/env python3

import sys

import rospy


def strip_ros_args(argv=None):
    return rospy.myargv(argv=sys.argv if argv is None else argv)


def strip_ros_args_from_sys_argv():
    sys.argv = strip_ros_args(sys.argv)
