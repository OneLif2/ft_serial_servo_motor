import serial  # pip3 install pyserial
import time

class Serial_rw:
    def __init__(self, ID):
        baudrate_STS = 1000000
        self.ID = ID
        try:
            port = "/dev/ttyUSB0"
            self.ser = serial.Serial(
                port, baudrate=baudrate_STS, bytesize=8, parity='N', stopbits=1, timeout=0.05)
        except Exception:
            port = "/dev/ttyUSB1"
            self.ser = serial.Serial(
                port, baudrate=baudrate_STS, bytesize=8, parity='N', stopbits=1, timeout=0.05)

        self.ser.read_all().hex()

    def update_check_digit(self, int_arr):
        checksum = 0
        for i in int_arr[2:-1]:
            checksum += i
        int_arr[-1] = (checksum & 255) ^ 255  # BitAND then BitXOR
        return int_arr

    def get_data(self, read_arr):
        newdata_hex = ""
        # Continue reading until we receive a frame that starts with the
        # expected header and contains enough data.  The previous logic used
        # ``and`` which would stop reading as soon as one of the conditions was
        # False.  That meant that data not starting with ``ffff`` could end the
        # loop prematurely when the length requirement was already satisfied.
        # Using ``or`` ensures we only exit when both conditions are met.
        while not newdata_hex.startswith("ffff") or len(newdata_hex) < 72:
            self.ser.write(serial.to_bytes(self.update_check_digit(read_arr)))
            time.sleep(0.06)
            newdata_hex = self.ser.read_all().hex()
            #print("newdata_hex_get",newdata_hex, len(newdata_hex))
            if self.ID == 254:
                break
        return newdata_hex

    def send(self, int_arr):
        newdata_hex = ""
        int_arr = self.update_check_digit(int_arr)
        # Wait until we receive an acknowledgement that starts with the
        # expected header and reports an "OK" status.  Similar to ``get_data``
        # the original code used ``and`` which could prematurely exit if one
        # condition became False before the other.  The loop should continue
        # while either condition is not satisfied.
        while not newdata_hex.startswith("ffff") or not newdata_hex[8:10] == "00":
            self.ser.write(serial.to_bytes(int_arr))
            time.sleep(0.06)
            newdata_hex = self.ser.read_all().hex()
            #print("newdata_hex_send",newdata_hex, len(newdata_hex))
            if self.ID == 254:
                break
        #print("To ID",self.ID,"SEND OK")
        return newdata_hex
