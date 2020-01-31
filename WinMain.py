'''''''''''''''''''''''''''''''''''''''''''''''''''
' Codec:utf-8
'
' Python[3.7] practice project
' Simple operation database demonstration program
'
' third equation library reference:
'  |___ PyQt5
'  |___ mysql.connector
'
' I have managed the source code to GitHub:\
'   https://github.com/xuhaowen940728/ademoc
'        
' TODO: Some dtor 
' FIXME: Use many SQL connect handle
' FIXME: More...
'''''''''''''''''''''''''''''''''''''''''''''''''''

import mysql.connector
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

# Qt rad tools import 
from DlgSQLSettings import *
from UiMain import *
from DlgFieldNameAppend import *

####### Global var #######
listUseMySQLDataType =\
[
  ##### INT #####
  'tinyint', #0
  'smallint', #1
  'mediumint', #2
  'int', #3 length
  'integer', #4
  'bigint', #5
  'float', #6
  'double', #7
  'decimal', #8
  
  ##### DATE ######
  'date', #9
  'time', #10
  'year', #11
  'datetime', #12
  'timestamp', #13
  
  #### CHAR || BIN ####
  'char', #14
  'varchar', #15
  'tinyblob', #16
  'tinytext', #17
  'blob', #18
  'text', #19
  'mediumblob', #20
  'mediumtext', #21
  'longblob', #22
  'longtext' #23
]


def makeTypeRange(intField, strFieldType, main, sub):
  strMain = str(main)
  strSub = str(sub)
  str_ = strFieldType
  
  if main != 0:
    if intField <= 5:
      str_ += '(' + strMain + ')'
    elif intField <= 8:
      str_ += '(' + strMain + ',' + strSub + ')'
    elif intField == 10:  # time
      str_ += '(' + strMain + ')'
    elif intField == 12:  # datetime
      str_ += '(' + strMain + ')'
    elif intField == 13:  # timestamp
      str_ += '(' + strMain + ')'
    elif intField == 14 \
      or intField == 15:  # [var]char
      str_ += '(' + strMain + ')'
  else:
    if intField == 14 \
      or intField == 15:  # [var]char
      str_ += '(0)'
  return str_
  
def getDataTypeIndex(typeString):
  pos = -1
  index = 0
  for iter in listUseMySQLDataType:
    if typeString == iter:
      pos = index
      break
    index = index + 1
  return pos

def getDataTypeString(typeIndex):
  if typeIndex < 0:
    return '0'
  elif (typeIndex < len(listUseMySQLDataType)):
    return listUseMySQLDataType[typeIndex]
  else:
    return '0'



class SQL_field(object):
  def __init__(self):
    self.strName = ''
    self.charLen = 0
    self.numbMainLen = 0
    self.numbSubLen = 0
    self.datePrec = 0
    self.collName = ''
    self.dataList = []
    self.intField = 0
    self.strFieldType = ''
    self.cache = False
  
class SQL_table(object):
  def __init__(self):
    self.strName = ''
    self.fieldList = []
    
class SQL_database(object):
  def __init__(self):
    self.strName = ''
    self.tableList = []
  
class SQL_connect(object):
  def __init__(self):
    self.strConnectName = ''
    self.strHost = ''
    self.strPort = ''
    self.strUserName = ''
    self.strPassword = ''
    self.databaseList = []
  def __init__(self, _strConnectName, _strHost, _strPort, _strUserName, _strPassword):
    self.strConnectName = _strConnectName
    self.strHost = _strHost
    self.strPort = _strPort
    self.strUserName = _strUserName
    self.strPassword = _strPassword
    self.databaseList = []
    
  def openSQLConnect(self):
    return mysql.connector.connect(host=self.strHost, port=self.strPort, user=self.strUserName, passwd=self.strPassword)
  
  def enumALLInfos(self):
    # Enum database and table
    handle = self.openSQLConnect()
    handle2= self.openSQLConnect()
    handle3= self.openSQLConnect()
    
    sqlCursor  = handle.cursor(buffered=True)
    sqlCursor2 = handle2.cursor(buffered=True)
    sqlCursor3 = handle3.cursor(buffered=True)
    
    sqlCursor.execute("SHOW DATABASES")
    
    # Append database infos
    for iter in sqlCursor:
      databaseItem = SQL_database()
      databaseItem.strName = iter[0]

      # Append database's table infos
      useDatabaseCommand = "USE `" + iter[0] + "`"

      sqlCursor2.execute(useDatabaseCommand)
      sqlCursor3.execute(useDatabaseCommand)
      
      if iter[0] != 'information_schema':
        sqlCursor2.execute("SHOW FULL TABLES WHERE TABLE_TYPE = 'BASE TABLE'; ")
      else:
        sqlCursor2.execute("SHOW FULL TABLES WHERE TABLE_TYPE = 'SYSTEM VIEW'; ")
        
      for iter2 in sqlCursor2:
        table = SQL_table()
        table.strName = iter2[0]
        databaseItem.tableList.append(table)

      self.databaseList.append(databaseItem)

    handle.close()
    handle2.close()
    handle3.close()

################## Override CDialog<Modal> MySQL Connect ##################
class CDialogSQLSettings(QtWidgets.QDialog):
  def __init__(self, SQL_connect_ref_list):
    # Exec base ctor
    QtWidgets.QDialog.__init__(self)
    
    self.newItem = None;
    self.isInsertDone_ = False;
    self.listConnect = SQL_connect_ref_list
    
    self.ui = Ui_Dialog()
    self.ui.setupUi(self)
    self.setModal(True)
    
    # Connect Settings Button
    self.ui.btOk.clicked.connect(self.onSettings)
    self.ui.btCancel.clicked.connect(self.close)
    
    # Fill default params
    self.ui.etConnectName.setPlainText('samples-link')
    self.ui.etHostName.setPlainText('localhost')
    self.ui.etPort.setPlainText('3306')
    self.ui.etUserName.setPlainText('root')
    # self.ui.etPassword.setPlainText('')
    
  def isInsertDone(self):
    return self.isInsertDone_
  
  def onSettings(self):
    strConnect = self.ui.etConnectName.toPlainText()
    strHost = self.ui.etHostName.toPlainText()
    strPort = self.ui.etPort.toPlainText()
    strUserName = self.ui.etUserName.toPlainText()
    strPassword = self.ui.etPassword.toPlainText()
    
    connectCurrent = SQL_connect(strConnect, strHost, strPort, strUserName, strPassword)
    # Try link datebase
    
    try:
      handle = mysql.connector.connect(host=strHost, port=strPort, user=strUserName, passwd=strPassword)
    except Exception as e:
      QtWidgets.QMessageBox().critical(None, 'MySQL Connect', str(e), QtWidgets.QMessageBox.Ok)
    else:
      # OK, Connect done
      # Insert list, EndDialog
      self.isInsertDone_ = True;
      self.listConnect.append(connectCurrent)
      self.newItem = connectCurrent
      self.close()
    finally:
      handle.close()


################## Override CDialog<Modal> Fieldname ##################
class CDialogAppendField(QtWidgets.QDialog):
  def __init__(self, CMainFrame_, pos_, strFieldNameAfter_):
    # Exec base ctor
    QtWidgets.QDialog.__init__(self)
    
    self.frame = CMainFrame_
    self.strFieldNameAfter = strFieldNameAfter_
    self.insertPos = pos_
    
    self.ui = Ui_dlgFieldNameAppend()
    self.ui.setupUi(self)
    self.setModal(True)
    
    # Connect Settings Button
    self.ui.btOk.clicked.connect(self.onSettings)

    # Fill default params
    self.ui.etFieldName.setPlainText('samples')
  
  def onSettings(self):
    strFieldName = self.ui.etFieldName.toPlainText()
    frame = self.frame
    
    if frame.pickTable != None \
      and frame.pickDatabase != None \
      and frame.pickConnect != None:
    
      handle = frame.pickConnect.openSQLConnect()
      
      
      sqlCursor = handle.cursor()

      command = 'USE `' + frame.pickDatabase.strName + '`'
      
      sqlCursor.execute(command)
      
      command = 'ALTER TABLE `' + frame.pickTable.strName + '` ADD COLUMN `' \
                + strFieldName + '` varchar(30)'
      
      if self.strFieldNameAfter == None:
        command += ' FIRST'
      else:
        command += ' AFTER `' + self.strFieldNameAfter + '`'
        
      try:
        sqlCursor.execute(command)
        
        # Append field
        field = SQL_field()
        field.strName = strFieldName
        field.strFieldType = 'varchar'
        field.collName = 'varchar(30)'
        field.numbMainLen = 0
        field.numbSubLen = 0
        field.datePrec = 0
        field.charLen = 30
        field.intField = getDataTypeIndex('varchar')
        
        if self.strFieldNameAfter == None:
          frame.ui.tbField.insertRow(0)
          frame.ui.tbData.insertColumn(0)
          frame.fieldList.append(field)
        else:
          frame.ui.tbField.insertRow(self.insertPos)
          frame.ui.tbData.insertColumn(self.insertPos)
          frame.fieldList.insert(self.insertPos, field)
        
        self.close()
      except Exception as e:
        QtWidgets.QMessageBox().critical(None, 'MySQL Connect', str(e), QtWidgets.QMessageBox.Ok)
      finally:
        handle.close()
        
      # else:


    else:
      pass

################## Override CMainFrame ##################
class CMainFrame(QtWidgets.QMainWindow):
  def __init__(self):
    # Exec base ctor
    QtWidgets.QMainWindow.__init__(self)

    self.comboxHoldIndex = -1
    self.comboxPrevIndex = -1
    self.onFieldRemove = False
    
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)
    self.ui.cmdNewMySQLConnect.triggered.connect(self.onSQLSettings)
    self.ui.actionQt.triggered.connect(lambda state:QtWidgets.QMessageBox().aboutQt(None, "About QT"))
    
    self.ui.tbField.currentItemChanged.connect(self.onFieldChanged)
    self.ui.tbField.currentCellChanged.connect(self.onSetComboxIndex)
    self.ui.tbField.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
    self.ui.tbField.customContextMenuRequested.connect(self.onFieldCtxMenu)
    
    # Create field context menu
    # Insert before
    # Insert After
    # Remove current
    self.tbFieldMenu = QtWidgets.QMenu(self.ui.tbField)
    self.actFieldInsertBefore = QtWidgets.QAction("Insert before", self.ui.tbField)
    self.actFieldInsertAfter = QtWidgets.QAction("Append to tail", self.ui.tbField)
    self.actFieldRemoveCurrent = QtWidgets.QAction("Remove current", self.ui.tbField)

    self.actFieldInsertBefore.triggered.connect(self.onInsertNewFieldBefore)
    self.actFieldInsertAfter.triggered.connect(self.onAppendField)
    self.actFieldRemoveCurrent.triggered.connect(self.onRemoveField)

    self.tbFieldMenu.addAction(self.actFieldInsertBefore)
    self.tbFieldMenu.addAction(self.actFieldInsertAfter)
    self.tbFieldMenu.addAction(self.actFieldRemoveCurrent)
    
    # Create data context menu
    # Insert before
    # Insert After
    # Remove current
    
    
    
    # self.ui.tbField.itemChanged.connect(onFieldItemChanged)
    # self.ui.tbField.cell
  
  
  
    self.ui.trConnect.itemDoubleClicked.connect(self.onSelectTreeItem)
    # self.ui.tbField.itemClicked.connect(self.onSelectTableFieldItem)
    self.fieldList = []
    self.listConnect = []
    self.listCacheComboBox = []
    self.listCommandField = []
    
    # Qt5 GUI Pick Connect/Database/Table var
    self.pickConnect = None
    self.pickDatabase= None
    self.pickTable = None

    # Ctor listview column header (SQL field header)
    self.ui.tbField.setColumnCount(4)
    self.ui.tbField.setHorizontalHeaderLabels(['name', 'type', 'length', 'decimals'])

    self.resize(960, 640)


  
  def onInsertNewFieldBefore(self):
    row = self.ui.tbField.currentRow()
    listLen = len(self.fieldList)
  
    if row >= 0 \
      and self.pickTable != None \
      and self.pickDatabase != None \
      and self.pickConnect != None:
    
      strFieldLink = None
    
      if listLen > 0 \
        and row < listLen:
        strFieldLink = self.fieldList[row].strName
    
      dlg = CDialogAppendField(self, 0, strFieldLink)
      dlg.exec()

  def onAppendField(self):
    
    if self.pickTable != None \
      and self.pickDatabase != None \
      and self.pickConnect != None:
  
      listLen = len(self.fieldList)
      strFieldLink = None
      pos = 0
      
      if listLen > 0:
        strFieldLink = self.fieldList[listLen-1].strName
      
        pos = listLen
        
      dlg = CDialogAppendField(self, pos, strFieldLink)
      dlg.exec()
  
  def onRemoveField(self):
    row = self.ui.tbField.currentRow()
    
    if row >= 0\
      and self.pickTable != None \
      and self.pickDatabase != None \
      and self.pickConnect != None:

      # Get remain ctx
      qItemfieldName = self.ui.tbField.item(row, 0)
  
      qItemfieldMain = self.ui.tbField.item(row, 2)
      qItemfieldSub = self.ui.tbField.item(row, 3)
  
      # self.pickConnect.
      handle = self.pickConnect.openSQLConnect()
  
      sqlCursor = handle.cursor(buffered=True)
      sqlCursor.execute('USE `' + self.pickDatabase.strName + '`')
  
      field = self.fieldList[row]
      # field.
  
      try:
        command = 'ALTER TABLE `' + self.pickTable.strName + '` DROP COLUMN `' \
                  + field.strName + '` '
        sqlCursor.execute(command)

        self.onFieldRemove = True

        self.fieldList.remove(field)
        
        # REmove gui item
        self.ui.tbData.removeColumn(row)
        self.ui.tbField.removeRow(row)
        
        self.onFieldRemove = False
      except Exception as e:
        QtWidgets.QMessageBox().critical(None, 'MySQL Connect', str(e), QtWidgets.QMessageBox.Ok)
    
        # Reset old infos
      finally:
        handle.close()

  def onFieldCtxMenu(self, point):
    self.tbFieldMenu.move(self.cursor().pos())
    self.tbFieldMenu.show()
    # self.comboxPrevIndex =
    
  def onSetComboxIndex(self, currentRow, currentColumn, previousRow, previousColumn):
    self.comboxHoldIndex = currentRow
    # self.comboxPrevIndex =
    
  def onFieldChanged(self, current, previous):
    if previous != None\
      and self.onFieldRemove == False:
      col = self.ui.tbField.column(previous)
      row = self.ui.tbField.row(previous)
      
      str_ = previous.text()
      if col >= 0 \
        and row >= 0\
        and row != 2\
				and self.pickTable != None\
				and self.pickDatabase != None\
				and self.pickConnect != None:
  
        # Get remain ctx
        qItemfieldName = self.ui.tbField.item(row, 0)
        
        qItemfieldMain = self.ui.tbField.item(row, 2)
        qItemfieldSub = self.ui.tbField.item(row, 3)
        
        # self.pickConnect.
        handle = self.pickConnect.openSQLConnect()
        
        
        sqlCursor = handle.cursor(buffered=True)
        sqlCursor.execute ('USE `' + self.pickDatabase.strName + '`')
        
        field = self.fieldList[row]
        # field.
				
        try:
          if col == 0:
            # Modify field-name
            command = 'ALTER TABLE `' + self.pickTable.strName +'` CHANGE COLUMN `'\
                    + field.strName + '` `' + str_ + '` ' + field.collName
            sqlCursor.execute(command)
          elif col == 1:
            # Modify type
            pass
          elif col == 2:
            # Modify length
            command = 'ALTER TABLE `' + self.pickTable.strName + '` MODIFY COLUMN `' \
                      + field.strName + '` ' + makeTypeRange(field.intField, field.strFieldType,\
                                                                           int(qItemfieldMain.text()),
                                                                           int(qItemfieldSub.text()))
            sqlCursor.execute(command)
          elif col == 3:
            # Modify Decimal
            command = 'ALTER TABLE `' + self.pickTable.strName + '` MODIFY COLUMN `' \
                      + field.strName + '` ' + makeTypeRange(field.intField, field.strFieldType,\
                                                                           int(qItemfieldMain.text()),
                                                                           int(qItemfieldSub.text()))
            sqlCursor.execute(command)
            
          # Update current item infos
          strCommand= "SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = "\
                          +                  "'" + self.pickDatabase.strName + "'"             \
                          + " AND TABLE_NAME = "                                      \
                          +                  "'" + self.pickTable.strName    + "'"
          sqlCursor.execute(strCommand)
          
          tupleArr = sqlCursor.fetchall()
          tupleItem = tupleArr[row]
  
          field.strName = tupleItem[3]
          field.strFieldType = tupleItem[7]
          field.collName = tupleItem[15]
          field.numbMainLen = tupleItem[10]
          field.numbSubLen = tupleItem[11]
          field.datePrec = tupleItem[12]
          field.charLen = tupleItem[8]

          qItemfieldName.setText(field.strName)
          qItemfieldMain.setText('0')
          qItemfieldSub.setText('0')
          
          if field.intField <= 8:
            qItemfieldMain.setText(str(field.numbMainLen))
            if field.intField >= 6:
              qItemfieldSub.setText(str(field.numbSubLen))
          elif field.intField <= 13:
            qItemfieldMain.setText(str(field.datePrec))
          elif field.intField <= 15:
            qItemfieldMain.setText(str(field.charLen))
            
        except Exception as e:
          QtWidgets.QMessageBox().critical(None, 'MySQL Connect', str(e), QtWidgets.QMessageBox.Ok)
      
          # Reset old infos
          qItemfieldName.setText(field.strName)
          qItemfieldMain.setText('0')
          qItemfieldSub.setText('0')
          
          if field.intField <= 8:
            qItemfieldMain.setText(str(field.numbMainLen))
            if field.intField >= 6:
              qItemfieldSub.setText(str(field.numbSubLen))
          elif field.intField <= 13:
            qItemfieldMain.setText(str(field.datePrec))
          elif field.intField <= 15:
            qItemfieldMain.setText(str(field.charLen))
        finally:
          handle.close()

  def onSelectTableFieldItem(self, tableWidgetItem):
    if tableWidgetItem.UserType & 1 << 30:
      index = tableWidgetItem.UserType & 0x7FFFFFFF >> 1

  
  
  def onSelectTreeItem(self, treeItem, dummyUsed):
    
    if treeItem.UserType & 0x80000000:
      try:
          # Enum field list
          self.fieldList = []
    
          connect = self.listConnect     [treeItem.parent().parent().UserType & 0x1FFFFFFF]
          database= connect.databaseList [treeItem.parent().UserType          & 0x3FFFFFFF]
          table   = database.tableList   [treeItem.UserType                   & 0x7FFFFFFF]

          handle = connect.openSQLConnect()
          handle2 = connect.openSQLConnect()
          handle3 = connect.openSQLConnect()
          
          # Update pick var
          self.pickConnect = connect
          self.pickDatabase= database
          self.pickTable   = table
          
          # Connect it
          sqlCursor  = handle.cursor(buffered=True)
          sqlCursor2 = handle2.cursor(buffered=True)
          sqlCursor3 = handle3.cursor(buffered=True)
    
          sqlCursor.execute ('USE `' + database.strName + '`')
          sqlCursor2.execute('USE `' + database.strName + '`')
          sqlCursor3.execute('USE `' + database.strName + '`')
          
          strCommand= "SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = "\
                          +                  "'" + database.strName + "'"             \
                          + " AND TABLE_NAME = "                                      \
                          +                  "'" + table.strName    + "'"
          sqlCursor.execute(strCommand)
        
          listHeader = []
          # Serach && Append field
          for iter in sqlCursor:
            field = SQL_field()
            field.strName = iter[3]
            field.strFieldType = iter[7]
            field.collName = iter[15]
            field.numbMainLen = iter[10]
            field.numbSubLen = iter[11]
            field.datePrec = iter[12]
            field.charLen = iter[8]
            field.intField = getDataTypeIndex(iter[7])
            
            # Append col header
            listHeader.append(field.strName)
       
            self.fieldList.append(field)
    
          self.ui.tbData.setColumnCount(len(listHeader))
          self.ui.tbData.setHorizontalHeaderLabels(listHeader)
     
          # Clear all cache combobox infos
          for iter in self.listCacheComboBox:
            del iter
            
          # Remove tbData header
          # self.ui.tbData.
    
          sqlCursor2.execute("SELECT COUNT(*) FROM " + "`" + table.strName + "`")
    
          for iter in sqlCursor2:
            self.ui.tbData.setRowCount(iter[0])
            break
            
          # Append to listview - field
          self.ui.tbField.setRowCount(len(self.fieldList))
          
          for posFieldItem in range(0, len(self.fieldList)):
            comboBox = QtWidgets.QComboBox()
            comboBox.activated.connect(self.onComboxChanged)
            
            sqlField = self.fieldList[posFieldItem]
            
            # Prepare combobox index infos
            for posComboItem in range(0, len(listUseMySQLDataType)):
              comboBox.insertItem(posComboItem, listUseMySQLDataType[posComboItem])
    
            self.listCacheComboBox.append(comboBox)
            
            QTbItem0 = QtWidgets.QTableWidgetItem(sqlField.strName)
            QTbItem1 = QtWidgets.QTableWidgetItem("")
            QTbItem2 = QtWidgets.QTableWidgetItem("0")
            QTbItem3 = QtWidgets.QTableWidgetItem("0")
            
            QTbItem0.UserType = sqlField
            QTbItem1.UserType = sqlField
            QTbItem2.UserType = sqlField
            QTbItem3.UserType = sqlField

            if sqlField.intField <= 8:
              QTbItem2.setText(str(sqlField.numbMainLen))
              if sqlField.intField >= 6:
                QTbItem3.setText(str(sqlField.numbSubLen))
            elif sqlField.intField <= 13:
              QTbItem2.setText(str(sqlField.datePrec))
            elif sqlField.intField <= 15:
              QTbItem2.setText(str(sqlField.charLen))
            
            if getDataTypeString(sqlField.intField) == None:
              comboBox.insertItem(0, "supported/unknown data")
              comboBox.setCurrentIndex(0)
              comboBox.setEnabled(False)
            else:
              comboBox.setCurrentIndex(sqlField.intField)
    
            self.ui.tbField.setItem(posFieldItem, 0, QTbItem0)
            self.ui.tbField.setItem(posFieldItem, 1, QTbItem1)
            self.ui.tbField.setItem(posFieldItem, 2, QTbItem2)
            self.ui.tbField.setItem(posFieldItem, 3, QTbItem3)
            
            self.ui.tbField.setCellWidget(posFieldItem, 1, comboBox)
    
            sqlCursor3.execute("SELECT `" + sqlField.strName + "` FROM `" + table.strName + "`")

            index = 0
            for iter in sqlCursor3:
             self.ui.tbData.setItem(index, posFieldItem, QtWidgets.QTableWidgetItem(str(iter[0])))
             index = index + 1

      except Exception as e:
        QtWidgets.QMessageBox().critical(None, 'MySQL Connect', str(e), QtWidgets.QMessageBox.Ok)
        
        self.pickConnect = None
        self.pickDatabase= None
        self.pickTable   = None
        
        # Clear gui attach
        self.ui.tbField.setRowCount(0)
        self.ui.tbData.setRowCount(0)
      else:
        pass
      finally:
        handle.close()
        handle2.close()
        handle3.close()

  def onComboxChanged(self, index):
    
    if index >= 0\
      and self.comboxHoldIndex >= 0 \
      and self.pickTable != None \
      and self.pickDatabase != None \
      and self.pickConnect != None:
      
      row = self.comboxHoldIndex
    
      qItemfieldName = self.ui.tbField.item(row, 0)
    
      qItemfieldMain = self.ui.tbField.item(row, 2)
      qItemfieldSub = self.ui.tbField.item(row, 3)
    
      # self.pickConnect.
      handle = self.pickConnect.openSQLConnect()
    
      sqlCursor = handle.cursor(buffered=True)
      sqlCursor.execute('USE `' + self.pickDatabase.strName + '`')
    
      field = self.fieldList[row]
      
      prevIndex = field.intField
      
      strNewField = getDataTypeString(index)

      try:
        command = 'ALTER TABLE `' + self.pickTable.strName + '` MODIFY COLUMN `' \
                  + field.strName + '` ' + makeTypeRange(field.intField, strNewField, \
                                                         int(qItemfieldMain.text()),
                                                         int(qItemfieldSub.text()))
        sqlCursor.execute(command)

        # Update current item infos
        strCommand = "SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = " \
                     + "'" + self.pickDatabase.strName + "'" \
                     + " AND TABLE_NAME = " \
                     + "'" + self.pickTable.strName + "'"
        sqlCursor.execute(strCommand)
      
        tupleArr = sqlCursor.fetchall()
        tupleItem = tupleArr[row]
      
        field.strName = tupleItem[3]
        field.strFieldType = tupleItem[7]
        field.collName = tupleItem[15]
        field.numbMainLen = tupleItem[10]
        field.numbSubLen = tupleItem[11]
        field.datePrec = tupleItem[12]
        field.charLen = tupleItem[8]

        if field.intField <= 8:
          qItemfieldMain.setText(str(field.numbMainLen))
          if field.intField >= 6:
            qItemfieldSub.setText(str(field.numbSubLen))
        elif field.intField <= 13:
          qItemfieldMain.setText(str(field.datePrec))
        elif field.intField <= 15:
          qItemfieldMain.setText(str(field.charLen))
        
      except Exception as e:
        QtWidgets.QMessageBox().critical(None, 'MySQL Connect', str(e), QtWidgets.QMessageBox.Ok)
      
        # Reset old infos
        combox = self.ui.tbField.cellWidget(row, 1)
        combox.__class__ = QtWidgets.QComboBox
        combox.setCurrentIndex(prevIndex)
        
      finally:
        handle.close()
      pass
  
  def onSQLSettings(self):
    dlgSQLSettings = CDialogSQLSettings(self.listConnect)
    dlgSQLSettings.exec()
    if dlgSQLSettings.isInsertDone() != False:
      # Reset all view
      # Append to tail (QTreeWidget)
      # TODO: check repeat name
      dlgSQLSettings.newItem.enumALLInfos()
      
      topCurrentNode = QtWidgets.QTreeWidgetItem([dlgSQLSettings.newItem.strConnectName])
      topCountNode = self.ui.trConnect.topLevelItemCount()
      topCurrentNode.UserType = topCountNode | 1 << 29
      
      for iter in dlgSQLSettings.newItem.databaseList:
        levelCurrentNode = QtWidgets.QTreeWidgetItem(topCurrentNode, [iter.strName])
        levelCurrentNode.UserType = topCurrentNode.childCount() - 1 | 1 << 30
        for iter2 in iter.tableList:
          # FIXME: index | shift, too simple mark range and index
          levelCurrentNode2 = QtWidgets.QTreeWidgetItem(levelCurrentNode, [iter2.strName])
          levelCurrentNode2.UserType = levelCurrentNode.childCount() - 1 | 1 << 31

      self.ui.trConnect.insertTopLevelItem(topCountNode, topCurrentNode)
      
      
if __name__ == '__main__':
  app = QtWidgets.QApplication(sys.argv)
  window = CMainFrame()
  window.show()
  sys.exit(app.exec_())
