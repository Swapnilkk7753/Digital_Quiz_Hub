from flask import Flask,render_template,url_for,redirect,request,session,flash,jsonify
import sqlite3 as sq
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash


app=Flask(__name__)
app.secret_key="supersecret"

#global Variable


#Database creation for userinfo
def init_db():
    conn=sq.connect("UserInfo.db")
    cur=conn.cursor()
    cur.execute('''create table if not exists UserData(id integer primary key autoincrement,Name text not null, Email text not null unique,Password text not null unique, Role text check(Role in ('admin','user')) default 'user',Active_Status integer default 1 , Registered_Time DATETIME DEFAULT Current_timestamp) 
                ''')
    conn.commit()
    conn.close()


#Database creation for categoryinfo
def init_db_Category():
    conn=sq.connect("CategoryInfo.db")
    cur=conn.cursor()
    cur.execute('''create table if not exists CategoryData(id integer primary key autoincrement,Category_Name text not null, Active_Status integer default 1,Total_Quiz integer default 0) 
                ''')
    conn.commit()
    conn.close()


#Database creation for categoryinfo_Quizz
def init_db_Quizz():
    conn=sq.connect("CategoryInfo.db")
    cur=conn.cursor()
    cur.execute('''create table if not exists QuizzData(id integer primary key autoincrement,Quizz_Title text not null,Category_Name text not null,Time integer not null, Active_Status integer default 1,Total_que integer default 0) 
                ''')
    conn.commit()
    conn.close()


#Database creation for categoryinfo_Question
def init_db_Quetion():
    conn=sq.connect("CategoryInfo.db")
    cur=conn.cursor()
    cur.execute('''create table if not exists QuestionData(id integer primary key autoincrement,Quizz_Title text not null,Question_Name text not null,Correct text not null,A text not null, B text not null,C text not null,D text not null,Active_Status integer default 1) 
                ''')
    conn.commit()
    conn.close()

#Database creation for UserQuizInfo_Question
def init_db_User_Quiz_Info():
    conn=sq.connect("UserInfo.db")
    cur=conn.cursor()
    cur.execute('''create table if not exists UserQuizData(id integer primary key autoincrement,Name text not null, Email text not null,Quizz_Title text not null,Category_Name text not null,Question_Name text not null,User_Answer text not null,Correct text not null,Date DATETIME DEFAULT Current_timestamp,Score integer not null) 
                ''')
    conn.commit()
    conn.close()
#Database creation for UserQuizResultInfo_Question
def init_db_User_Result_Info():
    conn=sq.connect("UserInfo.db")
    cur=conn.cursor()
    cur.execute('''create table if not exists UserResultData(id integer primary key autoincrement,Name text not null, Email text not null,Quizz_Title text not null,Category_Name text not null,Date DATETIME DEFAULT Current_timestamp,Score integer not null,Total_Que integer not null) 
                ''')
    conn.commit()
    conn.close()

#Database creation for userEnquiry
def init_db_Eq():
    conn=sq.connect("UserInfo.db")
    cur=conn.cursor()
    cur.execute('''create table if not exists UserEnquiry(id integer primary key autoincrement,Name text not null, Email text not null ,Message text not null unique,Active_Status integer default 1) 
                ''')
    conn.commit()
    conn.close()



@app.route("/")
def home():
    init_db()
    init_db_Category()
    init_db_User_Quiz_Info()
    init_db_User_Result_Info()
    init_db_Quetion()
    init_db_Quizz()
    init_db_Eq()

    session.pop("qui",None)
    session.pop("user",None)
    session.pop("role",None)
    session["ur"]="1"
    return render_template('Home.html',user=session["ur"])
@app.route("/Home")
def homep():
    return render_template('Home.html',user=session["ur"])
@app.route("/About")
def about():
    return render_template('about.html')


#category management
@app.route("/Admin_categories")
def admin_cat():
    if session["role"]=='admin':
      return render_template('admin_categories.html')
    return redirect(url_for('admin_d'))
@app.route("/Admin_category_d")
def admin_category_d():
    rwu=categoryinfo()
    user_l=[]
    for user in rwu:
        user_l.append({"id":user[0],"Name":user[1],"active":bool(user[2])})
    return jsonify(users=user_l)
@app.route("/Admin_categories_active/<int:id>",methods=["POST"])
def toggleStatusCategory(id):
    conn=sq.connect("CategoryInfo.db")
    cur=conn.cursor()
    cur.execute("SELECT Active_Status,Category_Name FROM CategoryData WHERE id=?",(id,))
    rw=cur.fetchone()
    Active_status=0 if rw[0] else 1
    quizzEnable(Active_status,rw[1])
    cur.execute("UPDATE CategoryData SET Active_Status=? WHERE id=?",(Active_status,id))
    conn.commit()
    conn.close()
    return {"active": bool(Active_status)}
@app.route("/Admin_categories_delete/<int:id>",methods=["POST"])
def delete_cate(id):
    conn=sq.connect("CategoryInfo.db")
    cur=conn.cursor()
    quizzDelete(id)
    cur.execute("DELETE FROM CategoryData WHERE id=?",(id,))
    conn.commit()
    conn.close()
    return {"delete"}
@app.route("/addCategory",methods=["POST","GET"])
def addcategory():
    if request.method=="POST":
        cat=request.form.get("Category")
        conn=sq.connect("CategoryInfo.db")
        cur=conn.cursor()    
        cur.execute("insert into CategoryData(Category_Name) values(?)",
                        (cat,))
        conn.commit()
        conn.close()
        return render_template('admin_categories.html')
    

@app.route("/Admin_dashboard" ,methods=["POST","GET"])
def admin_d():
    if session["role"]=='admin':
      return render_template('admin_dashboard.html',name=session["user"],email=session["Email"],qz=len(quizzcategoryinfo()),ur=len(userinfo()),qs=len(questioncategoryinfo()),Ta=len(resultListDispAll()))
    return render_template('login.html')

#Enquiry Management
@app.route("/Admin_enquiries")
def admin_enquiries():
 if session["role"]=='admin':
    return render_template('admin_enquiries.html')
 return redirect(url_for('admin_d'))

@app.route("/Admin_enquiry_d")
def admin_enqu_d():
    rwu=getEnquiry()
    enq=[]
    for user in rwu:
        enq.append({"id":user[0],"name":user[1],"email":user[2],"message":user[3],"read":bool(user[4])})
    return jsonify(users=enq)

@app.route("/Admin_enquiry_active/<int:id>",methods=["POST"])
def statusEnquiry(id):
    conn=sq.connect("UserInfo.db")
    cur=conn.cursor()
    cur.execute("SELECT Active_Status FROM UserEnquiry WHERE id=?",(id,))
    rw=cur.fetchone()
    Active_status=0 if rw[0] else 1
    cur.execute("UPDATE UserEnquiry SET Active_Status=? WHERE id=?",(Active_status,id))
    conn.commit()
    conn.close()
    return {"active": bool(Active_status)}

@app.route("/Admin_enquiry_delete/<int:id>",methods=["POST"])
def deleEnquiry(id):
    conn=sq.connect("UserInfo.db")
    cur=conn.cursor()
    cur.execute("Delete FROM UserEnquiry WHERE id=?",(id,))
    conn.commit()
    conn.close()
    return {"active"}

#question Management
@app.route("/Admin_questions")
def admin_questions():
    if session["role"]=='admin':
     quiz=quizzcategoryinfo()
     return render_template('admin_questions.html',quizz=quiz)
    return redirect(url_for('admin_d'))
@app.route("/Admin_questions_d")
def admin_questions_d():
    rwu=questioncategoryinfo()
    question=[]
    for user in rwu:
        question.append({"id":user[0],"quiz":user[1],"text":user[2],"correct":user[3],"active":bool(user[4])})
    return jsonify(questions=question)
@app.route("/Admin_questions_delete/<int:id>",methods=["POST"])
def delete_questions(id):
    conn=sq.connect("CategoryInfo.db")
    cur=conn.cursor()
    cur.execute("DELETE FROM QuestionData WHERE id=?",(id,))
    conn.commit()
    conn.close()
    return {"delete"}


@app.route("/addquestions",methods=["POST","GET"])
def addquestion():
    if request.method=="POST":
        quiz=request.form.get("Quiz")
        ques=request.form.get("Question")
        A=request.form.get("Op1")
        B=request.form.get("Op2")
        C=request.form.get("Op3")
        D=request.form.get("Op4")
        correct=request.form.get("C_op")
        if correct=="A":
            correct=A
        elif correct=="B":
            correct=B
        elif correct=="C":
            correct=C
        elif correct=="D":
            correct=D
        conn=sq.connect("CategoryInfo.db")
        cur=conn.cursor()    
        cur.execute("insert into QuestionData(Quizz_Title,Question_Name,Correct,A,B,C,D) values(?,?,?,?,?,?,?)",
                        (quiz,ques,correct,A,B,C,D))
        conn.commit()
        conn.close()
        quiz=quizzcategoryinfo()
        return render_template('admin_questions.html',quizz=quiz)
    


#Quiz Management
@app.route("/Admin_quizzes")
def admin_quizzes():
    if session["role"]=='admin':
     rwu=categoryinfo()
     return render_template('admin_quizzes.html',cate=rwu)
    return redirect(url_for('admin_d'))
@app.route("/Admin_quizzes_d")
def admin_quizzes_d():
    rwu=quizzcategoryinfo()
    quizzes=[]
    for user in rwu:
        quizzes.append({"id":user[0],"title":user[1],"category":user[2],"time":user[3],"active":bool(user[4])})
    return jsonify(quizzes=quizzes)
@app.route("/Admin_quizzes_active/<int:id>",methods=["POST"])
def toggleStatusQuizz(id):
    conn=sq.connect("CategoryInfo.db")
    cur=conn.cursor()
    cur.execute("SELECT Active_Status ,Quizz_Title FROM QuizzData WHERE id=?",(id,))
    rw=cur.fetchone()
    Active_status=0 if rw[0] else 1
    questionEnable(rw[1],Active_status)
    cur.execute("UPDATE QuizzData SET Active_Status=? WHERE id=?",(Active_status,id))
    conn.commit()
    conn.close()
    return {"active": bool(Active_status)}
@app.route("/Admin_quizzes_delete/<int:id>",methods=["POST"])
def delete_quizz(id):
    conn=sq.connect("CategoryInfo.db")
    cur=conn.cursor()
    questionDelete(id)
    cur.execute("DELETE FROM QuizzData WHERE id=?",(id,))
    conn.commit()
    conn.close()
    return {"delete"}
@app.route("/addquizzes",methods=["POST","GET"])
def addquizzes():
    if request.method=="POST":
        quiz=request.form.get("Quizz_Title")
        cat=request.form.get("Category")
        tim=request.form.get("Time")
        conn=sq.connect("CategoryInfo.db")
        cur=conn.cursor()    
        cur.execute("insert into QuizzData(Quizz_Title,Category_Name,Time) values(?,?,?)",
                        (quiz,cat,tim))
        conn.commit()
        conn.close()
        rwu=categoryinfo()
        return render_template('admin_quizzes.html',cate=rwu)

#Result Management
@app.route("/Admin_results")
def admin_results():
    if session["role"]=='admin':
     return render_template('admin_results.html')
    return redirect(url_for('admin_d'))
@app.route("/Admin_results_d")
def admin_results_d():
    rwu=resultListDispAll()
    results=[]
    for user in rwu:
        results.append({"id":user[0],"user":user[1],"quiz":user[3],"score":user[6],"total":user[7]})
    return jsonify(results=results)


#user management
@app.route("/Admin_users")
def admin_users():
    if session["role"]=='admin':
     return render_template('admin_users.html')
    return redirect(url_for('admin_d'))
@app.route("/Admin_users_d")
def admin_users_d():
    rwu=userinfon()
    user_l=[]
    for user in rwu:
        user_l.append({"id":user[0],"Name":user[1],"Email":user[2],"active":bool(user[3])})
    return jsonify(users=user_l)
@app.route("/Admin_users_active/<int:id>",methods=["POST"])
def toggleStatus(id):
    conn=sq.connect("UserInfo.db")
    cur=conn.cursor()
    cur.execute("SELECT Active_Status FROM UserData WHERE id=?",(id,))
    rw=cur.fetchone()
    Active_status=0 if rw[0] else 1
    cur.execute("UPDATE UserData SET Active_Status=? WHERE id=?",(Active_status,id))
    conn.commit()
    conn.close()
    return {"active": bool(Active_status)}
@app.route("/Admin_users_delete/<int:id>",methods=["POST"])
def delete_user(id):
    conn=sq.connect("UserInfo.db")
    cur=conn.cursor()
    cur.execute("DELETE FROM UserData WHERE id=?",(id,))
    conn.commit()
    conn.close()
    return {"delete"}

#Available quizzes
@app.route("/Available_quizzes")
def available_quizzes():
    rwu=availablecategoryinfo()
    if len(rwu)!=0:
     for i in rwu:
        updatCateTota(i[1])
     rwu=availablecategoryinfo()
    return render_template('available_quizzes.html',cate=rwu)

@app.route("/ExploreBtn",methods=["GET","POST"])
def exploreBtn():
    cat=request.form.get("Explore")
    session["cat"]=cat
    rw=availablequizzinfo(cat)
    if len(rw)!=0:
        for i in rw:
            updatQuiTota(i[1])
        rw=availablequizzinfo(cat)
    return render_template('available_quizzes_list.html',rw=rw)

@app.route("/Explore_Quiz",methods=["POST","GET"])
def explorequiz():
    qui=request.form.get("ExploreQuiz")
    session["qui"]=qui
    rw=availablequestioninfo(qui)
    t=quizTime(session["cat"],qui)
    session["count"]=0
    return render_template('quiz_attemp.html',rw=rw,i=session["count"],l=len(rw),t=t)

def quizTime(cat,qui):
    conn=sq.connect("CategoryInfo.db")
    cur=conn.cursor()
    conn.commit()
    cur.execute("SELECT Time FROM QuizzData where Category_Name=? and Active_Status=? and Quizz_Title=?",(cat,1,qui))
    return cur.fetchall()    

@app.route("/Next_available_question",methods=["POST","GET"])
def next_available_question():
    rw=availablequestioninfo(session["qui"])
    que=rw[session["count"]][2] 
    cor=rw[session["count"]][3] 
    t=quizTime(session["cat"],session["qui"])
    op=request.form.get("q1")
    if op==None:
        op="UnAttempted"
        sco=0
    elif cor==op:
        sco=1
    else:
        sco=0
    #ql=userQuizzeslist()
    ql=userQuizzeslistsp(que)
    if len(ql)==0:
        userQuizzes(session["user"],session["Email"],session["qui"],session["cat"],que,op,cor,sco,len(rw))
    elif ql[0][5]==que and session["Email"]==ql[0][2]:
        updateuserQuizzes(session["user"],session["Email"],session["qui"],session["cat"],que,op,sco,len(rw))
    else:
       userQuizzes(session["user"],session["Email"],session["qui"],session["cat"],que,op,cor,sco,len(rw))
    if session["count"]==len(rw)-1:
         resultListUpd(session["user"],session["Email"],session["qui"],session["cat"],len(rw))
         r=resultListdi(session["user"],session["Email"],session["qui"],session["cat"])
         
         return render_template('result.html',t=len(rw),r=r)
    session["count"]=session["count"]+1
    return render_template('Quiz_attemp.html',rw=rw,i=session["count"],l=len(rw),t=t)

@app.route("/Pre_available_question",methods=["POST","GET"])
def pre_available_question():
    session["count"]=session["count"]-1
    if session["count"]<=0:
        session["count"]=0
    rw=availablequestioninfo(session["qui"])
    return render_template('Quiz_attemp.html',rw=rw,i=session["count"],l=len(rw),t=quizTime(session["cat"],session["qui"])
)

@app.route("/Submit_Quizz",methods=["POST","GET"])
def submit_qu():
 stt=request.form.get("stt")
 if stt=="1":
  rw=availablequestioninfo(session["qui"])
  to=session["count"]
  for i in range(to,len(rw)):
    que=rw[session["count"]][2] 
    cor=rw[session["count"]][3] 
    t=quizTime(session["cat"],session["qui"])
    op=request.form.get("q1")
    if op==None:
        op="UnAttempted"
        sco=0
    elif cor==op:
        sco=1
    else:
        sco=0
    ql=userQuizzeslistsp(que)
    if len(ql)==0:
        userQuizzes(session["user"],session["Email"],session["qui"],session["cat"],que,op,cor,sco,len(rw))
    elif ql[0][5]==que and session["Email"]==ql[0][2]:
        updateuserQuizzes(session["user"],session["Email"],session["qui"],session["cat"],que,op,sco,len(rw))
    else:
       userQuizzes(session["user"],session["Email"],session["qui"],session["cat"],que,op,cor,sco,len(rw))
    if session["count"]==len(rw)-1:
         resultListUpd(session["user"],session["Email"],session["qui"],session["cat"],len(rw))
         r=resultListdi(session["user"],session["Email"],session["qui"],session["cat"])
         return render_template('result.html',t=len(rw),r=r)
    session["count"]=session["count"]+1
 else:
     session["count"]=session["count"]-1
     return redirect(url_for('next_available_question'))
    
  
  

def total_Qu(cat):
     conn=sq.connect("CategoryInfo.db")
     cur=conn.cursor()
     cur.execute("select * from QuizzData where Category_Name=?",(cat,))
     return cur.fetchall()

def updatCateTota(cat):
     conn=sq.connect("CategoryInfo.db")
     cur=conn.cursor()
     cur.execute("update CategoryData set Total_Quiz=? where Category_Name=?",(len(total_Qu(cat)),cat))
     conn.commit()
     conn.close()
 
def total_Que(qui):
     conn=sq.connect("CategoryInfo.db")
     cur=conn.cursor()
     cur.execute("select * from QuestionData where Quizz_Title=?",(qui,))
     return cur.fetchall()


def updatQuiTota(qui):
     conn=sq.connect("CategoryInfo.db")
     cur=conn.cursor()
     cur.execute("update QuizzData set Total_que=? where Quizz_Title=?",(len(total_Que(qui)),qui))
     conn.commit()
     conn.close()


@app.route("/Contact")
def contact():
    return render_template('contact.html')

@app.route("/SubmitEnquiry",methods=["GET","POST"])
def enqu():
    if request.method=="POST":
        Na=request.form.get("Name")
        Em=request.form.get("Email")
        Mg=request.form.get("Msg")
        conn=sq.connect("UserInfo.db")
        cur=conn.cursor()
        cur.execute("insert into UserEnquiry(Name,Email,Message) values(?,?,?)",(Na,Em,Mg))
        conn.commit()
        conn.close()
    return render_template("contact.html")

def getEnquiry():
    conn=sq.connect("UserInfo.db")
    cur=conn.cursor()
    cur.execute("select * from UserEnquiry")
    return cur.fetchall()

@app.route("/Dashboard",methods=["GET","POST"])
def dashboard():
   if "user" in session: 
    if session["role"]=="admin":
        return render_template("login.html")
    rw=resultListDisp(session["user"],session["Email"])
    p=totalQuizzpass()
    avg=totalQuizzavg()
    return render_template('dashboard.html',name=session["user"],email=session["Email"],p=p,rw=rw,avg=avg,le=len(rw))
   else:
           return render_template('login.html')

@app.route("/Forgot_password")
def forgot():
    return render_template('forgot_password.html')
@app.route("/Index")
def index():
    return render_template('index.html',user=session["ur"])
@app.route("/Login")
def login():
    return render_template('login.html')
@app.route("/Logout")
def logout():
    session.pop("user",None)
    session.pop("role",None)
    session.pop("qui",None)

    session["ur"]="1"
    return render_template('Home.html',user=session["ur"])
@app.route("/My_quizzes")
def my_quizzes():
    rw=resultListDisp(session["user"],session["Email"])
    return render_template('my_quizzes.html',rw=rw)

@app.route("/View_Result",methods=["POST","GET"])
def viewResult():
    cat=request.args.get("cat")
    qui=request.args.get("qui")
    rw=quizGetData(cat,qui)
    return render_template('view_results.html',rw=rw)

def quizGetData(cat,qui):
    conn=sq.connect("UserInfo.db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM UserQuizData where Name=? and Email=? and Category_Name=? and Quizz_Title=?",(session["user"],session["Email"],cat,qui))
    return cur.fetchall()


@app.route("/Privacy")
def privacy():
    return render_template('privacy.html')
@app.route("/Quiz_attemp")
def quiz_attemp():
    return render_template('quiz_attemp.html')
@app.route("/Quizzes")
def quizzes():
    if "user" in session:
      rwu=availablecategoryinfo()
      return render_template('available_quizzes.html',cate=rwu)
    return render_template('login.html')
@app.route("/Recent")
def Recent():
    return render_template('Recent.html')
@app.route("/Register")
def register():
    return render_template('Register.html')
@app.route("/Result")
def result():
   if "qui" in session: 
    rw=availablequestioninfo(session["qui"])
    r=resultListdi(session["user"],session["Email"],session["qui"],session["cat"])
    if len(r)!=0:
     return render_template('result.html',r=r,t=len(rw))
   return render_template('Result_hide.html')
@app.route("/Terms")
def terms():
    return render_template('terms.html')

#register user
@app.route("/RegisterUser",methods=["POST"])
def RegisterUser():
    if request.method=="POST":
        Name=request.form.get("FullName")
        Email=request.form.get("Email")
        Password=request.form.get("Password")
        CPassword=request.form.get("CPassword")
        
        if Password==CPassword:
            Hash_pass=generate_password_hash(Password,method='pbkdf2:sha256',salt_length=16)
            conn=sq.connect("UserInfo.db")
            cur=conn.cursor()
            try:
              cur.execute('insert into UserData(Name,Email,Password) values(?,?,?)',
                        (Name,Email,Hash_pass))
              #cur.execute('insert into UserData(Name,Email,Password,Role) values(?,?,?,?)',
               #         (Name,Email,Hash_pass,'admin'))
              conn.commit()
            except sq.IntegrityError:
                return ''' <h1>User already exists<h1>'''
            finally:
              conn.close()
            return redirect(url_for('login'))
        return render_template("Register.html")
    
@app.route("/Register_Status/<n>/<e>/<p>/<cp>",methods=["GET","POST"])
def reg_st(n,e,p,cp):  
       conn=sq.connect("UserInfo.db")
       cur=conn.cursor()
       conn.commit()
       cond='''select Name,Email,Password,Role from UserData where Email=?'''
       cur.execute(cond,(e,))
       rw=cur.fetchone()
       if rw is None:
           if (p==cp):
             return jsonify({"sta":0,"mess":"Candidate Register successfully","url":"/Login"})
           else:
             return jsonify({"sta":0,"mess":"Password Unmatched","url":"/Register"})
       else:
            return jsonify({"sta":0,"mess":"User Already Exists","url":"/Login"})


#Login User
@app.route("/LoginUser",methods=["GET","POST"])
def LoginUser():
    if request.method=="POST": 
       Email=request.form.get("Email")
       Password=request.form.get("Password")
       conn=sq.connect("UserInfo.db")
       cur=conn.cursor()
       conn.commit()
       cond='''select Name,Email,Password,Role from UserData where Email=?'''
       cur.execute(cond,(Email,))
       rw=cur.fetchone()
       if rw is None:
           return redirect(url_for('login'))
       else:
           if check_password_hash(rw[2],Password):
             session["ur"]="0"
             session["user"]=rw[0]
             session["Email"]=rw[1]
             session["role"]=rw[3]
             if rw[3]=="user":
               return redirect(url_for('dashboard'))
             elif rw[3]=="admin":
               return redirect(url_for('admin_d'))
    return redirect(url_for('login'))

@app.route("/Login_sta/<email>/<passw>",methods=["GET","POST"])
def stat(email,passw):
       conn=sq.connect("UserInfo.db")
       cur=conn.cursor()
       conn.commit()
       cond='''select Name,Email,Password,Role ,Active_Status from UserData where Email=?'''
       cur.execute(cond,(email,))
       rw=cur.fetchone()
       if rw is None:
           return jsonify({"sta":0,"mess":"Login Failed! Plese Register","url":"/Login"})
       elif (check_password_hash(rw[2],passw)):
           if (rw[3]=="user" and rw[4]==1):
            return jsonify({"sta":0,"mess":" User login Successfully","url":"/Dashboard"})
           if (rw[3]=="user" and rw[4]==0):
            return jsonify({"sta":0,"mess":"Admin Blocked You","url":"/Login"})
           elif (rw[3]=="admin"):
            return jsonify({"sta":0,"mess":" Admin login Successfully","url":"/Admin_dashboard"})
       else:
         return jsonify({"sta":0,"mess":" Password Incorrect","url":"/Login"})
           
       

    

#Forget Password
@app.route("/ForgotUser", methods=["POST"])
def forgetbtn():
        if request.method=="POST":
            em=request.form.get("Email")
            p=request.form.get("new_password")
            cp=request.form.get("confirm_password")
            if p==cp:
              Hash_pass=generate_password_hash(p,method='pbkdf2:sha256',salt_length=16)
      
            conn=sq.connect("UserInfo.db")
            cur=conn.cursor()
            conn.commit()
            cur.execute("update UserData set Password=? WHERE Email=?",(Hash_pass,em))
            rw=cur.fetchone()
            conn.commit()
            conn.close()
            return redirect(url_for('forgot'))
        
@app.route("/forgot_sta/<email>/<p>/<cp>",methods=["GET","POST"])
def forstat(email,p,cp):
       conn=sq.connect("UserInfo.db")
       cur=conn.cursor()
       conn.commit()
       cond='''select Name,Email,Password,Role ,Active_Status from UserData where Email=?'''
       cur.execute(cond,(email,))
       rw=cur.fetchone()
       if rw is None:
           return jsonify({"sta":0,"mess":"User not exist! Plese Register","url":"/Register"})
       else:
         if p==cp:
           return jsonify({"sta":0,"mess":" Password Reset Successfully","url":"/Login"})
         else:
            return jsonify({"sta":0,"mess":" Password UnMatched","url":"/Forgot_password"})

        
        
#Getting user from database
def userinfo():
    conn=sq.connect("UserInfo.db")
    cur=conn.cursor()
    conn.commit()
    cur.execute("SELECT id,Name, Email,Active_Status FROM UserData")
    return cur.fetchall()
def userinfon():
    conn=sq.connect("UserInfo.db")
    cur=conn.cursor()
    conn.commit()
    cur.execute("SELECT id,Name, Email,Active_Status FROM UserData where Role=?",('user',))
    return cur.fetchall()
def categoryinfo():
    conn=sq.connect("CategoryInfo.db")
    cur=conn.cursor()
    conn.commit()
    cur.execute("SELECT id,Category_Name,Active_Status FROM CategoryData")
    return cur.fetchall()
def quizzcategoryinfo():
    conn=sq.connect("CategoryInfo.db")
    cur=conn.cursor()
    conn.commit()
    cur.execute("SELECT id ,Quizz_Title ,Category_Name ,Time ,Active_Status FROM QuizzData")
    return cur.fetchall()
def quizzEnable(sta,name):
    conn=sq.connect("CategoryInfo.db")
    cur=conn.cursor()
    cur.execute("UPDATE QuizzData SET Active_Status=? WHERE Category_Name=?",(sta,name))
    conn.commit()
    cur.execute("select Quizz_Title from QuizzData where Category_Name=?",(name,))
    rw=cur.fetchall()
    for r in rw:
        questionEnable(r[0],sta)
    conn.close()
def quizzDelete(id):
    conn=sq.connect("CategoryInfo.db")
    cur=conn.cursor()
    cur.execute("select Category_Name FROM CategoryData WHERE id=?",(id,))
    rw=cur.fetchone()
    cur.execute("select Quizz_Title FROM QuizzData WHERE Category_Name=?",(rw[0],))
    rwu=cur.fetchall()
    cur.execute("DELETE FROM QuizzData WHERE Category_Name=?",(rw[0],))
    conn.commit()
    conn.close()
    for r in rwu:
        questionDeleteq(r[0])
def questioncategoryinfo():
    conn=sq.connect("CategoryInfo.db")
    cur=conn.cursor()
    cur.execute("SELECT id ,Quizz_Title ,Question_Name ,Correct ,Active_Status FROM QuestionData where Active_Status=?",(1,))
    conn.commit()
    return cur.fetchall()
def questionEnable(quiz,sta):
    conn=sq.connect("CategoryInfo.db")
    cur=conn.cursor()
    cur.execute("UPDATE QuestionData SET Active_Status=? WHERE Quizz_Title=?",(sta,quiz))
    conn.commit()
    conn.close()
def questionDelete(id):
    conn=sq.connect("CategoryInfo.db")
    cur=conn.cursor()
    cur.execute("select Quizz_Title FROM QuizzData WHERE id=?",(id,))
    rw=cur.fetchone()
    cur.execute("DELETE FROM QuestionData WHERE Quizz_Title=?",(rw[0],))
    conn.commit()
    conn.close()
def questionDeleteq(id):
    conn=sq.connect("CategoryInfo.db")
    cur=conn.cursor()
    cur.execute("DELETE FROM QuestionData WHERE Quizz_Title=?",(id,))
    conn.commit()
    conn.close()
def quizUserResult():
    conn=sq.connect("UserInfo.db")
    cur=conn.cursor()
    cur.execute("select * FROM UserQuizData WHERE Name=? and Email=?",(session["user"],session["Email"]))
    return cur.fetchall()
def availablequizzinfo(cat):
    conn=sq.connect("CategoryInfo.db")
    cur=conn.cursor()
    conn.commit()
    cur.execute("SELECT id ,Quizz_Title ,Category_Name ,Time ,Active_Status ,Total_que FROM QuizzData where Category_Name=? and Active_Status=?",(cat,1))
    return cur.fetchall()    
def availablecategoryinfo():
    conn=sq.connect("CategoryInfo.db")
    cur=conn.cursor()
    conn.commit()
    cur.execute("SELECT id,Category_Name,Active_Status,Total_Quiz FROM CategoryData where Active_Status=?",(1,))
    return cur.fetchall()
def availablequestioninfo(qui):
    conn=sq.connect("CategoryInfo.db")
    cur=conn.cursor()
    cur.execute("SELECT id ,Quizz_Title ,Question_Name ,Correct,A,B,C,D,Active_Status FROM QuestionData where Active_Status=? and Quizz_Title=?",(1,qui))
    conn.commit()
    return cur.fetchall()
def userQuizzes(n,e,qz,ca,qu,a,c,s,t):
    conn=sq.connect("UserInfo.db")
    cur=conn.cursor()
    cur.execute('insert into UserQuizData(Name,Email,Quizz_Title,Category_Name,Question_Name,User_Answer,Correct,Score) values(?,?,?,?,?,?,?,?)',(n,e,qz,ca,qu,a,c,s))
    conn.commit()
    if len(resultListDis(n,e,qz,ca))==0:
       resultList(n,e,qz,ca,s,t)
    else:
       resultListUpd(n,e,qz,ca,t)
def userQuizzeslist():
    conn=sq.connect("UserInfo.db")
    cur=conn.cursor()
    cur.execute("select * from  UserQuizData")
    return cur.fetchall()

def userQuizzeslistsp(q):
    conn=sq.connect("UserInfo.db")
    cur=conn.cursor()
    cur.execute("select * from  UserQuizData where Name=? and Email=? and Question_Name=?",(session["user"],session["Email"],q))
    return cur.fetchall()

def updateuserQuizzes(n,e,qz,ca,qu,a,s,t):
    conn=sq.connect("UserInfo.db")
    cur=conn.cursor()
    cur.execute("update UserQuizData set User_Answer=? ,Score=? where Email=? and Question_Name=?",(a,s,e,qu))
    conn.commit()
    resultListUpd(n,e,qz,ca,t)
def questionList():
    conn=sq.connect("UserInfo.db")
    cur=conn.cursor()
    cur.execute("select * from  UserQuizData where Name=? and Email=?",(session["user"],session["Email"]))
    return cur.fetchall()
def resultListDis(n,e,qz,ca):
    conn=sq.connect("UserInfo.db")
    cur=conn.cursor()
    cur.execute("select * from  UserResultData where Name=? and Email=? and Quizz_Title=? and Category_Name=?",(n,e,qz,ca))
    return cur.fetchall()
def resultList(n,e,qz,ca,s,t):
    conn=sq.connect("UserInfo.db")
    cur=conn.cursor()
    cur.execute('insert into UserResultData(Name,Email,Quizz_Title,Category_Name,Score,Total_que) values(?,?,?,?,?,?)',(n,e,qz,ca,s,t))
    conn.commit()
def resultListUpd(n,e,qz,ca,t):
    s=0
    conn=sq.connect("UserInfo.db")
    cur=conn.cursor()
    cur.execute("select Score from  UserQuizData where Name=? and Email=? and Quizz_Title=? and Category_Name=?",(n,e,qz,ca))
    rw=cur.fetchall()
    conn.commit()
    for i in rw:
        s=s+i[0]
    cur.execute("update UserResultData set Score=? ,Total_que=? where Email=? and Quizz_Title=? and Name=? and Category_Name=?",(s,t,e,qz,n,ca))
    conn.commit()
    conn.close()
def resultListDisp(n,e):
    conn=sq.connect("UserInfo.db")
    cur=conn.cursor()
    cur.execute("select * from  UserResultData where Name=? and Email=? ",(n,e))
    return cur.fetchall()
def resultListDispAll():
    conn=sq.connect("UserInfo.db")
    cur=conn.cursor()
    cur.execute("select * from  UserResultData ")
    return cur.fetchall()
def resultListdi(n,e,qz,ca):
    conn=sq.connect("UserInfo.db")
    cur=conn.cursor()
    cur.execute("select * from  UserResultData where Name=? and Email=? and Quizz_Title=? and Category_Name=?",(n,e,qz,ca))
    return cur.fetchall()
def totalQuizzpass():
    if len(resultListDisp(session["user"],session["Email"]))==0:
      return 0
    else:
        c=0
        r=resultListDisp(session["user"],session["Email"])
        for i in r:
            if (i[6]*100)/i[7]>=40:
                c=c+1
        return c
def totalQuizzavg():
    if len(resultListDisp(session["user"],session["Email"]))==0:
      return 0
    else:
        sco=0
        r=resultListDisp(session["user"],session["Email"])
        for i in r:
            sco=(i[6]*100)/i[7]+sco
        avg=sco/len(r)
        return round(avg,2)
    
@app.route("/UpdateName/<newName>",methods=["GET","POST"])   
def updname(newName):
    conn=sq.connect("UserInfo.db")
    cur=conn.cursor()
    cur.execute("update UserData set Name=? where Name=? and Email=? ",(newName,session["user"],session["Email"]))
    conn.commit()  
    conn.close()
    session["user"]=newName 
