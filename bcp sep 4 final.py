#Please open readme.txt for information regarding using this program


#variables defined
global used_qr_ID
global qr_ID_input
global whom
global used_qr_codes
global available_qr_ID
global useditem
global all_used_items
global name
global per_num
global br_pass

#lists defined
ID_list = []
useditem = []
all_used_items=[]
usedticket = []
qr_ID_unused = []
qr_ID_new = []
list_borrow = []
usedID=[]
used_qr_codes = []
assigned_qr_codes = []
lst_name = []
item_from_dict = []

unused_br_pass = [") bathroom pass #1",") bathroom pass #2", ") bathroom pass #3"]
used_br_pass = []

#dictionaries defined
my_dict = {}
my_atten_dict={}
dict_in_out={}
dict_qr_whom = {}
dict_qr_who = {}
qr_to_who_dict ={}
qr_to_whom_dict = {}
item_out_to_name_dict = {}
my_dict_item_to_name = {}
item_from_dict = []
qr_to_pn_dict = {}

time_start_MTHF_dict = {"per_1":"8:30","per_2":"10:08","per_3":"12:20",
                        "per_4":"1:58","per_5":"8:30","per_6":"10:08",
                        "per_7":"12:20","per_8":"1:58"
                      }

time_end_MTHF_dict = {"per_1":"10:02","per_2":"11:44","per_3":"1:52",
                      "per_4":"3:30","per_5":"10:02","per_6":"11:44",
                      "per_7":"1:52", "per_8":"3:30"
                      }

time_start_W_dict = {"per_1":"9:00","per_2":"10:31","per_3":"12:34",
                     "per_4":"3:30","per_5":"9:00","per_6":"10:31",
                     "per_7":"12:34","per_8":"3:30"
                    }
time_end_W_dict = {"per_1":"10:25","per_2":"11:58","per_3":"1:59",
                     "per_4":"3:30","per_5":"10:25","per_6":"11:58",
                     "per_7":"1:59","per_8":"3:30"
                    }

with open("c:\\barcodeprogram\qrscanID\\premade_qr_ID.txt","r") as inf:
    premade_qr_ID = eval(inf.read())
    
with open("c:\\barcodeprogram\qrscanID\\unusedticket.txt","r") as inf:
    unusedticket = eval(inf.read())

with open("c:\\barcodeprogram\qrscanID\\my_dict.txt","r") as inf:
    my_dict = eval(inf.read())

#Begin Program

def Main():
    global used_qr_ID
    global qr_ID_input
    global qrid
    global pn
    global whom
    global name    
    global get_index
    global available_qr_ID
  

    used_qr_codes = ""

    qr_ID_input = input('Scan Science ID QR code ')
        
    while qr_ID_input[0] != ("&"):
        qr_ID_input = input('Invalid ID, Scan Your Science ID ')

    while str(qr_ID_input) not in str(premade_qr_ID):
        qr_ID_input = input("Invalid, Scan Your Science ID ")

    while qr_ID_input[0] == ("&") and qr_ID_input in str(premade_qr_ID):
        qrid = qr_ID_input
        
             
        if qrid in str(my_dict):
            print ("welcome " + my_dict.get(qrid))
            action_scan_input()

        #if str(qr_ID_input) not in str(assigned_qr_codes):

        if str(qr_ID_input) not in str(my_dict):
            fn = input("First time user, type your first name ")
            ln = input("Please type your last name ")
            pn = input("Please enter your period number, 1 to 8 ")
            whom =[(fn + " " + ln + ", " + "period " + pn + ", ")]

            while int(pn) not in range(1,9,1):
                pn = int(pn)
                pn = input("Please re-enter your period number, 1 to 8 ")
                pn = [pn]
            qr_ID_input = [qr_ID_input]
            usedID.append(qrid)

           
            #assigned_qr_codes links a name to a qr code
            
            assigned_qr_codes.append(qrid)
            
            qr_to_who_dict = dict(zip(qr_ID_input,whom))

                      
            #my_dict stores the assigned qr code to a specific 
            
            my_dict.update(qr_to_who_dict)

            
            name = my_dict.get(qrid)
            lst_name.append(name)
            
            copy_premade_qr_ID = list(premade_qr_ID)
            
            available_qr_ID = copy_premade_qr_ID

            for i in usedID:
                try:
                    available_qr_ID.remove(i)
                    
                except ValueError:
                    pass
            name = my_dict.get(qrid)
            
            print ("Welcome " + name + ", Place your name label on the back of your Science ID")
           
            #create file mydict of all assigned qr ID and associated names
            f = open("c:\\barcodeprogram\qrscanID\\my_dict.txt", "w+")
            f.write(str(my_dict))
            f.close()

            #create file available qr ID, premade qr ID, used qr ID
            f = open("c:\\barcodeprogram\qrscanID\\available_qr_ID.txt", "w+")
            f.write(str(available_qr_ID))
            f.close()

            f = open("c:\\barcodeprogram\qrscanID\\premade_qr_ID.txt","w+")
            f.write(str(premade_qr_ID))
            f.close()

            f = open("c:\\barcodeprogram\qrscanID\\used_qr_codes.txt","w+")
            f.write(str(usedID))
            f.close()

                   
        action_scan_input()

def action_scan_input():

    global borrow
    global item_from_dict
    global all_used_items
    global name

    
    action = input("Scan Action Barcode ")

    lst_a = [("$"),("!"),("("),("#"),(")")]
    
    while action[0] not in lst_a:
        action = input("Scanning Error!  Re-Scan Action Barcode ")

    if action[0] == ("("):
        borrow = action
        import time
        localtime = time.asctime(time.localtime(time.time()))

        with open("c:\\barcodeprogram\qrscanID\\my_dict.txt","r") as inf:
            my_dict = eval(inf.read())
            
        
        
        # "(" it is an item to be checked (in or out) to a valid qr id user

        #if name and item checked out, check it in.
        #elif name and item not linked, checkout item
        #else item not checked in and is being checked out

        if action[0]==("("):
        
            borrow = action

        if  borrow in useditem and qrid in usedID:
   
            usedID.remove(qrid)
            useditem.remove(borrow)
            name = str(my_dict.get(qrid))
            
            f = open ("c:\\barcodeprogram\qrscanID\\check_in_out.txt","a+")
            f.write(name +" ," + " returned " + borrow + " on " + localtime + '\n')
            f.close()
            
            print(name + " returned "+ borrow + " on " + localtime  + '\n')
        
        elif borrow in useditem and qrid not in usedID:
            print("this item was not checked in yet, see instructor" + '\n')
            
        else:
            
            usedID.append(qrid)
            useditem.append(borrow)
            name = my_dict.get(qrid)
            f = open ("c:\\barcodeprogram\qrscanID\\check_in_out.txt","a+")
            f.write(name + "checked out "+ borrow + " on " + localtime + '\n')
            f.close()

            print(name + "checked out" + str(borrow) + " on " + localtime + '\n')

        while qrid not in premade_qr_ID:
            input('Invalid ID, Scan Science issued ID ')
            Main()
        
        Main()

    # if the qr code starts with "#" it is an interactive notebook code 

    if action[0] == ("#"):
        ticket = action
        import time
        localtime = time.asctime( time.localtime(time.time()) )

        with open("c:\\barcodeprogram\qrscanID\\my_dict.txt","r") as inf:
            my_dict = eval(inf.read())
            
            name = my_dict.get(qrid)
        
        if ticket in unusedticket:
            usedticket.append(ticket)
            unusedticket.remove(ticket)

            
            f = open ("c:\\barcodeprogram\qrscanID\\INB_work.txt","a+")
            f.write (name + "did work on " + localtime + " ("+ ticket+")"  + '\n')
            f.close()
            print(name + "did work " +"on " + localtime + "("+ ticket + ")" + '\n')

            Main()
            
        else:
            ticket in usedticket
            print("INB ticket is not valid and has already been used")
            Main()
            
# if the qr code starts with "$" it is an attendance code

    if action[0] == ("$"):

        import time
        localtime = time.asctime( time.localtime(time.time()) )

        with open("c:\\barcodeprogram\qrscanID\\my_dict.txt","r") as inf:
            my_dict = eval(inf.read())
            name = my_dict.get(qrid)
            print(name + " "+ "arrived on: " + localtime + '\n')
        
            f = open ("c:\\barcodeprogram\qrscanID\\attendance.txt","a+")
            f.write(name + " "+ "arrived on: " + localtime + '\n')
            f.close()
            

        Main()

# if the qr code starts with "@" it a bathroom pass QR code 
    
    if action[0] == (")"):
        br_pass = action
               
        

        #print("got br_pass, unused_br_pass, used _br_pass coded as )"  + str(br_pass)+ str(unused_br_pass)+ str(used_br_pass))
        
        import time
        localtime = time.asctime( time.localtime(time.time()) )

        with open("c:\\barcodeprogram\qrscanID\\my_dict.txt","r") as inf:
            my_dict = eval(inf.read())

            name = my_dict.get(qrid)
        
            if str(br_pass) in str(unused_br_pass):
                used_br_pass.append(br_pass)
                unused_br_pass.remove(br_pass)

                f = open ("c:\\barcodeprogram\qrscanID\\bathroom_in_out.txt","a+")
                f.write(str(name) + "left on " + str(localtime) + " with"+ str(used_br_pass) + '\n')
                f.close()

                print(str(name) + "left on " + str(localtime) + " with"+ str(used_br_pass) + '\n')
                
                Main()
                
            elif str(br_pass) in str(used_br_pass):
                
                f = open ("c:\\barcodeprogram\qrscanID\\bathroom_in_out.txt","a+")
                f.write(str(name) + "returned on " + str(localtime) + " with"+ str(used_br_pass) + '\n')
                f.close()

                print(str(name) + "returned on " + str(localtime) + " with"+ str(used_br_pass) + '\n')

                used_br_pass.remove(br_pass)
                unused_br_pass.append(br_pass)
                
       
        
    
#if the qr code starts with "!" it is an admin code    

#This admin function is to re-activate used tickets

    if action[0] == ("!"):
        import time
        localtime = time.asctime( time.localtime(time.time()) )
        
        
        while action[0] == ("!"):
            renew =input("reactivate used tickets now.  When done scan Purple Admin QR code")
            if renew in usedticket:        
                usedticket.remove(renew)
                unusedticket.append(renew)
                print("ticket "+ "\t" + renew +" is ready for reuse")
                print("used tickets are: "+ str(usedticket))
                                      
            if renew == (str("! Teacher Administrator")):
                Main()
        
