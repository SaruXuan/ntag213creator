# Ntag213Creator

A web-server to choose the data you want to write into ntag213.

Many Clients (RaspberryPi+RC522) can access the ntag213 and communicate with web-server.

## Web-server Setup (win10 or Raspbian)

### Environment

* Flask

        pip install Flask

* Flask-socketio (reboot after installed)

        pip install eventlet
        pip install flask-socketio

* mysql-connector

        pip install mysql-connector-python

### Run

* Run webserver.py

        python webserver.py

## RC522 Clients Setup (Raspbian)

### Hardware

* RPi
* RC522 x1
* Buzzer x1
* wiring and resistance

### Environment

* [SPI-Py][1]
    
        git clone https://github.com/lthiery/SPI-Py.git
        cd SPI-Py
        sudo python setup.py install
        
* Enable SPI (for RC522)

        sudo raspi-config

### Wiring

* **RC522:**

    RC522 | Pin# | Pin name
    ---- | ---- | ----
    VCC | 17 | 3.3v
    RST | 22 | GPIO25
    GND | 20 | GND
    MISO| 21 | GPIO9
    MOSI| 19 | GPIO10
    SCK | 23 | GPIO11
    NSS/SDA | 24 | GPIO8
    IRQ | None| None

* **Buzzer:** GPIO 18 (Pin#12)

### Run

* Run Cardreader.py

        python Cardreader.py

[1]: https://github.com/lthiery/SPI-Py