from machine import Pin, ADC
import time

# GPIO pins for input
ZERO_CROSS_PIN = 2
ENC_PIN_A = 14
ENC_PIN_B = 15
# GPIO pin for output
TRIAC_PIN = 5

# Initialize the GPIO pins
zero_cross_pin = Pin(ZERO_CROSS_PIN, Pin.IN, Pin.PULL_UP)
enc_pin_a = Pin(ENC_PIN_A, Pin.IN, Pin.PULL_UP)
enc_pin_b = Pin(ENC_PIN_B, Pin.IN, Pin.PULL_UP)
triac_pin = Pin(TRIAC_PIN, Pin.OUT)
triac_pin.off()  # Set the triac_pin to low when script starts up

# Initialize encoder variables
last_enc_a = enc_pin_a.value()
last_enc_b = enc_pin_b.value()
encoder_pos = 0

# Define a callback function for the zero crossing interrupt
def zero_cross_callback(pin):
    # Clear the triac_pin to ensure the triac is off
    triac_pin.off()
    # Wait for a short period of time to allow the signal to stabilize
    time.sleep_us(10)
    delay_time=7760

    # Calculate the delay time for the triac pulse based on the encoder position
    delay_del = delay_time-(int(encoder_pos*10) ) # Scale encoder position to 0-10 microseconds
    print(delay_del)
    print("triggered")
    # Generate the triac pulse by turning on the triac_pin for the appropriate delay time
    triac_pin.off()
    time.sleep_us(delay_del)
    triac_pin.on()
    
    
    
# Define a callback function for the rotary encoder
def encoder_callback(pin):
    
    global encoder_pos
    global last_enc_a
    global last_enc_b

    # Turn off the triac before updating the encoder position
    triac_pin.off()

    # Read the current state of the encoder pins
    enc_a = enc_pin_a.value()
    enc_b = enc_pin_b.value()

    # Determine the direction of rotation based on the current and last state of the encoder pins
    if enc_a != last_enc_a:
        if enc_b != enc_a:
            encoder_pos += 1
        else:
            encoder_pos -= 1
            
    
    # Limit the encoder position to be non-negative
    if encoder_pos < 0:
        encoder_pos = 0

    # Update the last state of the encoder pins
    last_enc_a = enc_a
    last_enc_b = enc_b
        

# Attach the zero crossing interrupt to the zero_cross_pin
zero_cross_pin.irq(trigger=Pin.IRQ_RISING, handler=zero_cross_callback)

# Attach interrupts to the encoder pins to detect changes
enc_pin_a.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=encoder_callback)
enc_pin_b.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=encoder_callback)

triac_pin.off()
