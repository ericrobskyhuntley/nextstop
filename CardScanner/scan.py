import pyinsane2
from PIL import Image, ImageChops
from CardReader import cr

def bg_trim(im):
    """
    Function to programmatically crop card to edge.
    `im` is a PIL Image Object.
    """
    bg = Image.new(im.mode, im.size, im.getpixel((1693, 2790)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)
    else:
        print("There's been a problem.")

try:
    # Initiation block.
    pyinsane2.init()
    devices = pyinsane2.get_devices()
    assert(len(devices) > 0)
    device = devices[0]
    print(f'PyInsane2 initiatied using {device.name}.')

    # Setup for Duplex scanning.
    try:
        pyinsane2.set_scanner_opt(device, 'source', ['Duplex ADF', 'ADF', 'Feeder'])
    except pyinsane2.PyinsaneException as e:
        print('No document feeder found', e)
    # Specify color scanning
    pyinsane2.set_scanner_opt(device, 'mode', ['Color'])
    # Set scan resolution
    pyinsane2.set_scanner_opt(device, 'resolution', [200])
    # specificy scan area
    # We want full area because otherwise,
    pyinsane2.maximize_scan_area(device)

    try:
        scan_session = device.scan(multiple=True)
        print("Scanning...")
        while True:
            try:
                scan_session.scan.read()
            except EOFError:
                print(f'Scanned page {len(scan_session.images)}.')
    except StopIteration:
        print(f'Document feeder is empty. Scanned {len(scan_session.images)} pages.')
    for i in range(0, len(scan_session.images)):
        image = bg_trim(scan_session.images[i])
        if (i % 2 == 0) | (i == 0):
            image.save(f'{i}-front-4.png')
        else:
            cr.read_back(image)
            image.rotate(180).save(f'assets/backs_test/{i-1}-back-3.png')


finally:
    pyinsane2.exit()
