from CardScanner import read, SCAN_DIR
list = read.get_file_list(SCAN_DIR + '*.png')
read.read_from_disk(list)
