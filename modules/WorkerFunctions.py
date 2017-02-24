# -*- coding: utf-8 -*-

import re
from classes.SourceQuery import SourceQuery

def is_valid_ip(ip: str):
	return re.match(r'^((\d{1,2}|1\d{2}|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d{2}|2[0-4]\d|25[0-5])$', ip);

def is_alive(ip: str, port=27015, timeout=2.0):
	lServer=SourceQuery(addr=ip, port=port, timeout=timeout).getInfo()
	return True if lServer is not False else False;