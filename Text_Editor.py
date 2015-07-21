

from Tkinter import *
import tkFileDialog
import tkMessageBox
import os

root = Tk(className=" FarBeyondAverage Text") # Instantiate Tk()

menubar = Menu(root) # creates all the menus
filemenu = Menu(menubar, tearoff=0)
editmenu = Menu(root, tearoff=0)
viewmenu = Menu(root, tearoff=0)
themesmenu = Menu(root, tearoff=0)

root.config(menu=menubar) # allows for the display of the menu

shortcutbar = Frame(root, height=15, bg='light sea green') 
shortcutbar.pack(expand=NO, fill=X)
lnlabel = Label(root, width=2, bg='antique white')
lnlabel.pack(side=LEFT, anchor='nw', fill=Y)




#shortcut bar
'''
icons = ['new_file', 'open_file', 'save','cut', 'copy', 'paste'
'undo', 'redo', 'find_menu' ,'about']


for i, icon in enumerate(icons):
	tbicon = PhotoImage(file='icons/'+icon+'.gif')  Create icons for shortcutbar, icon file
	cmd = eval(icon)
	toolbar = Button(shortcutbar, image=tbicon, command=cmd)
	toolbar.image = tbicon
	toolbar.pack(side=LEFT)
shortcutbar.pack(expand=NO, fill=X)
'''
# end shortcut bar


frame = Text(root, width=100, height=35)
frame.pack(expand=YES, fill=BOTH)
#scroll = Scrollbar(frame, orient=VERTICAL)  #These 3 lines cause conflict, the window opens up small
#scroll.pack(side=RIGHT, fill=Y)
#scroll.config(command=frame.yview)
           #end conflict


'''
textPad = Text(root, width=120, height=85)   # Scrollbar variables
textPad.pack(expand=YES, fill=BOTH)
scroll = Scrollbar(textPad)
textPad.configure(yscrollcommand=scroll.set)
scroll.config(command=textPad.yview)
scroll.pack(side=RIGHT, fill=Y)
'''





def update_line_number(event=None):
	showln = IntVar()
	showln.set(1)
	viewmenu.add_checkbutton(label="Show Line Number", variable=showln)
	update_line_number

	txt = ''
	if showln.get():
		endline, endcolumn, frame.index('end-1c').split('.')
		txt = '\n'.join(map(str, range(1, int(endline))))
	lnlabel.config(text=txt, anchor='nw')




def cut():
	frame.event_generate("<<Cut>>")
	#editmenu.add_command(label="Cut", compound=LEFT, accelerator="Ctrl+X", command=cut)
	update_line_number()


def copy():
	frame.event_generate("<<Copy>>")
	#editmenu.add_command(label="Copy", compound=LEFT, accelerator="Ctrl+C", command=copy)
	update_line_number()

def paste():
	frame.event_generate("<<Paste>>")
	#editmenu.add_command(label="Paste", compound=LEFT, accelerator="Ctrl+V", command=paste)

def undo():
	frame.event_generate("<<Undo>>")
	#editmenu.add_command(label="Undo", compound=LEFT,accelerator="Ctrl+Z", command=undo)
	#frame = Text(root, undo=True)

def redo():
	frame.event_generate("<<Redo>>")
	#editmenu.add_command(label="Redo", compound=LEFT,accelerator="Ctrl+Y", command=redo)
	#frame = Text(root, redo=True) # infinite redo
	update_line_number()

def select_all():
	frame.tag_add('sel', '1.0', 'end') # from beginning to the end

def new_file():   # Create a new window upon opening a new file
	root.title("Untitled")
	global filename
	filename = None
	frame.delete(1.0, END)


def open_file(): 
	global filename
	filename = tkFileDialog.askopenfilename(defaultextension=".txt", filetypes = [("All Files", "*.*"), ("Text Documents", "*.txt")])
	if filename == "":
		filename = None
	else:
		root.title(os.path.basename(filename) + " -pyPad")
		frame.delete(1.0,END)
		fh = open(filename,'r')
		frame.insert(1.0, fh.read())
		fh.close()

def save_as():
	try:
		f = tkFileDialog.asksaveasfilename(initialfile='Untitled.txt', defaultextension=".txt", filetypes=[("All Files","*.*"),("Text Documents", "*.txt")])
		fh = open(f, 'w')
		textoutput = frame.get(1.0, END)
		fh.write(textoutput)
		fh.close()
		root.title(os.path.basename(f) + " -pyPad")
	except:
		pass

def save_file():
	global filename
	try:
		f = open(filename, 'w')
		letter = frame.get('1.0', 'end')
		f.write(letter)
		f.close()
	except:
		save_as()

def search_for(needle, cssnstv,frame,t2,e):
	frame.tag_remove('match','1.0',END)
	count = 0
	if needle:
		pos = '1.0'
		while True:
			pos = frame.search(needle, pos, nocase=cssnstv, stopindex=END)
			if not pos:
				break
				lastpos = '%s+%dc' % (pos, len(needle))
				frame.tag_add('match',pos,foreground='red')
				count += 1
				pos = lastpos
			frame.tag_config('match', foreground='red', background='yellow')
			e.focus_set()
			t2.title('%d matches found' % count)

def find_menu():
	t2 = Toplevel(root)
	t2.title('Find')
	t2.geometry('262x65+200+250')
	t2.transient(root)
	Label(t2, text="Find All:").grid(row=0, column=0, sticky='e')
	v = StringVar()
	e = Entry(t2, width=25, textvariable=v)
	e.grid(row=0, column=1, padx=2, pady=2, sticky='we')
	e.focus_set()
	c = IntVar()
	Checkbutton(t2, text="Ignore Case", variable=c).grid(row=1,column=1,sticky='e',padx=2,pady=2)
	Button(t2, text="Find All", underline=0, command=lambda:search_for(v.get(), c.get(), root, t2, e)).grid(row=0, column=2, sticky='e'+'w', padx=2,pady=2)

def close_search():
	root.tag_remove('match', '1.0', END)
	t2.destroy()
	t2.protocol('WM_DELETE_WINDOW', close_search)

def about(event=None):
	tkMessageBox.showinfo("About", "FarBeyondAverage Developers\n www.FarBeyondAverage.com")

def help(event=None):
	tkMessageBox.showinfo("Help", "For help please go to www.FarBeyondAverage.com", icon='question')
	aboutmenu.add_cascade(label="Help", command=help)

def exit_program(event=None):
	if tkMessageBox.askokcancel("Quit", "Do you want to quit?"):
		root.destroy()
	root.protocol('WM_DELETE_WINDOW', exit_command) # override close
	filemenu.add_command(label="Exit", accelerator='Alt+f4', command=exit_program)


def dummy():
	print "I am a dummy"
def fummy():
	print "I am a fummy"





def file_menu():
	menubar.add_cascade(label="File",menu=filemenu)
	filemenu.add_command(label="New",accelerator="Ctrl+N",command=new_file)
	filemenu.add_command(label="Open...",accelerator="Ctrl+O",command=open_file)
	filemenu.add_command(label="Save",accelerator="Ctrl+S",command=save_file)
	filemenu.add_command(label="Save As...",accelerator="Ctrl+Shift+S" ,command=save_as)
	filemenu.add_separator()
	filemenu.add_command(label="Exit",accelerator="Alt+F4",command=exit_program)

def edit_menu():
	menubar.add_cascade(label="Edit", menu=editmenu)
	editmenu.add_command(label="Undo",accelerator="Ctrl+Z",command=undo,)
	editmenu.add_command(label="Redo",accelerator="Ctrl+Y",command=redo)
	editmenu.add_separator()
	editmenu.add_command(label="Cut",accelerator="Ctrl+X",command=cut)
	editmenu.add_command(label="Copy",accelerator="Ctrl+C",command=copy)
	editmenu.add_command(label="Paste",accelerator="Ctrl+V",command=paste)
	editmenu.add_separator()
	editmenu.add_command(label="Find",underline=0,accelerator="Ctrl+F",command=find_menu)
	editmenu.add_command(label="Select All",underline=7,accelerator="Ctrl+A",command=select_all)



def view_menu():
	menubar.add_cascade(label="View", menu=viewmenu)
	viewmenu.add_command(label="Show Line Number", command=update_line_number)
	viewmenu.add_command(label="Highlight Current Line", command=dummy)
	viewmenu.add_command(label="Show Info bar", command=dummy)
	viewmenu.add_separator()
	viewmenu.add_cascade(label="Color Schemes", menu=themesmenu)

	themesmenu.add_radiobutton(label="Default")
	themesmenu.add_radiobutton(label="Carbon Grey")
	themesmenu.add_radiobutton(label="Melanoid", variable=themesmenu)
	themesmenu.add_radiobutton(label="Terra-Cotta", variable=themesmenu)
	themesmenu.add_radiobutton(label="Rufescent", variable=themesmenu)


def help_menu():
	helpmenu = Menu(root, tearoff=0)
	menubar.add_cascade(label="Help", menu=helpmenu)
	helpmenu.add_command(label="About", command=about)
	helpmenu.add_separator()
	helpmenu.add_command(label="Website", command=fummy)
	helpmenu.add_separator()
	helpmenu.add_command(label="Documentation", command=fummy)

def themes_menu():
	pass



file_menu()
edit_menu()
view_menu()
help_menu()









'''
Add boolean True/False value for themes
Fix Undo/Redo options
Add scrollbar, Y axis, X axis
Fix Lambda function for find_all function
Create a new window when 'new file' is clicked. Keep track of open windows
Creatd line numbers
'''








root.mainloop()
