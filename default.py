"""Arctic Splash screensaver entry point. All scripting belongs to this add-on."""
from datetime import datetime
import threading
import time

import xbmc
import xbmcaddon
import xbmcgui

from resources.lib.states import STATES, Selectors, current_states, render_properties


def current():
    return current_states(datetime.now(), xbmc.getInfoLabel('System.Locale(iso)'),
                          xbmc.getInfoLabel('Weather.FanartCode'))


class ExitMonitor(xbmc.Monitor):
    def __init__(self, stopped):
        super().__init__()
        self.stopped = stopped

    def onScreensaverDeactivated(self):
        self.stopped.set()

    def onDPMSActivated(self):
        self.stopped.set()


class Splash(xbmcgui.WindowXMLDialog):
    def __init__(self, *args, **kwargs):
        self.stopped = threading.Event()
        self.ready = threading.Event()
        self.selectors = None
        self.properties = {}

    def onInit(self):
        self.refresh()
        self.ready.set()

    def onAction(self, action):
        if action.getId():
            self.stopped.set()

    def refresh(self):
        values = self.selectors.update(time.monotonic(), current())
        for key, value in render_properties(values).items():
            if self.properties.get(key) != value:
                self.setProperty('ArcticSplash.' + key, value)
                self.properties[key] = value


def run():
    addon = xbmcaddon.Addon()
    settings = {key + suffix: addon.getSetting(key + suffix)
                for key in STATES for suffix in ('.mode', '.state')}
    window = Splash('screensaver-arctic-splash.xml', addon.getAddonInfo('path'), 'default', '1080i')
    window.selectors = Selectors(settings, current(), time.monotonic())
    monitor = ExitMonitor(window.stopped)
    try:
        window.show()
        deadline = time.monotonic() + 10
        while not window.stopped.is_set() and not monitor.abortRequested():
            if window.ready.is_set():
                window.refresh()
            elif time.monotonic() > deadline:
                xbmc.log('Arctic Splash: screensaver window did not initialise.', xbmc.LOGERROR)
                break
            if monitor.waitForAbort(0.25):
                break
    finally:
        window.close()
        del monitor
        del window


if __name__ == '__main__':
    run()
