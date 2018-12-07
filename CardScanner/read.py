import cv2
import numpy as np

INTERVAL = 23
PIXEL_THRESHOLD = 300
COLOR_WINDOW = 15

QUESTION_HUES = [
    # My preferred transport mode(s) in 2020 will be...
    (4, np.array([1, 232, 190])),
    # In 2040, the average person will...
    (5, np.array([0, 255, 62])),
    # Responsibility for autonomous vehicle accidents belongs to...
    (6, np.array([27, 176, 242])),
    # In 2040, commuting will take...
    (7, np.array([60, 135, 150])),
    # In 2040, everyone will have access to...
    (8, np.array([107, 255, 42])),
    # The future of mobility will make the world
    (9, np.array([142, 192, 70])),
    # In the future, my transportation costs will...
    (10, np.array([88, 255, 62])),
    # Future mobility options will have the greatest imapact on...
    (12, np.array([174, 156, 208])),
    # In 2040...
    (13, np.array([106, 205, 120])),
    # Travel in the future will be more dangerous for...
    (14, np.array([13, 250, 243])),
]

def get_corners(img):
    from_corner = 25
    box_size = 10
    hsv = cv2.cvtColor(img, axis=0), cv2.COLOR_BGR2HSV)
    d = dict()
    d['height'], d['width'] = dst.shape[:2]
    tl_hsv = hsv[from_corner:from_corner+box_size+75, from_corner:from_corner+box_size+75]
    tl_hsv = np.median(np.median(tl_hsv, axis=0), axis=0)
    d['tl_hsv'] = tl_hsv
    tr_hsv = hsv[from_corner:from_corner+box_size+75, d['width']-from_corner-box_size-75:d['width']-from_corner]
    tr_hsv = np.median(np.median(tr_hsv, axis=0), axis=0)
    d['tr_hsv'] = tr_hsv
    bl_hsv = hsv[d['height']-from_corner-box_size:d['height']-from_corner, from_corner:from_corner + box_size]
    bl_hsv = np.median(np.median(bl_hsv, axis=0), axis=0)
    d['bl_hsv'] = bl_hsv
    br_hsv = hsv[d['height']-from_corner-box_size:d['height']-from_corner, d['width']-from_corner-box_size:d['width']-from_corner]
    br_hsv = np.median(np.median(br_hsv, axis=0), axis=0)
    d['br_hsv'] = br_hsv
    med = np.median(np.array([tl_hsv, tr_hsv, bl_hsv, br_hsv]), axis=0)
    d['med'] = med
    return d

def get_question(hsv):
    # print(hsv)
    possible_values = np.array([hsv['med'], hsv['tl_hsv'], hsv['tr_hsv'], hsv['bl_hsv'], hsv['br_hsv']])
    print(hsv)
    q = None
    for value in possible_values:
        for question in QUESTION_HUES:
            lower_bound = question[1] - COLOR_WINDOW
            upper_bound = question[1] + COLOR_WINDOW
            if np.all(value > lower_bound) and np.all(value < upper_bound):
                q = question
    return q

def get_answers(dst, q):
	if (q==5):
		"""
		In 2040, the average person will...
		"""
		f_x_dims = np.array([68, 333])
		f_y_dims = np.array([724, 795, 868])
		answers = []
		for i, x in enumerate(f_x_dims):
			for j, y in enumerate(f_y_dims):
				crop = dst[y:y+INTERVAL, x:x+INTERVAL]
				if (j < 2) or ((j == 2) and (i==0)):
					if (np.sum(crop) > PIXEL_THRESHOLD):
						# max_test = np.sum(crop)
						# i_max = i
						# j_max = j
						if (i==0) & (j==0):
							answers.append(10) # own a car
						elif (i==0) & (j==1):
							answers.append(11) # lease a car
						elif (i==0) & (j==2):
							answers.append(14) # have no car
						elif (i==1) & (j==0):
							answers.append(45) # own AV
						elif (i==1) & (j==1):
							answers.append(46) # lease AV
		return answers
	elif (q == 4):
		"""
		My preferred transport mode(s) in 2040 will be. . .
		"""
		answers = []
		f_x_dims = np.array([70, 472])
		f_y_dims = np.array([644, 704, 766, 825, 885, 944])
		for i, x in enumerate(f_x_dims):
			for j, y in enumerate(f_y_dims):
				crop = dst[y:y+INTERVAL, x:x+INTERVAL]
				if (j < 5) or ((j == 5) and (i==1)):
					if (np.sum(crop) > PIXEL_THRESHOLD):
						if (i==0) & (j==0):
							answers.append(15) #av bus
						elif (i==0) & (j==1):
							answers.append(48) # bus
						elif (i==0) & (j==2):
							answers.append(16) #av car
						elif (i==0) & (j==3):
							answers.append(47) # car
						elif (i==0) & (j==4):
							answers.append(49) # flying car
						elif (i==1) & (j==0):
							answers.append(21) # hyperloop
						elif (i==1) & (j==1):
							answers.append(18) # subways
						elif (i==1) & (j==2):
							answers.append(20) # walking
						elif (i==1) & (j==3):
							answers.append(19) # bikes
						elif (i==1) & (j==4):
							answers.append(17) # scooters
						elif (i==1) & (j==5):
							answers.append(23) # O T H E R
		return answers
	elif (q == 8):
		"""
		In 2040, everyone will have access to...
		"""
		f_x_dims = np.array([67, 473])
		f_y_dims = np.array([646, 706, 765, 825, 883, 943])
		answers = []
		# max_test = 0
		# i_max = -1
		# j_max = -1
		for i, x in enumerate(f_x_dims):
			for j, y in enumerate(f_y_dims):
				crop = dst[y:y+INTERVAL, x:x+INTERVAL]
				if (j < 5) or ((j == 5) and (i==1)):
					if (np.sum(crop) > PIXEL_THRESHOLD):
						if (i==0) & (j==0):
							answers.append(15) #av bus
						elif (i==0) & (j==1):
							answers.append(48) # bus
						elif (i==0) & (j==2):
							answers.append(16) #av car
						elif (i==0) & (j==3):
							answers.append(47) # car
						elif (i==0) & (j==4):
							answers.append(49) # flying car
						elif (i==1) & (j==0):
							answers.append(21) # hyperloop
						elif (i==1) & (j==1):
							answers.append(18) # subways
						elif (i==1) & (j==2):
							answers.append(20) # walking
						elif (i==1) & (j==3):
							answers.append(19) # bikes
						elif (i==1) & (j==4):
							answers.append(17) # scooters
						elif (i==1) & (j==5):
							answers.append(23) # O T H E R
		return answers
	# Dims donezo.
	elif (q == 13):
		"""
		In 2040...
		"""
		f_x_dims = np.array([72, 182])
		f_y_dims = np.array([607, 679, 753, 828, 902])

		max_test = 0
		i_max = -1
		j_max = -1
		for i, x in enumerate(f_x_dims):
			for j, y in enumerate(f_y_dims):
				crop = dst[y:y+INTERVAL, x:x+INTERVAL]
				if ((j < 4) and (i==0)) or ((j == 4) and (i==1)):
					if (np.sum(crop) > PIXEL_THRESHOLD) and (np.sum(crop) > max_test):
						max_test = np.sum(crop)
						i_max = i
						j_max = j
		if (i_max==0) & (j_max==0):
			return [50] # parking spots into parks
		elif (i_max==0) & (j_max==1):
			return [51] # streets are for robots
		elif (i_max==0) & (j_max==2):
			return [52] # garages house grandmas
		elif (i_max==0) & (j_max==3):
			return [53] # parking lots urban farms
		elif (i_max==1) & (j_max==4):
			return [23] # O T H E R
		else:
			# print(max_test)
			return []
	elif (q == 14):
		"""
		Travel in the future will be more dangerous for...
		"""
		f_x_dims = np.array([68, 333, 457, 548])
		f_y_dims = np.array([802, 874])

		max_test = 0
		i_max = -1
		j_max = -1
		for i, x in enumerate(f_x_dims):
			for j, y in enumerate(f_y_dims):
				crop = dst[y:y+INTERVAL, x:x+INTERVAL]
				if (i < 1) or ((i == 1) and (j == 0)) or ((i == 3) and (j == 0)) or ((i == 2) and (j == 1)):
					if (np.sum(crop) > PIXEL_THRESHOLD) and (np.sum(crop) > max_test):
						max_test = np.sum(crop)
						i_max = i
						j_max = j
		if (i_max==0) & (j_max==0):
			return [54] # pedestrians
		elif (i_max==0) & (j_max==1):
			return [57] # stray cats
		elif (i_max==1) & (j_max==0):
			return [55] # drivers
		elif (i_max==3) & (j_max==0):
			return [56] # bikers
		elif (i_max==2) & (j_max==1):
			return [23] # O T H E R
		else:
			# print(max_test)
			return []
	elif (q == 6):
		"""
		Responsibility for autonomous vehicle accidents belongs to...
		"""
		f_x_dims = np.array([71])
		f_y_dims = np.array([725, 785, 843, 900, 958])
		max_test = 0
		i_max = -1
		j_max = -1
		for i, x in enumerate(f_x_dims):
			for j, y in enumerate(f_y_dims):
				crop = dst[y:y+INTERVAL, x:x+INTERVAL]
				if (j < 5):
					if (np.sum(crop) > PIXEL_THRESHOLD) and (np.sum(crop) > max_test):
						max_test = np.sum(crop)
						i_max = i
						j_max = j
		if (i_max==0) & (j_max==0):
			return [24] # car maker
		elif (i_max==0) & (j_max==1):
			return [25] # software dev
		elif (i_max==0) & (j_max==2):
			return [27] # insurance co
		elif (i_max==0) & (j_max==3):
			return [28] # av owner
		elif (i_max==0) & (j_max==4):
			return [58] # user at time
		else:
			return []
	elif (q == 10):
		"""
		In the future, my transportation costs will...
		"""
		f_x_dims = np.array([74])
		f_y_dims = np.array([714, 787, 864])
		max_test = 0
		i_max = -1
		j_max = -1
		for i, x in enumerate(f_x_dims):
			for j, y in enumerate(f_y_dims):
				crop = dst[y:y+INTERVAL, x:x+INTERVAL]
				if (j < 3):
					if (np.sum(crop) > PIXEL_THRESHOLD) and (np.sum(crop) > max_test):
						max_test = np.sum(crop)
						i_max = i
						j_max = j
		if (i_max==0) & (j_max==0):
			return [38] # increase
		elif (i_max==0) & (j_max==1):
			return [39] # decrease
		elif (i_max==0) & (j_max==2):
			return [40] # stay about the same
		else:
			# print(max_test)
			return []
	elif (q == 7):
		"""
		In 2040, commuting will take...
		"""
		f_x_dims = np.array([70])
		f_y_dims = np.array([652, 723, 799, 870, 941])

		max_test = 0
		i_max = -1
		j_max = -1
		for i, x in enumerate(f_x_dims):
			for j, y in enumerate(f_y_dims):
				crop = dst[y:y+INTERVAL, x:x+INTERVAL]
				if (j < 5):
					if (np.sum(crop) > PIXEL_THRESHOLD) and (np.sum(crop) > max_test):
						max_test = np.sum(crop)
						i_max = i
						j_max = j
		if (i_max==0) & (j_max==0):
			return [30] # less time
		elif (i_max==0) & (j_max==1):
			return [31] # no add time
		elif (i_max==0) & (j_max==2):
			return [32] # up to 30 more
		elif (i_max==0) & (j_max==3):
			return [33] # 30 - 60 more
		elif (i_max==0) & (j_max==4):
			return [34] # 60+ more
		else:
			# print(max_test)
			return []
	elif (q == 9):
		"""
		The future of mobility will make the world...
		"""
		f_x_dims = np.array([66])
		f_y_dims = np.array([721, 793, 869])

		max_test = 0
		i_max = -1
		j_max = -1
		for i, x in enumerate(f_x_dims):
			for j, y in enumerate(f_y_dims):
				crop = dst[y:y+INTERVAL, x:x+INTERVAL]
				if (j < 3):
					if (np.sum(crop) > PIXEL_THRESHOLD) and (np.sum(crop) > max_test):
						max_test = np.sum(crop)
						i_max = i
						j_max = j
		if (i_max==0) & (j_max==0):
			return [60] # more fair/equitable
		elif (i_max==0) & (j_max==1):
			return [61] # less fair/equitable
		elif (i_max==0) & (j_max==2):
			return [62] # no more or no less equitable
		else:
			# print(max_test)
			return []
	elif (q == 12):
		"""
		Future mobility options will have the greatest impact on...
		"""
		f_x_dims = np.array([68])
		f_y_dims = np.array([734, 805, 882, 952])

		max_test = 0
		i_max = -1
		j_max = -1
		for i, x in enumerate(f_x_dims):
			for j, y in enumerate(f_y_dims):
				crop = dst[y:y+INTERVAL, x:x+INTERVAL]
				if (j < 2) or ((j == 2) and (i==0)):
					if (np.sum(crop) > PIXEL_THRESHOLD) and (np.sum(crop) > max_test):
						max_test = np.sum(crop)
						i_max = i
						j_max = j
		if (i_max==0) & (j_max==0):
			return [41] # truck drivers
		elif (i_max==0) & (j_max==1):
			return [42] # bike delivery people
		elif (i_max==0) & (j_max==2):
			return [63] # mass transit drivers
		elif (i_max==0) & (j_max==3):
			return [43] # taxi drivers
		else:
			# print(max_test)
			return []
	else:
		return []
