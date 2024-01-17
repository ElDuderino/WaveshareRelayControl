import logging
import serial

from waveshare_defs import WaveshareDef
import time


class WaveshareRelayController:
    """
    Relay B	Pico	Description
    VCC	    VSYS	Power input
    GND	    GND	    Ground
    CH1	    GP21	Control pin of Channel 1
    CH2	    GP20	Control pin of Channel 2
    CH3	    GP19	Control pin of Channel 3
    CH4	    GP18	Control pin of Channel 4
    CH5	    GP17	Control pin of Channel 5
    CH6	    GP16	Control pin of Channel 6
    CH7	    GP15	Control pin of Channel7
    CH8	    GP14	Control pin of Channel 8
    RGB	    GP13	Control pin of RGB LED
    BUZZER	GP6	    Control pin of buzzer
    """

    def __init__(self, serial_device="/dev/ttyUSB0", default_states: dict[WaveshareDef, bool] = None):

        self.logger = logging.getLogger(__name__)

        self.serial = serial.Serial(
            port=serial_device,
            baudrate=115200,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=0.5,
            xonxoff=False,
            writeTimeout=0.5
        )

        self.logger.info("Serial port status:{}".format(self.serial.is_open))

        self.default_states = default_states

        """
        We're keeping track of the states as best we can 
        Eventually I'd like to add logic that syncs the control state over UART,
        but for now, we have to track the state based on when we open/close the relay
        """
        self.current_states: dict[WaveshareDef, int] = dict()

        for item in WaveshareDef:
            self.current_states[item] = None

    def get_channel_states(self) -> dict[WaveshareDef, int]:
        """
        Return the channel states
        :return: a dict of states (1 is on 0 is off) indexed by waveshare channel def
        """
        return self.current_states

    @staticmethod
    def parse_default_states(default_states_str: str) -> dict[WaveshareDef, bool]:
        """
        Parse the default states from the config file, they should be in a string format like:
        1:True,2:True,3:True,4:True,5:False,6:False,7:False,8:False
        """
        ret = dict()

        str_to_ks = default_states_str.split(",")
        for config_pair in str_to_ks:
            channel_int = int(config_pair.split(":")[0])
            channel = WaveshareDef.from_channel_def(channel_int)
            if channel is None:
                continue
            channel_bool_str = config_pair.split(":")[1]
            channel_bool = True if channel_bool_str == "True" else False
            ret[channel] = channel_bool

        return ret

    def connect(self):
        """
        Connect to the serial port
        :return:
        """
        if self.serial and self.serial.is_open is False:
            self.serial.open()

    def disconnect(self):
        """
        Disconnect from the serial port
        :return:
        """
        if self.serial and self.serial.is_open:
            self.serial.close()

    def write_packet(self, cmd: int, target: int, value: int):
        cmd_str = WaveshareRelayController.get_packet(cmd, target, value)
        self.serial.write(cmd_str.encode('utf-8'))

    @staticmethod
    def get_packet(cmd: int, target: int, value: int) -> str:
        return "{0},{1},{2}\n".format(cmd, target, value)

    def set_channel_on(self, channel: WaveshareDef):
        self.current_states[channel] = 1
        target = int(channel.value)
        self.write_packet(0, target, 1)

    def set_channel_off(self, channel: WaveshareDef):
        self.current_states[channel] = 0
        target = int(channel.value)
        self.write_packet(0, target, 0)

    def set_default_state(self):
        """
        Note that this function is different from setting the default *states* (plural)
        Set all relays to OFF
        This is a special method the firmware offers to set all the relays off
        """
        self.write_packet(99, 0, 0)
        for channel in WaveshareDef:
            self.current_states[channel] = 0
        time.sleep(1)

    def set_default_states(self, default_states: dict[WaveshareDef, bool] = None):
        """
        set the default relay states
        optionally pass in default states, if default_states is None,
        attempt to use self.relay_states (from config)
        """
        n_channels_switched = 0

        if default_states is None:
            # use self default states
            default_states = self.default_states

        if default_states is not None:
            for channel, value in default_states.items():
                n_channels_switched += 1
                if value is True:
                    self.set_channel_on(channel)
                elif value is False:
                    self.set_channel_off(channel)

        return n_channels_switched
