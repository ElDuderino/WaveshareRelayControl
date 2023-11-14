from enum import IntEnum


class WaveshareDef(IntEnum):

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

    CH1 = 21
    CH2 = 20
    CH3 = 19
    CH4 = 18
    CH5 = 17
    CH6 = 16
    CH7 = 15
    CH8 = 14
    RGB = 13
    BUZZER = 6
