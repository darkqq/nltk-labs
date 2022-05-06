import time
from tkinter import *
from xml.dom import minidom

from tkinter import messagebox as mb
import main
from tkinter.filedialog import askopenfilename, asksaveasfile


def pars(event):
    starttime=time.time()
    string = enter_text.get(1.0, END)
    string = string.replace('.', '')
    string = string.replace(',', '')
    string = string.replace('!', '')
    string = string.replace('?', '')
    string = string.replace(':', '')
    string = string.replace(';', '')

    lexemes = main.get_lexemes_from_text(string)
    lexemes.sort(reverse=True)
    for i in enumerate(lexemes):
        dictionary = words.get(1.0, END).split('\n')[:-2]
        add_flag = True
        for j in dictionary:
            if i[1].lexeme == j:
                add_flag = False
        if add_flag:
            words.insert(1.0, i[1].lexeme + '\n')
            word_tag.insert(1.0, i[1].tags + '\n')
            word_description.insert(1.0, i[1].part_of_sent + '\n')
    print(time.time()-starttime)


def scroll(*args):
    words.yview(*args)
    word_tag.yview(*args)
    word_description.yview(*args)


def save_func(event):
    file = asksaveasfile(filetypes=(("dict file", "*.dict"),), defaultextension=("dict file", "*.dict"))
    doc = minidom.Document()
    root = doc.createElement('root')
    words_string = words.get(1.0, END).split("\n")[:-2]
    tags_string = word_tag.get(1.0, END).split("\n")[:-2]
    description_string = word_description.get(1.0, END).split("\n")[:-2]
    lexemes = []

    for i in range(len(words_string)):
        lexeme = main.Lexeme()
        lexeme.lexeme = words_string[i]
        lexeme.tags = tags_string[i]
        lexeme.part_of_sent = description_string[i]
        lexemes.append(lexeme)

    lexemes.sort(reverse=True)

    for i in lexemes:
        word = doc.createElement('word')
        lexeme = doc.createElement('lexeme')
        tag = doc.createElement('tag')
        description = doc.createElement('description')

        text1 = doc.createTextNode(i.lexeme)
        text2 = doc.createTextNode(i.tags)
        text3 = doc.createTextNode(i.part_of_sent)

        lexeme.appendChild(text1)
        tag.appendChild(text2)
        description.appendChild(text3)

        word.appendChild(lexeme)
        word.appendChild(tag)
        word.appendChild(description)

        root.appendChild(word)
    doc.appendChild(root)

    xml_str = doc.toprettyxml(indent="  ", encoding='UTF-8')

    file.write(str(xml_str, 'UTF-8'))
    file.close()


def open_file(event=None):
    filename = askopenfilename(filetypes=(("dict file", "*.dict"),), defaultextension=("dict file", "*.dict"))
    file_str = ''
    with open(filename) as file:
        file.readline()
        for line in file:
            file_str = file_str + line
    doc = minidom.parseString(file_str).documentElement
    word_elements = doc.getElementsByTagName("word")

    for i in word_elements:
        words.insert(1., i.getElementsByTagName("lexeme")[0].childNodes[0].nodeValue + '\n')
        if len(i.getElementsByTagName('tag')[0].childNodes):
            word_tag.insert(1., i.getElementsByTagName("tag")[0].childNodes[0].nodeValue + '\n')
        else:
            word_tag.insert(1., '\n')
        if len(i.getElementsByTagName('description')[0].childNodes):
            word_description.insert(1., i.getElementsByTagName("description")[0].childNodes[0].nodeValue + '\n')
        else:
            word_description.insert(1., '\n')


root = Tk()
mainmenu = Menu(root)
mainmenu.add_command(label='Файл', command=open_file)
root.config(menu=mainmenu)

label_frame = Frame(root)
label_frame.pack()

enter_label = Label(label_frame, text='Введите текст', width=10)
enter_label.pack(side=LEFT)

empty_label = Label(label_frame, text='', width=65)
empty_label.pack(side=RIGHT)

enter_text = Text(width=70, height=20, wrap=WORD)
enter_text.pack()

text_frame = Frame(root)
text_frame.pack()
scroll_y = Scrollbar(text_frame, orient=VERTICAL, command=scroll)
scroll_y.pack(side=LEFT)

text1 = Frame(text_frame)
text1.pack(side=LEFT)

text2 = Frame(text_frame)
text2.pack(side=LEFT)

text3 = Frame(text_frame)
text3.pack(side=RIGHT)

text1_label = Label(text1, text='Лексема', width=10)
text1_label.pack()
words = Text(text1, width=15, height=10)
words.configure(yscrollcommand=scroll_y.set)
words.pack()

text2_label = Label(text2, text='Тэги слова', width=17)
text2_label.pack()
word_tag = Text(text2, width=35, height=10)
word_tag.configure(yscrollcommand=scroll_y.set)
word_tag.pack()

text3_label = Label(text3, text='Член предложения', width=17)
text3_label.pack()
word_description = Text(text3, width=20, height=10)
word_description.configure(yscrollcommand=scroll_y.set)
word_description.pack()

buttons = Frame(root)
buttons.pack()

but = Button(text="Преобразовать")
but.bind('<Button-1>', pars)
but.pack(side=RIGHT)

save = Button(text="Сохранить")
save.bind('<Button-1>', save_func)
root.bind('<Control-s>', save_func)
root.bind('<Control-o>', open_file)
save.pack(side=LEFT)

root.mainloop()


