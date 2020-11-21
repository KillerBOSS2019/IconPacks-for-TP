from tkinter import *
from tkinter import filedialog
from tkinter import colorchooser
from PIL import ImageTk,Image
import os, glob, threading, zipfile, os
from pathlib import Path as PH
import tkinter.messagebox as messagebox
import tkinter as tk
from time import sleep

root = Tk()
root.title('IconPack Program')
root.geometry('600x300')
root.resizable(0,0)

x = 'Default_Image.jpg'
imgs = Image.open(x)
imgs = imgs.resize((128,128), Image.ANTIALIAS)
imgs = ImageTk.PhotoImage(imgs)
panel = Label(root, image=imgs)
panel.image = imgs
panel.place(x=400,y=20)
icon_image = 0
Mini = 0

#Functions
def Background():
    color = colorchooser.askcolor()
    if color[1] != None:
        BGBox.configure(fg=color[1])
        BGBox.config(state='normal')
        BGBox.delete(0, END)
        BGBox.insert(0, color[1])
        BGBox.config(state='readonly')
    else:
        pass
icons = []
def showIcon(ImageNumber,icon):
    global Iconwidth, Iconheight,Infos,img,currentImage
    gifs = 0
    x = icons[ImageNumber]
    img = Image.open(x)
    Iconwidth, Iconheight = img.size
    img = img.resize((128,128), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img, format="gif -index 0")
    panel = Label(root, image=img)
    panel.image = img
    panel.place(x=400,y=20)
    test = 0
    head, tail = os.path.split(x)
    print(head)
    currentImage = os.path.join(head,tail)
    File_size = round(os.stat(os.path.join(a,tail)).st_size/1024, 2)
    Infos = Label(root,text=f"Filename: {tail}\nFile Size: {File_size} KB\nDimensions: {Iconwidth} x {Iconheight}\nWidth: {Iconwidth} Height: {Iconheight}")
    Infos.place(x=380,y=210)
def Browse():
    global Max, Link,a,icons
    icons=[]
    FileName = []
    a = filedialog.askdirectory()
    Path.config(state='normal')
    Path.delete(0, END)
    Path.insert(0, a)
    Path.config(state='readonly')
    for file in glob.glob(os.path.join(a,'*.png')) or glob.glob(os.path.join(a,'*.PNG')) or glob.glob(os.path.join(a,'*.jpg')) or glob.glob(os.path.join(a,'*.JPG')) or glob.glob(os.path.join(a,'*.gif')) or glob.glob(os.path.join(a,'*.GIF')):
        icons.append(file)
    Max = len(icons)
    if Max > 1:
        button_next.configure(state='normal')
        button_back.configure(state='normal')
    button_back.configure(state='disabled')
    Link.place_forget()
    Link = Label(root, text=f'1/{Max}')
    Link.place(x=450, y=170)
    panel.place_forget()
    showIcon(0,icons)

def Next():
    global icon_image, panel, Link
    print(icon_image)
    panel.place_forget()
    icon_image += 1
    Link.place_forget()
    Infos.place_forget()
    Link = Label(root, text=f'{icon_image+1}/{Max}')
    Link.place(x=450, y=170)
    showIcon(icon_image,icons)
    if icon_image == Max-1:
        button_next.config(state='disabled')
    if icon_image != Max-1:
        button_back.config(state='normal')
        
def Back():
    global icon_image, panel, Link
    print(icon_image)
    panel.place_forget()
    icon_image -= 1
    Link.place_forget()
    Infos.place_forget()
    Link = Label(root, text=f'{icon_image+1}/{Max}')
    Link.place(x=450, y=170)
    showIcon(icon_image,icons)
    if icon_image == 0:
        button_back.config(state='disabled')
    if icon_image != 0:
        button_next.config(state='normal')
def Run():
    print('Name=',NameBox.get())
    print('Author=',AuthorBox.get())
    print('LinkBox=',LinkBox.get())
    print('BgColor=',BGBox.get())
    os.makedirs("Output",exist_ok=True)
    if os.path.isfile(os.path.join('Output',str(NameBox.get()+'.tpi'))):
        tk.messagebox.showerror(title="Warning", message='File exists please input diffent name')
    else:
        if NameBox.get() == '' or AuthorBox.get() == '' or LinkBox.get() == '' or BGBox.get() == '' or Path.get() == '':
            tk.messagebox.showerror(title="Warning", message='Please Fill in all the empty box')
            print('Skipped')
        else:
            with open(os.path.join('Output/info.txt'),'w+') as infoTxt:
                infoTxt.write(f'name={NameBox.get()}\n')
                infoTxt.write(f'author={AuthorBox.get()}\n')
                infoTxt.write(f'link={LinkBox.get()}\n')
                infoTxt.write(f'bgcolor={BGBox.get()}\n')
                infoTxt.close()
            MyZip = zipfile.ZipFile(f"Output/{NameBox.get()}.zip", 'w', allowZip64=True)
            MyZip.write(os.path.join('Output','info.txt'), arcname='info.txt')
            print(Path.get())
            for i in icons:
                head,tail = os.path.split(i)
                MyZip.write(os.path.join(Path.get(), i), arcname=tail)
                print(f'Zipped {i}')
            MyZip.close()
            os.rename(os.path.join(os.getcwd(), f"Output/{NameBox.get()}.zip"), os.path.join(os.getcwd(), f"Output/{NameBox.get()}.tpi"))
            os.remove('Output/info.txt')
            Saved = os.path.join(os.getcwd(),os.path.join("Output",f"{NameBox.get()}.tpi"))
            Finished = messagebox.askyesno(title="Done", message=f'Done Your File Saved at\n{Saved}')
            if Finished:
                print('Open Dirs')
                os.popen('open Output/')
            else:
                print('Skiped Not open dirs')
Name = Label(root, text='Name:')
Name.place(x=25, y=30)
NameBox = Entry(root, width=30)
NameBox.place(x=70,y=30)

Author = Label(root, text='Author:')
Author.place(x=25, y=60)
AuthorBox = Entry(root, width=30)
AuthorBox.place(x=70,y=60)

Link = Label(root, text='link:')
Link.place(x=25, y=90)
LinkBox = Entry(root, width=30)
LinkBox.place(x=70,y=90)

def ResetAndRun():
    icons=[]
    Browse()
color_button = Button(root, text="Browse", command=ResetAndRun)
color_button.place(x=25, y=120, width=75)
Path = Entry(root, width=30)
Path.place(x=110,y=125)
Path.config(state='readonly')

color_button = Button(root, text="Pick A Color", command=Background)
color_button.place(x=25, y=150)
BGBox = Entry(root, width=8)
BGBox.place(x=110,y=155)
BGBox.insert(0,'#00ff00')
BGBox.configure(fg='#00ff00')
BGBox.config(state='readonly')

Run_button = Button(root, text='RUN', command=Run)
Run_button.place(x=20, y=220, width=250, height=60)

#icon
button_back = Button(root, text="<<", command=Back)
button_back.place(x=360, y=170, width=60)
button_back.configure(state='disabled')
button_next = Button(root, text=">>", command=Next)
button_next.place(x=510, y=170, width=60)
button_next.configure(state='disabled')
Link = Label(root, text=f'1/1')
Link.place(x=450, y=170)

root.mainloop()
