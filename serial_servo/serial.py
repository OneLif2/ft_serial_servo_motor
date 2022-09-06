import serial  # pip3 install pyserial
import time


class Serial:
    def __init__(self, ID):
        baudrate_STS = 1000000
        self.read_goal_pos = 0
        self.read_curr_pos = 0
        self.read_move_state = 0
        try:
            port = "/dev/ttyUSB0"
            self.ser = serial.Serial(
                port, baudrate=baudrate_STS, bytesize=8, parity='N', stopbits=1, timeout=0.05)
        except Exception:
            port = "/dev/ttyUSB1"
            self.ser = serial.Serial(
                port, baudrate=baudrate_STS, bytesize=8, parity='N', stopbits=1, timeout=0.05)

        self.ID = ID
        self.GOAL_POS = 0x2A  # 2 bytes
        self.CURR_POS = 0x38  # 2 bytes
        self.MOVE_STATE = 0x42  # 1 bytes

        self.GOAL_POS = self.GOAL_POS - 0x25
        self.CURR_POS = self.CURR_POS - 0x25
        self.MOVE_STATE = self.MOVE_STATE - 0x25
        self.ser.read_all().hex()

    def str2arr(self, newdata_hex, split_strings):
        for index in range(0, len(newdata_hex), 2):
            split_strings.append(int(newdata_hex[index: index + 2], 16))

    def hexdata(self, a):
        print('[{}]'.format(', '.join(hex(x) for x in a)))

    def update_check_digit(self, int_arr):
        checksum = 0
        for i in int_arr[2:-1]:
            checksum += i
        int_arr[-1] = (checksum & 255) ^ 255  # BitAND then BitXOR
        return int_arr

    def calculate_checksum(self, int_arr):
        checksum = 0
        for i in int_arr[2:-1]:
            checksum += i
        return (checksum & 255) ^ 255 == int_arr[-1]

    def read(self):
        split_strings = []
        newdata_hex = self.get_data()
        self.str2arr(newdata_hex, split_strings)
        #self.hexdata(split_strings)
        if self.calculate_checksum(split_strings) == True:
            self.read_goal_pos = split_strings[self.GOAL_POS] & 0xff | (
                split_strings[self.GOAL_POS+1] & 0xff) << 8
            self.read_curr_pos = split_strings[self.CURR_POS] & 0xff | (
                split_strings[self.CURR_POS+1] & 0xff) << 8
            self.read_move_state = (split_strings[self.MOVE_STATE]) & 0xff
        return self.read_goal_pos, self.read_curr_pos, self.read_move_state
    
    def get_data(self):
        newdata_hex = ""
        read_arr = [0xff, 0xff, self.ID, 0x4, 0x2, 0x2a, 0x1e, 0x00]
        while not newdata_hex.startswith("ffff") and len(newdata_hex) < 72:
            self.ser.write(serial.to_bytes(self.update_check_digit(read_arr)))
            time.sleep(0.06)
            newdata_hex = self.ser.read_all().hex()
            #print("newdata_hex_get",newdata_hex, len(newdata_hex))
        return newdata_hex

    def send(self, int_arr):
        newdata_hex = ""
        int_arr = self.update_check_digit(int_arr)
        while not newdata_hex.startswith("ffff") and len(newdata_hex) < 12:
            self.ser.write(serial.to_bytes(int_arr))
            time.sleep(0.06)
            newdata_hex = self.ser.read_all().hex()
            #print("newdata_hex_send",newdata_hex, len(newdata_hex))
        return newdata_hex
