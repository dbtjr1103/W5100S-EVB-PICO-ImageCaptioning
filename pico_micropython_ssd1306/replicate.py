from machine import Pin, SPI, I2C
import network
import utime
import urequests
import json
import ssd1306

# Initialize OLED
def init_oled():
    i2c = I2C(1, scl=Pin(7), sda=Pin(6))
    display = ssd1306.SSD1306_I2C(128, 32, i2c)
    display.fill(0)
    display.show()
    return display

# Initialize W5x00
def init_ethernet():
    spi = SPI(0, 2_000_000, mosi=Pin(19), miso=Pin(16), sck=Pin(18))
    nic = network.WIZNET5K(spi, Pin(17), Pin(20))   # spi, cs, reset pin
    nic.active(True)
    while not nic.isconnected():
        utime.sleep(1)
        print('Connecting to ethernet...')
    print(f'Ethernet connected. IP: {nic.ifconfig()}')

def get_prediction_result(api_key, prediction_id):
    url = f"https://api.replicate.com/v1/predictions/{prediction_id}"
    headers = {"Authorization": f"Token {api_key}"}
    
    while True:
        response = urequests.get(url, headers=headers)
        result = json.loads(response.text)
        
        if result['status'] == 'succeeded':
            return result
        elif result['status'] == 'failed':
            print("Prediction failed")
            return None
        
        utime.sleep(1)
        
def wrap_text(text, max_chars=15):  # Set max_chars to 15
    if len(text) <= max_chars:
        return [text]

    return [text[:max_chars], text[max_chars:]]

def display_text(display, text, max_chars=15):
    lines = wrap_text(text, max_chars)
    y = 0
    for line in lines:
        display.text(line, 0, y, 1)
        y += 8
        
def main():
    display = init_oled()
    init_ethernet()

    api_key = "r8_JN1hLtD70SeB5og7RvdagRCiCo6zpuE3LhJsJ"
    url = "https://api.replicate.com/v1/predictions"
    #input_image_url = "https://github.com/dbtjr1103/W5100S-EVB-PICO-WORKINGASSISTANT/blob/main/image.jpg?raw=true"
    input_image_url = "http://222.98.173.248:80/16"
    
    headers = {"Authorization": f"Token {api_key}", "Content-Type": "application/json"}
    data = {
        "version": "4b32258c42e9efd4288bb9910bc532a69727f9acd26aa08e175713a0a857a608",
        "input": {"image": input_image_url, "caption":True}
    }

    response = urequests.post(url, headers=headers, data=json.dumps(data))
    response_data = json.loads(response.text)
    print(response_data)  # Print response data

    prediction_id = response_data['id']

    print(f"Prediction ID: {prediction_id}")
    print("Getting prediction result...")
    result = get_prediction_result(api_key, prediction_id)
    print(result)
    print("Prediction result:", result['output'])
    
    # Displaying the result on the screen
    print("Displaying result on screen...")
    display.fill(0)
    display_text(display, str(result['output']))
    display.show()
    print("Result displayed on screen.")
    
main()

