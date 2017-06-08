import RPi.GPIO as GPIO
import os
from time import sleep
from API import CreateDatabase
from API import ClientAPI
from API import MailboxAPI
from API import MailSender


def electromagnetic_setup():
	GPIO.setmode(GPIO.BOARD)
	
	#left block
	GPIO.setup(11, GPIO.OUT)
	GPIO.setup(13, GPIO.OUT)
	GPIO.setup(15, GPIO.OUT)
	
	#right block
	GPIO.setup(29, GPIO.OUT)
	GPIO.setup(31, GPIO.OUT)
	GPIO.setup(33, GPIO.OUT)

	GPIO.output(11, GPIO.HIGH)
	GPIO.output(29, GPIO.HIGH)

	
def left_box_open():	
	GPIO.output(13, GPIO.HIGH)
	GPIO.output(15, GPIO.LOW)
	print "\nLeft box is opened!"

def left_box_close():
	GPIO.output(13, GPIO.LOW)
	GPIO.output(15, GPIO.LOW)
	print "\nLeft box is closed!"
	
def right_box_open():
	GPIO.output(31, GPIO.HIGH)
	GPIO.output(33, GPIO.LOW)
	print "\nRight box is opened!"

def right_box_close():
	GPIO.output(31, GPIO.LOW)
	GPIO.output(33, GPIO.LOW)
	print "\nRigth box is closed!"
	
	
def root():
	print "1. Send Packages"
	print "2. Receive Packages"
	print ""
	user_input_root = input('What are you going to do: ')
	return user_input_root

def choose_person():
	print "1. Mr.Chen/1F "
	print "2. Mr.Chang/2F"
	print "3. Mr.Li/3F"
	print "4. Cancel"
	print ""
	user_input_choose_person = input('Choose the person that own the package: ')
	return user_input_choose_person

def blocks_needed():
	print "1. One block"
	print "2. Two blocks"
	print "3. Cancel"
	user_input_blocks =  input('How many blocks do you need? : ') 
	return user_input_blocks
	
def confirm():
	print "1. Confirm"
	print "2. Cancel"
	print ""
	user_input_confirm = input('Are you sure? ')
	return user_input_confirm

def enter_password():
	user_input_password = input('Please enter password : ')
	return user_input_password
	
def box_condition():

	mailboxList = MailboxAPI.MailboxRepository.GetAll()
	box_left_condition = mailboxList[0].inused
	box_right_condition = mailboxList[1].inused
	
	print "-------------------------------------------------"
	print "|                       |                       |"
	print "|                       |                       |"
	
	if box_left_condition == 1:
		if box_right_condition == 1:
			print "|         used          |          used         |"
		elif box_right_condition == 0:
			print "|         used          |          free         |"
			
	if box_left_condition == 0:
		if box_right_condition == 1:
			print "|         free          |          used         |"
		elif box_right_condition == 0:
			print "|         free          |          free         |"
		
	print "|                       |                       |"
	print "|                       |                       |"
	print "-------------------------------------------------\n"
	
	
if __name__ == "__main__":

	
	#GPIO setup and close the box
	electromagnetic_setup()
	left_box_close()
	right_box_close()
	
	
	thread = MailSender.ResendPasswordMailThread()
	thread.start()
	
	CreateDatabase.InitializeDatabase()
	#CreateDatabase.AddSystemData()
	clientList = ClientAPI.ClientRepository.GetAll()
	mailboxList = MailboxAPI.MailboxRepository.GetAll()
	
	
	
	box_left_condition = mailboxList[0].inused
	box_right_condition = mailboxList[1].inused
	user_input_blocks = 0
	system_box_space_assigned = 'none'
	
	try:
                while True:
                        os.system('clear')
                        #choose to send package or to receive package
                        user_input_root = root()
                        
                        ###SEND PACKAGE###
                        if user_input_root == 1:
                                while user_input_root == 1:
                                        os.system('clear')
                                        #show the condition of the box
                                        box_condition()
                                        
                                        #choose the person that owns the package
                                        user_input_choose_person = choose_person()
                                        
                                        if user_input_choose_person == 1:
                                                print "\nYou are going to send package to Mr.Wei-Ming Chen/1F\n"
                                                client = clientList[0]
                                                sleep(1)
                                                
                                        elif user_input_choose_person == 2:
                                                print "\nYou are going to send package to Mr.Hsiu-Chi Chang/2F\n"
                                                client = clientList[1]
                                                sleep(1)
                                                        
                                        elif user_input_choose_person == 3:
                                                print "\nYou are going to send package to Mr.Cheng-Yuan Li/3F\n"
                                                client = clientList[2]
                                                sleep(1)
                                                                                
                                        elif user_input_choose_person == 4:
                                                user_input_root = 0
                                        
                                        else:
                                                print "\nWrong number, please enter again\n"
                                                sleep(1)

                                        
                                        os.system('clear')
                                        box_condition()
                                        
                                        if user_input_root != 0:
                                                user_input_blocks = blocks_needed()
                                                if user_input_blocks < 3:
                                                        number_of_blocks = MailboxAPI.MailboxRepository.Assign(user_input_blocks)
                                                        count_blocks = 0
                                                        
                                                        for blocks in number_of_blocks:
                                                                if blocks.inused == 0:
                                                                        count_blocks = count_blocks + 1
                                                        
                                                        #print count_blocks
                                                        sleep(2)
                                                        
                                                        #Two blocks needed
                                                        if count_blocks == 2:
                                                                print "\nPlease put your package in the box\n"
                                                                
                                                                user_input_confirm = confirm()
                                                                                
                                                                if 	user_input_confirm == 1:
                                                                        MailboxAPI.MailboxRepository.ConfirmAssign(number_of_blocks, client)
                                                                        left_box_close()
                                                                        right_box_close()
                                                                        print "\nEmailbox locked successfully!\n"
                                                                        sleep(2)
                                                                                        
                                                                #cancel closing box	
                                                                elif user_input_confirm ==2:
                                                                        user_input_root = 0
                                                                
                                                                
                                                        #One block needed	
                                                        elif count_blocks == 1:
                                                                #put in the LEFT block
                                                                if number_of_blocks[0].id == 1:
                                                                        print "\nPlease put your package in the LEFT block\n"
                                                                        
                                                                        user_input_confirm = confirm()
                                                                                
                                                                        if 	user_input_confirm == 1:
                                                                                MailboxAPI.MailboxRepository.ConfirmAssign(number_of_blocks, client)
                                                                                left_box_close()
                                                                                print "\nEmailbox locked successfully!\n"
                                                                                sleep(2)
                                                                                                
                                                                        #cancel closing box	
                                                                        elif user_input_confirm ==2:
                                                                                user_input_root = 0
                                                                
                                                                        
                                                                #put in the RIGHT block	
                                                                elif number_of_blocks[0].id == 2:
                                                                        print "\nPlease put your package in the RIGHT block\n"
                                                                        
                                                                        user_input_confirm = confirm()
                                                                                
                                                                        if 	user_input_confirm == 1:
                                                                                MailboxAPI.MailboxRepository.ConfirmAssign(number_of_blocks, client)
                                                                                right_box_close()
                                                                                print "\nEmailbox locked successfully!\n"
                                                                                sleep(2)
                                                                                                
                                                                        #cancel closing box	
                                                                        elif user_input_confirm ==2:
                                                                                user_input_root = 0												
                                                                        
                                                                       
                                                        #No Space		
                                                        elif number_of_blocks == False:
                                                                print "No Space!"
                                                                sleep(3)
                                        
                                        
                                        
                                        

                        ###RECEIVE PACKAGE###		
                        elif user_input_root == 2:
                                os.system('clear')
                                user_input_password = enter_password()
                                system_open_box = MailboxAPI.MailboxRepository.GetPackage(str(user_input_password))

                                
                                if system_open_box == [1]:
                                        left_box_open()
                                        print "Please take out your package from LEFT block!"
                                elif system_open_box == [2]:
                                        right_box_open()
                                        print "Please take out your package from RIGHT block!"
                                elif system_open_box == [1, 2]:
                                        left_box_open()
                                        right_box_open()
                                        print "Please take out your package!"
                                else:
                                        print "Wrong password, please try again"
                                
                                sleep(3)
                        else:
                                print "\nWrong number, Please enter again!\n"
                                sleep(1)


	except 	KeyboardInterrupt:
                GPIO.cleanup()	
                thread.stop()
		print "\nProgram successfully closed"
		sleep(3)
		
		
		
		
		
		
		
		
