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

ui.run(host='0.0.0.0', port=80)

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

def update_slider(state, sl1, sl2, sl3, sl4, sl5, sl6, sl7):
    if not state:
        sl1.enable()
        sl2.enable()
        sl3.enable()
        sl4.enable()
        sl5.enable()
        sl6.enable()
        sl7.enable()
    else:
        sl1.disable()
        sl2.disable()
        sl3.disable()
        sl4.disable()
        sl5.disable()
        sl6.disable()
        sl7.disable()

# Create a card with full-screen width
with ui.card().classes('w-full').style('background-color: #a32425; color: white;'):  # Set width to full screen
    with ui.row().classes('w-full justify-center').style('align-items: center; left-padding:4px'):
        ui.label("Bassist's Mix").style('font-size: 20px;')
        ui.checkbox('Lock').classes('ml-auto').on_value_change(lambda e: update_slider(e.value, sl_bb,sl_bv, sl_bvk, sl_bp, sl_bt, sl_bd,sl_bov ))
    with ui.grid().classes("w-full").style("align-items: center; grid-template-columns:  50px auto 30px"):
        ui.label('Bass')
        sl_bb = ui.slider(min=1, max=100).classes('custom-slider').bind_value(demo, 'bass_bass').on_value_change(lambda e: send_midi_serial('bassist', 60, e.value, lb_bb))
        lb_bb= ui.label(f'{demo.bass_bass}')
        ui.label('Vocal')
        sl_bv = ui.slider(min=1, max=100).bind_value(demo, 'bass_vocal').on_value_change(lambda e: send_midi_serial('bassist',61, e.value, lb_bv))
        lb_bv= ui.label(f'{demo.bass_vocal}')
        ui.label('Back')
        sl_bvk = ui.slider(min=1, max=100).bind_value(demo, 'bass_back').on_value_change(lambda e: send_midi_serial('bassist', 62, e.value, lb_bvk))
        lb_bvk = ui.label(f'{demo.bass_back}')
        ui.label('Prs')
        sl_bp = ui.slider(min=1, max=100).bind_value(demo, 'bass_prs').on_value_change(lambda e: send_midi_serial('bassist',63, e.value, lb_bp))
        lb_bp= ui.label(f'{demo.bass_prs}')
        ui.label('Tele')
        sl_bt = ui.slider(min=1, max=100).bind_value(demo, 'bass_tele').on_value_change(lambda e: send_midi_serial('bassist',64, e.value, lb_bt))
        lb_bt= ui.label(f'{demo.bass_tele}')
        ui.label('Drums')
        sl_bd = ui.slider(min=1, max=100).bind_value(demo, 'bass_drums').on_value_change(lambda e: send_midi_serial('bassist',65, e.value, lb_bd))
        lb_bd= ui.label(f'{demo.bass_drums}')
        ui.label('Volume')
        sl_bov = ui.slider(min=1, max=100).bind_value(demo, 'bass_volume').on_value_change(lambda e: send_midi_serial('bassist',66, e.value, lb_bov))
        lb_bov= ui.label(f'{demo.bass_volume}')

with ui.card().classes('w-full').style('background-color: #d6a86d; color: white;'):
    with ui.row().classes('w-full justify-center').style('align-items: center;'):
        ui.label("Tele player's Mix").style('font-size: 20px;')
        ui.checkbox('Lock').classes('ml-auto').on_value_change(lambda e: update_slider(e.value, sl_vb,sl_vv, sl_vvk, sl_vp, sl_vt, sl_vd,sl_vov ))
    with ui.grid().classes("w-full").style("align-items: center; grid-template-columns:  50px auto 30px"):
        ui.label('Tele')
        sl_vt = ui.slider(min=1, max=100).bind_value(demo, 'tele_tele').on_value_change(lambda e: send_midi_serial('Tele-player',60, e.value, lb_vt))
        lb_vt= ui.label(f'{demo.tele_tele}')
        ui.label('Vocal')
        sl_vv = ui.slider(min=1, max=100).bind_value(demo, 'tele_vocal').on_value_change(lambda e: send_midi_serial('Tele-player',61, e.value, lb_vv))
        lb_vv= ui.label(f'{demo.tele_vocal}')
        ui.label('Back')
        sl_vvk = ui.slider(min=1, max=100).bind_value(demo, 'tele_back').on_value_change(lambda e: send_midi_serial('Tele-player', 62, e.value, lb_vvk))
        lb_vvk = ui.label(f'{demo.tele_back}')
        ui.label('Prs')
        sl_vp = ui.slider(min=1, max=100).bind_value(demo, 'tele_prs').on_value_change(lambda e: send_midi_serial('Tele-player',63, e.value, lb_vp))
        lb_vp= ui.label(f'{demo.tele_prs}')
        ui.label('Bass')
        sl_vb = ui.slider(min=1, max=100).bind_value(demo, 'tele_bass').on_value_change(lambda e: send_midi_serial('Tele-player',64, e.value, lb_vb))
        lb_vb= ui.label(f'{demo.tele_drums}')
        ui.label('Drums')
        sl_vd = ui.slider(min=1, max=100).bind_value(demo, 'tele_drums').on_value_change(lambda e: send_midi_serial('Tele-player',65, e.value, lb_vd))
        lb_vd= ui.label(f'{demo.tele_drums}')
        ui.label('Volume')
        sl_vov = ui.slider(min=1, max=100).bind_value(demo, 'tele_volume').on_value_change(lambda e: send_midi_serial('Tele-player',66, e.value, lb_vov))
        lb_vov= ui.label(f'{demo.tele_volume}')

with ui.card().classes('w-full').style('background-color: #032D61; color: white;'):
    with ui.row().classes('w-full justify-center').style('align-items: center;'):
        ui.label("Prs player's Mix").style('font-size: 20px;')
        ui.checkbox('Lock').classes('ml-auto').on_value_change(lambda e: update_slider(e.value, sl_pb, sl_pv, sl_pvk, sl_pp, sl_pt, sl_pd, sl_pov))
    with ui.grid().classes("w-full").style("align-items: center; grid-template-columns:  50px auto 30px"):
        ui.label('Prs')
        sl_pp = ui.slider(min=1, max=100).bind_value(demo, 'prs_prs').on_value_change(lambda e: send_midi_serial('Prs-player',60, e.value, lb_pp))
        lb_pp= ui.label(f'{demo.prs_prs}')
        ui.label('Vocal')
        sl_pv = ui.slider(min=1, max=100).bind_value(demo, 'prs_vocal').on_value_change(lambda e: send_midi_serial('Prs-player',61, e.value, lb_pv))
        lb_pv= ui.label(f'{demo.prs_vocal}')
        ui.label('Back')
        sl_pvk = ui.slider(min=1, max=100).bind_value(demo, 'prs_back').on_value_change(lambda e: send_midi_serial('Prs-player', 62, e.value, lb_pvk))
        lb_pvk = ui.label(f'{demo.prs_back}')
        ui.label('Tele')
        sl_pt = ui.slider(min=1, max=100).bind_value(demo, 'prs_tele').on_value_change(lambda e: send_midi_serial('Prs-player',63, e.value, lb_pt))
        lb_pt= ui.label(f'{demo.prs_tele}')
        ui.label('Bass')
        sl_pb = ui.slider(min=1, max=100).bind_value(demo, 'prs_bass').on_value_change(lambda e: send_midi_serial('Prs-player',64, e.value, lb_pb))
        lb_pb= ui.label(f'{demo.prs_bass}')
        ui.label('Drums')
        sl_pd = ui.slider(min=1, max=100).bind_value(demo, 'prs_drums').on_value_change(lambda e: send_midi_serial('Prs-player',65, e.value, lb_pd))
        lb_pd= ui.label(f'{demo.prs_drums}')
        ui.label('Volume')
        sl_pov = ui.slider(min=1, max=100).bind_value(demo, 'prs_volume').on_value_change(lambda e: send_midi_serial('Prs-player',66, e.value, lb_pov))
        lb_pov= ui.label(f'{demo.prs_volume}')

with ui.card().classes('w-full').style('background-color: #464646; color: white;'):
    with ui.row().classes('w-full justify-center').style('align-items: center;'):
        ui.label("Drummer's Mix").style('font-size: 20px;')
        ui.checkbox('Lock').classes('ml-auto').on_value_change(lambda e: update_slider(e.value, sl_db, sl_dv, sl_dvk, sl_dp, sl_dt, sl_dd, sl_dov))
    with ui.grid().classes("w-full").style("align-items: center; grid-template-columns:  50px auto 30px"):
        ui.label('Drums')
        sl_dd = ui.slider(min=1, max=100).bind_value(demo, 'drums_drums').on_value_change(lambda e: send_midi_serial('Drummer',60, e.value, lb_dd))
        lb_dd = ui.label(f'{demo.drums_drums}')
        ui.label('Vocal')
        sl_dv = ui.slider(min=1, max=100).bind_value(demo, 'drums_vocal').on_value_change(lambda e: send_midi_serial('Drummer',61, e.value, lb_dv))
        lb_dv= ui.label(f'{demo.drums_vocal}')
        ui.label('Back')
        sl_dvk = ui.slider(min=1, max=100).bind_value(demo, 'drums_back').on_value_change(lambda e: send_midi_serial('Drummer', 62, e.value, lb_dvk))
        lb_dvk = ui.label(f'{demo.drums_back}')
        ui.label('Tele')
        sl_dt = ui.slider(min=1, max=100).bind_value(demo, 'drums_tele').on_value_change(lambda e: send_midi_serial('Drummer',63, e.value, lb_dt))
        lb_dt= ui.label(f'{demo.drums_tele}')
        ui.label('Bass')
        sl_db = ui.slider(min=1, max=100).bind_value(demo, 'drums_bass').on_value_change(lambda e: send_midi_serial('Drummer',64, e.value, lb_db))
        lb_db= ui.label(f'{demo.drums_bass}')
        ui.label('Prs')
        sl_dp = ui.slider(min=1, max=100).bind_value(demo, 'drums_prs').on_value_change(lambda e: send_midi_serial('Drummer',65, e.value, lb_dp))
        lb_dp= ui.label(f'{demo.drums_prs}')
        ui.label('Volume')
        sl_dov = ui.slider(min=1, max=100).bind_value(demo, 'drums_volume').on_value_change(lambda e: send_midi_serial('Drummer',66, e.value, lb_dov))
        lb_dov= ui.label(f'{demo.drums_volume}')

ui.run()
