from .serial import Serial
from .ra_error import *


class Servo():
    def __init__(self, ID):
        self.ser = Serial(ID)
        self.ID = ID
        self.pos = None
        self.ser_spd = 0

    def change_mod(self, mode):
        int_arr = [0xFF, 0xFF, self.ID, 4, 3, 33, mode, 0x00]
        self.ser.send(int_arr)
        print("ID ", self.ID, " change mode", mode, "ok")

    def servo_pos(self, pos, ser_spd):
        self.pos = int(pos/360*4095)
        self.ser_spd = ser_spd
        int_arr = [0xFF, 0xFF, self.ID, 9, 3, 0x2A, self.pos % 256, self.pos >> 8, 0, 0,
                   int(self.ser_spd) % 256, int(self.ser_spd) >> 8, 0x00]
        self.ser.send(int_arr)

    def isMoving(self):
        a, b, c = self.ser.read()
        print("ID : ",self.ID ," | read_goal_pos = ", a, " | read_pres_pos = ", b, " | read_move_status = ", c)
        if c == 1:
            return True  # return 1009 while it is moving
        if c == 0:
            return False  # return 0 while stopped
        raise RAError()
    
    def clamp(self, n, minn, maxn):
        return max(min(maxn, n), minn)


"""
    def moveJoint(self, jPos):
        msg = 'MoveJ,0,' \
            + str(jPos.j1) + ',' + str(jPos.j2) + ',' \
            + str(jPos.j3) + ',' + str(jPos.j4) + ',' \
            + str(jPos.j5) + ',' + str(jPos.j6) + ',;'
        reply = self.ser.send(msg)
        self._validate(reply)
    
    def setSpeed(self, speed: int):
        msg = 'SetOverride,0,' \
            + str(speed) + ',;'
        reply = self.ser.send(msg)
        self._validate(reply)

    def getSpeed(self) -> int:
        msg = 'ReadOverride,0,;'
        reply = self.ser.send(msg)
        self._validate(reply)
        values = reply.split(',')
        if len(values) < 4:
            raise RAError('Received invalid response.')
        return values[2]
        
    def moveGripper(self, position, speed=250, force=10):
        self.clamp(position,0,140)
        self.clamp(speed,30,250)
        self.clamp(force,10,125)
        msg = 'SetRobotiq,' + str(position) + ',' + str(speed) + ',' + str(force) + ',;'
        reply = self.ser.send(msg)
        self._validate(reply)
    
    def resetGripper(self):
        msg = 'RobotIQReset,;'
        reply = self.ser.send(msg)
        self._validate(reply) #check if error raised
        print(reply)

    def isGripperMoving(self):
        reply = self.ser.send('RobotiqStatus,;')
        self._validate(reply)
        if reply == 'RobotiqStatus,OK,0,3,1,1,;':
            return True #return True while its moving
        if reply == 'RobotiqStatus,OK,2,3,1,1,;':
            return False #return True while it is grasping an object    
        if reply == 'RobotiqStatus,OK,3,3,1,1,;':
            return False #return False when the action is done
        raise RAError()
"""
