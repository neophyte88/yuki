from pyvirtualdisplay import Display
from tbselenium.utils import start_xvfb, stop_xvfb
from tbselenium.tbdriver import TorBrowserDriver
display = start_xvfb()
tbb_path = "/home/neophyte88/finalyearproject/yuki/support/bin/tor-browser/"
x = None
with TorBrowserDriver(tbb_path, executable_path="/usr/local/bin/geckodriver", tbb_logfile_path = "/home/neophyte88/1.json") as driver:
	x = driver.get('https://check.torproject.org')
