import mido
import math
from mido import Message
from nicegui import app, ui

class Demo:
    def __init__(self):
        self.midi_port = ""
        self.play_back = False
        self.bass_bass = 100
        self.bass_vocal = 90
        self.bass_back = 90
        self.bass_prs = 90
        self.bass_tele = 90
        self.bass_ldrums = 90
        self.bass_rdrums = 90
        self.bass_volume = 100
        self.bass_playback_volume = 90
        self.marshal_high = True
        self.marshal_presence = 100
        self.marshal_bass = 100
        self.marshal_middle = 100
        self.marshal_treble = 100
        self.marshal_master_output = 90
        self.marshal_lead_output = 90
        self.marshal_input_gain = 100
        self.tele_tele = 100
        self.tele_vocal = 90
        self.tele_back = 90
        self.tele_prs = 90
        self.tele_bass = 90
        self.tele_ldrums = 90
        self.tele_rdrums = 90
        self.tele_volume = 100
        self.tele_playback_volume = 90
        self.prs_prs = 100
        self.prs_vocal = 90
        self.prs_back = 90
        self.prs_tele = 90
        self.prs_bass = 90
        self.prs_ldrums = 90
        self.prs_rdrums = 90
        self.prs_volume = 100
        self.prs_playback_volume = 90
        self.drums_ldrums = 100
        self.drums_rdrums = 100
        self.drums_vocal = 90
        self.drums_back = 90
        self.drums_bass = 90
        self.drums_prs = 90
        self.drums_tele = 90
        self.drums_volume = 100
        self.drums_playback_volume = 90
demo = Demo()

ui.run(host='0.0.0.0', port=80)

# Save available output ports
midi_list = mido.get_output_names()
midi_output = None

def open_midi(midi_port):
    global midi_output
    midi_output = mido.open_output(midi_port)
    print("MIDI connection opened")

def close_midi():
    global midi_output
    if midi_output is not None:
        midi_output.close()
        print("MIDI connection closed")

# Function to send MIDI Control Change messages (simulate serial data)
def send_midi_serial(user,control, value, lbl):
    normalized_value = (value - 1) / (100 - 1)

    # Apply logarithmic scaling to make the upper range more sensitive
    # Adding a small constant (e.g., 1) to avoid log(0)
    log_transformed = math.log10(normalized_value * 9 + 1)

    # Map the log-transformed value to the 0-100 range
    percent_value = log_transformed * 100
    show_value = round(percent_value)

    scaled_value = log_transformed * 103
    midi_value = round(scaled_value)

    lbl.set_text(f'{show_value}')

    global midi_output
    control_change = Message('control_change', control=control, value=midi_value)
    midi_output.send(control_change)

    print(f'Sent MIDI Control Change: user={user}, control={control}, percentage={show_value}, value={midi_value}')

# Function to send MIDI Control Change messages (simulate serial data)
def send_midi_linear(user,control, value, lbl):

    scaled_value = value * 1.27
    midi_value = round(scaled_value)

    lbl.set_text(f'{value}')

    global midi_output
    control_change = Message('control_change', control=control, value=midi_value)
    midi_output.send(control_change)

    print(f'Sent MIDI Control Change: user={user}, control={control}, percentage={value}, value={midi_value}')


def send_midi_state(user, control, value):
    global midi_output

    state = 0
    if value:
        state = 127

    control_change = Message('control_change', control=control, value=state)
    midi_output.send(control_change)

    print(f'Sent MIDI Control Change: user={user}, control={control}, percentage={value}, value={value}')


def update_playback(user, solo_control, value, mute_control ):
    global midi_output

    solo_state = 0
    mute_state = 127
    if value:
       solo_state = 127
       mute_state = 0

    control_change = Message('control_change', control=solo_control, value=solo_state)
    midi_output.send(control_change)

    control_change = Message('control_change', control=mute_control, value=mute_state)
    midi_output.send(control_change)

    print(f'Sent MIDI Control Change: user={user}, solo_control={solo_control}, solo_state={solo_state},mute_control={mute_control}, mute_state={mute_state}')

def update_slider(state, sl1, sl2, sl3, sl4, sl5, sl6, sl7, sl8, sl9 = None):
    if not state:
        sl1.enable()
        sl2.enable()
        sl3.enable()
        sl4.enable()
        sl5.enable()
        sl6.enable()
        sl7.enable()
        sl8.enable()
        if sl9 is not None:
            sl9.enable()
    else:
        sl1.disable()
        sl2.disable()
        sl3.disable()
        sl4.disable()
        sl5.disable()
        sl6.disable()
        sl7.disable()
        sl8.disable()
        if sl9 is not None:
            sl9.disable()

def update_double_slider(state, sl1, sl2, sl3, sl4, sl5, sl6, sl7, sl8, sl9, sl10, sl11, sl12, sl13, sl14, sl15, sl16,sl17):
    update_slider(state, sl1, sl2, sl3, sl4, sl5, sl6, sl7, sl8, sl9)
    update_slider(state, sl10, sl11, sl12, sl13, sl14, sl15, sl16, sl17)

# Add custom CSS to change the slider colors
ui.add_head_html('''
<style>
    .bass-slider .q-slider__track {
        color: #fff0f5 !important;  /* Track color */
    }

    .bass-slider .q-slider__thumb {
        color: #fff0f5 !important;  /* Thumb color */
    }
    
    .marshal-slider .q-slider__track {
        color: black !important;  /* Track color */
    }

    .marshal-slider .q-slider__thumb {
        color: black !important;  /* Thumb color */
    }
    
    .tele-slider .q-slider__track {
        color: #623412 !important;  /* Track color */
    }

    .tele-slider .q-slider__thumb {
        color: #fffdd0 !important;  /* Thumb color */
    }
    
</style>
''')

app.on_shutdown(close_midi)

with ui.row().classes('w-full justify-center').style('align-items: center;'):
    midi_select = ui.select(options=midi_list, with_input=False, on_change=lambda e: ui.notify(e.value)).classes('w-40').on_value_change(
        lambda e: open_midi(e.value))
    switch_playback = ui.switch('Playback').bind_value(demo, 'play_back').on_value_change(
        lambda e: update_playback('All users', 88, e.value, 89))

# Create a card with full-screen width
with ui.card().classes('w-full').style('background-color: #a32425; color: white;'):  # Set width to full screen
    with ui.row().classes('w-full justify-center').style('align-items: center; left-padding:4px'):
        ui.label("Bassist's Mix").style('font-size: 20px;')
        ui.checkbox('Lock').classes('ml-auto').on_value_change(lambda e: update_slider(e.value, sl_bb,sl_bv, sl_bvk, sl_bp, sl_bt, sl_bld, sl_brd, sl_bov, sl_bpbv ))
    with ui.grid().classes("w-full").style("align-items: center; grid-template-columns:  50px auto 30px"):
        ui.label('Bass')
        sl_bb = ui.slider(min=1, max=100).classes('bass-slider').bind_value(demo, 'bass_bass').on_value_change(lambda e: send_midi_serial('bassist', 110, e.value, lb_bb))
        lb_bb= ui.label(f'{demo.bass_bass}')
        ui.label('Vocal')
        sl_bv = ui.slider(min=1, max=100).classes('bass-slider').bind_value(demo, 'bass_vocal').on_value_change(lambda e: send_midi_serial('bassist',111, e.value, lb_bv))
        lb_bv= ui.label(f'{demo.bass_vocal}')
        ui.label('Back')
        sl_bvk = ui.slider(min=1, max=100).classes('bass-slider').bind_value(demo, 'bass_back').on_value_change(lambda e: send_midi_serial('bassist', 112, e.value, lb_bvk))
        lb_bvk = ui.label(f'{demo.bass_back}')
        ui.label('Prs')
        sl_bp = ui.slider(min=1, max=100).classes('bass-slider').bind_value(demo, 'bass_prs').on_value_change(lambda e: send_midi_serial('bassist',113, e.value, lb_bp))
        lb_bp= ui.label(f'{demo.bass_prs}')
        ui.label('Tele')
        sl_bt = ui.slider(min=1, max=100).classes('bass-slider').bind_value(demo, 'bass_tele').on_value_change(lambda e: send_midi_serial('bassist',114, e.value, lb_bt))
        lb_bt= ui.label(f'{demo.bass_tele}')
        ui.label('LDrums')
        sl_bld = ui.slider(min=1, max=100).classes('bass-slider').bind_value(demo, 'bass_ldrums').on_value_change(lambda e: send_midi_serial('bassist',115, e.value, lb_bld))
        lb_bld= ui.label(f'{demo.bass_ldrums}')
        ui.label('RDrums')
        sl_brd = ui.slider(min=1, max=100).classes('bass-slider').bind_value(demo, 'bass_rdrums').on_value_change(lambda e: send_midi_serial('bassist', 116, e.value, lb_brd))
        lb_brd = ui.label(f'{demo.bass_ldrums}')
        ui.label('Volume')
        sl_bov = ui.slider(min=1, max=100).classes('bass-slider').bind_value(demo, 'bass_volume').on_value_change(lambda e: send_midi_linear('bassist', 117, e.value, lb_bov))
        lb_bov = ui.label(f'{demo.bass_volume}')
        ui.label('Playback')
        sl_bpbv = ui.slider(min=1, max=100).classes('bass-slider').bind_value(demo, 'bass_playback_volume').on_value_change(lambda e: send_midi_serial('bassist',118, e.value, lb_bpbv))
        lb_bpbv= ui.label(f'{demo.bass_playback_volume}')

with ui.card().classes('w-full').style('background-color: #d6a86d; color: white;'):
    with ui.row().classes('w-full justify-center').style('align-items: center;'):
        ui.label("Tele player's Mix").style('font-size: 20px;')
        checkbox_tele = ui.checkbox('Lock').classes('ml-auto').on_value_change(lambda e:
            update_double_slider(e.value, sl_vb,sl_vv, sl_vvk, sl_vp, sl_vt, sl_vld, sl_vrd, sl_vov,sl_vpbv, sl_msw, sl_mp, sl_mb, sl_mm, sl_mt, sl_mmo, sl_mlo,sl_mig) )
    with ui.card().classes('w-full').style('background-color: white; color: black;'):
        sl_msw = ui.switch('High Output').bind_value(demo, 'marshal_high').on_value_change(
            lambda e: send_midi_state('Tele-player', 90, sl_msw.value))
        with ui.grid().classes("w-full").style("align-items: center; grid-template-columns:  50px auto 30px"):

            ui.label('Presence')
            sl_mp = ui.slider(min=1, max=100).classes('marshal-slider').bind_value(demo, 'marshal_presence').on_value_change(
                lambda e: send_midi_linear('Tele-player', 91, e.value, lb_mp))
            lb_mp= ui.label(f'{demo.tele_tele}')

            ui.label('Bass')
            sl_mb = ui.slider(min=1, max=100).classes('marshal-slider').bind_value(demo, 'marshal_bass').on_value_change(
                lambda e: send_midi_linear('Tele-player', 92, e.value, lb_mb))
            lb_mb= ui.label(f'{demo.tele_tele}')

            ui.label('Middle')
            sl_mm = ui.slider(min=1, max=100).classes('marshal-slider').bind_value(demo, 'marshal_middle').on_value_change(
                lambda e: send_midi_linear('Tele-player', 93, e.value, lb_mm))
            lb_mm = ui.label(f'{demo.tele_tele}')

            ui.label('Treble')
            sl_mt = ui.slider(min=1, max=100).classes('marshal-slider').bind_value(demo, 'marshal_treble').on_value_change(
                lambda e: send_midi_linear('Tele-player', 94, e.value, lb_mt))
            lb_mt = ui.label(f'{demo.tele_tele}')

            ui.label('Master Output')
            sl_mmo = ui.slider(min=1, max=100).classes('marshal-slider').bind_value(demo, 'marshal_master_output').on_value_change(
                lambda e: send_midi_linear('Tele-player', 95, e.value, lb_mmo))
            lb_mmo = ui.label(f'{demo.tele_tele}')

            ui.label('Lead Output')
            sl_mlo = ui.slider(min=1, max=100).classes('marshal-slider').bind_value(demo, 'marshal_lead_output').on_value_change(
                lambda e: send_midi_linear('Tele-player', 96, e.value, lb_mlo))
            lb_mlo = ui.label(f'{demo.tele_tele}')

            ui.label('Input Gain')
            sl_mig = ui.slider(min=1, max=100).classes('marshal-slider').bind_value(demo, 'marshal_input_gain').on_value_change(
                lambda e: send_midi_linear('Tele-player', 97, e.value, lb_mig))
            lb_mig = ui.label(f'{demo.tele_tele}')

    with ui.grid().classes("w-full").style("align-items: center; grid-template-columns:  50px auto 30px"):
        ui.label('Tele')
        sl_vt = ui.slider(min=1, max=100).classes('tele-slider').bind_value(demo, 'tele_tele').on_value_change(lambda e: send_midi_serial('Tele-player',100, e.value, lb_vt))
        lb_vt= ui.label(f'{demo.tele_tele}')
        ui.label('Vocal')
        sl_vv = ui.slider(min=1, max=100).classes('tele-slider').bind_value(demo, 'tele_vocal').on_value_change(lambda e: send_midi_serial('Tele-player',101, e.value, lb_vv))
        lb_vv= ui.label(f'{demo.tele_vocal}')
        ui.label('Back')
        sl_vvk = ui.slider(min=1, max=100).classes('tele-slider').bind_value(demo, 'tele_back').on_value_change(lambda e: send_midi_serial('Tele-player', 102, e.value, lb_vvk))
        lb_vvk = ui.label(f'{demo.tele_back}')
        ui.label('Prs')
        sl_vp = ui.slider(min=1, max=100).classes('tele-slider').bind_value(demo, 'tele_prs').on_value_change(lambda e: send_midi_serial('Tele-player',103, e.value, lb_vp))
        lb_vp= ui.label(f'{demo.tele_prs}')
        ui.label('Bass')
        sl_vb = ui.slider(min=1, max=100).classes('tele-slider').bind_value(demo, 'tele_bass').on_value_change(lambda e: send_midi_serial('Tele-player',104, e.value, lb_vb))
        lb_vb= ui.label(f'{demo.tele_bass}')
        ui.label('LDrums')
        sl_vld = ui.slider(min=1, max=100).classes('tele-slider').bind_value(demo, 'tele_ldrums').on_value_change(lambda e: send_midi_serial('Tele-player', 105, e.value, lb_vld))
        lb_vld = ui.label(f'{demo.tele_ldrums}')
        ui.label('RDrums')
        sl_vrd = ui.slider(min=1, max=100).classes('tele-slider').bind_value(demo, 'tele_rdrums').on_value_change(lambda e: send_midi_serial('Tele-player',106, e.value, lb_vrd))
        lb_vrd= ui.label(f'{demo.tele_rdrums}')
        ui.label('Volume')
        sl_vov = ui.slider(min=1, max=100).classes('tele-slider').bind_value(demo, 'tele_volume').on_value_change(lambda e: send_midi_linear('Tele-player',107, e.value, lb_vov))
        lb_vov= ui.label(f'{demo.tele_volume}')
        ui.label('Playback')
        sl_vpbv = ui.slider(min=1, max=100).classes('tele-slider').bind_value(demo, 'tele_playback_volume').on_value_change(lambda e: send_midi_serial('Tele-player',108, e.value, lb_vpbv))
        lb_vpbv= ui.label(f'{demo.tele_playback_volume}')

with ui.card().classes('w-full').style('background-color: #032D61; color: white;'):
    with ui.row().classes('w-full justify-center').style('align-items: center;'):
        ui.label("Prs player's Mix").style('font-size: 20px;')
        ui.checkbox('Lock').classes('ml-auto').on_value_change(lambda e: update_slider(e.value, sl_pb, sl_pv, sl_pvk, sl_pp, sl_pt, sl_pld, sl_prd, sl_pov, sl_ppbv))
    with ui.grid().classes("w-full").style("align-items: center; grid-template-columns:  50px auto 30px"):
        ui.label('Prs')
        sl_pp = ui.slider(min=1, max=100).bind_value(demo, 'prs_prs').on_value_change(lambda e: send_midi_serial('Prs-player',0, e.value, lb_pp))
        lb_pp= ui.label(f'{demo.prs_prs}')
        ui.label('Vocal')
        sl_pv = ui.slider(min=1, max=100).bind_value(demo, 'prs_vocal').on_value_change(lambda e: send_midi_serial('Prs-player',1, e.value, lb_pv))
        lb_pv= ui.label(f'{demo.prs_vocal}')
        ui.label('Back')
        sl_pvk = ui.slider(min=1, max=100).bind_value(demo, 'prs_back').on_value_change(lambda e: send_midi_serial('Prs-player', 2, e.value, lb_pvk))
        lb_pvk = ui.label(f'{demo.prs_back}')
        ui.label('Tele')
        sl_pt = ui.slider(min=1, max=100).bind_value(demo, 'prs_tele').on_value_change(lambda e: send_midi_serial('Prs-player',3, e.value, lb_pt))
        lb_pt= ui.label(f'{demo.prs_tele}')
        ui.label('Bass')
        sl_pb = ui.slider(min=1, max=100).bind_value(demo, 'prs_bass').on_value_change(lambda e: send_midi_serial('Prs-player',8, e.value, lb_pb))
        lb_pb= ui.label(f'{demo.prs_bass}')
        ui.label('LDrums')
        sl_pld = ui.slider(min=1, max=100).bind_value(demo, 'prs_ldrums').on_value_change(lambda e: send_midi_serial('Prs-player', 5, e.value, lb_pld))
        lb_pld= ui.label(f'{demo.prs_ldrums}')
        ui.label('RDrums')
        sl_prd = ui.slider(min=1, max=100).bind_value(demo, 'prs_rdrums').on_value_change(lambda e: send_midi_serial('Prs-player',6, e.value, lb_prd))
        lb_prd= ui.label(f'{demo.prs_rdrums}')
        ui.label('Volume')
        sl_pov = ui.slider(min=1, max=100).bind_value(demo, 'prs_volume').on_value_change(lambda e: send_midi_linear('Prs-player',7, e.value, lb_pov))
        lb_pov= ui.label(f'{demo.prs_volume}')
        ui.label('Playback')
        sl_ppbv = ui.slider(min=1, max=100).bind_value(demo, 'prs_playback_volume').on_value_change(lambda e: send_midi_serial('Prs-player',9, e.value, lb_ppbv))
        lb_ppbv= ui.label(f'{demo.prs_playback_volume}')

with ui.card().classes('w-full').style('background-color: #464646; color: white;'):
    with ui.row().classes('w-full justify-center').style('align-items: center;'):
        ui.label("Drummer's Mix").style('font-size: 20px;')
        ui.checkbox('Lock').classes('ml-auto').on_value_change(lambda e: update_slider(e.value, sl_db, sl_dv, sl_dvk, sl_dp, sl_dt, sl_dld, sl_drd, sl_dov, sl_dpbv))
    with ui.grid().classes("w-full").style("align-items: center; grid-template-columns:  50px auto 30px"):
        ui.label('LDrums')
        sl_dld = ui.slider(min=1, max=100).bind_value(demo, 'drums_ldrums').on_value_change(lambda e: send_midi_serial('Drummer', 10, e.value, lb_dld))
        lb_dld = ui.label(f'{demo.drums_ldrums}')
        ui.label('RDrums')
        sl_drd = ui.slider(min=1, max=100).bind_value(demo, 'drums_rdrums').on_value_change(lambda e: send_midi_serial('Drummer',11, e.value, lb_drd))
        lb_drd = ui.label(f'{demo.drums_rdrums}')
        ui.label('Vocal')
        sl_dv = ui.slider(min=1, max=100).bind_value(demo, 'drums_vocal').on_value_change(lambda e: send_midi_serial('Drummer',12, e.value, lb_dv))
        lb_dv= ui.label(f'{demo.drums_vocal}')
        ui.label('Back')
        sl_dvk = ui.slider(min=1, max=100).bind_value(demo, 'drums_back').on_value_change(lambda e: send_midi_serial('Drummer', 13, e.value, lb_dvk))
        lb_dvk = ui.label(f'{demo.drums_back}')
        ui.label('Tele')
        sl_dt = ui.slider(min=1, max=100).bind_value(demo, 'drums_tele').on_value_change(lambda e: send_midi_serial('Drummer',14, e.value, lb_dt))
        lb_dt= ui.label(f'{demo.drums_tele}')
        ui.label('Bass')
        sl_db = ui.slider(min=1, max=100).bind_value(demo, 'drums_bass').on_value_change(lambda e: send_midi_serial('Drummer',15, e.value, lb_db))
        lb_db= ui.label(f'{demo.drums_bass}')
        ui.label('Prs')
        sl_dp = ui.slider(min=1, max=100).bind_value(demo, 'drums_prs').on_value_change(lambda e: send_midi_serial('Drummer',16, e.value, lb_dp))
        lb_dp= ui.label(f'{demo.drums_prs}')
        ui.label('Volume')
        sl_dov = ui.slider(min=1, max=100).bind_value(demo, 'drums_volume').on_value_change(lambda e: send_midi_linear('Drummer',17, e.value, lb_dov))
        lb_dov= ui.label(f'{demo.drums_volume}')
        ui.label('Playback')
        sl_dpbv = ui.slider(min=1, max=100).bind_value(demo, 'drums_playback_volume').on_value_change(lambda e: send_midi_serial('Drummer',18, e.value, lb_dpbv))
        lb_dpbv= ui.label(f'{demo.drums_playback_volume}')
try:
    ui.run()
except Exception as e:
    print(e)
finally:
    close_midi()



