import mysql.connector


#CRUD Operations
def CRUD(uname,password):

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
            upList=input("Enter the New Todo List:")
            mydb = mysql.connector.connect(host="localhost", user="root", passwd="12345678", database="todo_db")
            mycursor = mydb.cursor()
            mycursor.execute("SELECT * FROM todolist where todo_id='{}';".format(td_id))
            result=mycursor.fetchall()
            if(mycursor.rowcount>0):
                mycursor.execute("UPDATE todolist set todovalue='{}' where todo_id={};".format(upList,td_id))
                mydb.commit()
            else:
                print("Invalid Todo_List Number")

        elif(choice==4):#Delete Statement
            del_list=int(input("Enter Todo_Id to Delete your Existing List:"))
            mydb = mysql.connector.connect(host="localhost", user="root", passwd="12345678", database="todo_db")
            mycursor = mydb.cursor()
            mycursor.execute("SELECT * FROM todolist where todo_id='{}';".format(del_list))
            result = mycursor.fetchall()
            if (mycursor.rowcount > 0):
                mycursor.execute("DELETE FROM todolist where todo_id='{}';".format(del_list))
                mydb.commit()
                print("-----List Deleted------")
            else:
                print("No List Exist with Enter Todo_List value")

        elif(choice==5):#Exit
            print("------------Program Terminated-------------")
            mydb.close()
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
    result = mycursor.fetchall()
    # print(mycursor.rowcount)
    if(mycursor.rowcount!=0):
        password = input("Enter Your Password:")
        mycursor.execute("SELECT password FROM usertable WHERE username='{}';".format(uname))
        result=mycursor.fetchall()

        if(result[0][0]==password):
            CRUD(uname, password)
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
                    mycursor.execute("insert into usertable(username,password) value('{}','{}')".format(uname,password))
                    mydb.commit()
                    checkUP()
        else:
            print("-------Program Terminated---------")
            exit()




#Initial Start of The Program
checkUP()
