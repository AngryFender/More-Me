import mido
import math
from mido import Message
from nicegui import ui


class Demo:
    def __init__(self):
        self.bass_bass = 100
        self.bass_vocal = 90
        self.bass_back = 90
        self.bass_prs = 90
        self.bass_tele = 90
        self.bass_drums = 90
        self.bass_volume = 100
        self.tele_tele = 100
        self.tele_vocal = 90
        self.tele_back = 90
        self.tele_prs = 90
        self.tele_bass = 90
        self.tele_drums = 90
        self.tele_volume = 100
        self.prs_prs = 100
        self.prs_vocal = 90
        self.prs_back = 90
        self.prs_tele = 90
        self.prs_bass = 90
        self.prs_drums = 90
        self.prs_volume = 100
        self.drums_drums = 100
        self.drums_vocal = 90
        self.drums_back = 90
        self.drums_bass = 90
        self.drums_prs = 90
        self.drums_tele = 90
        self.drums_volume = 100
demo = Demo()
# Print available output ports
print("Available MIDI output ports:", mido.get_output_names())

# Function to send MIDI Control Change messages (simulate serial data)
def send_midi_serial(user,control, value, lbl):
    normalized_value = (value - 1) / (100 - 1)

    # Apply logarithmic scaling to make the upper range more sensitive
    # Adding a small constant (e.g., 1) to avoid log(0)
    log_transformed = math.log10(normalized_value * 9 + 1)

    # Map the log-transformed value to the 0-100 range
    percent_value = log_transformed * 100
    show_value = round(percent_value)

    scaled_value = log_transformed * 127
    midi_value = round(scaled_value)

    lbl.set_text(f'{show_value}')
    output_port = mido.open_output('custom_midi 2')

    control_change = Message('control_change', control=control, value=midi_value)
    output_port.send(control_change)

    print(f'Sent MIDI Control Change: user={user}, control={control}, percentage={show_value}, value={midi_value}')
    output_port.close()

# Create a card with full-screen width
with ui.card().classes('w-full').style('background-color: #f0eada; color: black;'):  # Set width to full screen
    ui.label("Bassist's Mix").style('font-size: 20px;')
    with ui.grid().classes("w-full").style("grid-template-columns:  50px auto 30px"):
        ui.label('Bass')
        ui.slider(min=1, max=100).bind_value(demo, 'bass_bass').on_value_change(lambda e: send_midi_serial('bassist',60, e.value, lb_bb))
        lb_bb= ui.label('1')
        ui.label('Vocal')
        ui.slider(min=1, max=100).bind_value(demo, 'bass_vocal').on_value_change(lambda e: send_midi_serial('bassist',61, e.value, lb_bv))
        lb_bv= ui.label('1')
        ui.label('Back')
        ui.slider(min=1, max=100).bind_value(demo, 'bass_back').on_value_change(lambda e: send_midi_serial('bassist', 62, e.value, lb_bvk))
        lb_bvk = ui.label('1')
        ui.label('Prs')
        ui.slider(min=1, max=100).bind_value(demo, 'bass_prs').on_value_change(lambda e: send_midi_serial('bassist',63, e.value, lb_bp))
        lb_bp= ui.label('1')
        ui.label('Tele')
        ui.slider(min=1, max=100).bind_value(demo, 'bass_tele').on_value_change(lambda e: send_midi_serial('bassist',64, e.value, lb_bt))
        lb_bt= ui.label('1')
        ui.label('Drums')
        ui.slider(min=1, max=100).bind_value(demo, 'bass_drums').on_value_change(lambda e: send_midi_serial('bassist',65, e.value, lb_bd))
        lb_bd= ui.label('1')
        ui.label('Volume')
        ui.slider(min=1, max=100).bind_value(demo, 'bass_volume').on_value_change(lambda e: send_midi_serial('bassist',66, e.value, lb_bov))
        lb_bov= ui.label('1')

with ui.card().classes('w-full').style('background-color: #d6a86d; color: white;'):
    ui.label("Tele players's Mix").style('font-size: 20px;')
    with ui.grid().classes("w-full").style("grid-template-columns:  50px auto 30px"):
        ui.label('Tele')
        ui.slider(min=1, max=100).bind_value(demo, 'tele_tele').on_value_change(lambda e: send_midi_serial('Tele-player',60, e.value, lb_vt))
        lb_vt= ui.label('1')
        ui.label('Vocal')
        ui.slider(min=1, max=100).bind_value(demo, 'tele_vocal').on_value_change(lambda e: send_midi_serial('Tele-player',61, e.value, lb_vv))
        lb_vv= ui.label('1')
        ui.label('Back')
        ui.slider(min=1, max=100).bind_value(demo, 'tele_back').on_value_change(lambda e: send_midi_serial('Tele-player', 62, e.value, lb_vvk))
        lb_vvk = ui.label('1')
        ui.label('Prs')
        ui.slider(min=1, max=100).bind_value(demo, 'tele_prs').on_value_change(lambda e: send_midi_serial('Tele-player',63, e.value, lb_vp))
        lb_vp= ui.label('1')
        ui.label('Bass')
        ui.slider(min=1, max=100).bind_value(demo, 'tele_bass').on_value_change(lambda e: send_midi_serial('Tele-player',64, e.value, lb_vb))
        lb_vb= ui.label('1')
        ui.label('Drums')
        ui.slider(min=1, max=100).bind_value(demo, 'tele_drums').on_value_change(lambda e: send_midi_serial('Tele-player',65, e.value, lb_vd))
        lb_vd= ui.label('1')
        ui.label('Volume')
        ui.slider(min=1, max=100).bind_value(demo, 'tele_volume').on_value_change(lambda e: send_midi_serial('Tele-player',66, e.value, lb_vov))
        lb_vov= ui.label('1')

with ui.card().classes('w-full').style('background-color: #032D61; color: white;'):
    ui.label("Prs player's Mix").style('font-size: 20px;')
    with ui.grid().classes("w-full").style("grid-template-columns:  50px auto 30px"):
        ui.label('Prs')
        ui.slider(min=1, max=100).bind_value(demo, 'prs_prs').on_value_change(lambda e: send_midi_serial('Prs-player',60, e.value, lb_pp))
        lb_pp= ui.label('1')
        ui.label('Vocal')
        ui.slider(min=1, max=100).bind_value(demo, 'prs_vocal').on_value_change(lambda e: send_midi_serial('Prs-player',61, e.value, lb_pv))
        lb_pv= ui.label('1')
        ui.label('Back')
        ui.slider(min=1, max=100).bind_value(demo, 'prs_back').on_value_change(lambda e: send_midi_serial('Prs-player', 62, e.value, lb_pvk))
        lb_pvk = ui.label('1')
        ui.label('Tele')
        ui.slider(min=1, max=100).bind_value(demo, 'prs_tele').on_value_change(lambda e: send_midi_serial('Prs-player',63, e.value, lb_pt))
        lb_pt= ui.label('1')
        ui.label('Bass')
        ui.slider(min=1, max=100).bind_value(demo, 'prs_bass').on_value_change(lambda e: send_midi_serial('Prs-player',64, e.value, lb_pb))
        lb_pb= ui.label('1')
        ui.label('Drums')
        ui.slider(min=1, max=100).bind_value(demo, 'prs_drums').on_value_change(lambda e: send_midi_serial('Prs-player',65, e.value, lb_pd))
        lb_pd= ui.label('1')
        ui.label('Volume')
        ui.slider(min=1, max=100).bind_value(demo, 'prs_volume').on_value_change(lambda e: send_midi_serial('Prs-player',66, e.value, lb_pov))
        lb_pov= ui.label('1')

with ui.card().classes('w-full').style('background-color: #464646; color: white;'):
    ui.label("Drummer's Mix").style('font-size: 20px;')
    with ui.grid().classes("w-full").style("grid-template-columns:  50px auto 30px"):
        ui.label('Drums')
        ui.slider(min=1, max=100).bind_value(demo, 'drums_drum').on_value_change(lambda e: send_midi_serial('Drummer',60, e.value, lb_dd))
        lb_dd= ui.label('1')
        ui.label('Vocal')
        ui.slider(min=1, max=100).bind_value(demo, 'drums_vocal').on_value_change(lambda e: send_midi_serial('Drummer',61, e.value, lb_dv))
        lb_dv= ui.label('1')
        ui.label('Back')
        ui.slider(min=1, max=100).bind_value(demo, 'drums_back').on_value_change(lambda e: send_midi_serial('Drummer', 62, e.value, lb_dvk))
        lb_dvk = ui.label('1')
        ui.label('Tele')
        ui.slider(min=1, max=100).bind_value(demo, 'drums_tele').on_value_change(lambda e: send_midi_serial('Drummer',63, e.value, lb_dt))
        lb_dt= ui.label('1')
        ui.label('Bass')
        ui.slider(min=1, max=100).bind_value(demo, 'drums_bass').on_value_change(lambda e: send_midi_serial('Drummer',64, e.value, lb_db))
        lb_db= ui.label('1')
        ui.label('Prs')
        ui.slider(min=1, max=100).bind_value(demo, 'drums_prs').on_value_change(lambda e: send_midi_serial('Drummer',65, e.value, lb_dp))
        lb_dp= ui.label('1')
        ui.label('Volume')
        ui.slider(min=1, max=100).bind_value(demo, 'drums_volume').on_value_change(lambda e: send_midi_serial('Drummer',66, e.value, lb_dov))
        lb_dov= ui.label('1')

ui.run()
