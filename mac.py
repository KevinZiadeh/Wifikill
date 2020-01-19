#!/usr/bin/python
import requests

def get_info(mac_address):
	return requests.get("https://macvendors.co/api/vendorname/"+mac_address+"/").text
