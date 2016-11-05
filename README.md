# xnm
xnm is a lightweight networkmanager menu for window managers missing one, such as xmonad.

## Install

Either retrieve from pypi using pip:

```
$ pip install xnm
```

or clone this repo, and install using `setup.py`:
```
$ git clone https://github.com/smcl/xnm
$ cd xnm
$ python setup.py install
```

## Using

Once xnm is installed you can either launch it standalone in an xterm...

```
$ python -m xnm
```

... or you can add it as an `action` in your xmobar setup, so that when you click an icon (I use `DynNetwork`) like so:

```
 template = "... <action=`python -m xnm`>%dynnetwork% <fn=1></fn></action> ..."
```

## TODO

NetworkManager can do a lot of things but I do not plan to do all of them, but my goals are (checkbox indicates whether completed or not):

* wifi
  * [x] search
  * [x] connect (open and authenticated using wpa-psk)
  * [x]  disconnect
* mobile broadband
  * [ ] configure new
  * [x] connect
  * [x] disconnect
* bluetooth
  * [ ] search
  * [ ] pair

Right now it can search for and connect to open and protected wifi networks, so there's quite a way to go :)

# screenshot

![work in progress](/xnm-screenshot.png?raw=true)
