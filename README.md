# xnm
xnm is a lightweight networkmanager menu for window managers missing one, such as xmonad. I have no idea if one exists already, and to be honest I don't want to know as it'll give me an excuse to bail out.

Basically I love my xmonad/xmobar setup but there's a handful of tasks that I can't currently accomplish using my current setup. One of these tasks is setting up and connecting to networks using NetworkManager. Xmobar doesn't really support little popup menus, so I'm creating python/tk app that will be launched with an xmobar <action>, and will be as similar in appearance to a popup as possible.

NetworkManager can do a lot of things but I do not plan to do all of them, but my goals are

* wifi
  * [x] search
  * [x] connect (open and authenticated using wpa-psk)
  * [ ] disconnect
* mobile broadband
  * [ ] configure
  * [ ] connect
  * [ ] disconnect
* bluetooth
  * [ ] search
  * [ ] pair

Right now it can search for and connect to open and protected wifi networks, so there's quite a way to go :)

# requirements

Currently there's a handful of dependencies:
* NetworkManager and stuff
* py-networkmanager
* Tk
* fonts:
  * Source Code Pro
  * Font Awesome

# screenshot

![work in progress](/xnm-screenshot.png?raw=true)
