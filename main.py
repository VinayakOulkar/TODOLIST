import mysql.connector


#CRUD Operations
def CRUD(result):
    user_id=result[0][0]
    uname=result[0][1]
    password=result[0][2]
    while(True):
        choice=int(input("Following Are the Operations :\n1.Your Todo list\n2.Add a Todo list\n3.Update Todo List\n4.Delete your Todo List\n5.Exit\nSelect Your Choice:"))

        if(choice==1):#Select Statement

            mydb = mysql.connector.connect(host="localhost", user="root", passwd="12345678", database="todo_db")
            mycursor = mydb.cursor()
            mycursor.execute("SELECT todo_id,(SELECT user_id from usertable where username='{}')AS user_id,todovalue FROM usertable FULL JOIN todolist ON (SELECT user_id from usertable where username='{}')=todolist.user_id;".format(uname,uname))
            result = mycursor.fetchall()

            if(mycursor.rowcount>0):
                print("------Todo List---------")
                print("Todo_Id  User_id  TodoValue")
                for i in result :
                    print(i)
            else:
                print("--------Your Todo List is Empty-----")

        elif(choice==2):#Insert Statement

            newList=input("Enter your New Todo List:")
            mydb = mysql.connector.connect(host="localhost", user="root", passwd="12345678", database="todo_db")
            mycursor = mydb.cursor()
            mycursor.execute("INSERT INTO todolist(user_id,todovalue) value((SELECT user_id from usertable where username='{}'),'{}');".format(uname,newList));
            mydb.commit()

        elif(choice==3):#Update Statement

            td_id=int(input("Enter Todo_Id Number that to be Updated:"))

            mydb = mysql.connector.connect(host="localhost", user="root", passwd="12345678", database="todo_db")
            mycursor = mydb.cursor()
            mycursor.execute("SELECT * FROM todolist where todo_id={} AND user_id={};".format(td_id,user_id));
            result=mycursor.fetchall()
            if(mycursor.rowcount>0):
                upList = input("Enter the New Todo List:")
                mycursor.execute("UPDATE todolist set todovalue='{}' where todo_id={};".format(upList,td_id))
                mydb.commit()
            else:
                print("Invalid Todo_List Number")

        elif(choice==4):#Delete Statement
            del_list=int(input("Enter Todo_Id to Delete your Existing List:"))
            mydb = mysql.connector.connect(host="localhost", user="root", passwd="12345678", database="todo_db")
            mycursor = mydb.cursor()
            mycursor.execute("SELECT * FROM todolist where todo_id={} AND user_id={};".format(del_list,user_id))
            result = mycursor.fetchall()
            # print("UserID",user_id,"\nResult",result)
            if (mycursor.rowcount > 0):
                # print(result[0][1])
                mycursor.execute("DELETE FROM todolist where todo_id='{}';".format(del_list))
                mydb.commit()
                print("-----List Deleted------")
            else:
                print("No List Exist with Entered Todo_List value")

        elif(choice==5):#Exit
            print("------------Program Terminated-------------")

            exit()
        else:
            print("Invalid Choice")



#Checks for Existing User or else Re-direct's the user for Registration
def checkUP():

    check=int(input("Are you a Todo User (1/0):"))

    if(check==1):
        checkCredentials()

    else:
        register()


#Checks for Existing User's Data in Database
def checkCredentials():
    uname = input("Enter Username:")
    mydb = mysql.connector.connect(host="localhost", user="root", passwd="12345678", database="todo_db")
    mycursor = mydb.cursor()
    mycursor.execute("Select * from usertable where username='{}'".format(uname))
    user_info = mycursor.fetchall()
    # print(mycursor.rowcount)
    if(mycursor.rowcount!=0):
        password = input("Enter Your Password:")
        mycursor.execute("SELECT password FROM usertable WHERE username='{}';".format(uname))
        result=mycursor.fetchall()

        if(result[0][0]==password):
            CRUD(user_info)
        else:
            print("-------Wrong Password------")


    else:
        print("No Username Found")
        register()


#New Users Registration
def register():

    reg = int(input("Do you want to Register(1/0):"))
    while(True):
        if (reg == 1):
            # Check if uname exist
            uname = input("Enter Username:")
            mydb = mysql.connector.connect(host="localhost", user="root", passwd="12345678", database="todo_db")
            mycursor = mydb.cursor()
            mycursor.execute("Select * from usertable where username='{}'".format(uname))
            result=mycursor.fetchall()
            # Check if uname exist

            if(mycursor.rowcount!=0):
                print("Username Already Exists Plz Enter Valid Username")

            else:
                    password = input("Enter a Password consisting of Alphabet and Numbers:")
                    # Add uname and pass to user database

                    # print(pass_check,"----",password[0].isalpha())
                    digit=0
                    alpha=0
                    for i in password:
                        if(i.isdigit()):
                            digit=1
                        elif(i.isalpha()):
                            alpha=1

                    if not(digit==1 and alpha==1):
                        print("Invalid Password")
                        exit()
                    mycursor.execute("insert into usertable(username,password) value('{}','{}')".format(uname, password))
                    mydb.commit()
                    mydb = mysql.connector.connect(host="localhost", user="root", passwd="12345678", database="todo_db")
                    mycursor = mydb.cursor()
                    mycursor.execute("Select * from usertable where username='{}'".format(uname))
                    result = mycursor.fetchall()
                    CRUD(result)





        else:
            print("-------Program Terminated---------")
            exit()




#Initial Start of The Program
checkUP()
