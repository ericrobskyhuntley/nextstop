import pyinsane2
from . import read, SCAN_DIR

def setup():
    pyinsane2.init()
    devices = pyinsane2.get_devices()
    # dir(devices[0])
    devices[0].options

    try:
        assert(len(devices) > 0)
        device = devices[0]
        # device.options['AutoDocumentSize']
        # Specify color scanning
        pyinsane2.set_scanner_opt(device, 'mode', ['24bit Color[Fast]'])
        # Set scan resolution
        pyinsane2.set_scanner_opt(device, 'resolution', [200])
        # pyinsane2.set_scanner_opt(device, 'MultifeedDetection', [0])
        # pyinsane2.set_scanner_opt(device, 'AutoDeskew', [1])
        # pyinsane2.set_scanner_opt(device, 'AutoDocumentSize', [1])

        # device.options
        # Set scan area
        pyinsane2.maximize_scan_area(device)
        try:
            pyinsane2.set_scanner_opt(device, 'source', ['Automatic Document Feeder(center aligned,Duplex)'])
        except pyinsane2.PyinsaneException as e:
            print('No document feeder found', e)
        print(f'PyInsane2 initiatied using {device.name}.')
        return device
    except AssertionError:
        print("no scanners found")
        pyinsane2.exit()

def scan_cards(device):
    try:
        scan_session = device.scan(multiple=True)
        print("Scanning ...")
        while True:
            try:
                scan_session.scan.read()
            except EOFError:
                print ("hi!")
    except StopIteration:
        im_list = scan_session.images
        pyinsane2.exit()
        return im_list
