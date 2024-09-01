# python D:\Github\caderno\caderno.py

import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from collections import deque

# Lista para armazenar o histórico de ações
action_history = []

def update_history(action, content, index):
    """
    Atualiza a lista de ações e adiciona o histórico à Listbox.
    """
    action_description = f"{action}: '{content}' at {index}"
    action_history.append((action, content, index))
    action_listbox.insert(tk.END, action_description)

def insert_text(index, text):
    """
    Insere o texto na área de texto e atualiza o histórico.
    """
    text_area.insert(index, text)
    update_history("Insert", text, index)

def delete_text(index, length):
    """
    Exclui o texto da área de texto e atualiza o histórico.
    """
    deleted_text = text_area.get(index, f"{index}+{length}c")
    text_area.delete(index, f"{index}+{length}c")
    update_history("Delete", deleted_text, index)

def on_key_release(event):
    """
    Captura as inserções e exclusões de texto manualmente.
    """
    if event.keysym in ("BackSpace", "Delete"):
        delete_text(tk.INSERT, 1)
    else:
        insert_text(tk.INSERT, event.char)

def new_file():
    text_area.delete(1.0, tk.END)

def open_file():
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
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(text_area.get(1.0, tk.END))

def save_as():
    save_file()

def exit_app():
    if messagebox.askokcancel("Quit", "Do you really want to quit?"):
        root.destroy()

def wrap_text():
    text_area.config(wrap=tk.WORD)
    horizontal_scrollbar.pack_forget()

def no_wrap_text():
    text_area.config(wrap=tk.NONE)
    horizontal_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

def align_center():
    content = text_area.get(1.0, tk.END)
    text_area.tag_configure("center", justify='center')
    text_area.delete(1.0, tk.END)
    text_area.insert(tk.INSERT, content, "center")

def align_left():
    content = text_area.get(1.0, tk.END)
    text_area.tag_configure("left", justify='left')
    text_area.delete(1.0, tk.END)
    text_area.insert(tk.INSERT, content, "left")

def align_right():
    content = text_area.get(1.0, tk.END)
    text_area.tag_configure("right", justify='right')
    text_area.delete(1.0, tk.END)
    text_area.insert(tk.INSERT, content, "right")

root = tk.Tk()
root.title("Notepad")

# Frame principal para o widget Text e a Listbox
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=1)

# Frame para a área de texto e barras de rolagem
text_frame = tk.Frame(main_frame)
text_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

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

# Frame para a Listbox de histórico
history_frame = tk.Frame(main_frame)
history_frame.pack(side=tk.RIGHT, fill=tk.Y)

# Listbox para exibir o histórico de ações
action_listbox = tk.Listbox(history_frame)
action_listbox.pack(side=tk.TOP, fill=tk.Y)

# Conectando eventos de teclado e mouse para capturar as alterações
text_area.bind("<KeyRelease>", on_key_release)

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
