# python D:\Github\notepad\caderno.py

import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

def new_file():
    """
    Limpa o conteúdo da área de texto para criar um novo arquivo.
    """
    text_area.delete(1.0, tk.END)

def open_file():
    """
    Abre um arquivo de texto existente e insere seu conteúdo na área de texto.
    Exibe uma mensagem de erro se o arquivo não estiver no formato UTF-8.
    """
    file_path = filedialog.askopenfilename(defaultextension=".txt",
                                           filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                text_area.delete(1.0, tk.END)
                text_area.insert(tk.END, file.read())
        except UnicodeDecodeError:
            messagebox.showerror("Error", "Cannot decode file. Please ensure it is in UTF-8 format.")

def save_file():
    """
    Salva o conteúdo atual da área de texto em um arquivo. 
    O usuário é solicitado a fornecer um nome e local para o arquivo.
    """
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(text_area.get(1.0, tk.END))

def save_as():
    """
    Salva o conteúdo da área de texto como um novo arquivo, 
    solicitando um novo nome e local para o arquivo.
    """
    save_file()

def exit_app():
    """
    Pergunta ao usuário se deseja realmente sair do aplicativo. 
    Se confirmado, encerra a aplicação.
    """
    if messagebox.askokcancel("Quit", "Do you really want to quit?"):
        root.destroy()

def wrap_text():
    """
    Ativa a quebra automática de linhas na área de texto 
    e remove a barra de rolagem horizontal.
    """
    text_area.config(wrap=tk.WORD)
    horizontal_scrollbar.pack_forget()

def no_wrap_text():
    """
    Desativa a quebra automática de linhas na área de texto 
    e adiciona a barra de rolagem horizontal.
    """
    text_area.config(wrap=tk.NONE)
    horizontal_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

def align_center():
    """
    Alinha o texto centralizado na área de texto.
    """
    content = text_area.get(1.0, tk.END)
    text_area.tag_configure("center", justify='center')
    text_area.delete(1.0, tk.END)
    text_area.insert(tk.INSERT, content, "center")

def align_left():
    """
    Alinha o texto à esquerda na área de texto.
    """
    content = text_area.get(1.0, tk.END)
    text_area.tag_configure("left", justify='left')
    text_area.delete(1.0, tk.END)
    text_area.insert(tk.INSERT, content, "left")

def align_right():
    """
    Alinha o texto à direita na área de texto.
    """
    content = text_area.get(1.0, tk.END)
    text_area.tag_configure("right", justify='right')
    text_area.delete(1.0, tk.END)
    text_area.insert(tk.INSERT, content, "right")

root = tk.Tk()
root.title("Notepad")

# Criando o widget Text com barras de rolagem
text_frame = tk.Frame(root)
text_frame.pack(fill=tk.BOTH, expand=1)

# Barra de rolagem vertical
vertical_scrollbar = tk.Scrollbar(text_frame)
vertical_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Barra de rolagem horizontal
horizontal_scrollbar = tk.Scrollbar(text_frame, orient=tk.HORIZONTAL)
horizontal_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

# Área de texto
text_area = tk.Text(text_frame, undo=True, wrap=tk.WORD, 
                    yscrollcommand=vertical_scrollbar.set, 
                    xscrollcommand=horizontal_scrollbar.set)
text_area.pack(fill=tk.BOTH, expand=1)

# Conectando as barras de rolagem com a área de texto
vertical_scrollbar.config(command=text_area.yview)
horizontal_scrollbar.config(command=text_area.xview)

# Criando Menu
menu_bar = tk.Menu(root)

# File Menu
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Save As...", command=save_as)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_app)
menu_bar.add_cascade(label="File", menu=file_menu)

# Format Menu
format_menu = tk.Menu(menu_bar, tearoff=0)
format_menu.add_command(label="Word Wrap", command=wrap_text)
format_menu.add_command(label="No Word Wrap", command=no_wrap_text)
format_menu.add_separator()
format_menu.add_command(label="Align Left", command=align_left)
format_menu.add_command(label="Align Center", command=align_center)
format_menu.add_command(label="Align Right", command=align_right)
menu_bar.add_cascade(label="Format", menu=format_menu)

root.config(menu=menu_bar)
root.mainloop()
