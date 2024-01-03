import json
import tkinter
from tkinter import *
from tkcalendar import DateEntry
from datetime import datetime
import hashlib

#Şifre ve database değişkenleri:
#aşağıda hash'ı bulunan şifre "a"dır
right_password_hashed = "ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb"
right_username = "a"
database_file_name = "task_database.json"
today = datetime.now().strftime("%Y-%m-%d")
#today_datetime = datetime_convert(today)


#Frontend, kullanılan renkler ve boyutlar:
general_background = "#00686e"
general_background2 = 	"#2c122d"
selected_button_color = "#0e3041"
normal_button_color = "#032238"
text_color = "#fffbd6"
title_label_background = "#2c122d"
title_label_background2 = "#222f5b"
title_label_text_color2 = text_color
entry_field_background = "#00686e"
update_button_background = "#ddb321"
tasks_background = general_background
completed_task_background = "#7ca751"
cancel_background = "#d44d4d"

button_height= 2
button_width=15
button_pady=1
button_padx=3

general_padx = 10
general_pady =10

task_name_length= 25
task_parameter_length = 15

#-----------------------------------------------------------------------

#Özel hatalar:
class Task_Not_Found(Exception):
    #Görev bulunamadığında fırlatılan hata:
    def __init__(self,message):
        super().__init__(message)

class Not_Valid_Type_Entered(Exception):
    #Kullanıcı istenilen şekilde veriyi girmediyse fırlatılan hata:
    def __init__(self,message):
        super().__init__(message)

def datetime_convert(time_string):
    #Zamanı alıp datetime kütüphanesinin kullandığı formata çeviren metot:
    converted_datetime = datetime.strptime(time_string, "%Y-%m-%d")
    return converted_datetime

#tarihleri "2023-01-01" şeklinde alır
def get_day_count_between(date2,date1):
    #iki gün arasındaki uzunluğu hesaplayan metot:
    return (datetime_convert(date2)-datetime_convert(date1)).days
#print(get_day_count_between("2020-1-1","2023-2-2"))
def add_task(tasks,name,start_date,end_date,isComplated):
    #Listeye görev ekleme işlemi yapan metot:
    tasks.append(Task(name,start_date,end_date,isComplated))
    #return tasks

def delete_task(tasks,task_name):
    #Listeden görevi silme işlemini yapan metot:
    for task in tasks:
        if task.name == task_name:
            tasks.remove(task)
            return None
    raise Task_Not_Found("Delete failed, task not found")
class Task():
    #Görevlerin örneklerinin oluşturulduğu ve değerlerinin depolandığı sınıf:
    def __init__(self,name,start_date,end_date,isComplated):
        self.start_date =start_date
        self.end_date =end_date
        self.name =name
        self.isCompleted = isComplated
    #Görevin bitişine kaç gün kaldığını döndüren metot:
    def get_days_left(self):
        return get_day_count_between(self.end_date,today)
    def get_total_day(self):
        #Görevin başlangıç tarihinden bitiş tarihine olan tüm süreyi döndüren metot:
        return get_day_count_between(self.start_date,self.end_date)
    #Görevin bitirilme yüzdesini gün sayısını kullanarak hesaplayan metot:
    def get_completion_percentage(self):
        if self.get_passed_day_count() / self.get_total_day() * 100 <= 0:
            return 0
        elif self.get_passed_day_count() / self.get_total_day() * 100 < 100:
            return self.get_passed_day_count() / self.get_total_day() * 100
        else:
            return 100
    #Görevin başlangıcından beri kaç gün geçtiğini döndüren metot:
    def get_passed_day_count(self):
        return get_day_count_between(today,self.start_date)
#--------------------------------------------------------------------

#Görevleri json dosyasından çeken fonksiyon:
def get_tasks():
    try:
        with open(database_file_name, 'r') as json_file:
            loaded_data = json.load(json_file)
        loaded_tasks = [Task(task['name'],task['start_date'], task['end_date'], task['isCompleted']) for task in loaded_data]
        return loaded_tasks
    except FileNotFoundError:
        with open(database_file_name, 'w') as json_file:
            json.dump([], json_file)
        return []
#Görevleri json dosyasına yazan fonksiyon:
def store_data(tasks):
    serialized_tasks = [task.__dict__ for task in tasks]
    with open(database_file_name, 'w') as json_file:
        json.dump(serialized_tasks, json_file, indent=len(tasks))
#----------------------------------------------------------------------
#Görevlerin kullanım için dosyadan alınması:
tasks = get_tasks()

#Uygulamanın çalıştırılmaya başlandığı ana tkinter sınıfı:
class ToDoListApp(tkinter.Tk):

    def __init__(self, *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)
        container = tkinter.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        #Mevcut Sayfaların tek tek tanımlanması:
        for i in (MainPage, AddPage, DeletePage, LoginPage):
            frame = i(container, self)
            self.frames[i] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginPage)

     #Verilen sayfayı gösteren metot:
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

#Görevlerin kullanıcıya gösterildiği ana navigasyon sayfası:
class MainPage(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)
        titleframe = tkinter.Frame(self, background=general_background)
        #Uygulamanın üst tarafında bulunan navigasyon butonlarının oluşturulduğu fonksiyon:
        def create_tittle_buttons():
            button = tkinter.Button(titleframe, text="Ana",
                                    command=lambda: controller.show_frame(MainPage),
                                    background=selected_button_color,
                                    foreground=text_color,
                                    height=button_height,
                                    width=button_width)
            button.grid(row=0, column=0, pady=button_pady, padx=button_padx)

            button = tkinter.Button(titleframe, text="Ekle",
                                    command=lambda: controller.show_frame(AddPage),
                                    background=normal_button_color,
                                    foreground=text_color,
                                    height=button_height,
                                    width=button_width)
            button.grid(row=0, column=1, pady=button_pady, padx=button_padx)
            button2 = tkinter.Button(titleframe, text="Sil",
                                     command=lambda: controller.show_frame(DeletePage),
                                     background=normal_button_color,
                                     foreground=text_color,
                                    height=button_height,
                                    width=button_width)
            button2.grid(row=0, column=2, pady=button_pady, padx=button_padx)

            button3 = tkinter.Button(titleframe, text="Çıkış Yap",
                                     command=lambda: controller.show_frame(LoginPage),
                                     background=normal_button_color,
                                     foreground=text_color,
                                     height=button_height,
                                     width=button_width)
            button3.grid(row=0, column=3, pady=button_pady, padx=button_padx)
        create_tittle_buttons()

        #Başlık.
        titleframe.pack(padx=6, pady=6)
        title_label = tkinter.Label(self, text="Görevler Listesi:", background=title_label_background, foreground=text_color)

        #Görevlerin ve butonalrının içerisinde bulunacağı frame.
        tasksframe = tkinter.Frame(self, background=general_background)

        #Görevlerin tamamlanıp tamamlanmadığını isCompleted değişkenini değiştirerek güncelleyen metot:
        def update_task_status(task_name, completed):
            print(task_name)
            for task in tasks:
                if task.name == task_name and task.isCompleted != completed.get():
                    task.isCompleted = completed.get()
                    break
            store_data(tasks)
            update_tasks()

        #Silme ve ekleme işlemlerinden sonra görevler listesinin güncellenemsinde kullanılan metot:
        def update_tasks():
            tasks = get_tasks()
            #Tüm eski görevlerin temizlenmesi ve güncellenmiş hallerin yazılması:
            for widget in tasksframe.winfo_children():
                widget.destroy()
            n = 0
            #Tüm görevlerin tek tek eklenmesi:
            for task in tasks:
                task_text = task.name.ljust(task_name_length, " ") + task.start_date.ljust(task_parameter_length, " ") + \
                                task.end_date.ljust(task_parameter_length, " ")

                completed = IntVar()
                task_label = tkinter.Label(tasksframe, text=task_text,
                                            background=general_background, foreground=text_color)
                task_label.grid(row=n, column=0, pady=10, padx=10)
                #Görevlerin yanında bulunan tamamlandı butonlarının isCompleted değişkenine göre yerleştirilmsi:
                if task.isCompleted:
                    complete_button = tkinter.Button(tasksframe, text="Tamamla", background=normal_button_color,
                                                     foreground=text_color,
                                                     command=lambda task_name=task.name, completed=completed: update_task_status(task_name,
                                                                                                    completed))
                    complete_button.grid(row = n, column=1, padx=10, pady=10)
                else:
                    completed_label = tkinter.Label(tasksframe, text="Tamamlandı",
                                               background=completed_task_background, foreground=text_color)
                    completed_label.grid(row=n, column=1, pady=10, padx=10)
                n +=1
            tasksframe.pack(pady=10, padx=10)
        #Değişiklikleri uygula butonu ve başlığın ekrana yerleştirilmsi:
        update_button = tkinter.Button(self, text="Değişiklikleri Uygula", background=update_button_background, foreground=text_color,
                                       command=update_tasks)
        update_button.pack(side="top", anchor="nw", padx=10, pady=10)
        title_label.pack(pady=10, padx=10)
        update_tasks()

        #arka plan rengi ayarlanması:
        self.configure(bg=general_background)

#Görev ekleme penceresini kontrol eden sınıf:
class AddPage(tkinter.Frame):

    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)
        titleframe = tkinter.Frame(self, background=general_background)
        #Navigasyon butonlarının oluşturulması:
        def create_tittle_buttons():
            button = tkinter.Button(titleframe, text="Ana",
                                    command=lambda: controller.show_frame(MainPage),
                                    background=normal_button_color,
                                    foreground=text_color,
                                    height=button_height,
                                    width=button_width)
            button.grid(row=0, column=0, pady=button_pady, padx=button_padx)

            button = tkinter.Button(titleframe, text="Ekle",
                                    command=lambda: controller.show_frame(AddPage),
                                    background=selected_button_color,
                                    foreground=text_color,
                                    height=button_height,
                                    width=button_width)
            button.grid(row=0, column=1, pady=button_pady, padx=button_padx)

            button2 = tkinter.Button(titleframe, text="Sil",
                                     command=lambda: controller.show_frame(DeletePage),
                                     background=normal_button_color,
                                     foreground=text_color,
                                    height=button_height,
                                    width=button_width)
            button2.grid(row=0, column=2, pady=button_pady, padx=button_padx)

            button3 = tkinter.Button(titleframe, text="Çıkış Yap",
                                     command=lambda: controller.show_frame(LoginPage),
                                     background=normal_button_color,
                                     foreground=text_color,
                                     height=button_height,
                                     width=button_width)
            button3.grid(row=0, column=3, pady=button_pady, padx=button_padx)
        create_tittle_buttons()
        titleframe.pack(padx=6, pady=6)

        #Kullanıcıdan eklenmek istenin görevin bilgilerinin alınması:
        entry_frame = tkinter.Frame(self,background=general_background2)
        title_label = tkinter.Label(entry_frame, text="Eklemek İstediğiniz Görevin Adı:", background=title_label_background, foreground=text_color)
        title_label.grid(row = 0,column=0,pady=10, padx=10)
        name_entry = tkinter.Entry(entry_frame, background=entry_field_background)
        name_entry.grid(row = 0, column=1, padx=general_padx, pady=general_pady)

        title_label = tkinter.Label(entry_frame, text="Görevin Başlangıç Tarihi:", background=title_label_background,
                                    foreground=text_color)
        title_label.grid(row = 1,column=0,pady=10, padx=10)
        startdate_entry = DateEntry(entry_frame, date_pattern='yyyy-mm-dd', background=entry_field_background)
        startdate_entry.grid(row = 1, column=1, padx=general_padx, pady=general_pady)

        title_label = tkinter.Label(entry_frame, text="Görevin Bitiş Tarihi:", background=title_label_background,
                                    foreground=text_color)
        title_label.grid(row = 2,column=0,pady=10, padx=10)
        enddate_entry = DateEntry(entry_frame, date_pattern='yyyy-mm-dd', background=entry_field_background)
        enddate_entry.grid(row = 2, column=1, padx=general_padx, pady=general_pady)

        #Kullanıcı hatalı bir işlem yaparsa onu uyarmak için kullanılacak uyarı label'i:
        warning_label = tkinter.Label(self, text="", background=general_background,
                                    foreground=text_color)
        warning_label.pack()
        #Ekle butonu metodu:
        def add_button_clicked():
            try:
                if name_entry.get() == "":
                    raise Not_Valid_Type_Entered("Empty task name not allowed")
                else:
                    add_task(tasks,name_entry.get(),startdate_entry.get(),enddate_entry.get(),1)
                    warning_label.configure(text="Ekleme İşlemi Başarılı", background=completed_task_background)
                    #ekleme işleminden sonra json dosyasının güncellenmesi:
                    store_data(tasks)
            except Not_Valid_Type_Entered:
                warning_label.configure(text="Lütfen geçerli bir isim giriniz",background=title_label_background)

        butonframe = tkinter.Frame(self,background=general_background2)
        add_button = tkinter.Button(butonframe, text="Ekle",
                                 command= add_button_clicked,
                                 background=selected_button_color,
                                 height=button_height,
                                 width=button_width)
        add_button.grid(row = 0,column=0,pady=button_pady, padx=button_padx)
        cancel_button = tkinter.Button(butonframe, text="İptal",
                                       command=lambda: controller.show_frame(MainPage),
                                       background=selected_button_color,
                                       height=button_height,
                                       width=button_width)
        cancel_button.grid(row = 0, column=1,pady=button_pady, padx=button_padx)
        #Kalan her şeyin ekrana yerleştirilmesi vearka plan rengi.
        entry_frame.pack()
        butonframe.pack()
        self.configure(bg=general_background)

#Görev silme penceresini kontrol eden sınıf:
class DeletePage(tkinter.Frame):

    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)
        titleframe = tkinter.Frame(self, background=general_background)
        #Navigasyon butonlarının oluşturulması:
        def create_tittle_buttons():
            button = tkinter.Button(titleframe, text="Ana",
                                    command=lambda: controller.show_frame(MainPage),
                                    background=normal_button_color,
                                    foreground=text_color,
                                    height=button_height,
                                    width=button_width)
            button.grid(row=0, column=0, pady=button_pady, padx=button_padx)

            button = tkinter.Button(titleframe, text="Ekle",
                                    command=lambda: controller.show_frame(AddPage),
                                    background=normal_button_color,
                                    foreground=text_color,
                                    height=button_height,
                                    width=button_width)
            button.grid(row=0, column=1, pady=button_pady, padx=button_padx)

            button2 = tkinter.Button(titleframe, text="Sil",
                                     command=lambda: controller.show_frame(DeletePage),
                                     background=selected_button_color,
                                     foreground=text_color,
                                    height=button_height,
                                    width=button_width)
            button2.grid(row=0, column=2, pady=button_pady, padx=button_padx)

            button3 = tkinter.Button(titleframe, text="Çıkış Yap",
                                     command=lambda: controller.show_frame(LoginPage),
                                     background=normal_button_color,
                                     foreground=text_color,
                                     height=button_height,
                                     width=button_width)
            button3.grid(row=0, column=3, pady=button_pady, padx=button_padx)
        create_tittle_buttons()

        #Kullanıcıdan verileri alma:
        titleframe.pack(padx=6, pady=6)
        title_label = tkinter.Label(self, text="Silmek İstediğiniz Görevin Adı:", background=title_label_background2,
                                    foreground=title_label_text_color2)
        title_label.pack(pady=10, padx=10)
        name_entry = tkinter.Entry(self, background=entry_field_background)
        name_entry.pack(padx=general_padx, pady=general_pady)

        #Kullanıcıyı uyarma label'i:
        warning_label = tkinter.Label(self, text="", background=general_background,
                                      foreground=text_color)
        warning_label.pack()

        #Silme işleminin gerçekleştirilmesi:
        def delete_button_clicked():
            try:
                if name_entry.get() == "":
                    raise Not_Valid_Type_Entered("Empty task name not allowed")
                else:
                    delete_task(tasks, name_entry.get())
                    warning_label.configure(text="Silme İşlemi Başarılı", background=completed_task_background)
                    store_data(tasks)

            except Not_Valid_Type_Entered:
                warning_label.configure(text="Lütfen geçerli bir isim giriniz",background=title_label_background)
            except Task_Not_Found:
                warning_label.configure(text="Silmek İstediğiniz Görev Bulunamadı, Doğru Adı Girdiğinizden Emin Olunuz",background=title_label_background)

        #İptal ve sil tuşları:
        butonframe = tkinter.Frame(self,background=general_background2)
        delete_button = tkinter.Button(butonframe, text="Sil",
                                       command=delete_button_clicked,
                                       background=selected_button_color,
                                       height=button_height,
                                       width=button_width)
        delete_button.grid(row=0, column=0, pady=button_pady, padx=button_padx)
        cancel_button = tkinter.Button(butonframe, text="İptal",
                                       command=lambda: controller.show_frame(MainPage),
                                       background=selected_button_color,
                                       height=button_height,
                                       width=button_width)
        cancel_button.grid(row=0, column=1, pady=button_pady, padx=button_padx)

        butonframe.pack()
        self.configure(bg=general_background)

#Giriş yapma penceresi:
class LoginPage(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)
        titleframe = tkinter.Frame(self, background=general_background)
        #Navigasyon butonlarının oluşturulması ve giriş yapılana kadar disable edilmesi:
        def create_tittle_buttons():
            button = tkinter.Button(titleframe, text="Ana",
                                    command=lambda: controller.show_frame(MainPage),
                                    background=normal_button_color,
                                    foreground=text_color,
                                    height=button_height,
                                    width=button_width)
            button.grid(row=0, column=0, pady=button_pady, padx=button_padx)
            button["state"] = "disabled"
            button2 = tkinter.Button(titleframe, text="Ekle",
                                    command=lambda: controller.show_frame(AddPage),
                                    background=normal_button_color,
                                    foreground=text_color,
                                    height=button_height,
                                    width=button_width)
            button2.grid(row=0, column=1, pady=button_pady, padx=button_padx)
            button2["state"] = "disabled"
            button3 = tkinter.Button(titleframe, text="Sil",
                                     command=lambda: controller.show_frame(DeletePage),
                                     background=normal_button_color,
                                     foreground=text_color,
                                    height=button_height,
                                    width=button_width)
            button3.grid(row=0, column=2, pady=button_pady, padx=button_padx)
            button3["state"] = "disabled"
            button4 = tkinter.Button(titleframe, text="Giriş Yap",
                                     command=lambda: controller.show_frame(LoginPage),
                                     background=selected_button_color,
                                     foreground=text_color,
                                     height=button_height,
                                     width=button_width)
            button4.grid(row=0, column=3, pady=button_pady, padx=button_padx)
        create_tittle_buttons()
        titleframe.pack(padx=6, pady=6)

        #Kullanıcı adı ve şifre alınması:
        entry_frame = tkinter.Frame(self,background=general_background2)
        username_label = tkinter.Label(entry_frame, text="Kullanıcı Adı:", background=title_label_background,
                                       foreground=text_color)
        username_label.grid(row=0, column=0, pady=10, padx=10)
        username_entry = tkinter.Entry(entry_frame, background=entry_field_background)
        username_entry.grid(row=0, column=1, padx=general_padx, pady=general_pady)

        password_label = tkinter.Label(entry_frame, text="Şifre:", background=title_label_background,
                                       foreground=text_color)
        password_label.grid(row=1, column=0, pady=10, padx=10)
        password_entry = tkinter.Entry(entry_frame,show="*", background=entry_field_background)
        password_entry.grid(row = 1, column=1, padx=general_padx, pady=general_pady)

        #Uyarı label'i:
        warning_label = tkinter.Label(self, text="Hoşgeldiniz", background=title_label_background,
                                       foreground=cancel_background)
        warning_label.pack()

        #Giriş yap butonu metotdu:
        def login_button():
            #Kullanıcının girdiği şifrenin hash'inin alınıp karşılaştırılması:
            hashed = hashlib.sha256(password_entry.get().encode('UTF-8')).hexdigest()
            #print(hashed)
            if username_entry.get()==right_username and hashed==right_password_hashed:
                controller.show_frame(MainPage)
                warning_label.configure(text="Hoşgeldiniz")
            else:
                warning_label.configure(text="Hatalı Şifre veya Kullanıcı Adı")
                print("hatalı şifre")


        butonframe = tkinter.Frame(self,background=general_background2)
        add_button = tkinter.Button(butonframe, text="Giriş Yap",
                                 command= login_button,
                                 background=completed_task_background,
                                 height=button_height,
                                 width=button_width)
        add_button.grid(row = 0,column=0,pady=button_pady, padx=button_padx)

        #ekrana yerleştirme ve arka plan rengi:
        entry_frame.pack(padx=6, pady=6)
        butonframe.pack()


        warning_label2 = tkinter.Label(self, text="Kullanıcı adı: \"a\", şifre: \"a\" olarak atanmıştır", background=title_label_background,
                                      foreground="yellow")
        warning_label2.pack()

        self.configure(bg=general_background)


#uygulamanın oluşturulması, başlığın ayarlanması çalıştırılması:
app = ToDoListApp()
app.title("To Do List Uygulaması")
app.mainloop()
store_data(tasks)
