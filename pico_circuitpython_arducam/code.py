import time as utime
import busio
import board
import usb_cdc
from Arducam import *
from board import *

import digitalio
import gc
from adafruit_wiznet5k.adafruit_wiznet5k import WIZNET5K
from adafruit_wiznet5k.adafruit_wiznet5k import *
from adafruit_wiznet5k.adafruit_wiznet5k_socket import socket
from adafruit_wiznet5k.adafruit_wiznet5k_socket import *
        
once_number=1024
#once_number=128
mode = 0
prev_mode = mode
start_capture = 0
stop_flag=0
data_in=0
value_command=0
flag_command=0
buffer=bytearray(once_number)

mycam = ArducamClass(OV2640)
mycam.Camera_Detection()
mycam.Spi_Test()
mycam.Camera_Init()
utime.sleep(1)
mycam.clear_fifo_flag()

def read_fifo_burst_socket(cli_sock, length):
    count=0
    mycam.SPI_CS_LOW()
    mycam.set_fifo_burst()
    while True:
        mycam.spi.readinto(buffer,start=0,end=once_number)
        cli_sock.send(buffer)
        count+=once_number
        if count+once_number>length:
            count=length-count
            mycam.spi.readinto(buffer,start=0,end=count)
            cli_sock.send(buffer[0:count])
            mycam.SPI_CS_HIGH()
            mycam.clear_fifo_flag()
            break

    gc.collect()    
    return length   


def w5x00_init():
    ##SPI0
    SPI0_SCK = board.GP18
    SPI0_TX = board.GP19
    SPI0_RX = board.GP16
    SPI0_CSn = board.GP17

    ##reset
    W5x00_RSTn = board.GP20

    print("Wiznet5k (DHCP)")

    # Setup your network configuration below
    # random MAC, later should change this value on your vendor ID
    MY_MAC = (0x00, 0x08, 0xDC, 0x1D, 0x6B, 0x52)
    IP_ADDRESS = (192, 168, 0, 5)
    SUBNET_MASK = (255, 255, 255, 0)
    GATEWAY_ADDRESS = (192, 168, 0, 1)
    DNS_SERVER = (8, 8, 8, 8)

    ethernetRst = digitalio.DigitalInOut(W5x00_RSTn)
    ethernetRst.direction = digitalio.Direction.OUTPUT

    led = digitalio.DigitalInOut(board.GP25)
    led.direction = digitalio.Direction.OUTPUT

    # For Adafruit Ethernet FeatherWing
    cs = digitalio.DigitalInOut(SPI0_CSn)
    spi_bus = busio.SPI(SPI0_SCK, MOSI=SPI0_TX, MISO=SPI0_RX)

    # Reset W5500 first
    ethernetRst.value = False
    time.sleep(1)
    ethernetRst.value = True


    # Initialize ethernet interface without DHCP
    eth = WIZNET5K(spi_bus, cs, is_dhcp=True, mac=MY_MAC)

    # Set network configuration
    #eth.ifconfig = (IP_ADDRESS, SUBNET_MASK, GATEWAY_ADDRESS, DNS_SERVER)
    print("Chip Version:", eth.chip)
    print("MAC Address:", [hex(i) for i in eth.mac_address])
    print("My IP address is:", eth.pretty_ip(eth.ip_address))
    print("Done!")

    return eth, led


def httpServer_init():
    eth, led = w5x00_init()
    set_interface(eth)
    sock = socket()
    return sock


def httpServer_listen(sock):
    sock.bind((None, 80))
    sock.listen()
    
def httpServer_accept(sock):    
    cli_sock, addr = sock.accept()
    while not cli_sock.connect:
        time.sleep(0.01)
    print('Connect')
    return cli_sock

def httpServer_read(cli_sock, max_retries=3, retry_interval=1):
    retry_count = 0
    while retry_count < max_retries:
        request = cli_sock.recv()
        print(request)
        if len(request) > 0:
            request = request.decode("utf-8")
            reqlines = request.split('\r\n')
            method = reqlines[0].split(' ')
            print(method)
            print(method[1][1:])
            return True, method[1][1:]
        else:
            # 요청이 빈 값일 경우, 재시도 로직
            retry_count += 1
            utime.sleep(retry_interval)  # 재시도 전 일정 시간 대기
    # 최대 재시도 횟수를 초과했을 경우s
    print("Stop")
    return False, b''

def httpServer_response_single(cli_sock):
    print('httpServer_response_single()')
    length = mycam.read_fifo_length()
    print(length)
    cli_sock.send(b'HTTP/1.1 200 OK\n')
    cli_sock.send(b'Connection: close\n')
    cli_sock.send(b"Content-Type: image/jpeg\n")
    cli_sock.send(b"Access-Control-Allow-Origin: *\n") # CORS 헤더 추가
    cli_sock.send(b"Content-Length: %d\n\n" % length)
    read_fifo_burst_socket(cli_sock, length)
    print('response done')

def httpServer_close(cli_sock):
    cli_sock.disconnect()
    time.sleep(0.05)


#########################################################################

mycam.OV2640_set_Light_Mode(Auto)
mycam.OV2640_set_Color_Saturation(Saturation0)
mycam.OV2640_set_Brightness(Brightness0)
mycam.OV2640_set_Contrast(Contrast0)
mycam.OV2640_set_Special_effects(Normal)
mycam.OV2640_set_JPEG_size(OV2640_320x240)
mycam.set_format(JPEG)
mycam.Camera_Init()
mycam.set_bit(ARDUCHIP_TIM,VSYNC_LEVEL_MASK)

sock = httpServer_init()
httpServer_listen(sock)

while True:
    cli_sock = httpServer_accept(sock)

    while True:
        has_cmd, cmd = httpServer_read(cli_sock)

        if has_cmd:
            value_command = cmd
            flag_command=1
        if flag_command==1:
            flag_command=0
            try:
                value = int(value_command)
                #print(value)
            except:
                value = -1
                httpServer_close(cli_sock)
                break
                
            if value==0:
                mycam.OV2640_set_JPEG_size(OV2640_160x120)
            elif value==1:
                mycam.OV2640_set_JPEG_size(OV2640_176x144)
            elif value==2:
                mycam.OV2640_set_JPEG_size(OV2640_320x240)
            elif value==3:
                mycam.OV2640_set_JPEG_size(OV2640_352x288)
            elif value==4:
                mycam.OV2640_set_JPEG_size(OV2640_640x480)
            elif value==5:
                mycam.OV2640_set_JPEG_size(OV2640_800x600)
            elif value==6:
                mycam.OV2640_set_JPEG_size(OV2640_1024x768)
            elif value==7:
                mycam.OV2640_set_JPEG_size(OV2640_1280x1024)
            elif value==8:
                mycam.OV2640_set_JPEG_size(OV2640_1600x1200)
            elif value==0x10:
                print('single capture')
                mode=1
                start_capture=1
            elif value==0x11:
                mycam.set_format(JPEG)
                mycam.Camera_Init()
                mycam.set_bit(ARDUCHIP_TIM,VSYNC_LEVEL_MASK)
            elif value==0x20:
                print('stream capture')
                mode=2
                start_capture=2
                stop_flag=0
                httpServer_response_stream_init(cli_sock)
            elif value==0x21:
                stop_flag=1
            elif value==0x30:
                mode=3
                start_capture=3
                
        if mode==1:
            if start_capture==1:
                mycam.flush_fifo();
                mycam.clear_fifo_flag();
                mycam.start_capture();
                start_capture=0
            if mycam.get_bit(ARDUCHIP_TRIG,CAP_DONE_MASK)!=0:
                #read_fifo_burst_socket(eth, s)
                httpServer_response_single(cli_sock)
                mode=0
        elif mode==2:
            if stop_flag==0:
                if start_capture==2:
                    start_capture=0
                    mycam.flush_fifo();
                    mycam.clear_fifo_flag();
                    mycam.start_capture();
                if mycam.get_bit(ARDUCHIP_TRIG,CAP_DONE_MASK)!=0:
                    httpServer_response_stream_burst(cli_sock)
                    #read_fifo_burst_socket(eth, s)
                    start_capture=2
            else:
                mode=0
                start_capture=0
        
        if mode == 0:
            if prev_mode != mode:
                print('Stop')
                httpServer_close(cli_sock)
                break

        prev_mode = mode