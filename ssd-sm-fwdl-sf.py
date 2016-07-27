import csv
import os
import re
import shutil
import datetime

from ConfigParser import SafeConfigParser

import _ug_lib.ugLog
import _ug_lib.ugPN

#inf = "C:\ssd_sm_fwdl_xp\UB88SMO512HCM1-HMF-UGN\Log file\20160722_SMI.csv"
#inf = "E:\ssd_sm_fwdl\\20160722_SMI.csv"
#----------------------------
#sn = "UCFAST-04GB0000000090"
#WO = "000000"
#PN = "UB31CFE4000IS1-BID"
#TESTER = "SSD-SM"
HOME = 'C:Python27_1'
#Capacity = "4"
PN_FW_VER = "00000"
#-----------------------------
class SM():
		
	def __init__(self):
		parser = SafeConfigParser()
		parser.read(HOME + "/config.ini")
		self.TESTER = parser.get('TESTER', 'id')
		self.WO = parser.get('TEST', 'wo')
		self.PN = parser.get('TEST', 'pn')	
		f = self.filecheck(self.PN)
		logpath = os.path.join(HOME, self.PN, f)
		inf = logpath + "_"
		shutil.move(logpath, inf)
		list_of_dict = self.csv_read(inf)
		self.testcasecheck(list_of_dict)		
		shutil.move(inf, inf + datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
		

	def filecheck(self, PN):
		rootdir = HOME + '\\' + PN + '\Log file'
		for subdir, dirs, files in os.walk(rootdir):
			for file in files:
				date = datetime.datetime.today().strftime("%Y%m%d")
				if re.search(date, file, re.I):
					file = 'Log file\\' + file
					return file		

	def csv_read(self, inFile):
		lst_of_dict = []
		iFile = open(inFile,"rb")
		reader = csv.reader(iFile, quoting = csv.QUOTE_NONE)
		row_idx = 0
		for row in reader:
			if row_idx == 0:
				header = row
			elif len(row) > 0:
				col_idx = 0
				dict = {} 
				for col in row:
					dict[header[col_idx]] = col
					col_idx += 1
				lst_of_dict.append(dict); 
			row_idx += 1
		iFile.close()
		return lst_of_dict
	
	#for future, take into account a failed test case, where there is no test detail information given - kevin le 07-22-2016
	def testcasecheck(self, lst_of_dict):
		log = _ug_lib.ugLog.Log()
		for i,row in enumerate(lst_of_dict):
			for x in lst_of_dict[i]:
				testrslt = lst_of_dict[i][x]
				if testrslt == 'Fail':
					TEST = str(x) 
					break
			log.startdate(lst_of_dict[i]['StartTime'])
			log.enddate(lst_of_dict[i]['EndTime'])
			slotid = lst_of_dict[i]['PortID']
			SN = lst_of_dict[i]['SerialNumber']
			if SN is "":
				SN = ""
			rslt = lst_of_dict[i]['Result']
			if rslt.startswith('Pass'):
				rslt = "Passed"
				TEST = ""
			else:
				rslt = "Failed: "
		log.add(SN, slotid, rslt, TEST)
		log.write(self.WO, self.PN + ".ini", self.TESTER, _ug_lib.ugPN.PN_Capacity(self.PN), PN_FW_VER)
				

	
			
	

		
SM()
