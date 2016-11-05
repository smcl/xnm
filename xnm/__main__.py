#!/usr/bin/python

import dbus
import NetworkManager
import tkSimpleDialog
import uuid

from Tkinter import *
from Xlib import display

bgColor = "black"
midColor = "dimgrey"
fgColor = "grey"
brightColor = "white"

headFont = ("Source Code Pro", 10, "bold")
bodyFont = ("Source Code Pro", 10)
iconFont = ("Font Awesome", 10)

wifiChar = u"\uf1eb"
lockChar = u"\uf023"
starChar = u"\uf005"
connChar = u"\uf0c1"

# we want the window to appear as a popup - so update geometry() on startup
# so that it's centered on the current mouse position
def center_on_mouse(window):
    mouse = display.Display().screen().root.query_pointer()._data
    mx = mouse["root_x"]
    my = mouse["root_y"]

    w = window.winfo_width()
    h = window.winfo_height()

    window.geometry("%dx%d+%d+%d" % (w, h, mx, my))

def renderStatus(container, connected=False, saved=False, protected=False):
    Label(container, text=lockChar, bg=bgColor, fg=fgColor if protected else bgColor, font=iconFont).grid(row = 0, column = 0, sticky="e")
    Label(container, text=starChar, bg=bgColor, fg=fgColor if saved else bgColor, font=iconFont).grid(row = 0, column = 1, sticky="e")
    Label(container, text=connChar, bg=bgColor, fg=fgColor if connected else bgColor, font=iconFont).grid(row = 0, column = 2, sticky="e")

def dbusNull(obj):
    return isinstance(obj, dbus.ObjectPath)

def enableDevice(dev):
    dev.AutoConnect = True
    sys.exit

def disableDevice(dev):
    dev.Disconnect()
    sys.exit

def createWifiConnection(ap, psk=None):
    wifiConn = {
        "802-11-wireless" : {
            "mode" : "infrastructure",
            "ssid" : ap.Ssid
        },
        "connection" : {
            "id" : ap.Ssid,
            "type" : "802-11-wireless",
            "uuid" : str(uuid.uuid4())
        },
        "ipv4" : {
            "method" : "auto"
        },
        "ipv6" : {
            "method" : "auto"
        }
    }

    if psk:
        wifiConn["802-11-wireless"]["security"] = "802-11-wireless-security"
        wifiConn["802-11-wireless-security"] = {
            "auth-alg" : "open",
            "key-mgmt" : "wpa-psk",
            "psk" : psk
        }

    return wifiConn

def disconnectDevice(dev):
    dev.Disconnect()
    sys.exit()

def connectExisting(dev, saved):
    NetworkManager.NetworkManager.ActivateConnection(saved, dev, "/")
    sys.exit()

def connectNew(dev, ap, protected):
    password = None

    if protected:
        title = ap.Ssid
        message = "Please input the password for %s" % (ap.Ssid)
        password = tkSimpleDialog.askstring(title, message)

    if password:
        newConn = createWifiConnection(ap, password)
        NetworkManager.Settings.AddConnection(newConn)
        NetworkManager.NetworkManager.ActivateConnection(newConn, dev, "/")

    sys.exit()


def addConnection(container, line):
    f = Frame(container, bg=bgColor)

    renderStatus(f)

    l = Label(f, text=" " + line, bg=bgColor, fg=fgColor, font=bodyFont, justify=LEFT, anchor=W)
    l.grid(row=0, column = 3, sticky="ew")

    l.bind("<Enter>", lambda e: e.widget.config(bg=midColor, fg=bgColor))
    l.bind("<Leave>", lambda e: e.widget.config(bg=bgColor, fg=fgColor))

    f.pack(fill="x", expand=1)

def addModemConnection(container, connId, connected, dev, connection):
    f = Frame(container, bg=bgColor)

    renderStatus(f, connected, False, False)

    if not connected:
        callback = lambda: connectExisting(dev, connection)
    else:
        callback = lambda: disconnectDevice(dev)

    b = Button(f, text=" " + connId, bg=bgColor, fg=fgColor, font=bodyFont, justify=LEFT, anchor=W, command=callback, highlightthickness=0, relief=FLAT, activeforeground=bgColor, activebackground=fgColor, pady=0)
    b.grid(row=0, column = 3, sticky="ew")

    f.pack(fill="x", expand=True)

def addWifiConnection(container, ap, connected=False, saved=None, protected=False, dev=None):
    f = Frame(container, bg=bgColor)

    renderStatus(f, connected, saved, protected)

    callback = None
    if connected:
        callback = lambda: disconnectDevice(dev)
    elif saved:
        callback = lambda: connectExisting(dev, saved)
    else:
        callback = lambda: connectNew(dev, ap, protected)

    b = Button(f, text=" " + ap.Ssid, bg=bgColor, fg=fgColor, font=bodyFont, justify=LEFT, anchor=W, command=callback, highlightthickness=0, relief=FLAT, activeforeground=bgColor, activebackground=fgColor, pady=0)
    b.grid(row=0, column = 3, sticky="ew")

    f.pack(fill="x", expand=True)

def savedWifiConnection(ssid, mac):
	connections = NetworkManager.Settings.ListConnections()

	for conn in connections:
		settings = conn.GetSettings()

		if not "802-11-wireless" in settings:
			continue

		wifi_settings = settings["802-11-wireless"]

		this_ssid = wifi_settings["ssid"]

		if this_ssid == ssid:
			return conn

	return None

def setupWifi(container, dev):
    for ap in dev.SpecificDevice().GetAllAccessPoints():
        connected = not dbusNull(dev.SpecificDevice().ActiveAccessPoint) and ap.Ssid == dev.SpecificDevice().ActiveAccessPoint.Ssid
        saved = savedWifiConnection(ap.Ssid, ap.HwAddress)
        protected = ap.Flags == 1
        addWifiConnection(container, ap, connected, saved, protected, dev)

def setupEthernet(container, dev):
    pass #addConnection(container, "(ethernet)")

def setupModem(container, dev):
    for connection in dev.AvailableConnections:
        connId = connection.GetSettings()["connection"]["id"]
        connected = not dbusNull(dev.ActiveConnection) and dev.ActiveConnection.Id == connId
        addModemConnection(container, connId, connected, dev, connection)

def setupGenericDevice(container, dev):
    addConnection(container, "(generic)")

root = Tk()
root.wm_title("xnm")

for i, dev in enumerate(NetworkManager.NetworkManager.GetDevices()):
    deviceHeader = " %s (%s) " % (dev.Interface, NetworkManager.const("device_state", dev.State))
    ifLabel = LabelFrame(root, text=deviceHeader, bg=bgColor, fg=midColor, font=headFont)

    #ifToggle = Checkbutton(ifLabel, bg=bgColor, fg=midColor, font=bodyFont, bd=0, highlightthickness=0, compound=RIGHT, activebackground=fgColor, activeforeground=bgColor)
    #ifToggle.pack(fill="both")
    #if (NetworkManager.const("device_state", dev.State) == "disconnected"):
    #    ifToggle.config(text="Enable", command=lambda: enableDevice(dev))
    #else:
    #    ifToggle.config(text="Disable", command=lambda: disableDevice(dev))

    #ifDisconnect = Button(ifLabel, text="Disconnect", bg=bgColor, fg=midColor, font=bodyFont, bd=0, highlightthickness=0, compound=RIGHT, activebackground=fgColor, activeforeground=bgColor)
    #ifDisconnect.pack(fill="both")

    if (isinstance(dev.SpecificDevice(), NetworkManager.Wireless)):
	setupWifi(ifLabel, dev)
    elif (isinstance(dev.SpecificDevice(), NetworkManager.Wired)):
	setupEthernet(ifLabel, dev)
    elif (isinstance(dev.SpecificDevice(), NetworkManager.Modem)):
	setupModem(ifLabel, dev)
    else:
	setupGenericDevice(ifLabel, dev)

    ifLabel.pack(fill="x", expand=1)

#center_on_mouse(root)


if __name__ == '__main__':
    root.mainloop()
    root.destroy()
