# -*- coding: utf-8 -*-

from gi.repository import GObject, Gtk, Gdk, Gedit

class GEdit3TabSwitch(GObject.Object, Gedit.WindowActivatable):
    window = GObject.property(type=Gedit.Window)

    KEYS_LEFT = ('ISO_Left_Tab', 'Page_Up')
    KEYS_RIGHT = ('Tab', 'Page_Down')
    KEYS = KEYS_LEFT + KEYS_RIGHT

    def __init__(self):
        GObject.Object.__init__(self)

    def do_activate(self):
        handlers = []
        handler_id = self.window.connect('key-press-event', self.on_key_press_event)
        handlers.append(handler_id)
        self.window.GEdit3TabSwitchHandlers = handlers

    def do_deactivate(self):
        handlers = self.window.GEdit3TabSwitchHandlers
        for handler_id in handlers:
            self.window.disconnect(handler_id)

    def do_update_state(self):
        pass

    def on_key_press_event(self, window, event):
        key = Gdk.keyval_name(event.keyval)

        if event.state & Gdk.ModifierType.CONTROL_MASK and key in self.KEYS:
            atab = window.get_active_tab()
            tabs = atab.get_parent().get_children()
            tlen = len(tabs)
            i = 0
            tab = atab

            for tab in tabs:
                i += 1
                if tab == atab:
                    break

            if key in self.KEYS_LEFT:
                i -= 2

            if i < 0:
                tab = tabs[tlen-1]
            elif i >= tlen:
                tab = tabs[0]
            else:
                tab = tabs[i]

            window.set_active_tab(tab)

            return True
