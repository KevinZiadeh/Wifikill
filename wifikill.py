#!/usr/bin/python3
# -*- coding: utf-8 -*-

import subprocess, re, time, csv, os, copy
import clients , targets, mac
from color import Color

def initialization():

	#check for root privilege
	if os.getuid() != 0:
		Color.pl('{!} {R}Error: {O} Wifikill {R} must run as {O} root {W}')
		Color.pl('{!} {R}R-run with {O} sudo {W}')		

	#check if there is a network card with monito mode enabled
	command1 = "iwconfig"
	interfacesOutput = str(subprocess.check_output(command1, shell = True, stderr = subprocess.STDOUT))
	interface_list = re.findall('Mode:Monitor', interfacesOutput)

	if len(interface_list) == 0:
		Color.pl("{!}  {R}Please make sure you have a {O}wireless card {R}in {O}monitor mode, {R}then try again {W}")
		return
	else:
		subprocess.run("iwconfig")
		time.sleep(0.5)
		Color.pl("{+}  {G}Enter {GR}name {G}of the {GR}interface {G} to use {D}[should be in monitor mode]{W} {G}: {W}")			
		interface = input().strip()
	
	#check name of interface is correct
	try:	
		subprocess.check_output("ifconfig "+ interface, shell = True, stderr = subprocess.STDOUT)
	except:	
		Color.pl("{!}  {R}Error: Name of {O}interface {R}is incorrect")
		Color.pl("{!}  {R}Re-run the program")
		return	

	#check if aircrack-ng is installed
	try:	
		Color.pl("\n{?}  {C}Checking for aicrack-ng")
		time.sleep(0.5)
		subprocess.check_output("dpkg -s aircrack-ng", shell = True, stderr = subprocess.STDOUT)
	except:	
		Color.pl("{!}  {R}Error: Make sure {O}aircrack-ng {R}is installed properly")
	
	Color.pl("{+}  {G}Aicrack-ng is installed properly {W} \n")
	
	#get network to attack
	time.sleep(1)
	target_list = targets.getTargets(interface)
	select_target_text = ''
	for i in range(len(target_list)):
		select_target_text += Color.s(' {C}\t' + str(i+1) + ": {G}" + target_list[i].essid + '\n {W}')
	print(select_target_text)
	Color.pl("\n{?}  {C}Select target: {W}")
	target_index = int(input())-1
	target = target_list[target_index]

	#get list of clients connected
	client_list = clients.getClients(target.bssid, target.channel, interface)

	#get list of clients to remove
	selected_list = select(target.bssid, target.channel, interface, client_list)
	for i in range(len(selected_list)):
		print(selected_list[i].station)
	Color.pl("{B} Starting deAuth request: {W}")
	time.sleep(1)
	death(target.bssid, target.channel, interface, selected_list)


def selectRemoveConnect(BSSID, channel, interface, client_list):
	select_client_text = ''
	Color.pl("{?}  {C}Enter (1) for {GR}more information {C}on clients {D}[takes more time]{W} {C}or (2) for {GR}less infomation {D}[takes less time]{W}{C}: {W}")
	select = int(input())
	if select == 1:
		for i in range(len(client_list)):
			select_client_text += Color.s( "{C}\t" + str(i+1) + ": {G}" + client_list[i].station + "{GR}(" + mac.get_info(client_list[i].station) + ")\n {W}")
	elif select == 2:
		for i in range(len(client_list)):
			select_client_text += Color.s( "{C}\t" + str(i+1) + ": {G}" + client_list[i].station + "\n {W}")
	else:
		Color.pl("{!}  {R}Error: Invalid entry")
	print(select_client_text)
	Color.pl("{C} Select devices to remove {GR}seperated by spaces: {W}")
	list_index = input().split(' ')
	list_index = [int(index)-1 for index in list_index]
	selected_list = []	
	for index in list_index:
		selected_list.append(client_list[index])
	print(selected_list)
	return selected_list

def selectKeepConnected(BSSID, channel, interface, client_list):
	select_client_text = ''
	Color.pl("{?}  {C}Enter (1) for {GR}more information {C}on clients {D}[takes more time]{W} {C}or (2) for {GR}less infomation {D}[takes less time]{W}{C}: {W}")
	select = int(input())
	if select == 1:
		for i in range(len(client_list)):
			select_client_text += Color.s( "{C}\t" + str(i+1) + ": {G}" + client_list[i].station + "{GR}(" + mac.get_info(client_list[i].station) + ")\n {W}")
	elif select == 2:
		for i in range(len(client_list)):
			select_client_text += Color.s( "{C}\t" + str(i+1) + ": {G}" + client_list[i].station + "\n {W}")
	else:
		Color.pl("{!}  {R}Error: Invalid entry")
	print(select_client_text)
	Color.pl("{C} Select devices to remove {GR}seperated by spaces: {W}")
	list_index = input().split(' ')	
	list_index = [int(index)-1 for index in list_index]
	selected_list = copy.deepcopy(client_list)
	for index in list_index:
		selected_list.remove(client_list[index])
	return selected_list

def select(BSSID, channel, interface, client_list):
	Color.pl("{?}  {C}Select who {GR}to remove(1) {C}or select who {GR}to keep connected(2) {C}: {W}")
	selection = int(input())
	if selection == 1:
		return selectRemoveConnect(BSSID, channel, interface, client_list)
	elif selection == 2:
		return selectKeepConnected(BSSID, channel, interface, client_list)
	else:
		Color.pl("{!}  {R}Error: Invalid entry")


def deauth(BSSID, channel, interface, selected_list):
	return


initialization()
