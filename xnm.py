#!/usr/bin/python

import dbus
import NetworkManager

from Tkinter import *

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

def renderStatus(container, connected=False, saved=False, protected=False):
    Label(container, text=lockChar, bg=bgColor, fg=fgColor if protected else bgColor, font=iconFont).grid(row = 0, column = 0)
    Label(container, text=starChar, bg=bgColor, fg=fgColor if saved else bgColor, font=iconFont).grid(row = 0, column = 1)
    Label(container, text=connChar, bg=bgColor, fg=fgColor if connected else bgColor, font=iconFont).grid(row = 0, column = 2)
    
def addConnection(container, line, connected=False, saved=None, protected=False, dev=None):
    f = Frame(container, bg=bgColor)

    renderStatus(f, connected, saved, protected)

    l = Label(f, text=" " + line, bg=bgColor, fg=fgColor, font=bodyFont, justify=LEFT, anchor=W)
    l.grid(row=0, column = 3, sticky="ew")
    
    l.bind("<Enter>", lambda e: e.widget.config(bg=midColor, fg=bgColor))
    l.bind("<Leave>", lambda e: e.widget.config(bg=bgColor, fg=fgColor))

    if saved and dev and not connected:
        l.bind("<Button-1>",lambda e: NetworkManager.NetworkManager.ActivateConnection(saved, dev, "/"))
        
    f.pack(fill="x")

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

def dumpWifi(container, dev):
    for ap in dev.SpecificDevice().GetAllAccessPoints():
        connected = not isinstance(dev.SpecificDevice().ActiveAccessPoint, dbus.ObjectPath) and ap.Ssid == dev.SpecificDevice().ActiveAccessPoint.Ssid
        saved = savedWifiConnection(ap.Ssid, ap.HwAddress)
        protected = ap.Flags == 1
        addConnection(container, ap.Ssid, connected, saved, protected, dev)
            
def dumpEthernet(container, dev):                        
    addConnection(container, "(ethernet)")

def dumpModem(container, dev):
    addConnection(container, "(modem)")

def dumpGeneric(container, dev):
    addConnection(container, "(generic)")

root = Tk()

for i, dev in enumerate(NetworkManager.NetworkManager.GetDevices()):
    deviceHeader = "%s (%s):" % (dev.Interface, NetworkManager.const("device_state", dev.State))
    ifLabel = LabelFrame(root, text=deviceHeader, bg=bgColor, fg=midColor, font=headFont)
    
    if (isinstance(dev.SpecificDevice(), NetworkManager.Wireless)):
	dumpWifi(ifLabel, dev)
    elif (isinstance(dev.SpecificDevice(), NetworkManager.Wired)):
	dumpEthernet(ifLabel, dev)
    elif (isinstance(dev.SpecificDevice(), NetworkManager.Modem)):
	dumpModem(ifLabel, dev)
    else:
	dumpGeneric(ifLabel, dev)

    ifLabel.pack(fill="both")
        
root.mainloop()
