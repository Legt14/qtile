# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import subprocess
import os

from libqtile import bar, layout, widget, extension, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy

from qtile_extras import widget
from qtile_extras.widget.decorations import PowerLineDecoration


mod = "mod1"
terminal = "alacritty"


@hook.subscribe.startup_once
def autostart():
    script = os.path.expanduser("~/.config/qtile/scripts/start.sh")
    subprocess.call([script])


colors = {
    "Black": "#282c34",
    "White": "#abb2bf",
    "Light Red": "#e06c75",
    "Dark Red": "#be5046",
    "Green": "#98c379",
    "Light Yellow": "#e5c07b",
    "Dark Yellow": "#d19a66",
    "Blue": "#61afef",
    "Magenta": "#c678dd",
    "Cyan": "#56b6c2",
    "Gutter Grey": "#4b5263",
    "Comment Grey": "#5c6370",
    "Midnight Blue": "#003366",
    "Smalt": "#033494",
    "Orange": "#ff5f1f",
}


keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key(
        [mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"
    ),
    Key(
        [mod, "shift"],
        "l",
        lazy.layout.shuffle_right(),
        desc="Move window to the right",
    ),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key(
        [mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"
    ),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key(
        [mod],
        "t",
        lazy.window.toggle_floating(),
        desc="Toggle floating on the focused window",
    ),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    ################
    ##Customs keys##
    ################
    Key([mod], "w", lazy.spawn("firefox"), desc="launch firefox"),
    Key([mod], "r", lazy.spawn("rofi -show drun"), desc="Rofi"),
    # Audio
    Key([mod], "minus", lazy.spawn("amixer sset Master,0 5%-")),
    Key([mod], "equal", lazy.spawn("amixer sset Master,0 5%+")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer sset Master,0 1%-")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer sset Master,0 1%+")),
    Key([], "XF86AudioMute", lazy.spawn("amixer sset Master,0 toggle")),
    Key(
        [],
        "XF86AudioPause",
        lazy.spawn("playerctl play-pause"),
        desc="Play/Pause player",
    ),
    Key(
        [],
        "XF86AudioPlay",
        lazy.spawn("playerctl play-pause"),
        desc="Play/Pause player",
    ),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next"), desc="Skip to next"),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous"), desc="Skip to previous"),
    Key([], "XF86AudioStop", lazy.spawn("playerctl stop"), desc="Stop"),
]

groups = [Group(i) for i in ["一", "二", "三", "四", "五", "六", "七", "八", "九"]]
group_hotkeys = "123456789"

for g, k in zip(groups, group_hotkeys):
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                k,
                lazy.group[g.name].toscreen(),
                desc=f"Switch to group {g.name}",
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                k,
                lazy.window.togroup(g.name, switch_group=False),
                desc=f"Switch to & move focused window to group {g.name}",
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )
layouts = [
    layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=1, margin=8),
    layout.Max(),
    # layout.MonadTall(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="Firacode Nerd Font",
    fontsize=12,
    padding=0,
)
extension_defaults = widget_defaults.copy()


def longNameParse(text):
    for string in [
        "Chromium",
        "Firefox",
        "nvim",
    ]:  # Add any other apps that have long names here
        if string in text:
            text = string
        else:
            text = text
    return text


#######################
#######POWERLINE#######
#######################

rounded_left = {"decorations": [PowerLineDecoration(path="rounded_left", size=12)]}
rounded_right = {"decorations": [PowerLineDecoration(path="rounded_right", size=12)]}
arrow_left = {"decorations": [PowerLineDecoration(path="arrow_left", size=12)]}
arrow_right = {"decorations": [PowerLineDecoration(path="arrow_right", size=12)]}
forward_slash = {"decorations": [PowerLineDecoration(path="forward_slash", size=12)]}
back_slash = {"decorations": [PowerLineDecoration(path="back_slash", size=12)]}

screens = [
    Screen(
        bottom=bar.Bar(
            [
                widget.TextBox(
                    text="",
                    background=colors["Magenta"],
                    foreground=colors["Black"],
                    padding=10,
                    fontsize=36,
                ),
                widget.Spacer(length=2, background=colors["Magenta"], **arrow_left),
                widget.Net(
                    padding=10,
                    background=colors["Black"],
                ),
                widget.Spacer(length=2, background=colors["Black"], **arrow_left),
                widget.Memory(
                    format="RAM {MemPercent}%",
                    background="#BC96E6",
                    foreground=colors["Black"],
                    padding=10,
                    fontsize=14,
                ),
                widget.Spacer(length=2, background="#BC96E6", **arrow_left),
                widget.CPU(
                    padding=10,
                    background=colors["Black"],
                ),
                widget.Spacer(length=1, background=colors["Black"], **arrow_left),
                widget.Spacer(length=1, background="#BC96E6", **arrow_left),
            ],
            25,
            margin=10,
            background=colors["Black"],
        ),
        top=bar.Bar(
            [
                widget.TextBox(
                    text="  ",
                    fontsize=20,
                    background=colors["Magenta"],
                    foreground=colors["Black"],
                ),
                widget.Spacer(length=2, background=colors["Magenta"], **rounded_left),
                widget.GroupBox(
                    background=colors["Light Yellow"],
                    foreground=colors["Black"],
                    fontsize=15,
                    borderwidth = 2,
                    font = 'Firacode Nerd Font',
                    block_highlight_text_color = colors["Magenta"],
                    padding = 3,
                    this_current_screen_border = "#6b58a7",
                    this_screen_border = "#6b58a7"

                ),
                widget.Spacer(
                    length=2, background=colors["Light Yellow"], **rounded_left
                ),
                widget.WindowName(
                    parse_text=longNameParse,
                    background=colors["Dark Yellow"],
                    foreground=colors["Black"],
                    fontsize=13,
                    padding=29,
                ),
                widget.Spacer(length=1, background=colors["Dark Yellow"], **arrow_left),
                widget.Spacer(length=400, background=colors["Black"], **rounded_right),
                widget.Systray(background="#6b58a7"),
                widget.Spacer(length=2, background="#6b58a7", **rounded_right),
                widget.Clock(
                    background=colors["Blue"],
                    format=" %d/%m/%y 󰥔 %H:%M",
                    foreground=colors["Black"],
                    fontsize=14,
                ),
                widget.Spacer(length=2, background=colors["Blue"], **rounded_right),
                widget.Volume(
                    fmt="墳 {}",
                    mute_command="amixer -D pulse set Master toggle",
                    background=colors["Green"],
                    foreground=colors["Black"],
                    fontsize=14,
                    padding=10,
                ),
                widget.Spacer(length=1, background=colors["Green"], **rounded_right),
                widget.QuickExit(
                    default_text="󰗼",
                    countdown_format="{}",
                    fontsize=20,
                    background=colors["Dark Red"],
                    padding=10,
                ),
            ],
            28,
            margin=5,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
        # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        # x11_drag_polling_rate = 60,
        wallpaper=os.path.expanduser("~/.config/qtile/wallpapers/01.png"),
        wallpaper_mode="stretch",
    ),
]

# Drag floating layouts.
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
