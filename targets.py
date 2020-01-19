#!/usr/bin/python3
# -*- coding: utf-8 -*-

import subprocess, csv, time
from color import Color


def getTargets(interface):
	try:
		command = "airodump-ng -w stations -o csv --write-interval 1 " + interface
		Color.pl("\t{P}Press {GR}CTRL+C {P}When you find your {GR}target {W}")
		time.sleep(2)
		subprocess.run(command, shell = True)
	except KeyboardInterrupt:
		target_list = []
		csv_file = find_csvfile("stations", 8)
		targets = get_targets_from_csv(csv_file)
		subprocess.run("rm " + csv_file, shell = True)
	return targets

def get_targets_from_csv(csv_filename):
	'''Returns list of Target objects parsed from CSV file.'''
	from target_model import Target
	targets = []
	with open(csv_filename, 'r') as csvopen:
		lines = []
		for line in csvopen:
			line = line.replace('\0', '')
			lines.append(line)
		csv_reader = csv.reader(lines,
			delimiter=',',
			quoting=csv.QUOTE_ALL,
			skipinitialspace=True,
			escapechar='\\')

		hit_clients = False
		for row in csv_reader:
                # Each 'row' is a list of fields for a target/client

			if len(row) == 0: continue

			if row[0].strip() == 'BSSID':
                    # This is the 'header' for the list of Targets
				hit_clients = False

			elif row[0].strip() == 'Station MAC':
                        # This is the 'header' for the list of Clients
				hit_clients = True
				continue

			if hit_clients:
				break

			try:
				target = Target(row)
				if target.essid == None:
					continue
				targets.append(target)
			except Exception:
				continue
	return targets


def find_csvfile(prefix, length):
	files = str(subprocess.check_output("ls")).replace("b'", '').split("\\n")
	for i in range(len(files)-1, -1, -1):
		pre = files[i].split(".")[0][0:length]
		extension = files[i].split(".")[-1]
		if extension == "csv" and pre == prefix:
			return files[i]
	return 0

