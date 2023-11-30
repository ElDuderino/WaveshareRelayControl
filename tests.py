import configparser

from waveshare_defs import WaveshareDef
from relaycontrolmain import WaveshareRelayController
import time

if __name__ == "__main__":

    # read in the global app config
    config = configparser.ConfigParser()
    config.read('testcfg.cfg')

    serial_port = config.get("DEFAULT", "serial_port")

    default_states_str = config.get("DEFAULT", "default_relay_states")

    # ensure we can convert to channel int
    print(int(WaveshareDef.CH1.value))

    print(WaveshareDef.from_channel_def(1))

    # initialize the WaveshareRelayController class
    relay_controller = WaveshareRelayController(serial_port)

    # connect the serial port
    relay_controller.connect()

    # turn off all the relays
    relay_controller.set_default_state()
    time.sleep(1.0)

    # iterate through all the channels and turn each one on
    for ch in WaveshareDef:
        relay_controller.set_channel_on(ch)
        time.sleep(0.5)

    # iterate through all the channels and turn each one off
    for ch in WaveshareDef:
        relay_controller.set_channel_off(ch)
        time.sleep(0.5)

