import cv2
import numpy as np
from CardScanner import CHECKBOX_SIZE, CHECKBOX_THRESH, Q_COLOR_WINDOW, QUESTION_HUES, SERVER_TEMPLATES, SERVER_DATA_DIR, SERVER_RAW, SERVER_URL, SERVER_PROCESSED, process
from glob import glob
import os
import json
import uuid
from datetime import datetime
import pytz
from scipy.misc import bytescale
from PIL import Image

def get_corners(img):
    t_from_corner = 25
    b_from_corner = 25
    box_size = 10
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    d = dict()
    d['height'], d['width'] = img.shape[:2]
    tl_hsv = hsv[t_from_corner:t_from_corner + box_size, t_from_corner:t_from_corner+box_size]
    tl_hsv = np.median(np.median(tl_hsv, axis=0), axis=0)
    d['tl_hsv'] = tl_hsv
    tr_hsv = hsv[t_from_corner:t_from_corner+box_size, d['width']-t_from_corner-box_size:d['width']-t_from_corner]
    tr_hsv = np.median(np.median(tr_hsv, axis=0), axis=0)
    d['tr_hsv'] = tr_hsv
    bl_hsv = hsv[d['height']-b_from_corner-box_size:d['height']-b_from_corner, b_from_corner:b_from_corner + box_size]
    bl_hsv = np.median(np.median(bl_hsv, axis=0), axis=0)
    d['bl_hsv'] = bl_hsv
    br_hsv = hsv[d['height']-b_from_corner-box_size:d['height']-b_from_corner, d['width']-b_from_corner-box_size:d['width']-b_from_corner]
    br_hsv = np.median(np.median(br_hsv, axis=0), axis=0)
    d['br_hsv'] = br_hsv
    med = np.median(np.array([tl_hsv, tr_hsv, bl_hsv, br_hsv]), axis=0)
    d['med'] = med
    return d

def get_question(hsv):
    possible_values = np.array([hsv['med'], hsv['tl_hsv'], hsv['tr_hsv'], hsv['bl_hsv'], hsv['br_hsv']])
    q = None
    for value in possible_values:
        for question in QUESTION_HUES:
            lower_bound = question[1] - Q_COLOR_WINDOW
            upper_bound = question[1] + Q_COLOR_WINDOW
            if np.all(value > lower_bound) and np.all(value < upper_bound):
                q = question
    return q

def get_answers(dst, q):
	if (q==5):
		"""
		In 2040, the average person will...
		"""
		f_x_dims = np.array([45, 308])
		f_y_dims = np.array([700, 770, 843])
		answers = []
		for i, x in enumerate(f_x_dims):
			for j, y in enumerate(f_y_dims):
				crop = dst[y:y+CHECKBOX_SIZE, x:x+CHECKBOX_SIZE]
				if (j < 2) or ((j == 2) and (i==0)):
					if (np.sum(crop) > CHECKBOX_THRESH):
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
		f_x_dims = np.array([45, 447])
		f_y_dims = np.array([619, 679, 741, 800, 860, 920])
		for i, x in enumerate(f_x_dims):
			for j, y in enumerate(f_y_dims):
				crop = dst[y:y+CHECKBOX_SIZE, x:x+CHECKBOX_SIZE]
				if (j < 5) or ((j == 5) and (i==1)):
					if (np.sum(crop) > CHECKBOX_THRESH):
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
		f_x_dims = np.array([45, 448])
		f_y_dims = np.array([621, 781, 740, 800, 858, 918])
		answers = []
		# max_test = 0
		# i_max = -1
		# j_max = -1
		for i, x in enumerate(f_x_dims):
			for j, y in enumerate(f_y_dims):
				crop = dst[y:y+CHECKBOX_SIZE, x:x+CHECKBOX_SIZE]
				if (j < 5) or ((j == 5) and (i==1)):
					if (np.sum(crop) > CHECKBOX_THRESH):
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
		f_x_dims = np.array([45, 157])
		f_y_dims = np.array([582, 654, 728, 803, 977])

		max_test = 0
		i_max = -1
		j_max = -1
		for i, x in enumerate(f_x_dims):
			for j, y in enumerate(f_y_dims):
				crop = dst[y:y+CHECKBOX_SIZE, x:x+CHECKBOX_SIZE]
				if ((j < 4) and (i==0)) or ((j == 4) and (i==1)):
					if (np.sum(crop) > CHECKBOX_THRESH) and (np.sum(crop) > max_test):
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
		f_x_dims = np.array([44, 308, 432, 523])
		f_y_dims = np.array([777, 849])

		max_test = 0
		i_max = -1
		j_max = -1
		for i, x in enumerate(f_x_dims):
			for j, y in enumerate(f_y_dims):
				crop = dst[y:y+CHECKBOX_SIZE, x:x+CHECKBOX_SIZE]
				if (i < 1) or ((i == 1) and (j == 0)) or ((i == 3) and (j == 0)) or ((i == 2) and (j == 1)):
					if (np.sum(crop) > CHECKBOX_THRESH) and (np.sum(crop) > max_test):
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
		f_x_dims = np.array([45])
		f_y_dims = np.array([700, 760, 818, 875, 933])
		max_test = 0
		i_max = -1
		j_max = -1
		for i, x in enumerate(f_x_dims):
			for j, y in enumerate(f_y_dims):
				crop = dst[y:y+CHECKBOX_SIZE, x:x+CHECKBOX_SIZE]
				if (j < 5):
					if (np.sum(crop) > CHECKBOX_THRESH) and (np.sum(crop) > max_test):
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
		f_x_dims = np.array([47])
		f_y_dims = np.array([689, 762, 839])
		max_test = 0
		i_max = -1
		j_max = -1
		for i, x in enumerate(f_x_dims):
			for j, y in enumerate(f_y_dims):
				crop = dst[y:y+CHECKBOX_SIZE, x:x+CHECKBOX_SIZE]
				if (j < 3):
					if (np.sum(crop) > CHECKBOX_THRESH) and (np.sum(crop) > max_test):
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
		f_x_dims = np.array([45])
		f_y_dims = np.array([627, 698, 774, 845, 916])

		max_test = 0
		i_max = -1
		j_max = -1
		for i, x in enumerate(f_x_dims):
			for j, y in enumerate(f_y_dims):
				crop = dst[y:y+CHECKBOX_SIZE, x:x+CHECKBOX_SIZE]
				if (j < 5):
					if (np.sum(crop) > CHECKBOX_THRESH) and (np.sum(crop) > max_test):
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
		f_x_dims = np.array([44])
		f_y_dims = np.array([696, 768, 844])

		max_test = 0
		i_max = -1
		j_max = -1
		for i, x in enumerate(f_x_dims):
			for j, y in enumerate(f_y_dims):
				crop = dst[y:y+CHECKBOX_SIZE, x:x+CHECKBOX_SIZE]
				if (j < 3):
					if (np.sum(crop) > CHECKBOX_THRESH) and (np.sum(crop) > max_test):
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
		f_x_dims = np.array([44])
		f_y_dims = np.array([711, 780, 857, 927])

		max_test = 0
		i_max = -1
		j_max = -1
		for i, x in enumerate(f_x_dims):
			for j, y in enumerate(f_y_dims):
				crop = dst[y:y+CHECKBOX_SIZE, x:x+CHECKBOX_SIZE]
				if (j < 2) or ((j == 2) and (i==0)):
					if (np.sum(crop) > CHECKBOX_THRESH) and (np.sum(crop) > max_test):
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

def get_file_list(dir):
    file_list = glob(dir)
    file_list = sorted(file_list, key=str.lower)
    return file_list

def read_from_disk(list):
    # print(card_no)
    with open(SERVER_DATA_DIR+'read.json', 'w') as f:
        for i in range(0, len(list), 2):
            # print(list[i])
            front_idx = i
            back_idx = i + 1
            tz = pytz.timezone('America/New_York')
            timestamp = datetime.fromtimestamp(os.path.getmtime(list[front_idx]), tz).isoformat()
            front = cv2.imread(list[front_idx])
            back = cv2.imread(list[back_idx])
            corners = get_corners(front)
            diff = corners['tl_hsv'][1] - corners['bl_hsv'][1]
            if abs(diff) > 20:
                print("front forward")
                front, back = back, front
                front_idx, back_idx = back_idx, front_idx
                # print("wobble")
            else:
                print("back forward")
            corners = get_corners(back)
            diff = corners['tl_hsv'][1] - corners['bl_hsv'][1]
            # rotate if necessary
            if diff < -20:
                print('upside down')
                front = process.rotate(front)
                back = process.rotate(back)
            # blur = cv2.blur(front,(3, 3))
            corners = get_corners(front)
            # print(corners)
            question = get_question(corners)
            print(question)
            # print(question)
            front_file = os.path.basename(list[front_idx]).replace('-a.png','-front.jpg').replace('-b.png','-front.jpg')
            back_file = os.path.basename(list[back_idx]).replace('-a.png','-back.jpg').replace('-b.png','-back.jpg')
            if question is not None:
                ref_front = cv2.imread(SERVER_TEMPLATES+'{:02}_front.jpg'.format(question[0]))
                ref_h, ref_w = ref_front.shape[0], ref_front.shape[1]
                print(front_file, back_file)
                ref_front = ref_front[0+25:ref_h-25, 0+25:ref_w-25]
                aligned_front = process.align_images_orb(front, ref_front)
                cv2.imwrite(SERVER_PROCESSED+front_file, aligned_front, [int(cv2.IMWRITE_JPEG_QUALITY), 60])
                cv2.imwrite(SERVER_PROCESSED+back_file, back, [int(cv2.IMWRITE_JPEG_QUALITY), 60])
                masked = process.mask_front(aligned_front, 2,  question[1])
                answers = get_answers(masked, question[0])
                if len(answers) > 0:
                    # print(answers)
                    print(str(timestamp))
                    f.write(json.dumps({
                        'id': str(uuid.uuid4()),
                        'q_id': question[0],
                        'a_id': answers,
                        'gender': '',
                        'age': '',
                        'zip_code': '',
                        'home': '',
                        'free_q_id': 2,
                        'free_resp': '',
                        'survey_id': 6,
                        'front': SERVER_URL + front_file,
                        'back': SERVER_URL + back_file,
                        'timestamp': timestamp
                    }, default=str) + "\n")
            else:
                cv2.imwrite(SERVER_PROCESSED+front_file, front, [int(cv2.IMWRITE_JPEG_QUALITY), 60])
                cv2.imwrite(SERVER_PROCESSED+back_file, back, [int(cv2.IMWRITE_JPEG_QUALITY), 60])
