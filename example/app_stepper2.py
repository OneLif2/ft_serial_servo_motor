# Example for stepper servo mode
import os
import sys
# Append parent directory to import path, import file from parent directory
sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print(__file__) #./file.py
print(os.path.abspath(__file__)) #./file.py
print(os.path.dirname(os.path.abspath(__file__))) #./
print(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) #../

from serial_servo import *
import time


def timer(delay):
    start_time = time.time()
    time_diff = 0
    while time_diff < delay:
        a, b, c, d = svo1.read_mv_status()
        print("read_goal_pos = ", a, "read_pres_pos = ",
              b, "read_move_status = ", c)
        time_diff = time.time() - start_time


def move3svo(pos, svo_speed=-1):
    svo1.servo_pos_spd(pos, svo_speed)
    svo2.servo_pos_spd(pos, svo_speed)
    svo3.servo_pos_spd(pos, svo_speed)
    while svo1.isMoving() and svo2.isMoving() and svo3.isMoving():
        continue


def initial_setup():
    svo1.change_mod(0)
    svo2.change_mod(0)
    svo3.change_mod(0)


def stepper_mode():
    #initial_setup()
    print("====RESET Position to Zero====")
    print("==============================")
    #svo_all.servo_pos_spd(0, 0)  # reset position to zero
    while svo1.isMoving() and svo2.isMoving() and svo3.isMoving():
        continue

    svo_all.change_mod(3)
    read_all_motor_info()
    print(svo1.read_pos_ctr)
    print(svo2.read_pos_ctr)
    print(svo3.read_pos_ctr)
    svo1.servo_pos_spd(-svo1.read_pos_ctr, 0)
    svo2.servo_pos_spd(-svo2.read_pos_ctr, 0)
    svo3.servo_pos_spd(-svo3.read_pos_ctr, 0)
    while svo1.isMoving() and svo2.isMoving() and svo3.isMoving():
        continue

    read_all_motor_info()
    print(svo1.read_pos_ctr)
    print(svo2.read_pos_ctr)
    print(svo3.read_pos_ctr)
    time.sleep(1)


def read_all_motor_info():
    svo1.read_all_info()
    svo2.read_all_info()
    svo3.read_all_info()


def main():
    move3svo(-360*2,2000)
    read_all_motor_info()
    time.sleep(1)
    # move3svo(360*2)
    # read_all_motor_info()
    # time.sleep(5)
    svo1.read_all_info()
    time.sleep(1)


if __name__ == '__main__':
    svo1 = Servo(1)
    svo2 = Servo(2)
    svo3 = Servo(3)
    svo_all = Servo(254, 3)
    stepper_mode()
    svo1.setSpeed(500)
    svo2.setSpeed(500)
    svo3.setSpeed(500)
    main()
