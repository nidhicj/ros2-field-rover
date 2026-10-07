from setuptools import find_packages, setup

package_name = 'crawler_ros2'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Nidhi Joshi',
    maintainer_email='nidhicj@users.noreply.github.com',
    description='TODO: Package description',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'joystick = crawler_ros2.ui.joystick:main',
            'velocity_joy = crawler_ros2.ui.steer_accel_joystick:main',
            'velocity_ras = crawler_ros2.ui.steer_accel_raspad:main',
            'controller = crawler_ros2.controller.controller:main',
            'leftist = crawler_ros2.motion.left_motion:main',
            'rightist = crawler_ros2.motion.right_motion:main',
            'strightness = crawler_ros2.motion.straight_motion:main',
            'servo_node = crawler_ros2.servos.servo_control:main',
        ],
    },
)
