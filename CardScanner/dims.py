import numpy as np

age_yDims = np.array([382, 432, 482])
gdr_yDims = np.array([563])
# q3_yDims = np.array([780, 820, 870])
hom_yDims = np.array([805])
x_dims = np.array([215, 433, 615])

f_x_dims = np.array([50, 305])
f_y_dims = np.array([530, 590, 650])

black =  [0, 120]
white = [190, 255]

white_hsv = [(0,0,180),(180, 15, 255)]
black_hsv = [(0,0,0),(180, 255, 100)]
# green_h = 131 / 360 * 180
# green_s = 55 / 100 * 255
# green_v = 64 / 100 * 255
# green = [(green_h-20,green_s-20,green_v-20), (green_h+20, green_s+20, green_v+20)]

# blue_h = 220 / 360 * 180
# blue_s = 96 / 100 * 255
# blue_v = 44 / 100 * 255
# blue = [(blue_h-20, blue_s-20,blue_v-20), (blue_h+20, blue_s+20, blue_v+20)]

INTERVAL = 25
IMG_PATH = ''
PIXEL_THRESHOLD = 12500
FRONT_BLUR = 3
BACK_BLUR = 1

def get_answers(dst, q):
	if (q==5):
		"""
		In 2040, the average person will...
		"""
		f_x_dims = np.array([40, 303])
		f_y_dims = np.array([694, 766, 841])
		max_test = 0
		i_max = -1
		j_max = -1
		for i, x in enumerate(f_x_dims):
			for j, y in enumerate(f_y_dims):
				crop = dst[y:y+INTERVAL, x:x+INTERVAL]
				if (j < 2) or ((j == 2) and (i==0)):
					if (np.sum(crop) > PIXEL_THRESHOLD):
						max_test = np.sum(crop)
						i_max = i
						j_max = j
		if (i_max==0) & (j_max==0):
			return 10 # own a car
		elif (i_max==0) & (j_max==1):
			return 11 # lease a car
		elif (i_max==0) & (j_max==2):
			return 14 # have no car
		elif (i_max==1) & (j_max==0):
			return 45 # own AV
		elif (i_max==1) & (j_max==1):
			return 46 # lease AV
		else:
			# print(max_test)
			return None
	elif (q == 4):
		"""
		My preferred transport mode(s) in 2040 will be. . .
		"""
		f_x_dims = np.array([40, 442])
		f_y_dims = np.array([615, 675, 735, 795, 855, 914])

		max_test = 0
		i_max = -1
		j_max = -1
		for i, x in enumerate(f_x_dims):
			for j, y in enumerate(f_y_dims):
				crop = dst[y:y+INTERVAL, x:x+INTERVAL]
				if (j < 5) or ((j == 5) and (i==1)):
					if (np.sum(crop) > PIXEL_THRESHOLD):
						max_test = np.sum(crop)
						i_max = i
						j_max = j
			if (i_max==0) & (j_max==0):
				return 15 #av bus
			elif (i_max==0) & (j_max==1):
				return 48 # bus
			elif (i_max==0) & (j_max==2):
				return 16 #av car
			elif (i_max==0) & (j_max==3):
				return 47 # car
			elif (i_max==0) & (j_max==4):
				return 49 # flying car
			elif (i_max==1) & (j_max==0):
				return 21 # hyperloop
			elif (i_max==1) & (j_max==1):
				return 18 # subways
			elif (i_max==1) & (j_max==2):
				return 20 # walking
			elif (i_max==1) & (j_max==3):
				return 19 # bikes
			elif (i_max==1) & (j_max==4):
				return 17 # scooters
			elif (i_max==1) & (j_max==5):
				return 23 # O T H E R
			else:
				# print(max_test)
				return None
	elif (q == 8):
		"""
		In 2040, everyone will have access to...
		"""
		f_x_dims = np.array([40, 442])
		f_y_dims = np.array([615, 675, 735, 795, 855, 914])

		max_test = 0
		i_max = -1
		j_max = -1
		for i, x in enumerate(f_x_dims):
			for j, y in enumerate(f_y_dims):
				crop = dst[y:y+INTERVAL, x:x+INTERVAL]
				if (j < 5) or ((j == 5) and (i==1)):
					if (np.sum(crop) > PIXEL_THRESHOLD):
						max_test = np.sum(crop)
						i_max = i
						j_max = j
			if (i_max==0) & (j_max==0):
				return 15 #av bus
			elif (i_max==0) & (j_max==1):
				return 48 # bus
			elif (i_max==0) & (j_max==2):
				return 16 #av car
			elif (i_max==0) & (j_max==3):
				return 47 # car
			elif (i_max==0) & (j_max==4):
				return 49 # flying car
			elif (i_max==1) & (j_max==0):
				return 21 # hyperloop
			elif (i_max==1) & (j_max==1):
				return 18 # subways
			elif (i_max==1) & (j_max==2):
				return 20 # walking
			elif (i_max==1) & (j_max==3):
				return 19 # bikes
			elif (i_max==1) & (j_max==4):
				return 17 # scooters
			elif (i_max==1) & (j_max==5):
				return 23 # O T H E R
			else:
				# print(max_test)
				return None
	elif (q == 13):
		"""
		In 2040...
		"""
		f_x_dims = np.array([40, 153])
		f_y_dims = np.array([577, 649, 724, 798, 871])

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
			return 50 # parking spots into parks
		elif (i_max==0) & (j_max==1):
			return 51 # streets are for robots
		elif (i_max==0) & (j_max==2):
			return 52 # garages house grandmas
		elif (i_max==0) & (j_max==3):
			return 53 # parking lots urban farms
		elif (i_max==1) & (j_max==4):
			return 23 # O T H E R
		else:
			# print(max_test)
			return None
	elif (q == 14):
		"""
		Travel in the future will be more dangerous for...
		"""
		f_x_dims = np.array([40, 303, 423, 517])
		f_y_dims = np.array([769, 841])

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
			return 54 # pedestrians
		elif (i_max==0) & (j_max==1):
			return 57 # stray cats
		elif (i_max==1) & (j_max==0):
			return 55 # drivers
		elif (i_max==3) & (j_max==0):
			return 56 # bikers
		elif (i_max==2) & (j_max==1):
			return 23 # O T H E R
		else:
			# print(max_test)
			return None
	elif (q == 6):
		"""
		Responsibility for autonomous vehicle accidents belongs to...
		"""
		f_x_dims = np.array([40])
		f_y_dims = np.array([695, 753, 813, 870, 930])

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
			return 24 # car maker
		elif (i_max==0) & (j_max==1):
			return 25 # software dev
		elif (i_max==0) & (j_max==2):
			return 27 # insurance co
		elif (i_max==0) & (j_max==3):
			return 28 # av owner
		elif (i_max==0) & (j_max==4):
			return 58 # user at time
		else:
			# print(max_test)
			return None
	elif (q == 10):
		"""
		In the future, my transportation costs will...
		"""
		f_x_dims = np.array([40])
		f_y_dims = np.array([685, 756, 832])

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
			return 38 # increase
		elif (i_max==0) & (j_max==1):
			return 39 # decrease
		elif (i_max==0) & (j_max==2):
			return 40 # stay about the same
		else:
			# print(max_test)
			return None
	elif (q == 7):
		"""
		In 2040, commuting will take...
		"""
		f_x_dims = np.array([40])
		f_y_dims = np.array([621, 694, 768, 839, 911])

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
			return 30 # less time
		elif (i_max==0) & (j_max==1):
			return 31 # no add time
		elif (i_max==0) & (j_max==2):
			return 32 # up to 30 more
		elif (i_max==0) & (j_max==3):
			return 33 # 30 - 60 more
		elif (i_max==0) & (j_max==4):
			return 34 # 60+ more
		else:
			# print(max_test)
			return None
	elif (q == 9):
		"""
		The future of mobility will make the world...
		"""
		f_x_dims = np.array([40])
		f_y_dims = np.array([694, 766, 841])

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
			return 60 # more fair/equitable
		elif (i_max==0) & (j_max==1):
			return 61 # less fair/equitable
		elif (i_max==0) & (j_max==2):
			return 62 # no more or no less equitable
		else:
			# print(max_test)
			return None
	elif (q == 12):
		"""
		Future mobility options will have the greatest impact on...
		"""
		f_x_dims = np.array([40])
		f_y_dims = np.array([694, 766, 841, 912])

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
			return 41 # truck drivers
		elif (i_max==0) & (j_max==1):
			return 42 # bike delivery people
		elif (i_max==0) & (j_max==2):
			return 63 # mass transit drivers
		elif (i_max==0) & (j_max==3):
			return 43 # taxi drivers
		else:
			# print(max_test)
			return None
	else:
		return None
