# -*- coding: utf-8 -*-

import re
import asyncio
from classes.SourceQuery import SourceQuery

def is_valid_ip(ip: str):
	return re.match(r'^((\d{1,2}|1\d{2}|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d{2}|2[0-4]\d|25[0-5])$', ip);

@asyncio.coroutine
async def is_alive(ip: str, port=27015, sleep_duration=0):
	if sleep_duration > 0:
		print("\t\t  Sleeping for {0} seconds…".format(sleep_duration))
		await asyncio.sleep(sleep_duration)
	lServer = await SourceQuery(addr=ip, port=port, timeout=2.0).getInfo()
	return True if lServer is not False else False;