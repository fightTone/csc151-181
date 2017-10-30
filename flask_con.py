from flask import Flask, render_template, request
import sqlite3 as sql

app = Flask(__name__)

class Student(object):
    def __init__(self, idnum, firstname, lastname, middlename,sex, Course, Yr):
        self.id_no = idnum
        self.f_name = firstname
        self.l_name = lastname
        self.mid = middlename
        self.sex = sex
        self.course = Course
        self.Yr = Yr

conn = sql.connect('database.db')
conn.execute('CREATE TABLE IF NOT EXISTS stud_Courses (course_id TEXT PRIMARY KEY, c_name TEXT, College TEXT)')
cur =  conn.cursor()
cur.execute("INSERT OR IGNORE INTO stud_Courses (course_id, c_name, College)VALUES ('BSCS', 'Bachelor of Science in Computer Science', 'SCS' )" )
cur.execute("INSERT OR IGNORE INTO stud_Courses (course_id, c_name, College)VALUES ('BSIT', 'Bachelor of Science in Information Technology', 'SCS' )" )
cur.execute("INSERT OR IGNORE INTO stud_Courses (course_id, c_name, College)VALUES ('BSECT', 'Bachelor of Science in Electronics and Computer Technology', 'SCS' )" )
cur.execute("INSERT OR IGNORE INTO stud_Courses (course_id, c_name, College)VALUES ('ECET', 'Electrical and Computer Engineering Technology', 'SCS' )" )

conn.execute('CREATE TABLE IF NOT EXISTS studentRecord(ID TEXT PRIMARY KEY  NOT NULL CHECK(length(ID)=9), First_Name TEXT  CHECK(length(First_Name)>0 AND length(First_Name)<=20 ), Last_Name TEXT CHECK(length(Last_Name)>0 AND length(Last_Name)<=20 ), Middle_Name TEXT CHECK(length(Middle_Name)>0 AND length(Middle_Name)<=20 ) , Sex TEXT CHECK(length(Sex)=1), Course TEXT CHECK(length(Course)>0 AND length(Course)<=20 ), Yr_Lvl INTEGER CHECK(length(Yr_Lvl)=1), FOREIGN KEY(Course) REFERENCES stud_Courses(course_id))')


#conn.execute("SELECT  course_id, Last_Name, First_NAME, c_name, Yr_Lvl FROM studentRecord CROSS JOIN stud_Courses")


print "im executed"

conn.execute("CREATE VIEW IF NOT EXISTS result AS SELECT course_id, College, Last_Name, First_NAME, c_name, Yr_Lvl FROM studentRecord CROSS JOIN stud_Courses WHERE stud_Courses.course_id = studentRecord.Course")
conn.execute("CREATE VIEW IF NOT EXISTS ALL_info AS SELECT course_id, College, ID, Last_Name, First_NAME,Middle_Name, Sex, c_name, Yr_Lvl FROM studentRecord CROSS JOIN stud_Courses WHERE stud_Courses.course_id = studentRecord.Course")

#conn.execute("INSERT INTO result(course_id, Last_Name, First_NAME, Course_name, Yr_Lvl)")
#conn.execute("SELECT  course_id, Last_Name, First_NAME, c_name, Yr_Lvl FROM studentRecord CROSS JOIN stud_Courses")


print "we're joined"


print "table created successfully"

conn.close()



@app.route("/profile/<name>")
def profile(name):
    return render_template("profile.html", name=name)

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/add",methods = ['POST','GET'])
def add():
    return render_template("login.html")

@app.route("/adding",methods = ['POST','GET'])
def adding():
    if request.method == "POST":
        try:
            print "i'm performed.........................."
            id_number = request.form['id_number']
            print id_number
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            middle = request.form['Middle']
            sex =request.form['Sex']
            course = request.form['Course']
            Yr = request.form['Year']

            stud = Student(id_number,firstname,lastname,middle,sex,course,Yr)
            print "wwwoooooohhhhh............................"
            with sql.connect("database.db") as conn:
                cur = conn.cursor()
                print "im performed here........... fun add_entry"
                cur.execute("INSERT INTO studentRecord(ID,First_Name,Last_Name,Middle_Name, Sex, Course,Yr_Lvl) VALUES(?,?,?,?,?,?,?)",
                    (stud.id_no, stud.f_name, stud.l_name, stud.mid, stud.sex, stud.course,stud.Yr))
                conn.commit()

                print "wooohoooooooo"
                msg = "Record added successfully!"
        except:
            print " ERRORRRRRRRRR"
            conn.rollback()
            msg = "Error in insertion operation. The ID no. may already Existed or Maybe You leave some Blank info. erlier "

        finally:
            print "finally ariel happen to me"
            conn = sql.connect("database.db")
            conn.row_factory = sql.Row
            cur = conn.cursor()
            cur.execute("SELECT * FROM studentRecord")
            rows = cur.fetchall()
            return render_template("result.html", rows=rows, msg=msg)
            conn.close()





@app.route("/delete",methods=['POST', 'GET'])
def delete():
    conn = sql.connect("database.db")
    conn.row_factory = sql.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM studentRecord")
    rows = cur.fetchall()
    conn.close()
    return render_template("delete.html",rows=rows)

@app.route("/deleting",methods = ['POST','GET'])
def deleting():
    if request.method == "POST":
        try:
            id_number = request.form['id_number']
            print id_number
            with sql.connect("database.db") as conn:
                print "connected"
                cur = conn.cursor()
                cur.execute("SELECT * FROM studentRecord")
                for row in cur.fetchall():
                    print row
                    if row[0] == id_number:
                        cur.execute("DELETE FROM studentRecord WHERE ID = ?", (id_number,))
                        conn.commit()
                        msg = "Successfully Deleted"
                        break
                    else:
                        msg = "That student does not exist.. Who's that pokemon!"
        except:
            msg = "Fail to delete"
        finally:
            conn = sql.connect("database.db")
            conn.row_factory = sql.Row
            cur = conn.cursor()
            cur.execute("SELECT * FROM studentRecord")
            rows = cur.fetchall()
            return render_template("result.html", rows=rows,msg=msg)
        conn.close()


@app.route("/update",methods = ['POST', 'GET'])
def update():
    conn = sql.connect("database.db")
    conn.row_factory = sql.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM studentRecord")
    rows = cur.fetchall()
    return render_template("update.html",rows=rows)

@app.route("/updating",methods = ['POST', 'GET'])
def updating():
    if request.method == "POST":
        try:
            id_number = request.form['id_number']
            print "meeeee"
            with sql.connect("database.db") as conn:
                print "connected"
                cur = conn.cursor()
                cur.execute("SELECT * FROM studentRecord")
                for row in cur.fetchall():
                    if row[0] == id_number:
                        print row
                        copied = row
                        msg = " existed"
                        break
                    else:
                        msg = "uuuhmm... wait, Who's that Pokemon?"
                        copied = " "
        except:
            msg = "ERROR"
            copied=" "
        finally:
            return render_template("up.html", msg=msg, copied=copied)
            conn.close()

@app.route("/dating",methods = ['POST', 'GET'])
def dating():
    if request.method =="POST":
        try:
            id_number = request.form['id_number']
            print id_number
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            middle = request.form['Middle']
            sex = request.form['Sex']
            course = request.form['Course']
            Yr = request.form['Year']

            with sql.connect("database.db") as conn:
                cur = conn.cursor()
                cur.execute("SELECT * FROM studentRecord")
                for row in cur.fetchall():
                    print row
                    if row[0] == id_number:
                        print id_number
                        cur.execute("UPDATE studentRecord set First_Name = ?, Last_Name = ?, Middle_Name = ?,  Sex = ?, Course = ?, Yr_Lvl = ? where ID = ?",
                            ( firstname, lastname, middle, sex, course,Yr,id_number))
                        conn.commit()
                        msg = "successfully UPDATED"
                        break
                    elif not row[0] == id_number:
                        msg = "ERROR. You cannot Change your ID no."

        except:
            msg = "FAIL to UPDATE"
        finally:
            conn = sql.connect("database.db")
            conn.row_factory = sql.Row
            cur = conn.cursor()
            cur.execute("SELECT * FROM studentRecord")
            rows = cur.fetchall()
            return render_template("result.html", rows=rows, msg=msg)
            conn.close()


@app.route("/list")
def show_list():
    conn = sql.connect("database.db")
    conn.row_factory = sql.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM studentRecord")
    rows = cur.fetchall()

    conn.close()
    return render_template("list.html",rows=rows)

@app.route("/CourseTable")
def CourseTable():
    conn = sql.connect("database.db")

    conn.row_factory = sql.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM result")
    rows = cur.fetchall()

    conn.close()

    return render_template("cur_tab.html", rows=rows)

@app.route("/search",methods = ['POST', 'GET'])
def search():
    return render_template("search.html")

@app.route("/searching",methods = ['POST', 'GET'])
def searching():
    if request.method == "POST":
        try :
            dis = request.form["srch"]
            print dis

            conn = sql.connect("database.db")
            cur = conn.cursor()
            cur.execute("SELECT * FROM ALL_info where course_id = ? or First_Name = ? or c_name=? or Last_Name=? or Middle_Name=? or ID = ? or College=? or Sex=? or Yr_Lvl=?", (dis,dis,dis,dis,dis,dis,dis,dis,dis))
            print "im still performed"
            coffee = cur.fetchall()
            msg = "existed"
            '''for row in cur.fetchall():
    #coffee = row
    print coffee
    msg = "existed"'''

        except:
            msg = "ERROR"
        finally:
            print coffee
            print " copied"
            print "the message: " + msg
            return render_template("exist.html", msg=msg, coffee=coffee)


@app.route("/course_mangr")
def course_mangr():
    conn = sql.connect("database.db")
    conn.row_factory = sql.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM stud_Courses")
    rows = cur.fetchall()
    conn.close()
    return render_template("crs_tab.html", rows=rows)

@app.route("/course_add",methods = ['GET','POST'])
def course_add():
    return render_template("c_add.html")

@app.route("/added_cur",methods = ['GET','POST'])
def added_cur():
    crsid = request.form['courseID']
    crsn = request.form['courseName']
    clg = request.form['college']

    with sql.connect("database.db") as conn:
        if request.method == "POST":
            try:
                cur = conn.cursor()
                cur.execute("INSERT INTO stud_Courses(course_id,c_name,College) VALUES(?,?,?)",(crsid,crsn,clg))
                conn.commit()

            except:
                print"error"
                conn.rollback()
            finally:
                conn = sql.connect("database.db")
                conn.row_factory = sql.Row
                cur = conn.cursor()
                cur.execute("SELECT * FROM stud_Courses")
                rows = cur.fetchall()
                conn.close()
                return render_template("crs_tab.html", rows=rows)
        conn.close()


@app.route("/course_del",methods = ['GET','POST'])
def course_del():
    return render_template("c_del.html")


@app.route("/del_cur",methods = ['GET','POST'])
def del_cur():
    crsid = request.form['courseID']

    with sql.connect("database.db") as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM stud_Courses WHERE course_id = ?", (crsid,))
        conn.row_factory = sql.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM stud_Courses")
        rows = cur.fetchall()
        return render_template("crs_tab.html", rows=rows)

    conn.close()


@app.route("/course_up",methods = ['GET','POST'])
def course_up():
    return render_template("c_up.html")

@app.route("/up_cur",methods = ['GET','POST'])
def up_cur():
    with sql.connect("database.db") as conn:
        up_dis = request.form['courseID']
        n_id =  request.form['ncourseID']
        n_name = request.form['cname']
        n_col = request.form['col']
        cur = conn.cursor()
        cur.execute("UPDATE stud_Courses set course_id = ?, c_name = ?, College = ? where course_id = ?",( n_id, n_name,n_col,up_dis))
        conn.commit()
        conn.row_factory = sql.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM stud_Courses")
        rows = cur.fetchall()
        return render_template("crs_tab.html", rows=rows)
    conn.close()


@app.route("/course_src",methods = ['GET','POST'])
def course_src():
    return render_template("c_src.html")

@app.route("/src_cur",methods = ['GET','POST'])
def src_cur():
    dis = request.form["src"]
    print dis

    conn = sql.connect("database.db")
    cur = conn.cursor()
    conn.row_factory = sql.Row
    cur.execute("SELECT * FROM stud_Courses where course_id = ? or c_name=? or College=?", (dis,dis,dis))
    rows = cur.fetchall()
    print rows
    return render_template("crs_exist.html", rows=rows)

if __name__ == "__main__":
    app.run(debug=True)