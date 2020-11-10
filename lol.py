# print("LOLterpreter!")
from tkinter import * 
from tkinter import filedialog
from tkinter import ttk

#* -- GUI INITIALIZATIONS --
window = Tk()
window.geometry("1450x750") #widthxheight
window.title("Ang ganda ni Maam Kat LOLTERPRETER")

#* -- CLASSES --
class SourceCode():
    def __init__(self):
        # constructor

#* -------------
#* -- FUNCTIONS --
def selectSourceCode():
    # pass
    filename = filedialog.askopenfilename(initialdir = "/", title = "Select a File", filetypes = (("Text files", "*.lol*"),("all files","*.*")))
    # print(filename)
    # TODO: create a class (SourceCode) for the code input
    # TODO: store the source code by using SourceCode.addCode()
#* ---------------


#* -- GUI ELEMENTS --
selectSourceCode = Button(window, text="Select LOLCode file", width = 19, command=selectSourceCode)
selectSourceCode.place(x=10, y=20)



window.mainloop()