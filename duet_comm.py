import requests
import json
import time

gcode_list = {"M291": 'M291 P"Waiting for permission to continue" S3', "M292": 'M292', "M23": 'M23', "M24": 'M24', "M25": 'M25', "M226": 'M226', "M104": 'M104 S240',
"M408": 'M408 S0'}

ip8 = "192.168.0.18"
ip7 = "192.168.0.17"
ip6 = "192.168.0.16"
ip5 = "192.168.0.15"

def issue_gcode(ip, com, filename=""):

	base_request = ("http://{0}:{1}/rr_gcode?gcode=" + gcode_list[com] + filename).format(ip,"")
	r = requests.get(base_request)
	return r

def request_joblist(ip):

	base_request = ("http://{0}:{1}/rr_filelist?dir=gcodes").format(ip,"")
	return requests.get(base_request).json()

def request_status(ip):

	base_request = ("http://{0}:{1}/rr_status?type=0").format(ip,"")
	return requests.get(base_request).json()

if __name__ == "__main__":

	issue_gcode(ip5, "M23", "AMBOT1_2022_10_13_16_37.gcode")
	#issue_gcode(ip6, "M23", "")
	issue_gcode(ip7, "M23", "AMBOT2_2022_10_13_16_37.gcode")
	#ssue_gcode(ip8, "M23", "AMBOT2_2022_09_27_21_24.gcode")
	issue_gcode(ip5, "M24")
	issue_gcode(ip7, "M24")
	#issue_gcode(ip8, "M24")

	layerdone_P1 = False
	layerdone_P2 = False
	interfacing_P1 = False
	interfacing_P2 = False

	statusIP6 = request_status(ip5)
	statusIP8 = request_status(ip7)

	status_P1 = request_status(ip5)["status"]
	status_P2 = request_status(ip7)["status"]

	while status_P1 != "I" and status_P2 != "I":

		if status_P1 == "S" and status_P2 == "S" and not layerdone_P1 and not layerdone_P2: #Essentially means a new layer

			issue_gcode(ip5, "M24")
			layerdone_P1 = True

		time.sleep(0.5)

		statusIP6 = request_status(ip5)
		statusIP8 = request_status(ip7)

		status_P1 = statusIP6["status"]
		status_P2 = statusIP8["status"]

		try: 

			message = statusIP6["output"]["message"]

			print(message)

			if message == "Interfacing":

				interfacing_P1 = True

			else:

				interfacing_P1 = False

		except: pass

		if not interfacing_P1 and status_P2 == "S" and layerdone_P1 and not layerdone_P2:

			issue_gcode(ip7, "M24")
			layerdone_P2 = True

		time.sleep(0.5)

		statusIP6 = request_status(ip5)
		statusIP8 = request_status(ip7)

		status_P1 = statusIP6["status"]
		status_P2 = statusIP8["status"]

		if status_P1 == "S" and status_P2 == "S" and layerdone_P1 and layerdone_P2:

			layerdone_P1 = False
			layerdone_P2 = False
			interfacing_P1 = False
			interfacing_P2 = False

		pos_P1 = statusIP6["coords"]["xyz"]
		pos_P2 = statusIP8["coords"]["xyz"]

		temp_P1 = statusIP6["temps"]["current"]
		temp_P2 = statusIP8["temps"]["current"]

		print("Printer 1: ", status_P1, pos_P1, "Temperature: ", temp_P1, "Printer 2 :", status_P2, pos_P2, "Temperature: ", temp_P2)
