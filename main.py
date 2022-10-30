#Importing important libraries
import pyrebase

import firebase_admin
from firebase_admin import credentials, firestore

# Function to find the key of a document.
def findindex(ui):
    col = db.collection('runs').get()
    for doc in col:
        if doc.to_dict()['Name'].lower() == ui.lower():
            key = doc.id
            return key



cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

#Config
firebaseConfig={'apiKey': "AIzaSyAA-_0T0Ms2iwU_H_ZztDMcTOlzjMns8PE",
  'authDomain': "running-database-63f04.firebaseapp.com",
  'projectId': "running-database-63f04",
  'storageBucket': "running-database-63f04.appspot.com",
  'messagingSenderId': "277589345493",
 'appId': "1:277589345493:web:942e3f18efb737b72c8e5c",
  'measurementId': "G-K7W40EGZ3N",
  'databaseURL': "https://running-database-63f04.firebaseio.com"}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firestore.client()
auth = firebase.auth()
access = False

#User auth.
userchoice = input("\nDo you want to Login or Signup (L,S) ")
if userchoice.lower() == 'l':
    #Login
    username = input("\nEnter your Email: ")
    password = input("\nEnter your Password: ")
    try:
        auth.sign_in_with_email_and_password(username,password)
        print(f"\n{username} successfully logged in. ")
        access = True
    except:
        print("\nUsername or password is invalid. Please try again. ")
elif userchoice.lower() == 's':
    #signup
    username = input("\nEnter your Email: ")
    password = input("\nCreate your password: ")
    confirmpassword = input("\nConfirm Password: ")
    if password == confirmpassword:
        try:
            auth.create_user_with_email_and_password(username, password)
            print("\nAccount creation completed.")
            access = True
        except:
            print("\nEmail already in use. ")
de = 1
if access:
    while de >0:
        #Action Selector
        de = int(input("""\nWhat Action do you want to take?
0 Exit 
1 Add a new entry
2 Modify an existing entry
3 Delete an existing entry
4 Display all entries
"""))
#Creating a new entry
        if de == 1:
            rn = input("\nWhat do you want to name the run? ")
            time = float(input("\nWhat was the duration of the run in minutes? "))
            dst = float(input("\nWhat was the distance of the run in miles? "))
            db.collection('runs').add({'Name': rn,'Time': time, 'Distance': dst})
#Modifing an existing entry
        elif de == 2:
            modify = input("\nWhat is the name of the entry you want to edit? ")
            me = 1
            while me > 0:
                me = int(input("""\nWhat elements do you want to modify?
0 Exit
1 Run Name
2 Run Time
3 Run Distance
"""))
                if me == 1 :
                    rn = input("\nNew run name: ")
                elif me == 2:
                    time = float(input("\nNew run time: "))
                elif me == 3:
                    dst = float(input("\nNew run distance: "))
            key = findindex(modify)
            db.collection('runs').document(key).update({'Name': rn, 'Time': time, 'Distance': dst})
# Deleting an entry        
        elif de == 3:
            dlt = input("\nWhat is the name of the run you want to delete? ")
            key = findindex(dlt)
            #Deletion selection 
            di = int(input("""\nWhat do you want to delete?
1 Full Run
2 Run detail
"""))
            if di == 1:
                db.collection('runs').document(key).delete()
            elif di == 2:
                dlte = int(input("""\nWhat detail do you want to delete?
1 Run Time
2 Run Distance
"""))
                if dlte == 1:
                    db.collection('runs').document(key).update({"Time":firestore.DELETE_FIELD})
                elif dlte == 2:
                    db.collection('runs').document(key).update({"Distance":firestore.DELETE_FIELD})
#Displaying entries
        elif de == 4:
            display = db.collection('runs').get()
            print("")
            for line in display:
                data = line.to_dict()
                print(data)
#Doesn't have accesss
else:
    print("\nACCESS DENIED\n")