from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():

    launch_args=[
        DeclareLaunchArgument(
            "zivid_type",
            default_value="tl",
            description="the model of zivid camera",
            choices=["os", "om", "ol", "tm", "tl"],
        )
    ]

    robot_description_content = Command(
            [
                PathJoinSubstitution([FindExecutable(name="xacro")]),
                " ",
                PathJoinSubstitution([FindPackageShare("zivid_description"),
                    "urdf",
                    "zivid_select.urdf.xacro"]),
                " ",
                "zivid_type:=",
                LaunchConfiguration('zivid_type'),
                " ",
                "prefix:=",
                LaunchConfiguration('prefix'),
            ]
        )

    robot_description = {"robot_description": robot_description_content}

    rviz_config_file = PathJoinSubstitution(
        [FindPackageShare('zivid_description'), "config", "config.rviz"]
    )

    robot_state_publisher_node = Node(
        name="robot_state_publisher",
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="both",
        parameters=[robot_description],
    )

    rviz_node = Node(
        name="rviz2",
        package="rviz2",
        executable="rviz2",
        output="log",
        arguments=["-d", rviz_config_file],
    )

    nodes = [
        robot_state_publisher_node,
        rviz_node,
    ]

    return LaunchDescription(launch_args + nodes)
