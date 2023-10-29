import os
import tkinter as tk
from tkinter import ttk
import sqlite3

# класс главного окна
class main2(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    # хранение и инициализация объектов GUI
    def init_main(self):
        # создаем панель инструментов (тулбар)
        # bg - фон
        # bd - границы
        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        # упаковка
        # side закрепляет вверху окна
        # fill растягивает по X (горизонтали)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        add_button = tk.Button(toolbar, text="Добавить",command=self.add_dialog)
        # упаковка и выравнивание по левому краю
        add_button.pack(side=tk.LEFT)

        add_button = tk.Button(toolbar, text="Изменеие",command=self.change_dialog)
        # упаковка и выравнивание по левому краю
        add_button.pack(side=tk.LEFT)

        add_button = tk.Button(toolbar, text="Удаление", command=self.delete_records)
        # упаковка и выравнивание по левому краю
        add_button.pack(side=tk.LEFT)

        add_button = tk.Button(toolbar, text="Поиск",command=self.open_search_dialog)
        # упаковка и выравнивание по левому краю
        add_button.pack(side=tk.LEFT)

        add_button = tk.Button(toolbar, text="Обновление", command=self.view_records)
        # упаковка и выравнивание по левому краю
        add_button.pack(side=tk.LEFT)

    # Добавляем Treeview
        # columns - столбцы
        # height - высота таблицы
        # show='headings' скрываем нулевую (пустую) колонку таблицы
        self.tree = ttk.Treeview(self, columns=('ID', 'name', 'tel', 'email', 'salary'),
                                 height=45, show='headings')
        # добавляем параметры колонкам
        # width - ширина
        # anchor - выравнивание текста в ячейке
        self.tree.column("ID", width=30, anchor=tk.CENTER)
        self.tree.column("name", width=300, anchor=tk.CENTER)
        self.tree.column("tel", width=150, anchor=tk.CENTER)
        self.tree.column("email", width=150, anchor=tk.CENTER)
        self.tree.column("salary", width=150, anchor=tk.CENTER)

        # подписи колонок
        self.tree.heading("ID", text='ID')
        self.tree.heading("name", text='ФИО')
        self.tree.heading("tel", text='Телефон')
        self.tree.heading("email", text='E-mail')
        self.tree.heading("salary", text='Зараплата')

        # упаковка
        self.tree.pack(side=tk.LEFT)

        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)


    # процедуры класса

    # добавление данных
    def add_records(self, name, tel, email, salary):
        self.db.insert_data(name, tel, email, salary)
        self.view_records()
    
    # обновление (изменение) данных иправить и дописать
    def update_record(self, name, tel, email, salary):
        self.db.c.execute('''UPDATE db SET name=?, tel=?, email=?, salary=? WHERE ID=?''',
                          (name, tel, email, salary, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records()

    # поиск записи по имени
    def search_records(self, name):
        name = ('%' + name + '%',)
        self.db.c.execute(
            '''SELECT * FROM db WHERE name LIKE ?''', name)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row)
         for row in self.db.c.fetchall()]

       # удаление записей
    
    def delete_records(self):
        # цикл по выделенным записям
        for selection_item in self.tree.selection():
            # удаление из БД
            self.db.c.execute('''DELETE FROM db WHERE id=?''',
                              (self.tree.set(selection_item, '#1'),))
        # сохранение изменений в БД
        self.db.conn.commit()
        # обновление виджета таблицы
        self.view_records()

    # вывод данных в виджет таблицы
    def view_records(self):
        # выбираем информацию из БД
        self.db.c.execute('''SELECT * FROM db''')
        # удаляем все из виджета таблицы
        [self.tree.delete(i) for i in self.tree.get_children()]
        # добавляем в виджет таблицы всю информацию из БД
        [self.tree.insert('', 'end', values=row)
         for row in self.db.c.fetchall()]
    
    
    #-------------------------------------------------------------------------------------
        # метод отвечающий за вызов дочернего окна Добавления
    def add_dialog(self):
        Add_ChldWind()
    # метод отвечающий за вызов окна дочернего окна изменения данных
    def change_dialog(self):
        Cng_ChldWind()
    # метод отвечающий за вызов окна для поиска
    def open_search_dialog(self):
        Search_ChldWind()


# Toplevel - окно верхнего уровня
class Add_ChldWind(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        # заголовок окна
        self.title('Добавить')
        # размер окна
        self.geometry('400x220')
        # ограничение изменения размеров окна
        self.resizable(False, False)

        # перехватываем все события происходящие в приложении
        self.grab_set()
        # захватываем фокус
        self.focus_set()

        # подписи
        label_name = tk.Label(self, text='ФИО:')
        label_name.place(x=50, y=50)
        label_select = tk.Label(self, text='Телефон')
        label_select.place(x=50, y=80)
        label_sum = tk.Label(self, text='E-mail')
        label_sum.place(x=50, y=110)
        label_sum = tk.Label(self, text='Зарплата')
        label_sum.place(x=50, y=140)

        # добавляем строку ввода для наименования
        self.entry_name = tk.Entry(self)
        # меняем координаты объекта
        self.entry_name.place(x=200, y=50)

        # добавляем строку ввода для email
        self.entry_email = tk.Entry(self)
        self.entry_email.place(x=200, y=80)

        # добавляем строку ввода для телефона
        self.entry_tel = tk.Entry(self)
        self.entry_tel.place(x=200, y=110)

        # добавляем строку ввода для зарплаты
        self.entry_sal = tk.Entry(self)
        self.entry_sal.place(x=200, y=140)

        # кнопка закрытия дочернего окна
        self.btn_cancel = tk.Button(
            self, text='Закрыть', command=self.destroy)
        self.btn_cancel.place(x=300, y=180)

        # кнопка добавления
        self.btn_ok = tk.Button(self, text='Добавить')
        self.btn_ok.place(x=220, y=180)
        # срабатывание по ЛКМ
        # при нажатии кнопки вызывается метод records, которому передаюся значения из строк ввода
        self.btn_ok.bind('<Button-1>', lambda event: self.view.add_records(self.entry_name.get(),
                                                                           self.entry_email.get(),
                                                                           self.entry_tel.get(),
                                                                           self.entry_sal.get()))
        self.btn_ok.bind('<Button-1>', lambda event: self.destroy(), add='+')

# класс окна для обновления, наследуемый от класса дочернего окна
class Cng_ChldWind(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()

    def init_edit(self):
        # заголовок окна
        self.title('Редактировать позицию')
        # размер окна
        self.geometry('400x220')
        # ограничение изменения размеров окна
        self.resizable(False, False)

        # подписи
        label_name = tk.Label(self, text='ФИО:')
        label_name.place(x=50, y=50)
        label_select = tk.Label(self, text='Телефон')
        label_select.place(x=50, y=80)
        label_sum = tk.Label(self, text='E-mail')
        label_sum.place(x=50, y=110)
        label_sum = tk.Label(self, text='Зарплата')
        label_sum.place(x=50, y=140)

        # добавляем строку ввода для наименования
        self.entry_name = tk.Entry(self)
        # меняем координаты объекта
        self.entry_name.place(x=200, y=50)

        # добавляем строку ввода для email
        self.entry_email = tk.Entry(self)
        self.entry_email.place(x=200, y=80)

        # добавляем строку ввода для телефона
        self.entry_tel = tk.Entry(self)
        self.entry_tel.place(x=200, y=110)

        # добавляем строку ввода для зарплаты
        self.entry_sal = tk.Entry(self)
        self.entry_sal.place(x=200, y=140)



        btn_edit = tk.Button(self, text='Редактировать')
        btn_edit.place(x=205, y=170)
        btn_edit.bind('<Button-1>', lambda event: self.view.update_record(self.entry_name.get(),
                                                                          self.entry_email.get(),
                                                                          self.entry_tel.get(),
                                                                          self.entry_sal.get()))

        # закрываем окно редактирования
        # add='+' позваляет на одну кнопку вешать более одного события
        btn_edit.bind('<Button-1>', lambda event: self.destroy(), add='+')
        

    def default_data(self):
        self.db.c.execute('''SELECT * FROM db WHERE id=?''',
                          (self.view.tree.set(self.view.tree.selection()[0], '#1'),))
        
        # получаем доступ к первой записи из выборки
        row = self.db.c.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_email.insert(0, row[2])
        self.entry_tel.insert(0, row[3])
        self.entry_sal.insert(0, row[4])

# класс поиска записи
class Search_ChldWind(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.title('Поиск')
        self.geometry('300x100')
        self.resizable(False, False)

        label_search = tk.Label(self, text='Поиск')
        label_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=105, y=20, width=150)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text='Поиск')
        btn_search.place(x=105, y=50)
        btn_search.bind('<Button-1>', 
                        lambda event: self.view.search_records(self.entry_search.get()))
        btn_search.bind('<Button-1>', 
                        lambda event: self.destroy(), add='+')



# класс БД
class DB:
    def __init__(self):
        # создаем соединение с БД
        self.conn = sqlite3.connect('./Project WorkerList/db/employee.db')
        
        # создание объекта класса cursor, используемый для взаимодействия с БД
        self.c = self.conn.cursor()
        # выполнение запроса к БД
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS db (id integer primary key, name text, tel text, email text, salary  text)''')
        # сохранение изменений БД
        self.conn.commit()

    # метод добавления в БД
    def insert_data(self, name, tel, email, salary):
        self.c.execute('''INSERT INTO db (name, tel, email, salary) VALUES (?, ?, ?, ?)''',
                       (name, tel, email, salary))
        self.conn.commit()



if __name__ == '__main__':
    root = tk.Tk()
    #os.chdir('./Project WorkerList')
    
    # экземпляр класса DB
    db = DB()
    app = main2(root)
    app.pack()
    # заголовок окна
    root.title('Список сотрудников компании')
    # размер окна
    root.geometry('815x450')
    # ограничение изменения размеров окна
    root.resizable(False, False)
    root.mainloop()