# Known issues and used fixes

## 1. System-wide python package installation blocked

docker container uses following command to unblock system package installation.

```bash
python -m pip config set global.break-system-packages true
```

## 2. Feature ID not being fixed for docker

This devcontainer uses a docker network `bridge` and a fixed mac address to stablize the feature id.

## 3. Devcontainer not connecting to robot with bridge networking

If you are running inside the devcontainer with Docker bridge networking, set `reverse_ip` to the host machine's IP on the robot network so the robot can connect back to ports `50001`, `50003`, and `50004`. 

In the devcontainer.json add,

```json
  "runArgs": [
    "--network=bridge",
    "-p",
    "50001:50001",
    "-p",
    "50002:50002",
    "-p",
    "50003:50003",
    "-p",
    "50004:50004"
  ],
```

while in the ur10.launch.py, set the default value of `reverse_ip` to the host machine's IP on the robot network.

```python
DeclareLaunchArgument('reverse_ip', default_value=' <host_robot_network_ip>'),
```

Then launch the arm control node with:

```bash
source install/setup.bash
ros2 launch grasping_control ur10.launch.py
``` 