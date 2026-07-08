# Catkin Workspace

This workspace contains the ROS1 packages used by NavRL:

- `uav_simulator`
- `navigation_runner`
- `onboard_detector`
- `map_manager`

Only source files are tracked. Build products such as `build/`, `devel/`,
`install/`, and `logs/` should be generated locally and are ignored by Git.

## Download on another system

```bash
git clone https://github.com/Zhefan-Xu/NavRL.git
cd NavRL/catkin_ws
```

If this work is on a feature branch, fetch and check it out first:

```bash
git fetch origin codex/add-catkin-ws-20260708-113618
git checkout codex/add-catkin-ws-20260708-113618
cd catkin_ws
```

## Build

Install ROS1 and the package dependencies for your ROS distribution first. For
example, on Ubuntu with ROS Noetic:

```bash
sudo apt update
sudo apt install ros-noetic-desktop-full python3-catkin-tools \
  ros-noetic-gazebo-ros ros-noetic-mavros ros-noetic-mavros-extras \
  ros-noetic-cv-bridge ros-noetic-image-transport ros-noetic-message-filters \
  ros-noetic-vision-msgs
```

Then build and source the workspace:

```bash
catkin_make
source devel/setup.bash
```

For a persistent shell setup:

```bash
echo "source $(pwd)/devel/setup.bash" >> ~/.bashrc
```
