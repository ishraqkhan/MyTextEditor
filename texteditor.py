from tkinter import *
from tkinter import messagebox
import tkinter.filedialog
from tkinter.font import Font
import os, re

class TextEditor:
    @staticmethod
    def quitApp(event=None):
        if messagebox.askyesno("Exit Text Editor?", "Do you really want to quit?"):
            root.quit()

    def setTitle(self, event=None):
        title = re.findall("[ \w-]+\.", self.file_name)
        title = str(title[0])
        title = title[:len(title) - 1]
        root.title(title)

    def printFile(self, event=None):
        # Currently only prints to default printer
        os.startfile(self.file_name, "print")

    def openFile(self, event=None):
        txt_file = tkinter.filedialog.askopenfilename(parent=root, initialdir="/Users/Ishraq/PyCharmProjects")

        if txt_file:
            self.text_area.delete(1.0, END)

            self.file_name = txt_file
            print(self.file_name)

            with open(txt_file) as curr_file:
                self.text_area.insert(1.0, curr_file.read())
                root.update_idletasks()
                self.setTitle()


    def save(self, event=None):
        contents = self.text_area.get('1.0', END)
        try:
            with open(self.file_name, mode='w', encoding='utf-8') as curr_file:
                curr_file.write(contents)
                curr_file.close()
        except:
            self.saveAs()

    def saveAs(self, event=None):
        file = tkinter.filedialog.asksaveasfile(mode='w')

        if file != None:
            data = self.text_area.get('1.0', END)
            file.write(data)
            self.file_name = file
            file.close()

        self.setTitle()

    def changeFont(self, event=None):
        new_font = Font(family = self.text_font.get(), size = self.text_size.get())

        try:
            self.text_area.tag_add('Highlighted', SEL_FIRST, SEL_LAST)
            self.text_area.tag_configure('Highlighted', font=new_font)
        except TclError:
            self.text_area.configure(font=new_font)

    def showAbout(self, event=None):
        messagebox.showinfo("About", "This is the premise of a text editor. Help will be shown in the near future, "
                                    "thank you very much!")

    # initialize text editor
    def __init__(self, root):

        root.title("Ishraq Text Editor")
        root.geometry("600x550")

        frame = Frame(root, width=600, height=550)

        # Current file being used
        self.file_name = ""

        scrollBar = Scrollbar(frame)
        self.text_area = Text(frame, width=600, height=550, font=Font(family="Times New Roman", size=11),
                              yscrollcommand=scrollBar.set,
                              padx=10, pady=10)

        scrollBar.pack(side=RIGHT, fill=Y)

        self.text_area.pack(side=LEFT, fill=BOTH, expand=True)

        frame.pack()

        main_menu = Menu(root)

        # -- File Menu --
        file_menu = Menu(main_menu, tearoff=0)
        file_menu.add_command(label="Open", command=self.openFile)
        file_menu.add_command(label="Save", command=self.save)
        file_menu.add_command(label="Save As", command=self.saveAs)
        file_menu.add_command(label="Print", command=self.printFile)
        file_menu.add_command(label="Quit", command=TextEditor.quitApp)

        main_menu.add_cascade(label="File", menu=file_menu)

        # -- Font Menu ---
        self.text_font = StringVar()
        self.text_font.set("Times New Roman")

        font_menu = Menu(main_menu, tearoff=0)
        font_menu.add_radiobutton(label="Ariel", variable=self.text_font, command=self.changeFont)
        font_menu.add_radiobutton(label="Calibri", variable=self.text_font, command=self.changeFont)
        font_menu.add_radiobutton(label="Comic Sans", variable=self.text_font, command=self.changeFont)
        font_menu.add_radiobutton(label="Courier", variable=self.text_font, command=self.changeFont)
        font_menu.add_radiobutton(label="Times New Roman", variable=self.text_font, command=self.changeFont)

        # -- Size Menu For Text--
        self.text_size = IntVar()
        self.text_size.set(11)

        size_menu = Menu(main_menu, tearoff=0)
        for i in range(11, 33):
            size_menu.add_radiobutton(label=i, variable=self.text_size, command=self.changeFont)

        # -- View Menu --
        view_menu = Menu(main_menu, tearoff=0)
        view_menu.add_command(label="Line Numbers")
        view_menu.add_cascade(label="Fonts", menu=font_menu)
        view_menu.add_cascade(label="Size", menu=size_menu)

        main_menu.add_cascade(label="View", menu=view_menu)

        # -- Help Menu --
        help_menu = Menu(main_menu, tearoff=0)
        help_menu.add_command(label="About", command=self.showAbout)

        main_menu.add_cascade(label="Help", menu=help_menu)

        root.config(menu=main_menu)

root = Tk()

text_editor = TextEditor(root)

root.protocol("WM_DELETE_WINDOW", text_editor.quitApp)
root.mainloop()


