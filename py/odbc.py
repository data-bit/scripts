# =====================================================================================================================================
# AUTHOR:   Mitch Alves (idp7116)
# DATE:     2021-02-23
# DESC:     APP EXECUTION - QUERY DB
# DRIVERS:  https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver15
#
# =====================================================================================================================================

import pyodbc 

class odbc:
  def __init__(self, server, database):
    self.server = server or ''
    self.database = database or ''
    self.uid = ''
    self.pwd = ''

  def connection(self):
    return 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+self.server+';DATABASE='+self.database+';UID='+self.uid+';PWD='+ self.pwd +';Trusted_connection=yes'
   

# ========================================================================================
# TEST
# ========================================================================================
"""
db = odbc(None,None)
sql = 'INSERT INTO dbo.test (ID,Description) VALUES (?,?)'

try:
  print('Inserting...')
  conn = pyodbc.connect(db.connection())
  cursor = conn.cursor()
  cursor.execute(sql,(3,'Test3'))
  conn.commit()
except pyodbc.Error as ex:
  print(ex)
"""