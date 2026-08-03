FROM ros:humble AS base

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    python3 \
    ros-${ROS_DISTRO}-rviz2 \
    ros-${ROS_DISTRO}-rqt-tf-tree \
    ros-${ROS_DISTRO}-teleop-twist-joy \
    ros-${ROS_DISTRO}-teleop-twist-keyboard \
    sudo  \
    iputils-ping \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

############################################################################
####      Add vscode user
############################################################################

# Add vscode user with same UID and GID as your host system
# (modified from https://code.visualstudio.com/remote/advancedcontainers/add-nonroot-user#_creating-a-nonroot-user)
# ubuntu now has a 1000 user ubuntu

ARG USERNAME=ubuntu
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && usermod -aG dialout $USERNAME

RUN echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

############################################################################
####        Install Anygrasp ROS packages
############################################################################

# make sure folders exist
WORKDIR /home/${USERNAME}/colcon_ws/src

RUN git clone https://github.com/CollaborativeRoboticsLab/anygrasp_ros.git

WORKDIR /home/${USERNAME}/colcon_ws/src/anygrasp_ros

## remove the anygrasp_ros package after cloning to avoid accidentally launching
## anygrasp_ros package by the user within this devcontainer. The user is 
## expected to use the external devcontainer for anygrasp_ros instead (which 
## provided with anygrasp_ros package). This is done to avoid unforeseen issues 
## that can occur due to unique setup (including system file changes) required 
## for anygrasp affecting other packages and systems

RUN rm -rf anygrasp_ros

############################################################################
####        Install Realsense packages
############################################################################

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    ros-${ROS_DISTRO}-librealsense2* \
    ros-${ROS_DISTRO}-realsense2-* \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

############################################################################
####        Install OMRON robot packages
############################################################################

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    ros-${ROS_DISTRO}-moveit \
    ros-${ROS_DISTRO}-controller-manager \
    ros-${ROS_DISTRO}-joint-trajectory-controller \
    ros-${ROS_DISTRO}-joint-state-broadcaster \
    ros-${ROS_DISTRO}-joint-state-publisher \
    ros-${ROS_DISTRO}-joint-state-publisher-gui \
    ros-${ROS_DISTRO}-gazebo-ros-pkgs \
    ros-${ROS_DISTRO}-ros-gz \
    ros-${ROS_DISTRO}-ros-gz-sim \
    ros-${ROS_DISTRO}-ign-ros2-control \
    ros-${ROS_DISTRO}-vision-opencv \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /home/${USERNAME}/colcon_ws/src/

RUN git clone https://github.com/CollaborativeRoboticsLab/tm2_ros2.git -b humble

############################################################################
####        Install grippers packages
############################################################################

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    python3-serial \
    ros-${ROS_DISTRO}-dynamixel-sdk \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /home/${USERNAME}/colcon_ws/src/

RUN git clone https://github.com/CollaborativeRoboticsLab/grippers.git


############################################################################
####        Install grasping packages
############################################################################

WORKDIR /home/${USERNAME}/colcon_ws/src/

RUN git clone https://github.com/CollaborativeRoboticsLab/grasping.git

############################################################################
####        Change user
############################################################################

# Switch from root to user
USER $USERNAME

# Source the ROS setup file
RUN echo "source /opt/ros/${ROS_DISTRO}/setup.bash" >> ~/.bashrc
