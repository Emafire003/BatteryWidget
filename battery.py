import PySimpleGUI as sg
import psutil
import sys

"""
    Another simple Desktop Widget using PySimpleGUI
    This time a RAM indicator.  The Widget is square.  The bottom section will be shaded to
    represent the total amount of RAM currently in use.
    The % and number of bytes in use is shown on top in text.
    Uses the theme's button color for colors.

    Copyright 2020 PySimpleGUI.org
"""

ALPHA = 0.8
THEME = 'Dark Green 5'
GSIZE = (50, 50)
UPDATE_FREQUENCY_MILLISECONDS = 10 * 1000


sg.theme(THEME)

'''def convertTime(seconds):
	minutes, seconds = divmod(seconds, 60)
	hours, minutes = divmod(minutes, 60)
	return "%d:%02d:%02d" % (hours, minutes, seconds)'''

def main(location):

    graph = sg.Graph(GSIZE, (0, 0), GSIZE, key='-GRAPH-', enable_events=True)
    layout = [[graph]]

    window = sg.Window('Battery Left', layout, location=location, no_titlebar=True, grab_anywhere=True, margins=(0, 0), element_padding=(0, 0), alpha_channel=ALPHA, finalize=True, right_click_menu=[[''], 'Exit'], keep_on_top = True)


    while True:  # Event Loop
        # ----------- update the graphics and text in the window ------------
        battery = psutil.sensors_battery()
        if(battery.percent < 15 and not battery.power_plugged):
            sg.popup("⚡LOW BATTERY⚡", text_color = "#f41202", no_titlebar = True, font="Any 10 bold", keep_on_top = True, button_type = 0)
        rect_height = int(GSIZE[1] * float(battery.percent) / 100)
        rect_id = graph.draw_rectangle((0, rect_height), (GSIZE[0], 0), fill_color="#1eed60", line_width=0)
        text_id1 = graph.draw_text(f'{int(battery.percent)}%', (GSIZE[0] // 2, GSIZE[1] // 2), font='Any 20', text_location=sg.TEXT_LOCATION_CENTER,
                       color="#1ea4ed")
        text_id2 = graph.draw_text("a", (GSIZE[0], 0))
        if(battery.power_plugged):
            text_id2 = graph.draw_text(f'⚡', (GSIZE[0] // 2, GSIZE[1] // 4), font='Any 10', text_location=sg.TEXT_LOCATION_CENTER, color="#ebf704")
        else:
            text_id2 = graph.draw_text(f'⚡', (GSIZE[0] // 2, GSIZE[1] // 4), font='Any 8', text_location=sg.TEXT_LOCATION_CENTER, color="#898989")
        #text_id3 = graph.draw_text(str(convertTime(battery.secsleft)), (GSIZE[0] // 5.2, GSIZE[1] // 200), font='Any 8', text_location=sg.TEXT_LOCATION_BOTTOM_LEFT, color="#1ea4ed")

        event, values = window.read(timeout=UPDATE_FREQUENCY_MILLISECONDS)
        try:
            if event == sg.WIN_CLOSED or event == 'Exit' or event == None:
                break
        except KeyboardInterrupt:
            break
        if event == '-GRAPH-':  # exit if clicked in the bottom left 20 x 20 pixel area
            if values['-GRAPH-'][0] < 20 and values['-GRAPH-'][1] < 20:
                break
        graph.delete_figure(rect_id)
        graph.delete_figure(text_id1)
        graph.delete_figure(text_id2)
        #graph.delete_figure(text_id3)
    window.close()

if __name__ == '__main__':

    if len(sys.argv) > 1:
        location = sys.argv[1].split(',')
        location = (int(location[0]), int(location[1]))
    else:
        location = (None, None)
    try:
        main(location)
    except KeyboardInterrupt:
        print("gbye")
