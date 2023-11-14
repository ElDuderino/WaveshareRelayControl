import logging
import serial

from waveshare_defs import WaveshareDef


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

    def __init__(self, serial_device="/dev/ttyUSB0"):

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

    def connect(self):
        """

        :return:
        """
        if self.serial and self.serial.is_open is False:
            self.serial.open()

    def disconnect(self):
        """

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
        target = int(channel.value)
        self.write_packet(0, target, 1)

    def set_channel_off(self, channel: WaveshareDef):
        target = int(channel.value)
        self.write_packet(0, target, 0)

    def set_default_state(self):
        """
        Set all relays to OFF
        """
        self.write_packet(99, 0, 0)
