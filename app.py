from serial_servo import *
import time


def timer(delay):
    start_time = time.time()
    time_diff = 0
    while time_diff < delay:
        a, b, c = svo1.ser.read()
        print("read_goal_pos = ", a,
              "read_pres_pos = ", b,
              "read_move_status = ", c)
        time_diff = time.time() - start_time


def move3svo(pos, svo_speed):
    svo1.servo_pos(pos, svo_speed)
    svo2.servo_pos(pos, svo_speed)
    svo3.servo_pos(pos, svo_speed)
    while svo1.isMoving() and svo2.isMoving() and svo3.isMoving():
        continue


def initial_setup():
    svo1.change_mod(0)
    svo2.change_mod(0)
    svo3.change_mod(0)


def main():
    svo_speed = 0
    while (True):
        move3svo(0, svo_speed)
        svo_speed += 250
        move3svo(90, svo_speed)
        svo_speed += 250
        move3svo(180, svo_speed)
        svo_speed += 250
        move3svo(270, svo_speed)
        svo_speed += 250
        move3svo(360, svo_speed)
        svo_speed += 250
        if svo_speed > 3500:
            svo_speed = 0

if __name__ == '__main__':
    svo1 = Servo(1)
    svo2 = Servo(2)
    svo3 = Servo(3)
    initial_setup()
    main()
