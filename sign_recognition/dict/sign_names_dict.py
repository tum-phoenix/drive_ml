# -*- coding: utf-8 -*-
# mapping: GTSRB id (as int) to sign description (string)
import pickle

# outdated: various GTSRB signs
sign_name_GTSRB_full_dict = {
	0: 'speed limit 20 (prohibitory)',
	1: 'speed limit 30 (prohibitory)',
	2: 'speed limit 50 (prohibitory)',
	3: 'speed limit 60 (prohibitory)',
	4: 'speed limit 70 (prohibitory)',
	5: 'speed limit 80 (prohibitory)',
	6: 'restriction ends 80 (other)',
	7: 'speed limit 100 (prohibitory)',
	8: 'speed limit 120 (prohibitory)',
	9: 'no overtaking (prohibitory)',
	10: 'no overtaking (trucks) (prohibitory)',
	11: 'priority at next intersection (danger)',
	12: 'priority road (other)',
	13: 'give way (other)',
	14: 'stop (other)',
	15: 'no traffic both ways (prohibitory)',
	16: 'no trucks (prohibitory)',
	17: 'no entry (other)',
	18: 'danger (danger)',
	19: 'bend left (danger)',
	20: 'bend right (danger)',
	21: 'bend (danger)',
	22: 'uneven road (danger)',
	23: 'slippery road (danger)',
	24: 'road narrows (danger)',
	25: 'construction (danger)',
	26: 'traffic signal (danger)',
	27: 'pedestrian crossing (danger)',
	28: 'school crossing (danger)',
	29: 'cycles crossing (danger)',
	30: 'snow (danger)',
	31: 'animals (danger)',
	32: 'restriction ends (other)',
	33: 'go right (mandatory)',
	34: 'go left (mandatory)',
	35: 'go straight (mandatory)',
	36: 'go right or straight (mandatory)',
	37: 'go left or straight (mandatory)',
	38: 'keep right (mandatory)',
	39: 'keep left (mandatory)',
	40: 'roundabout (mandatory)',
	41: 'restriction ends (overtaking) (other)',
	42: 'restriction ends (overtaking (trucks)) (other)'
}

gtsrb_to_carolo = {
	9: 9,
	12: 12,
	13: 13,
	14: 14,
	33: 33,
	34: 34,
	38: 38,
	41: 41
}

LISA_to_carolo = {
	'stop': 14
}

# using the short number naming used in the _cleaned.txt files
BTSD_to_carolo = {
	31: 13,
	36: 100,
	41: 12,
	61: 9,
	62: 41,
	16: 107,
	25: 108,
# parkschild (87) is etwas breiter
	87: 109,
# Fahrzeug sieht leicht anders auf dem Kraftfahrstrassenschild aus (183, 110)
	183: 110,
	110: 111,
	151: 102,
	77: 34
}

STS_to_carolo = {
	'STOP': 14,
	'PEDESTRIAN_CROSSING': 115,
	'PRIORITY_ROAD': 12,
	'PASS_RIGHT_SIDE': 38
}

# all carolo cup signs currently in use
sign_name_carolo_dict = {
	0: '20 Zone Anfang (speed limit 20 start)',
	1: '30 Zone Anfang (speed limit 30 start)',
	2: '50 Zone Anfang (speed limit 50 start)',
	3: '60 Zone Anfang (speed limit 60 start)',
	4: '70 Zone Anfang (speed limit 70 start)',
	5: '80 Zone Anfang (speed limit 80 start)',
	9: 'Absolutes Ueberholverbot Anfang (no passing zone start)',
	12: 'Vorfahrtstrasse (priority on next intersections)',
	13: 'Vorfahrt Gewaehren (give way to incoming)',
	14: 'Stop Zeichen (stop for at least 3 sec)',
	33: 'Vorgeschriebene Fahrtrichtung Rechts (turn right on intersection)',
	34: 'Vorgeschriebene Fahrtrichtung Links (turn left on intersection)',
	38: 'Vorgeschriebene Vorbeifahrt rechts (pass by on right)',
	41: 'Absolutes Ueberholverbot Ende (no passing zone end)',
	43: 'Nullklasse (zero class)',
	100: 'Gegenverkehr Vorrang gewaehren (Barred area, let oncoming pass)',
	101: 'Zone Ende (end of speed limit)',
	102: 'Fussgaengerueberweg (crosswalk)',
	103: 'Richtungstafel Kurve links (sharp turn left)',
	104: 'Richtungstafel Kurve links (even sharper turn left)',
	105: 'Richtungstafel Kurve rechts (sharp turn right)',
	106: 'Richtungstafel Kurve rechts (even sharper turn right)',
	107: 'Gefaelle 10% (downhill 10%)',
	108: 'Steigung 10% (uphill 10%)',
	109: 'Parken Bereich (parking zone)',
	110: 'Kraftfahrtstrasse Anfang (expressway begin)',
	111: 'Kraftfahrtstrasse Ende (expressway end)',
	112: '10 Zone Anfang (speed limit 10 start)',
	113: '40 Zone Anfang (speed limit 40 start)',
	114: '90 Zone Anfang (speed limit 90 start)',
	115: 'Pedestrian'
}

if __name__ == '__main__':
	with open('sign_names_dict.pkl', 'wb') as f:
		pickle.dump(sign_name_carolo_dict, f)

