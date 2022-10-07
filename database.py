
import sqlite3

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
StudentCode VARCHAR(10) NOT NULL,
SubjectCode VARCHAR(10) NOT NULL,
Grade FLOAT(50) NOT NULL,
FOREIGN KEY (StudentCode) REFERENCES Students(StudentCode),
FOREIGN KEY (SubjectCode) REFERENCES Subjects(SubjectCode),
PRIMARY KEY (SubjectCode,StudentCode)
);
''')

conn.commit()
conn.close()
