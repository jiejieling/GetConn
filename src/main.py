#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
from PyQt4 import QtGui, QtCore
import paramiko, threading, re, ConfigParser

try:
	_fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
	def _fromUtf8(s):
		return s

try:
	_encoding = QtGui.QApplication.UnicodeUTF8
	def _translate(context, text, disambig):
		return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
	def _translate(context, text, disambig):
		return QtGui.QApplication.translate(context, text, disambig)

CONFIG_FILE = 'config.ini'
CONFIG = {}

class Ui_commandCtr(object):
	def setupUi(self, commandCtr):
		'''Main Windows'''
		self.commandCtr = commandCtr
		commandCtr.setObjectName(_fromUtf8("commandCtr"))
		commandCtr.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)
		commandCtr.resize(824, 750)
		commandCtr.setFixedSize(commandCtr.width(), commandCtr.height())

		'''main widget'''
		self.centralWdt = QtGui.QWidget(commandCtr)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.centralWdt.sizePolicy().hasHeightForWidth())
		self.centralWdt.setSizePolicy(sizePolicy)
		self.centralWdt.setObjectName(_fromUtf8("centralWdt"))
		commandCtr.setCentralWidget(self.centralWdt)
		
		self.gridLayout = QtGui.QGridLayout(self.centralWdt)
		self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
		
		'''cmd widget'''
		self.widget = QtGui.QWidget(self.centralWdt)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
		self.widget.setSizePolicy(sizePolicy)
		self.widget.setMinimumSize(QtCore.QSize(130, 40))
		self.widget.setObjectName(_fromUtf8("widget"))
		self.gridLayout.addWidget(self.widget, 0, 0, 1, 6)
		
		'''cmd excute button'''
		self.cmdex = QtGui.QPushButton(self.widget)
		self.cmdex.setGeometry(QtCore.QRect(0, 0, 71, 31))
		self.cmdex.setObjectName(_fromUtf8("cmdex"))
		self.cmdex.clicked.connect(self.on_cmdex_clicked)

		'''cmd line text'''
		self.cmdline = QtGui.QLineEdit(self.widget)
		self.cmdline.setGeometry(QtCore.QRect(80, 5, 711, 20))
		self.cmdline.setObjectName(_fromUtf8("cmdline"))

		'''Main table widget'''
		self.tblwdtApp = QtGui.QTableWidget(self.centralWdt)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.tblwdtApp.sizePolicy().hasHeightForWidth())
		self.tblwdtApp.setSizePolicy(sizePolicy)
		self.tblwdtApp.setMinimumSize(QtCore.QSize(800, 0))
		self.tblwdtApp.setObjectName(_fromUtf8("tblwdtApp"))
		self.tblwdtApp.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
		self.tblwdtApp.setColumnCount(4)
		self.tblwdtApp.horizontalHeader().setMovable(True)
		self.tblwdtApp.setAlternatingRowColors(True)
		self.tblwdtApp.setHorizontalHeaderLabels(['', "Host", "IP", "Result"])
		#self.tblwdtApp.horizontalHeader().setResizeMode(QtGui.QHeaderView.Fixed)
		self.tblwdtApp.horizontalHeader().resizeSection(0, 30)  #选择框
		self.tblwdtApp.horizontalHeader().resizeSection(1, 100) #Host列
		self.tblwdtApp.horizontalHeader().resizeSection(2, 120) #IP列
		self.tblwdtApp.horizontalHeader().resizeSection(3, 533) #结果列
		self.tblwdtApp.horizontalHeader().sectionClicked.connect(self.HorSectionClicked)
		self.tblwdtApp.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
		self.tblwdtApp.itemClicked.connect(self.on_itemClicked)
		self.tblwdtApp.setRowCount(0)
		self.gridLayout.addWidget(self.tblwdtApp, 1, 0, 1, 6)

		'''result  text'''	
		self.rettxt = QtGui.QTextEdit(self.centralWdt)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
		self.rettxt.setSizePolicy(sizePolicy)
		self.rettxt.setMinimumSize(QtCore.QSize(800, 0))
		self.rettxt.setObjectName(_fromUtf8("widget"))
		self.gridLayout.addWidget(self.rettxt, 2, 0, 1, 4)
		
		'''All select button'''
		self.pbtnAllSelect = QtGui.QPushButton(self.centralWdt)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.pbtnAllSelect.sizePolicy().hasHeightForWidth())
		self.pbtnAllSelect.setSizePolicy(sizePolicy)
		self.pbtnAllSelect.setObjectName(_fromUtf8("pbtnAllSelect"))
		self.pbtnAllSelect.clicked.connect(self.on_pbtnAllSelect_clicked)
		self.gridLayout.addWidget(self.pbtnAllSelect, 3, 0, 1, 1)
		
		'''Inverse button'''
		self.pbtnReturn = QtGui.QPushButton(self.centralWdt)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.pbtnReturn.sizePolicy().hasHeightForWidth())
		self.pbtnReturn.setSizePolicy(sizePolicy)
		self.pbtnReturn.setObjectName(_fromUtf8("pbtnReturn"))
		self.pbtnReturn.clicked.connect(self.on_pbtnReturn_clicked)
		self.gridLayout.addWidget(self.pbtnReturn, 3, 1, 1, 1)

		'''Clear button'''
		self.pbtnClear = QtGui.QPushButton(self.centralWdt)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.pbtnClear.sizePolicy().hasHeightForWidth())
		self.pbtnClear.setSizePolicy(sizePolicy)
		self.pbtnClear.setObjectName(_fromUtf8("pbtnClear"))
		self.pbtnClear.clicked.connect(self.on_pbtnClear_clicked)
		self.gridLayout.addWidget(self.pbtnClear, 3, 2, 1, 1)
		
		'''status bar'''
		self.statusBar = QtGui.QStatusBar(commandCtr)
		self.statusBar.setObjectName(_fromUtf8("statusBar"))
		commandCtr.setStatusBar(self.statusBar)
		
		self.retranslateUi(commandCtr)
		QtCore.QMetaObject.connectSlotsByName(commandCtr)
		
		'''init data'''
		iplist = self.init_data()
		if iplist:
			if len(iplist) > 30:
				self.tblwdtApp.horizontalHeader().resizeSection(3, 512) #结果列
			self.tblwdtApp.setRowCount(len(iplist))
			for idx, ip in enumerate(iplist):
				self.tblwdtApp.setRowHeight(idx, 20)
				newItem = QtGui.QTableWidgetItem()
				newItem.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable)
				newItem.setCheckState(QtCore.Qt.Unchecked)
				self.tblwdtApp.setItem(idx, 0, newItem)
				
				item_host = QtGui.QTableWidgetItem(ip[1])
				item_ip = QtGui.QTableWidgetItem(ip[0])
				self.tblwdtApp.setItem(idx, 1, item_host)
				self.tblwdtApp.setItem(idx, 2, item_ip)
		else:
			sys.exit(1)
			
	def retranslateUi(self, commandCtr):
		commandCtr.setWindowTitle(_translate("commandCtr", "GetConn", None))
		self.pbtnAllSelect.setText(_translate("commandCtr", "All", None))
		self.pbtnReturn.setText(_translate("commandCtr", "Inverse", None))
		self.pbtnClear.setText(_translate("commandCtr", "Clear", None))
		self.cmdex.setText(_translate("commandCtr", "Exec", None))


	def init_data(self):
		'''init data from config file'''
		global CONFIG
		cp = ConfigParser.ConfigParser()
		try:
			cp.read(CONFIG_FILE)
		except Exception, e:
			self.errorBox("Read configure file %s error, err:%s"%(CONFIG, e))
			return False
		
		for sec in cp.sections():
			if sec == 'global':
				CONFIG['IP_FILE'] = cp.get(sec, 'IP_FILE') if cp.get(sec, 'IP_FILE') else 'iplist.ini'
				CONFIG['PROXY_IP'] = cp.get(sec, 'PROXY_IP') if cp.get(sec, 'PROXY_IP') else ''
				try:
					CONFIG['PROXY_PORT'] = int(cp.get(sec, 'PROXY_PORT')) if cp.get(sec, 'PROXY_PORT') else 22
				except:
					self.errorBox("PROXY_PORT must be a number")
					return False
				
				CONFIG['PROXY_USER'] = cp.get(sec, 'PROXY_USER') if cp.get(sec, 'PROXY_USER') else 'root'
				CONFIG['PROXY_PASS'] = cp.get(sec, 'PROXY_PASS') if cp.get(sec, 'PROXY_PASS') else ''
				CONFIG['PROXY_KEY'] = cp.get(sec, 'PROXY_PRIVATE_KEY') if cp.get(sec, 'PROXY_PRIVATE_KEY') else '~/.ssh/id_rsa'
				CONFIG['PROXY_KEY'] = os.path.expanduser(CONFIG['PROXY_KEY'])
		
		if not CONFIG.get('IP_FILE', '') or not CONFIG.get('PROXY_IP', '') or not CONFIG.get('PROXY_PORT', '') or not CONFIG.get('PROXY_USER', ''):
			self.errorBox("Configure invalid. Please check configure file.")
			return False
	
		if not CONFIG.get('PROXY_PASS', '') and not CONFIG.get('PROXY_KEY', ''):
			self.errorBox("PROXY_PASS and PROXY_PRIVATE_KEY must configure at lease one of them.")
			return False
					
		try:
			fp = open(CONFIG['IP_FILE'])
		except Exception, e:
			self.errorBox("Open IP config file %s error:%s"%(CONFIG['IP_FILE'], e))
			return False
	
		iplist = []
		for line in fp.readlines():
			if not line.strip() or line.strip()[0] == '#':
				continue
			ip = line.strip().split()
			if len(ip) == 2:
				iplist.append(ip)
		
		fp.close()
		
		return iplist
		
	@QtCore.pyqtSlot()
	def HorSectionClicked(self, i = 1):
		self.tblwdtApp.sortByColumn(i, QtCore.Qt.SortOrder())

	@QtCore.pyqtSlot()
	def on_pbtnAllSelect_clicked(self):
		"""
		All Select.
		"""
		row_count = self.tblwdtApp.rowCount()
		for i in range(row_count):
			self.tblwdtApp.item(i, 0).setCheckState(2)
			
	@QtCore.pyqtSlot()
	def on_pbtnReturn_clicked(self):
		"""
		Return Select.
		"""
		row_count = self.tblwdtApp.rowCount()
		for i in range(row_count):
			if self.tblwdtApp.item(i, 0).checkState() == 2:
				
				self.tblwdtApp.item(i, 0).setCheckState(0)
			else:
				self.tblwdtApp.item(i, 0).setCheckState(2)

	@QtCore.pyqtSlot()
	def on_pbtnClear_clicked(self):
		"""
		All Select.
		"""
		row_count = self.tblwdtApp.rowCount()
		for i in range(row_count):
			self.tblwdtApp.item(i, 0).setCheckState(0)
		
	@QtCore.pyqtSlot()
	def on_cmdex_clicked(self):
		'''
		cmd button clicked
		'''
		
		selectedSvrs = []
		row_count = self.tblwdtApp.rowCount()
		for i in range(row_count):
			if self.tblwdtApp.item(i, 0):
				if self.tblwdtApp.item(i, 0).checkState() == 2:
					ip = str(self.tblwdtApp.item(i, 2).text())
					selectedSvrs.append({'ip':ip, 'row':i})
		
		if not selectedSvrs:
			self.warnBox("No server selected")
			return False
		
		cmd = unicode(self.cmdline.text()).strip()
		if not cmd:
			self.warnBox("Invalid cmd")
			return False
		
		self.runCmd(selectedSvrs, re.escape(cmd))
		
	@QtCore.pyqtSlot()
	def on_itemClicked(self, i):
		try:
			ret = self.tblwdtApp.item(i.row(), 3).text()
		except:
			ret = ''
		self.rettxt.setText(ret)
	
	@QtCore.pyqtSlot()
	def updateStatusBar(self, text):
		'''
		Set the status of executing on tbsReuslt
		'''
		#self.tbsResult.setText(text)
		self.statusBar.showMessage(text)

	def runCmd(self, svrs, cmd):
		lock = threading.RLock()
		success = []
		fails = []
		all = len(svrs)
		if not self.__dict__.get('ss', False):
			self.ss = []
			for i in range(3):
				s = paramiko.SSHClient()
				s.load_system_host_keys()
				s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
				try:
					s.connect(CONFIG['PROXY_IP'], CONFIG['PROXY_PORT'], CONFIG['PROXY_USER'], CONFIG['PROXY_PASS'] if CONFIG['PROXY_PASS'] else None, key_filename = (CONFIG['PROXY_KEY'] if CONFIG['PROXY_KEY'] else None), timeout = 10)
				except Exception, e:
					self.errorBox("Connect to proxy error: %s"%e)
					return False
				lock = threading.RLock()
				self.ss.append((s, lock))
		
		n = m = len(self.ss)
		for i in svrs:
			if n >= m:
				n = 0
			s, lock = self.ss[n]
			t = SSHThread(self.commandCtr, s, i['ip'], cmd, self.tblwdtApp, i['row'], 3, all, success, fails, lock)
			t.sinOut.connect(self.updateStatusBar)
			t.start()
			n += 1
			
	def errorBox(self, text):
		qtm = QtGui.QMessageBox
		msg_box = qtm(qtm.Critical, "Error", unicode(text), qtm.Yes)
		msg_box.exec_()

	def warnBox(self, text):
		qtm = QtGui.QMessageBox
		msg_box = qtm(qtm.Warning, "Warning", unicode(text), qtm.Yes)
		msg_box.exec_()
				
class SSHThread(QtCore.QThread):
	'''SSH WORK THREAD'''
	sinOut = QtCore.pyqtSignal(str)
	'''
	def __init__(self, parent, svr, cmd, tbl, column):
		QtCore.QThread.__init__(self, parent)
		self.parent = parent
		self.svrs = svrs
		self.cmd = cmd
		self.tbl = tbl
		self.column = column
	'''
	def __init__(self, parent, ssh, svr, cmd, tbl, row, column, all, success, fails, lock):
		QtCore.QThread.__init__(self, parent)
		self.parent = parent
		self.ssh = ssh
		self.svr = svr
		self.cmd = cmd
		self.tbl = tbl
		self.row = row
		self.column = column
		self.all = all
		self.success = success
		self.fails = fails
		self.lock = lock

	def run(self):
		s = self.ssh
		try:
			self.lock.acquire()
			stdin, stdout, stderr = s.exec_command("ssh %s %s"%(self.svr, self.cmd))
			stdout_buffer = stdout.read()
			stderr_buffer = stderr.read()
			self.lock.release()
			
			if stderr_buffer and not stdout_buffer:
				ret = ' '.join(stderr_buffer.split('\n'))
				self.lock.acquire()
				self.fails.append(self.svr)
				self.lock.release()
			else:
				ret = stdout_buffer + stderr_buffer
				self.lock.acquire()
				self.success.append(self.svr)
				self.lock.release()
		except Exception, e:
			ret = "Exec command error: %s"%e
			self.lock.acquire()
			self.fails.append(self.svr)
			self.lock.release()
			
		newItem = QtGui.QTableWidgetItem(ret)
		self.tbl.setItem(self.row, self.column, newItem)
		self.sinOut.emit("Result: %s/%s Success, %s/%s Fail, %i executing" %(len(self.success), self.all, len(self.fails), self.all, (self.all - len(self.success) - len(self.fails))))
	
			
if __name__ == "__main__":
	if os.path.dirname(__file__):
		os.chdir(os.path.dirname(__file__))
	app = QtGui.QApplication(sys.argv)
	commandCtr = QtGui.QMainWindow()
	ui = Ui_commandCtr()
	ui.setupUi(commandCtr)
	commandCtr.show()
	sys.exit(app.exec_())

