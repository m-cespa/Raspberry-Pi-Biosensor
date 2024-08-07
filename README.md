# Method: (for RPI Model 3B)

**PCA9546** (4 Channel Multiplexer):\
The multiplexer was used to hook 4 BME280's onto 1 rpi. The multiplexer's package `adafruit-circuitpython-tca9548a` was installed to initialise multiple same address i2c device access [1](https://learn.adafruit.com/adafruit-tca9548a-1-to-8-i2c-multiplexer-breakout/circuitpython-python). The `mux` list seen in the script contains the devices connected to each of the multiplexer's 4 channels. The PCA9546's specifications can be found here [2](https://www.adafruit.com/product/5663).


**BME280** (Pressure, Temperature, Humidity):\
The sensor's adafruit package `adafruit-circuitpython-bme280` was installed to access the sensor class' methods [3](https://pypi.org/project/adafruit-circuitpython-bme280/). The adafruit package was used rather than the standard `bme280` package as creating instances of the `BME280` class in the adafruit package automates calibration which was convenient given multiple instances were called. If using a single BME280, it can be initialised in the script following the steps given by the `bme280` package's repository [4](https://pypi.org/project/RPi.bme280/). The `smbus2` package [5](https://pypi.org/project/smbus2/) did not need to be installed for our configuration using the multiplexer and `adafruit-circuitpython-bme280` package (for the `smbus2` method, refer to [6](https://randomnerdtutorials.com/raspberry-pi-bme280-python/)). For our purposes, the i2c initialisation steps were done for the multiplexer, and for each of the 4 entires in `mux`, the `0x76` address device (the BME280) was passed as argument. Each BME280 was connected to a pair of clock (SCL) and data (SDA) pins on the multiplexer. The BME280's specifications can be found here [7](https://thepihut.com/products/bme280-environmental-sensor#:~:text=A%20tiny%20sensor%20breakout%20with,3.3V%2F5V%20voltage%20levels.).


**DS18B20** (1-Wire Temperature):\
The sensor was connected to the rpi following the steps given by [8](https://www.circuitbasics.com/raspberry-pi-ds18b20-temperature-sensor-tutorial/). The sensor's package `ds18b20` was installed and imported to access the sensor class' methods. The DS18B20 was initialised in the script following the steps given by the 'Setup' section of the package's GitHub repository [9](https://github.com/rgbkrk/ds18b20). The DS18B20's specifications can be found here [10](https://thepihut.com/products/ds18b20-one-wire-digital-temperature-sensor).


**ADS1115** (4 Analogue-Digital Converter for Turbidity):\
The sensor was connected across the same SCL/SDA pins as the PCA9546. The two devices have different addresses (`0x70` for PCA9546 & `0x48`,`0x49` for 2 ADS1115) and can be recognised as different inputs along the same i2c pins. To check that both multiplexer (mux) and analogue-digital converter (adc) are being read by the rpi, type `sudo i2cdetect -y 1` into the terminal and the above addresses should appear.

The following lines were passed into terminal (order specific) to install the `ads1x15` library:
1. `pip3 install --upgrade adafruit-python-shell`
2. `wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py`
3. `python3 raspi-blinka.py`
4. `pip3 install adafruit-circuitpython-ads1x15`\

To run multiple adc's on the same rpi i2c pins, the multiple address feature of the ADS1115 was used. Connecting the ADDR pin to one of GND, VIN, SDA, SCL will change the device address to `0x48`, `0x49`, `0x4a`, `0x4b` accordingly. When creating the `ADS.ADS1115` object, the same `i2c` argument as for the mux is passed to all ADS1115 provided they are in fact all connected to the same i2c bus whilst the address argument is altered as required.

(python packages were all installed to a virtual environment, see [11](https://learn.adafruit.com/python-virtual-environment-usage-on-raspberry-pi/overview) for documentation)\
NOTE: the `board` package must not be installed explicitly, it is installed via the `raspi.blinka` package. Concurrent explicit installation of the package can cause package failure. Further documentation on installing the `adafruit` and `blinka` packages necessary for the ADS1115 can be found here [12](https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi). The ADS1115 was initialised in the script following the steps given by [13](https://www.instructables.com/How-to-Use-ADS1115-With-the-Raspberry-Pi-Part-1/). The ADS1115's specifications can be found here [14](https://thepihut.com/products/adafruit-ads1115-16-bit-adc-4-channel-with-programmable-gain-amplifier).

The `busio` package was also installed. Either the `busio` or `board` packages can be used to initialise i2c bus connections. The `busio` package allows for explicit intialisation of an i2c connection where the clock and data i2c pins can be specified (if a non default i2c bus is being used). The `board` package's `I2C()` method (`i2c_init = board.I2C()`) on the other hand will initialise the i2c bus using the standard clock and data pins. To enable future intialisation of non-default i2c buses, the `busio` initialisation (which still requires the `board` package) was chosen.


**IR EMITTER-RECEIVER**:\
To yield a proxy measurement of solution turbidity, a pair of IR emitter and IR Photodiode were used. The WL-TIRC THT Infrared Round Waterclear was selected as an emitter (datasheet: [15](https://docs.rs-online.com/c30e/A700000007241424.pdf)) and the IR T-1 3/4 PIN Silicon Photodiode as a receiver (datasheet: [16](https://docs.rs-online.com/461d/0900766b808b25c5.pdf)), to note: the photodiode is opaque to visible light. Photodiodes were positioned at 180° and 90° on the opposing side of the reactor beakers to measure through and deflected beams accordingly. To measure only the change in voltage across the photodiodes, an op-amp differential amplifier circuit was trialled where one photodiode would be in an isolated environment and the other exposed to IR. Due to variations in the base resistances of the photodiodes, wires and resistors, this configuration resulted in non-zero base reading output and was hence not used. Instead, a background dataset was first obtained with the base voltage readings across the photodiodes which could then be subtracted from the experimental data series. The IR emitters were put in series with 39Ω ±5% resistors and the photodiodes in series with 47Ω ±5% resistors. The voltages across the photodiodes were passed into the ADS1115.


**PWM STIRRER**:\
Cooling fans with magnets were used to drive magnetic stirrer beads in each reactor beaker. The `PWM_Stirrer.py` script was run in the background to `ALL_Sensors.py` to keep the stirrers rotating at a prescribed fixed velocity. The script uses the `RPi.GPIO` package which should be pre-installed on updated versions of Raspbian - to check this refer to [17](https://sourceforge.net/p/raspberry-gpio-python/wiki/install/).


**FULL SENSORS CONFIG** (per reactor):
*   1 BME (pressure, temperature, humidity)
*   1 through beam & 1 deflected beam IR photodiode
*   1 DS18B20 external temperature probe
*   1 stirrer per reaction beaker
