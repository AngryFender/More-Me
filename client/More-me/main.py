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

demo = Demo()
# Print available output ports
print("Available MIDI output ports:", mido.get_output_names())

# Function to send MIDI Control Change messages (simulate serial data)
def send_midi_serial(user,control, value):
    output_port = mido.open_output('custom_midi 2')  # This will use the first available port automatically
    control_change = Message('control_change', control=control, value=value)
    # control_change = Message('note_on', note=control, velocity=value)
    output_port.send(control_change)

    #time.sleep(1)
    print(f'Sent MIDI Control Change: user={user}, control={control}, value={value}')
    output_port.close()

bass_data = {'bass':'1'}

# Function to update the label, with the label reference passed in as a parameter
update_label = lambda value, lbl: lbl.set_text(f'Slider value: {value}')

# Create a card with full-screen width
with ui.card().classes('w-full'):  # Set width to full screen
    ui.label("Bassist's Mix")
    with ui.grid().classes("w-full").style("grid-template-columns:  50px auto 60px"):
        ui.label('Bass')
        slider1 = ui.slider(min=1, max=100).bind_value(demo, 'bass_bass').on_value_change(lambda: send_midi_serial('bassist',60, demo.bass_bass)).classes('flex-grow')
        ui.number().bind_value(demo, 'bass_bass')
        ui.label('Vocal')
        ui.slider(min=1, max=100).bind_value(demo, 'bass_vocal').classes('flex-grow')
        ui.number().bind_value(demo, 'bass_vocal')
        ui.label('Prs')
        ui.slider(min=1, max=100).bind_value(demo, 'bass_prs').classes('flex-grow')
        ui.number().bind_value(demo, 'bass_prs')
        ui.label('Tele')
        ui.slider(min=1, max=100).bind_value(demo, 'bass_tele').classes('flex-grow')
        ui.number().bind_value(demo, 'bass_tele')
        ui.label('Drums')
        ui.slider(min=1, max=100).bind_value(demo, 'bass_drums').classes('flex-grow')
        ui.number().bind_value(demo, 'bass_drums')
        ui.label('Volume')
        ui.slider(min=1, max=100).bind_value(demo, 'bass_volume').classes('flex-grow')
        ui.number().bind_value(demo, 'bass_volume')



ui.run()
