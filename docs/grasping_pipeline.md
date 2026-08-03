# AnyGrasp Grasping Pipeline

This document covers the pipeline controller implemented by the `anygrasp_grasping` package.

## Node

- Package: `anygrasp_grasping`
- Executable: `anygrasp_grasping`
- Default node name: `anygrasp_grasping_node`

When the node runs in server mode, it exposes the Trigger service `/anygrasp_grasping_node/run_grasp`.

## Responsibilities

The node only orchestrates the grasp cycle. It does not perform TF transforms or call MoveIt directly.

Its runtime flow is:

1. Call `anygrasp_msgs/srv/GetGrasps` with `count = 1`.
2. Take the first returned `geometry_msgs/PoseStamped`.
3. Send that pose to `motion_execution_node` through `grasping_msgs/action/MoveToPose`.
4. Close the gripper after a successful move.
5. Optionally request the post-grasp move through the same action interface.

This keeps grasp generation, arm motion, and gripper control loosely coupled.

## Running Modes

The node supports two operating modes through `server_mode`.

- `true` (default): wait for external requests through the Trigger service.
- `false`: run one grasp cycle immediately after startup and then exit.

### Trigger the service in server mode

Start the node in server mode with:

```bash
ros2 run anygrasp_grasping anygrasp_grasping
```

Then on a separate terminal, call the service with:

```bash
ros2 service call /anygrasp_grasping_node/run_grasp std_srvs/srv/Trigger {}
```

### Trigger the service in one-shot mode

```bash
ros2 run anygrasp_grasping anygrasp_grasping --ros-args -p server_mode:=false
```

## Launch

The package-level launch file is:

```bash
ros2 launch anygrasp_grasping grasping_bridge.launch.py
```

That launch only starts `anygrasp_grasping_node`.

Start robot driver, MoveIt, and `motion_execution_node` separately through `grasping_control`.

## AnyGrasp Interaction

The node expects an AnyGrasp service that returns a list of `geometry_msgs/PoseStamped` values.

- Default service name: `detection`
- Alternate service name used in this repo: `tracking`

The returned pose keeps the original point-cloud header. The node forwards that pose as-is and relies on `motion_execution_node` to transform it into the planning frame.

## Gripper Interaction

The node uses the standard `control_msgs/action/GripperCommand` action on `/gripper_command`.

- Open command: send `command.position=gripper_open_width` in meters.
- Close command: send `command.position=gripper_closed_width` in meters.
- Effort command: send `command.max_effort` in newtons when the active gripper backend is calibrated.

The default grasp cycle uses position-based closing by sending `max_effort=gripper_close_effort`.

Available helpers in the node:

- `close_gripper_position()`
- `close_gripper_torque(torque)`

The helper name is kept for compatibility; the value is sent as `max_effort` to `GripperCommand`.

## Post-Grasp Move

If `do_post_grasp_move` is enabled, the node asks `motion_execution_node` to execute the workspace-configured post-grasp pose. The bridge package does not own that pose configuration.

## Parameters

### Pipeline Behavior

- `server_mode`: expose the Trigger service when true, or run once and exit when false
- `anygrasp_service`: AnyGrasp service name, default `detection`
- `arm_action_name`: motion-execution action name, default `move_arm_to_pose`
- `do_post_grasp_move`: enable post-grasp motion, default `true`

### Gripper Actions

- `gripper_action_name`: default `/gripper_command`
- `gripper_open_width`: default `0.09`
- `gripper_closed_width`: default `0.0`
- `gripper_close_effort`: default `0.0`

## Required Services and Actions

For a successful cycle, the node depends on:

1. An AnyGrasp service configured by `anygrasp_service`.
2. A `grasping_msgs/action/MoveToPose` server configured by `arm_action_name`.
3. A `control_msgs/action/GripperCommand` server configured by `gripper_action_name`.

## Failure Cases

The pipeline returns failure when any of these stages fails:

- AnyGrasp service is unavailable or returns no pose.
- The motion-execution action server is unavailable.
- The motion-execution goal is rejected or aborts.
- The close-gripper action server is unavailable or the close action fails.
- The optional post-grasp move fails.

## Troubleshooting

- AnyGrasp call fails or returns no pose: check the configured service name with `ros2 service list` and inspect the AnyGrasp node logs.
- MoveToPose action not available: check the configured action name with `ros2 action list`.
- Gripper action not available: verify that the gripper driver is running and the configured action names exist.