from Tkinter import *
import tkFileDialog
import os
root = Tk()
root.title("Arcadame")
root.geometry("1000x700")
root.configure(bg = '#ff0000')
root.grid()

def load():
    file = tkFileDialog.askopenfile()
    if file:
        input.delete('1.0', END)
        with open(file.name) as fp:
            for line in fp:
                input.insert(END, line)

def save():
    file = tkFileDialog.asksaveasfile(mode='w', defaultextension=".arcadame")
    if file is None: # asksaveasfile return `None` if dialog closed with "cancel".
        return
    text2save = str(input.get(1.0, END)) # starts from `1.0`, not `0.0`
    file.write(text2save)
    file.close()
    return file.name

def compile():
    file = save()
    if file:
        os.system('python arcadame.py -i ' + file)

def compileSaved():
    file = tkFileDialog.askopenfile()
    if file:
        os.system('python arcadame.py -i ' + file.name)

def execute():
    compile()
    os.system('python2.7-32 arcadameVM.py -o output.txt')
    output['text'] = ""
    with open('output.txt') as fp:
        for line in fp:
            output['text'] += line


def executeSaved():
    compileSaved()
    os.system('python2.7-32 arcadameVM.py -o output.txt')
    output['text'] = ""
    with open('output.txt') as fp:
        for line in fp:
            output['text'] += line

for r in range(7):
    root.rowconfigure(r, weight=1)
for c in range(2):
    root.columnconfigure(c, weight=1)

topFrame = Frame(root, bg = '#00FF00', padx = 10)
topFrame.grid(row = 0, column = 0, rowspan = 5, columnspan = 2, sticky = W+E+N+S)

bottomFrame = Frame(root)
bottomFrame.grid(row = 5, column = 0, rowspan = 2, columnspan = 2, sticky = W+E+N+S)

loadProgram = Button(bottomFrame, text = 'Load program', command = load)
loadProgram.pack(fill = X)

saveProgram = Button(bottomFrame, text = 'Save program', command = save)
saveProgram.pack(fill = X)

compileProgram = Button(bottomFrame, text = 'Compile program', command = compile)
compileProgram.pack(fill = X)

executeProgram = Button(bottomFrame, text = 'Execute program', command = execute)
executeProgram.pack(fill = X)

executeProgram = Button(bottomFrame, text = 'Execute saved program', bg = '#0000FF', command = executeSaved)
executeProgram.pack(fill = X)

input = Text(topFrame, bg = '#ffffff', width = 80, height = 33)
input.pack(side = "left")

output = Label(topFrame, bg = '#000000', fg = '#ffffff', width = 40, height = 32)
output.pack(side = "right")

root.mainloop()
