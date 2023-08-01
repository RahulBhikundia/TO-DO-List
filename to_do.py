"""
Project Name: To-Do List

Description:
A simple, daily utility tool, a To-Do List. It keeps a record of tasks to do and their status,
whether it is Pending or Complete. When all the Tasks are Marked Complete, 
they can be removed with the option given on GUI.

Dependencies:
Python:
Libraries Used - boto3, os, pymysql
AWS:
Amazon RDS(MySQL), Amazon EC2, IAM

Platform:
VS Code, AWS Management Console
"""


# Importing necessary libraries to connect to mysql-server
import os
import pymysql
import boto3

# Configuring parameters with thier necessary values. Details Taken from Amazon RDS
ENDPOINT = "database-1.cc6zyirfnzmy.ap-south-1.rds.amazonaws.com"
PORT = 3306
USER = "rahul"
REGION = "ap-south-1"
DBNAME = "db1"
os.environ['LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN'] = '1'

#gets the credentials from .aws/credentials
session = boto3.Session(profile_name='default')
client = session.client('rds')

# Generating an authentication token that allows the Python code to connect securely to the Amazon RDS database.
token = client.generate_db_auth_token(DBHostname=ENDPOINT, Port=PORT, DBUsername=USER, Region=REGION)

class TodoList:
    """Class for to do list"""
    def add_task(self, task_name):
        """This method adds the task to the to-do list, or to the database hosted on Amazon RDS"""
        try:
            conn =  pymysql.connect(host=ENDPOINT, user=USER, passwd=token, port=PORT, database=DBNAME, ssl_ca="C:\\Users\\rahul\\Downloads\\ap-south-1-bundle.pem")
            cur = conn.cursor()
            cur.execute("""INSERT INTO TODO (Task, Status) VALUES (%s, %s)""",(task_name, "Pending"))
            conn.commit()
            cur.close()
            conn.close()
        except Exception as _:
            print("Unable to ADD TASK to the list")

    def view_tasks(self):
        """This method is used to view the Tasks and thier respective Status"""
        try:
            conn =  pymysql.connect(host=ENDPOINT, user=USER, passwd=token, port=PORT, database=DBNAME, ssl_ca="C:\\Users\\rahul\\Downloads\\ap-south-1-bundle.pem")
            cur = conn.cursor()
            cur.execute("""SELECT COUNT(*) FROM TODO;""")
            row_count = cur.fetchone()[0]

            if row_count == 0 :
                print("No Task Available!!")
            else:
                cur.execute("""SELECT * FROM TODO;""")
                rows = cur.fetchall()

                for row in rows:
                    print(row)

            cur.close()
            conn.close()
        except Exception as _:
            print("Unable to view the Tasks in the TO-DO list")

    def mark_completed(self, task_name):
        """This method is used to mark the task as COMPLETED!"""
        try:
            conn =  pymysql.connect(host=ENDPOINT, user=USER, passwd=token, port=PORT, database=DBNAME, ssl_ca="C:\\Users\\rahul\\Downloads\\ap-south-1-bundle.pem")
            cur = conn.cursor()
            cur.execute("""SELECT * FROM TODO WHERE Task = %s;""",(task_name))
            rows = cur.fetchall()

            if len(rows) > 0:
                cur.execute("""UPDATE TODO SET Status = %s WHERE Task = %s;""",("Completed", task_name))
                conn.commit()
            else:
                print("Invalid Task or No such Task Exist!")
            cur.close()
            conn.close()
        except Exception as _:
            print("Unable to mark the Task as Completed!")

    def remove_completed_tasks(self):
        """This method is used to remove all the completed Tasks from the To Do List"""
        try:
            conn =  pymysql.connect(host=ENDPOINT, user=USER, passwd=token, port=PORT, database=DBNAME, ssl_ca="C:\\Users\\rahul\\Downloads\\ap-south-1-bundle.pem")
            cur = conn.cursor()
            cur.execute("""DELETE FROM TODO WHERE Status = %s;""",("Completed"))
            conn.commit()
            cur.close()
            conn.close()
            print("All Completed Tasks have been Removed!")
        except Exception as _:
            print("Unable to remove Completed Task.")

def main():
    """The Main Function"""
    todolist = TodoList()
    while True:
        print("\n---------------- To Do List ------------------")
        print("1.   Add Task")
        print("2.   View Task")
        print("3.   Mark Task")
        print("4.   Remove Completed Task")
        print("5.   Close")

        choice = input("Enter Your Choice from 1-5 : ")

        if choice == '1':
            task_name = input("Enter Task Name: ")
            todolist.add_task(task_name)
        elif choice == '2':
            todolist.view_tasks()
        elif choice == '3':
            task_name = input("Enter the task Name (WARNING - It is CASE SENSITIVE): ")
            todolist.mark_completed(task_name)
        elif choice == '4':
            todolist.remove_completed_tasks()
        elif choice == '5':
            print("Thanks for using To do list system\n")
            break
        else:
            print("Invalid option choosen!!..... Please Try Again")


if __name__ == '__main__':
    main()