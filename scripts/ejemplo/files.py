import os
import glob   

def create_file(name,size):
	#os.system("dd if=/dev/zero of=../files/"+str(name)+".log bs="+str(size)+"KB count=1")
	choices = "9"
	string = choices*size*1024
	file = open("../files/"+str(name), 'w')
	file.write(string)

def create_files():
	sizes=[1,5,10,50,100,200,500,2048]
	for i in sizes:
		create_file(i,i)

def files_to_strings(path):
	path = path+"*"
	files=glob.glob(path) 
	list=[]  
	for file in files:     
	    f=open(file, 'r')  
	    list.append(f.read())
	    f.close()
	return list

if __name__ == "__main__":
	create_files()
