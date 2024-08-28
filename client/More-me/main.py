import mido
from mido import Message
import time
from nicegui import ui


class Demo:
    def __init__(self):
        self.number = 1
        self.bass_bass = 1
        self.bass_vocal = 1
        self.bass_back = 1
        self.bass_prs = 1
        self.bass_tele = 1
        self.bass_drums = 1
        self.bass_volume = 1
        self.tele_tele = 1
        self.tele_vocal = 1
        self.tele_back = 1
        self.tele_prs = 1
        self.tele_bass = 1
        self.tele_drums = 1
        self.tele_volume = 1
        self.prs_prs = 1
        self.prs_vocal = 1
        self.prs_back = 1
        self.prs_tele = 1
        self.prs_bass = 1
        self.prs_drums = 1
        self.prs_volume = 1
        self.drums_drums = 1
        self.drums_vocal = 1
        self.drums_back = 1
        self.drums_bass = 1
        self.drums_prs = 1
        self.drums_tele = 1
        self.drums_volume = 1
demo = Demo()
# Print available output ports
print("Available MIDI output ports:", mido.get_output_names())

# Function to send MIDI Control Change messages (simulate serial data)
def send_midi_serial(user,control, value, lbl):
    lbl.set_text(f'{value}')
    output_port = mido.open_output('custom_midi 2')
    control_change = Message('control_change', control=control, value=value)
    output_port.send(control_change)

    print(f'Sent MIDI Control Change: user={user}, control={control}, value={value}')
    output_port.close()

# Create a card with full-screen width
with ui.card().classes('w-full'):  # Set width to full screen
    ui.label("Bassist's Mix")
    with ui.grid().classes("w-full").style("grid-template-columns:  50px auto 60px"):
        ui.label('Bass')
        slider1 = ui.slider(min=1, max=100).bind_value(demo, 'bass_bass').on_value_change(lambda: send_midi_serial('bassist',60, demo.bass_bass, lb_bb))
        lb_bb= ui.label('1')
        ui.label('Vocal')
        ui.slider(min=1, max=100).bind_value(demo, 'bass_vocal').on_value_change(lambda: send_midi_serial('bassist',61, demo.bass_vocal, lb_bv))
        lb_bv= ui.label('1')
        ui.label('Back')
        ui.slider(min=1, max=100).bind_value(demo, 'bass_back').on_value_change(lambda: send_midi_serial('bassist', 62, demo.bass_back, lb_bvk))
        lb_bvk = ui.label('1')
        ui.label('Prs')
        ui.slider(min=1, max=100).bind_value(demo, 'bass_prs').on_value_change(lambda: send_midi_serial('bassist',63, demo.bass_prs, lb_bp))
        lb_bp= ui.label('1')
        ui.label('Tele')
        ui.slider(min=1, max=100).bind_value(demo, 'bass_tele').on_value_change(lambda: send_midi_serial('bassist',64, demo.bass_tele, lb_bt))
        lb_bt= ui.label('1')
        ui.label('Drums')
        ui.slider(min=1, max=100).bind_value(demo, 'bass_drums').on_value_change(lambda: send_midi_serial('bassist',65, demo.bass_drums, lb_bd))
        lb_bd= ui.label('1')
        ui.label('Volume')
        ui.slider(min=1, max=100).bind_value(demo, 'bass_volume').on_value_change(lambda: send_midi_serial('bassist',66, demo.bass_volume, lb_bov))
        lb_bov= ui.label('1')


ui.run()
