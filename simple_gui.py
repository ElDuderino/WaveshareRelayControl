import PySimpleGUI as sg
import configparser
from waveshare_defs import WaveshareDef
from relaycontrolmain import WaveshareRelayController


class WaveshareGUI:

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('testcfg.cfg')

        self.serial_port = config.get("DEFAULT", "serial_port")

        default_states_str = config.get("DEFAULT", "default_relay_states")
        self.default_states = WaveshareRelayController.parse_default_states(default_states_str)

        self.relay_controller = WaveshareRelayController(
            serial_device=self.serial_port,
            default_states=self.default_states)

        print("Connecting relay controller")
        self.relay_controller.connect()
        print("Setting all relays off")
        self.relay_controller.set_default_state()
        print("Setting relay default states")
        self.relay_controller.set_default_states()

    def main(self):
        layout = [
            [sg.Checkbox('Channel 1', key='channel1', change_submits=True),
             sg.Checkbox('Channel 2', key='channel2', change_submits=True)],
            [sg.Checkbox('Channel 3', key='channel3', change_submits=True),
             sg.Checkbox('Channel 4', key='channel4', change_submits=True)],
            [sg.Checkbox('Channel 5', key='channel5', change_submits=True),
             sg.Checkbox('Channel 6', key='channel6', change_submits=True)],
            [sg.Checkbox('Channel 7', key='channel7', change_submits=True),
             sg.Checkbox('Channel 8', key='channel8', change_submits=True)],
            [sg.Button('Exit')]
        ]

        window = sg.Window('Pico Relay-B Controller', layout, finalize=True)

        for channel, state in self.default_states.items():

            if channel == WaveshareDef.CH1:
                window['channel1'].Update(value=state)
            elif channel == WaveshareDef.CH2:
                window['channel2'].Update(value=state)
            elif channel == WaveshareDef.CH3:
                window['channel3'].Update(value=state)
            elif channel == WaveshareDef.CH4:
                window['channel4'].Update(value=state)
            elif channel == WaveshareDef.CH5:
                window['channel5'].Update(value=state)
            elif channel == WaveshareDef.CH6:
                window['channel6'].Update(value=state)
            elif channel == WaveshareDef.CH7:
                window['channel7'].Update(value=state)
            elif channel == WaveshareDef.CH8:
                window['channel8'].Update(value=state)

        while True:
            event, values = window.read()

            if event == sg.WINDOW_CLOSED or event == 'Exit':
                break

            # Check which checkbox triggered the event and print its state
            for i in range(1, 9):
                channel_key = f'channel{i}'
                if event == channel_key:
                    print(f'{channel_key} is {"checked" if values[channel_key] else "unchecked"}')
                    channel_state = values[channel_key]
                    self.toggle_channel(channel_key, channel_state)

        window.close()

    def set_channel_state(self, channel: WaveshareDef, channel_state: bool):
        if channel_state is True:
            self.relay_controller.set_channel_on(channel)
        else:
            self.relay_controller.set_channel_off(channel)

    def toggle_channel(self, channel_id: str, channel_state: bool):
        if channel_id == 'channel1':
            self.set_channel_state(WaveshareDef.CH1, channel_state)

        elif channel_id == 'channel2':
            self.set_channel_state(WaveshareDef.CH2, channel_state)

        elif channel_id == 'channel3':
            self.set_channel_state(WaveshareDef.CH3, channel_state)

        elif channel_id == 'channel4':
            self.set_channel_state(WaveshareDef.CH4, channel_state)

        elif channel_id == 'channel5':
            self.set_channel_state(WaveshareDef.CH5, channel_state)

        elif channel_id == 'channel6':
            self.set_channel_state(WaveshareDef.CH6, channel_state)

        elif channel_id == 'channel7':
            self.set_channel_state(WaveshareDef.CH7, channel_state)

        elif channel_id == 'channel8':
            self.set_channel_state(WaveshareDef.CH8, channel_state)


if __name__ == '__main__':
    gui = WaveshareGUI()
    gui.main()
