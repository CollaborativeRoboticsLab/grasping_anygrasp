from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
	grasping_anygrasp_node = Node(
		package='grasping_anygrasp',
		executable='grasping_anygrasp',
		name='grasping_anygrasp_node',
		output='screen',
		parameters=[
			{
				'server_mode': LaunchConfiguration('server_mode'),
				'anygrasp_service': LaunchConfiguration('anygrasp_service'),
				'arm_action_name': LaunchConfiguration('arm_action_name'),
				'arm_named_pose_action_name': LaunchConfiguration('arm_named_pose_action_name'),
				'do_post_grasp_move': LaunchConfiguration('do_post_grasp_move'),
				'gripper_action_name': LaunchConfiguration('gripper_action_name'),
				'gripper_open_width': LaunchConfiguration('gripper_open_width'),
				'gripper_closed_width': LaunchConfiguration('gripper_closed_width'),
				'gripper_close_effort': LaunchConfiguration('gripper_close_effort'),
			}
		],
	)

	return LaunchDescription(
		[
			DeclareLaunchArgument('server_mode', default_value='true'),
			DeclareLaunchArgument('anygrasp_service', default_value='detection'),
			DeclareLaunchArgument('arm_action_name', default_value='move_arm_to_pose'),
			DeclareLaunchArgument('arm_named_pose_action_name', default_value='move_arm_to_named_pose'),
			DeclareLaunchArgument('gripper_action_name', default_value='/gripper_command'),
			DeclareLaunchArgument('gripper_open_width', default_value='0.09'),
			DeclareLaunchArgument('gripper_closed_width', default_value='0.0'),
			DeclareLaunchArgument('gripper_close_effort', default_value='0.0'),
			DeclareLaunchArgument('do_post_grasp_move', default_value='true'),
			grasping_anygrasp_node,
		]
	)