# Next Stop

Backend for [@civic-data-design-lab](http://github.com/civic-data-design-lab)'s work for the Cooper Hewitt's _Reimagining Mobility_ exhibition.

## Install SANE

1. See if homebrew is installed on your Mac (type `brew --version` into a terminal window).
2. If not, run this command in a terminal window: `/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"`
3. In a terminal window, `run brew install sane-backend`

## Install PIP (Python Package Manager)

1. Check if PIP is installed by typing `pip -V` into a terminal window.
2. In a terminal window, type `curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py`
3. In a terminal window, type `python3 get-pip.py`

## [Download and Extract My Repository](https://github.com/ericmhuntley/nextstop/archive/master.zip)

## Install Project Dependencies

1. In a terminal window, change directory into the repository root (for example, cd ~/Downloads/nextstop
2. Install my project dependencies by typing `pip install -r requirements.txt`

## Run our Scheduler

Assuming you have the scanner hooked up to a USB port, you should now be able to run `python3 scheduler.py` from a terminal window. This will get the scanner running - drop a card in and within a few sections it will scan.
