#!/usr/bin/python3
# -*- coding: utf-8 -*-

import subprocess, csv, time
from color import Color


def getClients(BSSID, channel, interface):
	try:
		command3 = "airodump-ng --write-interval 1 -w clients -o csv -c " + channel + " --bssid " + BSSID + " " + interface	
		Color.pl("\t{P}Press {GR}CTRL+C {P}when you feel like you found enough {GR}connected devices {W}")
		time.sleep(2.5)
		subprocess.run(command3, shell = True)
	except KeyboardInterrupt:
		client_list = []
		csv_file = find_csvfile("clients", 7)
		clients = get_clients_from_csv(csv_file)
		subprocess.run("rm " + csv_file, shell = True)	
	return clients

def get_clients_from_csv(csv_filename):
	'''Returns list of Target objects parsed from CSV file.'''
	from client_model import Client
	clients = []
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
				continue

			elif row[0].strip() == 'Station MAC':
                        # This is the 'header' for the list of Clients
				hit_clients = True
				continue

			if hit_clients:
                        # The current row corresponds to a 'Client' (computer)
				try:
					client = Client(row)
					clients.append(client)
				except (IndexError, ValueError) as e:
                        # Skip if we can't parse the client row
					continue

				if 'not associated' in client.bssid:
                        # Ignore unassociated clients
					continue
	return clients

def find_csvfile(prefix, length):
	files = str(subprocess.check_output("ls")).replace("b'", '').split("\\n")
	for i in range(len(files)-1, -1, -1):
		pre = files[i].split(".")[0][0:length]
		extension = files[i].split(".")[-1]
		if extension == "csv" and pre == prefix:
			return files[i]
	return 0


