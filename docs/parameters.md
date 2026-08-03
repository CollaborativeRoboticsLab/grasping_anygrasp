# Launch Arguments

## Shared Pipeline Arguments

| Argument | Default | Description |
| --- | --- | --- |
| `server_mode` | `true` | Exposes the `/grasping_anygrasp_node/run_grasp` Trigger service when enabled. When set to `false`, the node executes one grasp cycle and exits. |
| `anygrasp_service` | `detection` | Name of the AnyGrasp service queried for candidate grasp poses. |
| `arm_action_name` | `move_arm_to_pose` | Name of the `grasping_msgs/action/MoveToPose` action server used to forward the selected grasp pose to `motion_execution_node`. |
| `gripper_action_name` | `/gripper_command` | Name of the `control_msgs/action/GripperCommand` action used for open and close commands. |
| `gripper_open_width` | `0.09` | Jaw opening in meters used before the grasp attempt to open the gripper. |
| `gripper_closed_width` | `0.0` | Jaw opening in meters used after the arm reaches the target pose to close the gripper. |
| `gripper_close_effort` | `0.0` | Close command `max_effort` in newtons when calibrated. |
| `do_post_grasp_move` | `true` | Requests the post-grasp move from the control stack after a successful close when enabled. |
