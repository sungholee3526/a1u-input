import serial

REQUEST_BYTES = bytes([0xA6, 0x01, 0x00])

def print_byte(byte: int):
    print('{:08b}'.format(byte))

with serial.Serial('/dev/cu.usbserial-A50285BI', 115200) as s:
    while True:
        s.write(REQUEST_BYTES)
        res = s.read(18)
        # print(res.hex(' '))
        print_byte(res[4])
