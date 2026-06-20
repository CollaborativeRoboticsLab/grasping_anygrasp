# Anygrasp Grasping

This meta package brings together the [grasping stack](https://github.com/CollaborativeRoboticsLab/grasping), [AnyGrasp](https://github.com/graspnet/anygrasp_sdk), [anygrasp_ros](https://github.com/CollaborativeRoboticsLab/anygrasp_ros), and the gripper stack into one integration flow.

It does the following tasks:

1. Call the configured AnyGrasp service for grasp poses.
2. Forward the selected pose to grasping stack's [grasping_control/motion_execution_node](https://github.com/CollaborativeRoboticsLab/grasping/blob/main/docs/control/control_stack_overview.md) through `grasping_msgs/action/MoveToPose`.
3. Trigger gripper open/close actions and optionally request the post-grasp move.

The devcontainer is based on [nvidia/cuda:12.6.0-cudnn-devel-ubuntu22.04](https://hub.docker.com/layers/nvidia/cuda/12.6.0-cudnn-devel-ubuntu22.04/images/sha256-3814ef2c9d46ca559e601374029a576596f016e33ddf48d6e2ad778d21bfa3f0) image and provides the following software stack:

- Pytorch 2.10
- CUDA 12.6
- CUDNN9
- ROS Humble (Base container is ubuntu 22.04)
- [chenxi-wang/MinkowskiEngine](https://github.com/chenxi-wang/MinkowskiEngine.git)
- [CollaborativeRoboticsLab/graspnetAPI](https://github.com/CollaborativeRoboticsLab/graspnetAPI.git)
- [graspnet/anygrasp_sdk](https://github.com/graspnet/anygrasp_sdk.git)
- [Realsense packages](https://github.com/realsenseai/realsense-ros)
- [UR packages](https://github.com/UniversalRobots/Universal_Robots_ROS2_Driver)

Read here for [known issues and how we fixed them](./docs/issues.md)


## Building container

Install VSCode and add the [DevContainer addon](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers).

Clone this repo and open using VSCode. Generally VScode should auto detect, if not press Shift+Ctrl+P to open the command palette and select "DevContainer: Rebuild and Reopen the container" option.

Following are quick commands to match our specific setup.

## Connecting with External Docker Containers/Devcontainers

To connect with external devices running other Docker containers, follow these guidelines:

- [External container using network=host](./docs/external/container.md)

## System Architecture

![System Architecture](./docs/images/system.png)

### RGBD to Pointcloud

As shown in the system architecture diagram, the RGB and depth images are combined into a colored point cloud before grasp detection. This is done by `anygrasp_ros/rgbd_to_pointcloud_node`, which subscribes to the RGB and depth image topics, synchronizes them, and publishes the resulting colored point cloud for grasp pose detection.

- [RGBD to Pointcloud Node](https://github.com/CollaborativeRoboticsLab/anygrasp_ros/blob/main/docs/rgbd_to_pointcloud.md)

### AnyGrasp Node

This integration stack uses AnyGrasp for grasp pose detection. AnyGrasp is interfaced with ROS 2 through `anygrasp_ros/anygrasp_detection_node` and `anygrasp_ros/anygrasp_tracking_node`. These two nodes expect a colored point cloud as input, which is provided by `rgbd_to_pointcloud_node`. The devcontainer installs AnyGrasp and its dependencies. See the related documentation below.

- [License requesting and loading, node customization and starting](https://github.com/CollaborativeRoboticsLab/anygrasp_ros/blob/main/README.md)
- [Testing the anygrasp installation](https://github.com/CollaborativeRoboticsLab/anygrasp_ros/blob/main/docs/testing.md)
- [Anygrasp Detection Node](https://github.com/CollaborativeRoboticsLab/anygrasp_ros/blob/main/docs/detection.md)
- [Anygrasp Tracking Node](https://github.com/CollaborativeRoboticsLab/anygrasp_ros/blob/main/docs/tracking.md)

### Camera Driver

Camera setup, configuration, and customization are documented in the linked file. The current supported device is:

- [Realsense Camera](https://github.com/CollaborativeRoboticsLab/grasping/blob/main/docs/camera/realsense.md)

### Gripper Controller

This integration stack supports multiple gripper types. The gripper controller focuses on custom-built grippers using servo configurations documented in [CollaborativeRoboticsLab/grippers](https://github.com/CollaborativeRoboticsLab/grippers). Setup, configuration, and customization details are in the linked documents.

- [Dynamixel Grippers](https://github.com/CollaborativeRoboticsLab/grippers/blob/main/docs/dynamixel.md)
- [Feetech Grippers](https://github.com/CollaborativeRoboticsLab/grippers/blob/main/docs/feetech.md)

### Arm Controller

This integration stack uses the UR10 manipulator in the documented setups. Instructions for setup, configuration, and calibration are in the linked files.

- [UR10 and Devcontainer connection](https://github.com/CollaborativeRoboticsLab/grasping/blob/main/docs/manipulator/connection.md)
- [UR10 calibration](https://github.com/CollaborativeRoboticsLab/grasping/blob/main/docs/manipulator/calibration.md)
- [UR10 startup](https://github.com/CollaborativeRoboticsLab/grasping/blob/main/docs/manipulator/universal.md)
- [UR10 TF frames for gripper compatibility](https://github.com/CollaborativeRoboticsLab/grasping/blob/main/docs/manipulator/tf_frames.md)
- [UR10 attaching new gripper and components](https://github.com/CollaborativeRoboticsLab/grasping/blob/main/docs/manipulator/adding_new_components.md)
- [Moveit Servo and Keyboard Teleop](https://github.com/CollaborativeRoboticsLab/grasping/blob/main/docs/manipulator/teleop.md)

### Arm Control and Workspace Creation

This component transforms grasp poses, applies workspace obstacles to MoveIt, visualizes the calibrated workspace area, and rejects poses outside that area.

- [Workspace Creation](https://github.com/CollaborativeRoboticsLab/grasping/blob/main/docs/workspace/creation.md)
- [Arm Control](https://github.com/CollaborativeRoboticsLab/grasping/blob/main/docs/control/arm_control.md)
- [Control stack overview](https://github.com/CollaborativeRoboticsLab/grasping/blob/main/docs/control/control_stack_overview.md)

### AnyGrasp Grasping Pipeline

The grasping pipeline is the main component that orchestrates the grasping process: it requests a grasp pose from AnyGrasp, calls the arm-control action, closes the gripper, and optionally runs a post-grasp move. 

- [Grasping pipeline](./docs/grasping_pipeline.md)


## Quick Commands

### Starting the camera

Use the following command to start the realsense D435 camera.

```bash
source install/setup.bash
ros2 launch grasping_camera d435.launch.py
```

### Starting the AnyGrasp Detection System

Use the following command to start the AnyGrasp system.

```bash
source install/setup.bash
ros2 launch anygrasp_ros detection.launch.py
```

### Start the UR10 Manipulator and Gripper with MoveIt

#### For `UR10 with soft two-finger gripper`

```bash
source install/setup.bash
ros2 launch grasping_control ur10_soft_two_fingers.launch.py
```

### Then Start the AnyGrasp Bridge

```bash
source install/setup.bash
ros2 launch anygrasp_grasping grasping_bridge.launch.py
```

### Finally Trigger One Grasp Cycle

```bash
source install/setup.bash
ros2 service call /anygrasp_grasping_node/run_grasp std_srvs/srv/Trigger {}
```

## Typical Run

1. Start MoveIt and the robot driver.
2. Calibrate or update `workspace.yaml` with `workspace_creation` if needed.
3. Start the gripper action server.
4. Start AnyGrasp.
5. Launch a `grasping_control` robot bringup such as `ur10.launch.py` or `ur10_soft_two_fingers.launch.py`.
6. Launch `grasping_bridge.launch.py`.
7. Trigger `/anygrasp_grasping_node/run_grasp`, or run the node with `server_mode:=false`.