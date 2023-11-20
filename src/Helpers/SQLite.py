import sqlite3
from datetime import date
import os.path

class ActivitivityLogDB:
    def __init__(self):
        self.db_path = os.path.join(os.getcwd(),"data","ActivityLog.db")
        self.connection = self.connect()


    def connect(self):
        dir_path = os.path.dirname(self.db_path)
        os.makedirs(dir_path, exist_ok=True)
        return sqlite3.connect(self.db_path)

    def create_table(self, table_name, columns):
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)})"
        self.connection.execute(query)

    def insert(self, table_name, data):
        placeholders = ', '.join(['?' for _ in data])
        query = f"INSERT INTO {table_name} VALUES ({placeholders})"
        self.connection.execute(query, tuple(data))
        self.connection.commit()

    def select_all(self, table_name):
        query = f"SELECT * FROM {table_name}"
        cursor = self.connection.execute(query)
        return cursor.fetchall()

    def tableExist(self, table_name):
        query = f"SELECT count(*) FROM sqlite_master WHERE type='table' AND name='{table_name}'"
        cursor = self.connection.execute(query)
        if cursor.fetchall()[0][0] > 0:
            return True
        else:
            return False


    # Activities specific functions
    def createActivities(self):
        query = "CREATE TABLE IF NOT EXISTS activities (ID INTEGER PRIMARY KEY AUTOINCREMENT, year INTEGER, month INTEGER, day INTEGER, project TEXT, duration REAL, activity TEXT)"
        self.connection.execute(query)

    def insertActivity(self, data):
        self.createActivities()
        placeholders = ', '.join(['?' for _ in data])
        query = f"INSERT INTO activities (year,month,day,project,duration,activity) VALUES ({placeholders})"
        self.connection.execute(query, tuple(data))
        self.connection.commit()

    def selectActivities(self, reqDate: date):
        query = f"SELECT * FROM activities WHERE year='{reqDate.year}' AND month='{reqDate.month}' AND day='{reqDate.day}' "
        cursor = self.connection.execute(query)
        return cursor.fetchall()
    
    def selectActivity(self, ID):
        query = f"SELECT * FROM activities WHERE ID='{ID}'"
        cursor = self.connection.execute(query)
        return cursor.fetchall()[0]
    
    def deleteActivity(self, actID):
        query = f"DELETE FROM activities WHERE ID='{actID}'"
        self.connection.execute(query)
        self.connection.commit()

    def updateActivity(self, actID, project, duration, activity):
        query = f"UPDATE activities SET project='{project}', duration={duration}, activity='{activity}' WHERE ID={actID}"
        self.connection.execute(query)
        self.connection.commit()
    
    #Project specific functions
    def createProjects(self):
        query = "CREATE TABLE IF NOT EXISTS projects (projectName TEXT PRIMARY KEY, jobNumber TEXT, jobEnab BOOLEAN, projectDesc TEXT)"
        self.connection.execute(query)
    
    def insertProject(self, data):
        self.createProjects()
        placeholders = ', '.join(['?' for _ in data])
        query = f"INSERT INTO projects VALUES ({placeholders})"
        self.connection.execute(query, tuple(data))
        self.connection.commit()

    def updateProject(self, projName, jobNo, jobEnab):
        query = f"UPDATE projects SET jobNumber='{jobNo}', jobEnab={jobEnab} WHERE projectName='{projName}'"
        self.connection.execute(query)
        self.connection.commit()

    def deleteProject(self, projName):
        query = f"DELETE FROM projects WHERE projectName='{projName}'"
        self.connection.execute(query)
        self.connection.commit()

    def selectProject(self, projName):
        query = f"SELECT * FROM projects WHERE projectName='{projName}'"
        cursor = self.connection.execute(query)
        project = cursor.fetchall()
        if(len(project) > 0):
            return project[0]
        else:
            return ('N.A.', 'N.A.', 0, '')