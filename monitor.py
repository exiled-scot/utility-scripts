import subprocess
import re

def get_mouse_location():
    cmd = 'xdotool getmouselocation --shell'
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = (p.communicate()[0]).decode()
    location = output.split('\n')
    x = int(location[0].split('=')[1])
    y = int(location[1].split('=')[1])
    return x,y

def get_monitor_details(monitor):
    cmd = 'xrandr --current --verbose | grep ^' + monitor
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = (p.communicate()[0]).decode()
    pos = re.search(r'\+(\d*)\+(\d*)',output)
    res = re.search(r'(\d*)[xX](\d*)',output)
    p_width = int(pos.group(1))
    p_height = int(pos.group(2))
    r_width = int(res.group(1))
    r_height = int(res.group(2))
    return p_width, p_height, r_width, r_height

def identify_active_monitor():
    """Identifies the monitor the mouse is currently active on and returns
    the ID of that monitor (e.g. eDP-1, DP-1, HDMI-1).
    """
    # Get the list of connected monitors
    output = subprocess.check_output('xrandr')
    monitors = [m.group(1) for m in re.finditer(r'(\w*-\d) connected', output.decode('utf-8'))]

    # Get the current mouse position
    mouse_x, mouse_y =  get_mouse_location()

    # Get the display location for each monitor and check if the mouse coordinates are inside
    # the boundary of the display
    for monitor in monitors:
        width, height, r_width, r_height = get_monitor_details(monitor)
        # print(f' monitor {monitor}\n X {mouse_x}\n Y {mouse_y}\n width {width}\n height {height}')
        if mouse_x >= width and mouse_x <= width + r_width and mouse_y >= height and mouse_y <= height + r_height:
            return monitor

print(identify_active_monitor())
