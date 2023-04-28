# Triac_control
This is a simple implementation of Phase angle control for a Triac. The code is written in micropython and has been tested on pi pico development board with RP2040 microcontroller.
The phase angle of the AC voltage applied across Load is controlled via MOC3022 optoisolater. The optoisolater features a high surge Isolation and thus protecting the sensetive electronics if something goes wrong.

Before getting started,You should note that this involves working with Mains voltage, I will be assuming that you know what your doing! If your new to circuits involving High voltages then be extra attentive and test your circuits using lower voltages (using a step-down transformer)before connecting mains.
RP2040 has interrupt at pin 2, this is used to detect a zero crossing pulse generated through a DP817 optocoupler.
The mains AC signal is stepped-down to 24V using a transformer and rectified using a Full Bridge Rectifier. The rectified output should not be filterd has we want to detect the peaks.
Since the applied AC signal had a frequency of 50Hz, the rectified unfiltered ouptut would have a frequency of 100Hz (the negetive peaks of AC are shifted to a DC level). This voltage is fed to the optocoupler through a current limiting resistor.
Choose right value for current limiting resistor by referencing the optocouplers datasheet. If your resistors seems to be a little hot (like mine),its probably because the power dissipation at resistor is quite high. The solution is using a resistor with higher power dissipation.
You can also use two resistors in series to divide the dissipation equally.

(do note that there are other methods for zero-crossing detection. You can directly connect the optocoupler to mains using quite large value resistors, but I find this not so safe while working,so I will stick with this method)

The Triac side of circuit consists of an RC snubber circuits. This is not mandatory if your using resistive loads like a heater but is essential if its an inductive load. I will be adding this anyway since it doesn't hurt to have the feature.
Since I'm working on a heater project,the snubber vlaues are just the default ones stated in MOC3022 datasheet. If you want to calculate exact values for your applicaton, I would recommend watching this youtube video as starter!
https://www.youtube.com/watch?v=wgNMepGIrTk&t=13s 


