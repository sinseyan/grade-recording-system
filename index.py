import sys
import json
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.uic import loadUi
import os.path
from pathlib import Path
import sqlite3
from sqlite3 import Error
from PyQt5.QtCore import QDate, QTime, QDateTime, Qt, QTimer
import collections
import math


class Login(QDialog):
    def __init__(self):
        super(Login,self).__init__()
        loadUi('ui\login.ui',self)

        self.btnLogin.clicked.connect(self.login_buttonclicked)

    def login_buttonclicked(self):
        if self.txtUsername.text() == "admin" and self.txtPassword.text() == "password":
            self.index = Index()
            self.index.show()
            self.close()

        else:
            QMessageBox.about(self,"Error","Incorrect username or password.")
            self.txtUsername.setText("")
            self.txtPassword.setText("")
            self.txtUsername.setFocus()


class Index(QMainWindow):

    c = sqlite3.connect('System.sqlite')

    def __init__(self):
        super(Index,self).__init__()
        loadUi('ui\index.ui', self)

        self.showStudents.triggered.connect(self.show_Students)
        self.showSubjects.triggered.connect(self.show_Subjects)
        self.addGrades.triggered.connect(self.add_Grade)
        self.actionExit.triggered.connect(self.exit_App)
        self.showStudentReport.triggered.connect(self.show_StudentReport)
        

        self.showSubjectReport.triggered.connect(self.show_SubjectReport)

        


        activity = QTimer(self)
        activity.timeout.connect(self.showActivity)
        activity.start(100)

        date = QDate.currentDate()
        self.lblDate.setText(date.toString(Qt.DefaultLocaleLongDate))

        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        time = QTime.currentTime()
        self.lblTime.setText(time.toString(Qt.DefaultLocaleLongDate))

        update = QTimer(self)
        update.timeout.connect(self.statusSystem)
        update.start(100)

        DB = Path('System.sqlite')
        if not DB.is_file():

            try:
                conn = sqlite3.connect('System.sqlite')
                cur = conn.cursor()

                cur.executescript('''
                CREATE TABLE Subjects(
                SubjectCode VARCHAR(50) NOT NULL,
                SubjectName VARCHAR(100) NOT NULL,
                PRIMARY KEY (SubjectCode)
                );

                CREATE TABLE Students(
                StudentCode VARCHAR(50) NOT NULL,
                LastName VARCHAR(100) NOT NULL,
                FirstName VARCHAR(100) NOT NULL,
                MiddleName VARCHAR(100),
                PRIMARY KEY (StudentCode)
                );

                CREATE TABLE Records(
                RecordID INTEGER PRIMARY KEY,
                StudentCode VARCHAR(10) NOT NULL,
                SubjectCode VARCHAR(10) NOT NULL,
                Grade FLOAT(50) NOT NULL,
                FOREIGN KEY (StudentCode) REFERENCES Students(StudentCode),
                FOREIGN KEY (SubjectCode) REFERENCES Subjects(SubjectCode)
                );
                ''')

                conn.commit()
                conn.close()
            except Error as e:
                QMessageBox.about(self,"Error",str(e))
            


    def statusSystem(self):
        totalStud=0
        totalSub=0
        cur=self.c.cursor()
        studRows = cur.execute("Select * From Students")
        for row in studRows:
            totalStud+=1
        self.lblTotal.setText(str(totalStud))
        subRows = cur.execute("Select * From Subjects")
        for row in subRows:
            totalSub+=1
        self.lblTotalSub.setText(str(totalSub))

    def showActivity(self):
        try:
            cur=self.c.cursor()
            self.tableRecords.clear()
            rows = cur.execute('SELECT Students.StudentCode,Students.LastName,Students.FirstName,Students.MiddleName,Subjects.SubjectName,Grade FROM Records INNER JOIN Students ON Records.StudentCode = Students.StudentCode INNER JOIN Subjects ON Records.SubjectCode = Subjects.SubjectCode')
            self.tableRecords.setHorizontalHeaderLabels(["Student Code","Last Name","First Name","Middle Name","Subject Name","Grade"])
##            rows = cur.execute('SELECT * FROM Records')
##            self.tableRecords.setHorizontalHeaderLabels(["Student Code","Subject Code","Grade"])
            self.tableRecords.setRowCount(0)
            for row,row_data in enumerate(rows):
                self.tableRecords.insertRow(row)
                for column,column_data in enumerate(row_data):
                    self.tableRecords.setItem(row, column, QTableWidgetItem(str(column_data)))
            self.tableRecords.resizeColumnsToContents()
        except Error as e:
            QMessagebox.about(self,"Error",str(e))

    def showTime(self):
        time = QTime.currentTime()
        self.lblTime.setText(time.toString(Qt.DefaultLocaleLongDate))
        date = QDate.currentDate()
        self.lblDate.setText(date.toString(Qt.DefaultLocaleLongDate))

    def show_Students(self):
        students=Students()
        students.exec()

    def show_Subjects(self):
        subjects=Subjects()
        subjects.exec()

    def add_Grade(self):
        grade = Grades()
        grade.exec()

    def show_StudentReport(self):
        studentReport = StudentReport()
        studentReport.exec()

    def show_SubjectReport(self):
        subjectReport = SubjectReport()
        subjectReport.exec()

    def exit_App(self):
        self.close()

class Students(QDialog):

    c = sqlite3.connect('System.sqlite')

    def __init__(self):
        super(Students,self).__init__()
        loadUi('ui\students.ui',self)

        self.btnAdd.clicked.connect(self.on_AddButton_clicked)
        self.btnClear.clicked.connect(self.on_ClearButton_clicked)
        self.btnEdit.clicked.connect(self.on_EditButton_clicked)
        self.btnDelete.clicked.connect(self.on_DeleteButton_clicked)
        self.tableStudents.clicked.connect(self.tableStudentItem_changed)

        self.updateStudentList()

        cur = self.c.cursor()


    def updateStudentList(self):
        cur = self.c.cursor()
        self.tableStudents.clear()
        columns=["Student Code", "Last Name","First Name","Middle Name"]
        rows = cur.execute("Select * From Students")
        self.tableStudents.setHorizontalHeaderLabels(columns)
        self.tableStudents.setRowCount(0)
        for row,row_data in enumerate(rows):
            self.tableStudents.insertRow(row)
            for column,column_data in enumerate(row_data):
                self.tableStudents.setItem(row, column, QTableWidgetItem(column_data))

    def tableStudentItem_changed(self):
        cur = self.c.cursor()
        row = self.tableStudents.currentRow()
        if row > -1:
            code = self.tableStudents.item(row,0).text()
            rows = cur.execute('Select * From Students Where StudentCode = ?', (code,))
            row = rows.fetchone()
            self.txtStudCode.setText(str(row[0]))
            self.txtLName.setText(str(row[1]))
            self.txtFName.setText(str(row[2]))
            self.txtMName.setText(str(row[3]))

    def on_ClearButton_clicked(self):
        self.txtStudCode.clear()
        self.txtLName.clear()
        self.txtFName.clear()
        self.txtMName.clear()
        self.tableStudents.clearSelection()
        self.txtStudCode.setFocus()

    def on_AddButton_clicked(self):
        try:
            cur = self.c.cursor()
            code = self.txtStudCode.text()
            lname = self.txtLName.text()
            fname = self.txtFName.text()
            mname = self.txtMName.text()
            cur.execute('INSERT INTO Students (StudentCode,LastName,FirstName,MiddleName) VALUES (?,?,?,?)', (code,lname,fname,mname))
            self.c.commit()
            self.on_ClearButton_clicked()
            self.updateStudentList()
        except Error as e:
            QMessagebox.about(self,"Error",str(e))

    def on_EditButton_clicked(self):
        try:
            reply = QMessageBox.question(self, "Edit", "Do you want to edit this record?", QMessageBox.Yes, QMessageBox.No)

            if reply == QMessageBox.Yes:
                cur = self.c.cursor()
                code = self.txtStudCode.text()
                lname = self.txtLName.text()
                fname = self.txtFName.text()
                mname = self.txtMName.text()

                cur.execute('UPDATE Students SET LastName = ?, FirstName = ?,MiddleName = ? WHERE StudentCode = ?', (lname,fname,mname,code))
                self.c.commit()
                self.on_ClearButton_clicked()
                self.updateStudentList()
        except Error as e:
            QMessageBox.about(self,"Error",str(e))
    def on_DeleteButton_clicked(self):
        try:

            #Display question dialog box to confirm if user really want to delete record
            reply = QMessageBox.question(self, "Delete", "Do you want to delete this record?", QMessageBox.Yes, QMessageBox.No)

            if reply == QMessageBox.Yes:
                cur = self.c.cursor()
                code = self.txtStudCode.text()

                cur.execute('DELETE FROM Students WHERE StudentCode = ?', (code,))
                self.c.commit()
                self.updateStudentList()
                self.on_ClearButton_clicked()


        except Error as e:
            QMessageBox.about(self,"Error",str(e))

class Subjects(QDialog):
    c = sqlite3.connect('System.sqlite')

    def __init__(self):
        super(Subjects,self).__init__()
        loadUi('ui\subjects.ui',self)

        self.btnAdd.clicked.connect(self.on_AddButton_clicked)
        self.btnClear.clicked.connect(self.on_ClearButton_clicked)
        self.btnEdit.clicked.connect(self.on_EditButton_clicked)
        self.btnDelete.clicked.connect(self.on_DeleteButton_clicked)
        self.tableSubjects.clicked.connect(self.tableSubjectItem_changed)
        self.updateSubjectList()

    def updateSubjectList(self):
        cur = self.c.cursor()
        self.tableSubjects.clear()
        rows = cur.execute("Select * From Subjects")
        self.tableSubjects.setHorizontalHeaderLabels(["Subject Code", "Subject Name"])
        self.tableSubjects.setRowCount(0)
        for row,row_data in enumerate(rows):
            self.tableSubjects.insertRow(row)
            for column,column_data in enumerate(row_data):
                self.tableSubjects.setItem(row, column, QTableWidgetItem(str(column_data)))

    def on_ClearButton_clicked(self):
        self.txtSubjectCode.clear()
        self.txtSName.clear()
        self.txtSubjectCode.setFocus()

    def on_AddButton_clicked(self):
        try:
            cur = self.c.cursor()
            code = self.txtSubjectCode.text()
            sname = self.txtSName.text()
            cur.execute('INSERT INTO Subjects (SubjectCode,SubjectName) VALUES (?,?)', (code,sname,))
            self.c.commit()
            self.on_ClearButton_clicked()
            self.updateSubjectList()
        except Error as e:
            QMessagebox.about(self,"Error",str(e))

    def on_EditButton_clicked(self):
        try:
            reply = QMessageBox.question(self, "Edit", "Do you want to edit this record?", QMessageBox.Yes, QMessageBox.No)

            if reply == QMessageBox.Yes:
                cur = self.c.cursor()
                code = self.txtSubjectCode.text()
                sname = self.txtSName.text()
                cur.execute('UPDATE Subjects SET SubjectName = ? WHERE SubjectCode = ?', (sname,code,))
                self.c.commit()
                self.on_ClearButton_clicked()
                self.updateSubjectList()
        except Error as e:
            QMessageBox.about(self,"Error",str(e))

    def on_DeleteButton_clicked(self):
        try:
            reply = QMessageBox.question(self, "Delete", "Do you want to delete this record?", QMessageBox.Yes, QMessageBox.No)

            if reply == QMessageBox.Yes:
                cur = self.c.cursor()
                code = self.txtSubjectCode.text()
                cur.execute('DELETE FROM Subjects WHERE SubjectCode = ?', (code,))
                self.c.commit()
                self.updateSubjectList()


        except Error as e:
            QMessageBox.about(self,"Error",str(e))

    def tableSubjectItem_changed(self):
        cur = self.c.cursor()
        row = self.tableSubjects.currentRow()
        if row > -1:
            code = self.tableSubjects.item(row,0).text()
            rows = cur.execute('Select * From Subjects WHERE SubjectCode = ?', (code,))
            row = rows.fetchone()
            self.txtSubjectCode.setText(str(row[0]))
            self.txtSName.setText(str(row[1]))

class Grades(QDialog):
    c = sqlite3.connect('System.sqlite')

    def __init__(self):
        super(Grades,self).__init__()
        loadUi('ui\grades.ui',self)

        self.btnAdd.clicked.connect(self.on_AddButton_clicked)
        self.btnClear.clicked.connect(self.on_ClearButton_clicked)
        self.btnEdit.clicked.connect(self.on_EditButton_clicked)
        self.btnDelete.clicked.connect(self.on_DeleteButton_clicked)
        self.tableStudents.clicked.connect(self.tableStudentItem_changed)

        cur = self.c.cursor()
        rows = cur.execute("Select * From Subjects")
        for row in rows:
            self.cboSubjects.addItem(row[1])
            
        self.updateStudentList()


    def updateStudentList(self):
        cur = self.c.cursor()
        self.tableStudents.clear()
        columns=["Student Code", "Last Name","First Name","Middle Name"]
        rows = cur.execute("Select * From Students")
        self.tableStudents.setHorizontalHeaderLabels(columns)
        self.tableStudents.setRowCount(0)
        for row,row_data in enumerate(rows):
            self.tableStudents.insertRow(row)
            for column,column_data in enumerate(row_data):
                self.tableStudents.setItem(row, column, QTableWidgetItem(column_data))

    def tableStudentItem_changed(self):
        cur = self.c.cursor()
        row = self.tableStudents.currentRow()
        if row > -1:
            code = self.tableStudents.item(row,0).text()
            rows = cur.execute('Select * From Students Where StudentCode = ?', (code,))
            row = rows.fetchone()
            self.txtStudCode.setText(str(row[0]))
            self.txtLName.setText(str(row[1]))
            self.txtFName.setText(str(row[2]))
            self.txtMName.setText(str(row[3]))


    def on_ClearButton_clicked(self):
        self.txtStudCode.clear()
        self.txtLName.clear()
        self.txtFName.clear()
        self.txtMName.clear()
        self.txtGrade.clear()
        self.tableStudents.clearSelection()
        self.txtStudCode.setFocus()

    def on_AddButton_clicked(self):
        try:
            
            cur = self.c.cursor()
            
            codeStud = self.txtStudCode.text()
            codeSub = self.cboSubjects.currentText()
            grade = self.txtGrade.text()
            
            rows = cur.execute('SELECT SubjectCode FROM Subjects WHERE SubjectName = ?',(codeSub,))
            row = rows.fetchone()
            subjectCode = row[0]
            rows = cur.execute('SELECT * FROM Records WHERE StudentCode = ? AND SubjectCode = ?',(codeStud,subjectCode,))
            data = rows.fetchall()
            cur.execute('INSERT INTO Records (StudentCode,SubjectCode,Grade) VALUES (?,?,?)', (codeStud,subjectCode,float(grade),))
            self.c.commit()
            
            self.on_ClearButton_clicked()
            
        except Error as e:
            QMessagebox.about(self,"Error",str(e))

    def on_EditButton_clicked(self):
        try:
            reply = QMessageBox.question(self, "Edit", "Do you want to edit this record?", QMessageBox.Yes, QMessageBox.No)

            if reply == QMessageBox.Yes:
                cur = self.c.cursor()
                codeStud = self.txtStudCode.text()
                codeSub = self.cboSubjects.currentText()
                grade = self.txtGrade.text()
                rows = cur.execute('SELECT SubjectCode FROM Subjects WHERE SubjectName = ?',(codeSub,))
                row = rows.fetchone()
                subjectCode = row[0]
                cur.execute('UPDATE Records SET Grade = ? WHERE StudentCode = ? AND SubjectCode = ?', (float(grade),codeStud,subjectCode,))
                self.c.commit()
                self.on_ClearButton_clicked()
        except Error as e:
            QMessageBox.about(self,"Error",str(e))

    def on_DeleteButton_clicked(self):
        try:
            reply = QMessageBox.question(self, "Delete", "Do you want to delete this record?", QMessageBox.Yes, QMessageBox.No)

            if reply == QMessageBox.Yes:
                cur = self.c.cursor()
                codeStud = self.txtStudCode.text()
                codeSub = self.cboSubjects.currentText()
                grade = self.txtGrade.text()
                rows = cur.execute('SELECT SubjectCode FROM Subjects WHERE SubjectName = ?',(codeSub,))
                row = rows.fetchone()
                subjectCode = row[0]
                cur.execute('DELETE FROM Records WHERE StudentCode = ? AND SubjectCode = ?', (codeStud,subjectCode))
                self.c.commit()


        except Error as e:
            QMessageBox.about(self,"Error",str(e))

class StudentReport(QDialog):

    c = sqlite3.connect('System.sqlite')

    def __init__(self):
        super(StudentReport,self).__init__()
        loadUi('ui/studentReport.ui',self)

        self.btnCompute.clicked.connect(self.compute)
        self.btnClear.clicked.connect(self.on_ClearButton_clicked)
        self.tableStudents.clicked.connect(self.tableStudentItem_changed)

        self.updateStudentList()

        cur = self.c.cursor()


    def updateStudentList(self):
        cur = self.c.cursor()
        self.tableStudents.clear()
        columns=["Student Code", "Last Name","First Name","Middle Name"]
        rows = cur.execute("Select * From Students")
        self.tableStudents.setHorizontalHeaderLabels(columns)
        self.tableStudents.setRowCount(0)
        for row,row_data in enumerate(rows):
            self.tableStudents.insertRow(row)
            for column,column_data in enumerate(row_data):
                self.tableStudents.setItem(row, column, QTableWidgetItem(column_data))

    def tableStudentItem_changed(self):
        cur = self.c.cursor()
        row = self.tableStudents.currentRow()
        if row > -1:
            code = self.tableStudents.item(row,0).text()
            rows = cur.execute('Select * From Students Where StudentCode = ?', (code,))
            row = rows.fetchone()
            self.txtStudCode.setText(str(row[0]))
            self.txtLName.setText(str(row[1]))
            self.txtFName.setText(str(row[2]))
            self.txtMName.setText(str(row[3]))

    def on_ClearButton_clicked(self):
        self.txtStudCode.clear()
        self.txtLName.clear()
        self.txtFName.clear()
        self.txtMName.clear()
        self.tableStudents.clearSelection()
        self.txtStudCode.setFocus()

    def compute(self):
        try:
            cur = self.c.cursor()
            code = self.txtStudCode.text()
            grades=[]
            mode = []
            modeDict = {}
            totalGrades = 0
            totalStud=0
            totalSub=0
            rows = cur.execute('SELECT Grade FROM Records WHERE StudentCode = ?', (code,))

            for row in rows:
                grades.append(float(row[0]))


            for i in grades:
                totalGrades +=i
                    
            studRows = cur.execute("Select * From Students")
            for row in studRows:
                totalStud+=1
            subRows = cur.execute("Select * From Subjects")
            for row in subRows:
                totalSub+=1
            grades.sort()
            minimum = grades[0]
            maximum = grades[len(grades)-1]
            dataRange = maximum - minimum
            if len(grades) % 2 == 0:
                first_median = grades[len(grades) // 2]
                second_median = grades[len(grades) // 2 - 1]
                median = (first_median + second_median) / 2
            else:
                median = grades[len(grades) // 2]

            data = collections.Counter(grades)
            data_list = dict(data)
            max_value = max(list(data.values()))
            mode_val = [num for num, freq in data_list.items() if freq == max_value]
            mean = totalGrades/totalSub
            varSum = 0
            for i in grades:
                x = i-mean
                varSum += float(x*x)

            variance = varSum / totalSub
            stDev = math.sqrt(variance)
            self.lblMean.setText("%.2f"%(mean))
            self.lblMedian.setText("%.2f"%(median))
            if len(mode_val) == len(grades):
                self.lblMode.setText("No Mode")
            else:
                mode = ', '.join(map(str, mode_val))
            self.lblMode.setText("%s"%(mode))
            self.lblRange.setText("%d"%(int(dataRange)))
            self.lblVariance.setText("%.2f"%(float(variance)))
            self.lblSD.setText("%.2f"%(float(stDev)))
        except Error as e:
            QMessagebox.about(self,"Error",str(e))

class SubjectReport(QDialog):

    c = sqlite3.connect('System.sqlite')

    def __init__(self):
        super(SubjectReport,self).__init__()
        loadUi('ui/subjectReport.ui',self)

        self.btnCompute.clicked.connect(self.compute)
        self.btnClear.clicked.connect(self.on_ClearButton_clicked)
        self.tableSubjects.clicked.connect(self.tableSubjectItem_changed)

        self.updateSubjectList()

        cur = self.c.cursor()


    def updateSubjectList(self):
        cur = self.c.cursor()
        self.tableSubjects.clear()
        rows = cur.execute("Select * From Subjects")
        self.tableSubjects.setHorizontalHeaderLabels(["Subject Code", "Subject Name"])
        self.tableSubjects.setRowCount(0)
        for row,row_data in enumerate(rows):
            self.tableSubjects.insertRow(row)
            for column,column_data in enumerate(row_data):
                self.tableSubjects.setItem(row, column, QTableWidgetItem(str(column_data)))

    def on_ClearButton_clicked(self):
        self.txtSubjectCode.clear()
        self.txtSName.clear()
        self.txtSubjectCode.setFocus()

    def tableSubjectItem_changed(self):
        cur = self.c.cursor()
        row = self.tableSubjects.currentRow()
        if row > -1:
            code = self.tableSubjects.item(row,0).text()
            rows = cur.execute('Select * From Subjects WHERE SubjectCode = ?', (code,))
            row = rows.fetchone()
            self.txtSubjectCode.setText(str(row[0]))
            self.txtSName.setText(str(row[1]))

    def compute(self):
        try:
            cur = self.c.cursor()
            code = self.txtSubjectCode.text()
            grades=[]
            totalGrades = 0
            totalStud=0
            totalSub=0
            rows = cur.execute('SELECT Grade FROM Records WHERE SubjectCode = ?', (code,))
        
            for row in rows:
                grades.append(float(row[0]))
                totalStud+=1

            for i in grades:
                totalGrades +=i
            subRows = cur.execute("Select * From Subjects")
            for row in subRows:
                totalSub+=1
            grades.sort()
            minimum = grades[0]
            maximum = grades[len(grades)-1]
            dataRange = maximum - minimum
            if len(grades) % 2 == 0:
               first_median = grades[len(grades) // 2]
               second_median = grades[len(grades) // 2 - 1]
               median = (first_median + second_median) / 2
            else:
               median = grades[len(grades) // 2]

            data = collections.Counter(grades)
            data_list = dict(data)
            max_value = max(list(data.values()))
            mode_val = [num for num, freq in data_list.items() if freq == max_value]
            mean = totalGrades/totalStud

            

            
            

            varSum = 0
            for i in grades:
                x = i-mean
                varSum += float(x*x)

            variance = varSum / totalStud
            stDev = math.sqrt(variance)
            self.lblMean.setText("%.2f"%(mean))
            self.lblMedian.setText("%.2f"%(median))
            if len(mode_val) == len(grades):
                self.lblMode.setText("No Mode")
            else:
                mode = ', '.join(map(str, mode_val))
                self.lblMode.setText("%s"%(mode))
            self.lblRange.setText("%d"%(int(dataRange)))
            self.lblVariance.setText("%.2f"%(float(variance)))
            self.lblSD.setText("%.2f"%(float(stDev)))
            self.c.commit()
            self.updateSubjectList()
        except Error as e:
            QMessagebox.about(self,"Error",str(e))

app = QApplication(sys.argv)
widget = Login()
widget.show()
sys.exit(app.exec())
