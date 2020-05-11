# -*- coding:UTF8 -*-
# Author: wcwac
import re
from uuid import uuid4 as uid
import datetime
from datetime import datetime, timedelta
times = [[0, 45], [55, 100], [130, 175], [245, 290], [360, 405], 
	[415, 460], [480, 525], [535, 580], [660, 705], [715, 760]]
string = """BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//ZZU//SCHEDULE//EN"""

weeknum = 20 #int(input("请输入本学期周数：（20）") or '20') ##由于所有课程会在20周内结束 因此预处理20周日期即可
start = int(input("请输入学期开始的时间：（20200210）") or '20200210')
weeks = [None]
now = datetime(int(start/10000), int(start/100) % 100, start % 100)
for i in range(weeknum):
	temp = []
	for j in range(7):
		temp.append(now)
		now = now + timedelta(days=1)
	weeks.append(temp)


def makelist(s):
	flag = 0
	ans = []
	if s[0] == '单': s, flag = s[1:], 1
	if s[0] == '双': s, flag = s[1:], 2
	if s.find('-') == -1:
		ans.append(int(s))
		return ans
	st, ed = s.split('-')
	for i in range(int(st), int(ed)+1):
		if flag == 1 and i % 2 == 0:
			continue
		if flag == 2 and i % 2 == 1:
			continue
		ans.append(i)
	return ans


filename = input("请输入网页文件的文件名：(input.htm)") or 'input.htm'
with open(filename, "r") as f:
	fl = f.read()
	classes = re.findall(r"<td.*class.*td>", fl)
	for i in classes:
		itime = int(re.search(r'TD.*?_0', i).group()[2:-2])
		iday = int(itime/10)
		nthclass = itime % 10
		if i.find('rowspan')>0:
			ilength = int(re.search(r'rowspan=".*?"', i).group()[9:-1]) - 1
		else:
			ilength = 0
		iclass = list(filter(None, re.search(r'title=".*?"', i).group()[7:-1].split(';')))
		for j in range(0, len(iclass), 2):
			iclassname = iclass[j]
			iweeks, ilocation = iclass[j+1][1:-1].split(',')
			iweeks = iweeks.split()
			for k in iweeks:
				ilist=makelist(k)
				for t in ilist:
					string = string + "\nBEGIN:VEVENT\nDTSTAMP:20200101T000000Z\nUID:" + str(uid()) + "\nSUMMARY:" + iclassname +"\n"
					string = string + "DTSTART:" + (weeks[t][iday] + timedelta(minutes=times[nthclass][0])).strftime("%Y%m%dT%H%M%SZ\n")
					string = string + "DTEND:" + (weeks[t][iday] + timedelta(minutes=times[nthclass+ilength][1])).strftime("%Y%m%dT%H%M%SZ\n")
					string = string + "DESCRIPTION:" + iclass[j+1][1:-1] + "\nEND:VEVENT"


string = string + "\nEND:VCALENDAR"

filename = input("请输入输出文件的文件名：(result.ics)") or 'result.ics'
with open(filename,"w") as out:
	out.write(string)
