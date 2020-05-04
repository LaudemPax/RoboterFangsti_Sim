"""alphabot2_test_controller controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot

# create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

# setup camera
cam = robot.getCamera('alphabot_cam')
cam.enable(timestep)

cam_servo = robot.getMotor('cam_servo')
cam_servo.setPosition(float('inf'))
cam_servo.setVelocity(0.0)

# setup wheels
wheels = []
wheel_r = robot.getMotor('WHEEL_R')
wheel_l = robot.getMotor('WHEEL_L')

wheels.append(wheel_r)
wheels.append(wheel_l)

for wheel in wheels:
    wheel.setPosition(float('inf'))
    wheel.setVelocity(0.0)

# setup ir obstacle sensors
ir_left = robot.getDistanceSensor('ir_left')
ir_left.enable(timestep)

ir_right = robot.getDistanceSensor('ir_right')
ir_right.enable(timestep)

# obstacle avoidance indicators
led_obstacle_L = robot.getLED('led_obstacle_L')
led_obstacle_R = robot.getLED('led_obstacle_R')
led_obstacle_L.set(0)
led_obstacle_R.set(0)

# setup ustrasonic sensor
us_sensor = robot.getDistanceSensor('ultrasonic_sensor')
us_sensor.enable(timestep)

# line following sensor
ir_line = robot.getDistanceSensor('ir_line')
ir_line.enable(timestep)

# floor led
led_floor = robot.getLED('led_floor')
led_floor.set(1)

# define vars
speed = 4.0
ir_threshhold = 900
avoidRightCounter = 0
avoidLeftCounter = 0
avoidancePeriod = 30
cam_servoDirection = -1
cam_sweep_counter = 50
cam_sweep_speed = 0.5
led_color_duration = 100
led_change_counter = led_color_duration

# Main loop:
while robot.step(timestep) != -1:

    speed_L = 0
    speed_R = 0

    if avoidLeftCounter > 0:
        avoidLeftCounter -= 1
        # turn right
        speed_R = -speed
        speed_L = speed
        led_obstacle_L.set(1)
        led_obstacle_R.set(0)
    elif avoidRightCounter > 0:
        avoidRightCounter -= 1
        # turn left
        speed_R = speed
        speed_L = -speed
        led_obstacle_R.set(1)
        led_obstacle_L.set(0)
    elif ir_left.getValue() < ir_threshhold and ir_left.getValue() < ir_right.getValue():
        avoidLeftCounter = avoidancePeriod
    elif ir_right.getValue() < ir_threshhold and ir_right.getValue() < ir_left.getValue():
        avoidRightCounter = avoidancePeriod
    else:
        speed_L = speed
        speed_R = speed
        led_obstacle_L.set(0)
        led_obstacle_R.set(0)

    wheel_l.setVelocity(speed_L)
    wheel_r.setVelocity(speed_R)

    # camera sweeping motion
    if cam_sweep_counter > 0:
        cam_sweep_counter -= 1
        cam_servo.setVelocity(cam_sweep_speed * cam_servoDirection)
    else:
        cam_sweep_counter = 100
        cam_servoDirection *= -1

    # vary the floor led colour
    if led_change_counter < 0:
        if led_floor.get() == 1:
            led_floor.set(2)
        else:
            led_floor.set(1)
        led_change_counter = led_color_duration
    else:
        led_change_counter -= 1

    print("Sensors: ir_left: {0:.3f} ir_right: {1:.3f} usonic: {2:.3f} ir_line: {3:.3f}".format(ir_left.getValue(), ir_right.getValue(), us_sensor.getValue(), ir_line.getValue()))

# Enter here exit cleanup code.
