#Required Libraries importing
from tkinter import *
from tkinter import filedialog
from Crypto.Cipher import DES
from Crypto.Hash import SHA256
import turtle
import argon2
import requests
import os
from getpass import getpass
from Crypto.Protocol.KDF import PBKDF2

Key_length=100005
salt="$ez*&214097GDAKACNASC;LSOSSBAdjskasnmosuf!@#$^()_adsa"

# Create global variables to store password and path
key_enc = ""
path = ""

#Encrypting function
def encryptor():

	global path
	global key_enc
	image_path = os.path.basename(path)
	
	#creating result labels
	result_label = Label(root, text="")
	result_label.pack(padx=10, pady=15)

	result_label2 = Label(root, text="")
	result_label2.pack(padx=10, pady=15)


	#Opening the image file
	try:
		with open(path, 'rb') as imagefile:
			image=imagefile.read()
			
		#Padding	
		while len(image)%8!=0:
			image+=b" "
	except:
		result_label.config(text="Error loading the file !")
		exit()
	
	#hashing original image in SHA256	
	hash_of_original=SHA256.new(data=image)
	
	
	#Salting and hashing password
	key_enc=PBKDF2(key_enc,salt,48,Key_length)

	
	#Encrypting using triple 3 key DES	
	result_label.config(text="Encrypting...")
	try:
		
		cipher1=DES.new(key_enc[0:8],DES.MODE_CBC,key_enc[24:32])
		ciphertext1=cipher1.encrypt(image)
		cipher2=DES.new(key_enc[8:16],DES.MODE_CBC,key_enc[32:40])
		ciphertext2=cipher2.decrypt(ciphertext1)
		cipher3=DES.new(key_enc[16:24],DES.MODE_CBC,key_enc[40:48])
		ciphertext3=cipher3.encrypt(ciphertext2)
		
		result_label.config(text="Encryption Successfull...")
	except:
		print("	Encryption failed...Possible causes:Library not installed properly/low device memory/Incorrect padding or conversions")
		exit()
	
	#Adding hash at end of encrypted bytes
	ciphertext3+=hash_of_original.digest()

	
	#Saving the file encrypted
	try:
		dpath="encrypted_"+image_path
		with open(dpath, 'wb') as image_file:
				image_file.write(ciphertext3)
		result_label2.config(text="Encrypted Image Saved successfully as imagename "+dpath)

		
	except:
		temp_path=input("Saving image failed!. Enter alternate name without format to save the encrypted image. If it is still failing then check system memory")
		try:
			dpath=temp_path+path
			dpath="encrypted_"+path
			with open(dpath, 'wb') as image_file:
					image_file.write(ciphertext3)
			print("Encrypted Image Saved successfully as imagename in the same directory "+dpath)
			exit()
		except:
			print("	Failed....Exiting...")
			exit()

#decrypting function
def decryptor():
	global path
	global key_enc
	image_name = os.path.basename(path)
	
	#creating result labels
	result_label = Label(root, text="")
	result_label.pack(padx=10, pady=15)

	result_label2 = Label(root, text="")
	result_label2.pack(padx=10, pady=15)


	try:
		with open(path,'rb') as encrypted_file:
			encrypted_data_with_hash=encrypted_file.read()
			
	except:
		print("	Unable to read source cipher data. Make sure the image is in same directory...Exiting...")
		exit()
	
	
	
	
	#extracting hash and cipher data without hash
	extracted_hash=encrypted_data_with_hash[-32:]
	encrypted_data=encrypted_data_with_hash[:-32]

	
	#salting and hashing password
	key_enc=PBKDF2(key_enc,salt,48,Key_length)
	

	#decrypting using triple 3 key DES
	result_label.config(text="Decrypting...")
	try:
		
		cipher1=DES.new(key_enc[16:24],DES.MODE_CBC,key_enc[40:48])
		plaintext1=cipher1.decrypt(encrypted_data)
		cipher2=DES.new(key_enc[8:16],DES.MODE_CBC,key_enc[32:40])
		plaintext2=cipher2.encrypt(plaintext1)
		cipher3=DES.new(key_enc[0:8],DES.MODE_CBC,key_enc[24:32])
		plaintext3=cipher3.decrypt(plaintext2)
		
		
	except:
		print("Decryption failed...Possible causes:Library not installed properly/low device memory/Incorrect padding or conversions")
		
	#hashing decrypted plain text
	hash_of_decrypted=SHA256.new(data=plaintext3)

	
	#matching hashes
	if hash_of_decrypted.digest()==extracted_hash:
		result_label2.config(text="Password Correct !!!")
		result_label2.config(text="Decryption Successfull...")
	else:
		result_label.config(text="Pasword Incorrect!!!")
		exit()
		
		
		
	#saving the decrypted file	
	try:
		epath = os.path.basename(path)
		if epath[:10]=="encrypted_":
			epath=epath[10:]
		epath="decrypted_image"+epath
		with open(epath, 'wb') as image_file:
			image_file.write(plaintext3)
		result_label2.config(text="	Image saved successully with name " + epath)
	except:
		temp_path=input("Saving image failed!. Enter alternate name without format to save the decrypted file. If it is still failing then check system memory")
		try:
			epath=temp_path+path
			with open(epath, 'wb') as image_file:
				image_file.write(plaintext3)
			print("	Image saved successully with name " + epath)
			print("	Note: If the decrypted image is appearing to be corrupted then password may be wrong or it may be file format error")
		except:
			result_label.config(text="Failed Exiting..")
			exit()


# Function to get password from user and store it securely
def get_key():
    global password
    
    password = key_entry.get()
    if show_password_checkbox_var.get():
        key_entry.config(show="")
    else:
        key_entry.config(show="*")

# Function to submit the password
def submit():
	key_entry.delete(0, END)
	path_label.configure(text="Password Submitted")

# Function to get name from user and store it
def select_image(): 
    global path
    
    path = filedialog.askopenfilename()
    path_label.config(text="Image selected: {}".format(path))
    if path:
      encrypt_button = Button(root, text="Encrypt", command=encryptor)
      encrypt_button.pack(side=LEFT, padx=10, pady=10)
      decrypt_button = Button(root, text="Decrypt", command=decryptor)
      decrypt_button.pack(side=RIGHT, padx=10, pady=10)
    else:
	    path_label.config(text="Please Select an Image.")
   

# Create the main window
root = Tk()
root.title("Image Encryption/Decryption")
root.geometry("300x300")

# Create widgets

key_label = Label(root, text="Enter password:")
key_entry = Entry(root, show="*")
show_password_checkbox_var = IntVar()
show_password_checkbox = Checkbutton(root, text="Show Password", variable=show_password_checkbox_var, command=get_key)
submit_button = Button(root, text="Submit", command=submit)
path_button = Button(root, text="Select", command=select_image)
path_label = Label(root, text="")


# Position widgets
key_label.pack(padx=10, pady=10)
key_entry.pack(padx=10, pady=10)
show_password_checkbox.pack(padx=10, pady=5)
submit_button.pack(side=LEFT,padx=10, pady=5)
path_button.pack(side=RIGHT,padx=10, pady=10)
path_label.pack(pady=10)


# Start the main loop
root.mainloop()



