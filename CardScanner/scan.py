import pyinsane2
from . import read, SCAN_DIR

def setup():
    pyinsane2.init()
    devices = pyinsane2.get_devices()
    try:
        assert(len(devices) > 0)
        device = devices[0]
        # device.options['AutoDocumentSize']
        # Specify color scanning
        pyinsane2.set_scanner_opt(device, 'mode', ['24bit Color[Fast]'])
        # Set scan resolution
        pyinsane2.set_scanner_opt(device, 'resolution', [200])
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

def save_ab(image_list):
    start_no = floor(len(read.get_file_list(SCAN_DIR + "*png"))/2)
    archive_no = floor(len(read.get_file_list(ARCHIVE_DIR + "*png"))/2)
    for i in range(0, len(image_list), 2):
        image_list[i].save(SCAN_DIR+"{:06}-a.png".format(floor(i/2 + start_no+archive_no)))
        image_list[i+1].save(SCAN_DIR+"{:06}-b.png".format(floor(i/2 + start_no+archive_no)))

def bg_trim(im):
    """
    Function to programmatically crop card to edge.
    `im` is a PIL Image Object.
    """
    # This initial crop is hacky and stupid (should just be able to set device
    # options) but scanner isn't 'hearing' those settings.
    # w,h = im.size
    im = im.crop((443, 0, 1242, 1200))
    # bg = Image.new(im.mode, im.size, im.getpixel((2, 2)))
    # diff = ImageChops.difference(im, bg)
    # diff = ImageChops.add(diff, diff, 2.0, -100)
    # bbox = diff.getbbox()
    return im
    # if bbox:
    #     return im
    # else:
    #     print("There's been a problem.")
