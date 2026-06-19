# Launch Arguments

## Shared Pipeline Arguments

| Argument | Default | Description |
| --- | --- | --- |
| `server_mode` | `true` | Exposes the `/anygrasp_grasping_node/run_grasp` Trigger service when enabled. When set to `false`, the node executes one grasp cycle and exits. |
| `anygrasp_service` | `detection` | Name of the AnyGrasp service queried for candidate grasp poses. |
| `arm_action_name` | `move_arm_to_pose` | Name of the `grasping_msgs/action/MoveToPose` action server used to forward the selected grasp pose to `motion_execution_node`. |
| `open_action_name` | `/open_gripper` | Name of the gripper action used before the grasp attempt to open the gripper. |
| `close_action_name` | `/close_gripper` | Name of the gripper action used after the arm reaches the target pose to close the gripper. |
| `do_post_grasp_move` | `true` | Requests the post-grasp move from the control stack after a successful close when enabled. |
