from tkinter import *
import os
import pickle
from tkinter import filedialog
from tkinter import messagebox
from pygame import mixer
import tkinter.font as font
from tkinter import filedialog
import ast
import mysql.connector as mysql

root=Tk()
root.title('Music Player login')
root.geometry("925x500+300+200")
root.configure(bg="#fff")
root.resizable(False,False)

def signin():
    username=user.get()
    password=code.get()

    con=mysql.connect(host="localhost", user="root", password="Aman@123", database="music_player")
    cursor=con.cursor()
    cursor.execute("select * from user")
    r=cursor.fetchall()
    cursor.execute("commit");
    con.close();
    output=''
    
    for i in r:
        output=output +i[0]+ ' ' +i[1]+ '\n'
    
    
    
    
    if username in output and password in output:

#Music Player Code Begins .............................
        class Player(Frame):
            def __init__(self, master=None):
                super().__init__(master)
                self.master = master
                self.pack()
                mixer.init()

                if os.path.exists('songs.pickle'):
                        with open('songs.pickle', 'rb') as f:
                                self.playlist = pickle.load(f)
                         
                else:
                        self.playlist=[]
                    

                self.current = 0
                self.paused = True
                self.played = False

                self.create_frames()
                self.track_widgets()
                self.control_widgets()
                self.tracklist_widgets()

                self.master.bind('<Left>', self.prev_song)
                self.master.bind('<space>', self.play_pause_song)
                self.master.bind('<Right>', self.next_song)

            def create_frames(self):
                self.track = LabelFrame(self, text='Song Track', font=("times new roman",15,"bold"),bg="grey",fg="white",bd=5,relief=GROOVE)
                self.track.config(width=410,height=300)
                self.track.grid(row=0, column=0, padx=10)

                self.tracklist = LabelFrame(self, text=f'PlayList - {str(len(self.playlist))}',font=("times new roman",15,"bold"),bg="grey",fg="white",bd=5,relief=GROOVE)
                self.tracklist.config(width=220,height=400)
                self.tracklist.grid(row=0, column=1, rowspan=3, pady=5)

                self.controls = LabelFrame(self,font=("times new roman",15,"bold"),bg="white",fg="white",bd=2,relief=GROOVE)
                self.controls.config(width=410,height=80)
                self.controls.grid(row=2, column=0, pady=5, padx=10)

            def track_widgets(self):
                self.canvas = Label(self.track, image=img)
                self.canvas.configure(width=400, height=240)
                self.canvas.grid(row=0,column=0)

                self.songtrack = Label(self.track, font=("times new roman",16,"bold"),bg="white",fg="dark blue")
                self.songtrack['text'] = 'Music MP3 Player'
                self.songtrack.config(width=30, height=1)
                self.songtrack.grid(row=1,column=0,padx=10)

            def control_widgets(self):
                self.loadSongs = Button(self.controls, bg='green', fg='white', font=10)
                self.loadSongs['text'] = 'Load Songs'
                self.loadSongs['command'] = self.retrieve_songs
                self.loadSongs.grid(row=0, column=0, padx=10)

                self.prev = Button(self.controls, image=prev)
                self.prev['command'] = self.prev_song
                self.prev.grid(row=0, column=1)

                self.pause = Button(self.controls, image=pause)
                self.pause['command'] = self.pause_song
                self.pause.grid(row=0, column=2)

                self.next = Button(self.controls, image=next_)
                self.next['command'] = self.next_song
                self.next.grid(row=0, column=3)

                self.volume = DoubleVar(self)
                self.slider = Scale(self.controls, from_ = 0, to = 10, orient = HORIZONTAL)
                self.slider['variable'] = self.volume
                self.slider.set(8)
                mixer.music.set_volume(0.8)
                self.slider['command'] = self.change_volume
                self.slider.grid(row=0, column=4, padx=5)

                self.log_out = Button(self.controls, width=6,text='Log out',border=0,bg='white',cursor='hand2',fg='red',command=self.logout)
                self.log_out.grid(row=0, column=5)

                #sea=Button(self.tracklist,width=6,text='?',border=0,bg='white',cursor='hand2',fg='green',command=self.search)
                #self.sea.grid(row=10, column=2)

                #def on_enter(e):
                    #self.search.delete(0,'end')

                #def on_leave(e):
                    #nm=user.get()
                    #if nm=="":
                        #self.search.insert(0,'Search')


                #self.search=Entry(self.tracklist ,width=20,fg='black',border=1,bg='white',font=('Arial',8))
                #self.search.grid(row=10, column=1)
                #self.search.insert(0,'Search')
                #self.search.bind('<FocusIn>',on_enter)
                #self.search.bind('FocusOut>',on_leave)


                

                


            def tracklist_widgets(self):
                self.scrollbar = Scrollbar(self.tracklist, orient=VERTICAL)
                self.scrollbar.grid(row=0,column=2, rowspan=5, sticky='ns')

                self.list = Listbox(self.tracklist, selectmode=SINGLE, yscrollcommand=self.scrollbar.set, selectbackground='sky blue')
                self.enumerate_songs()
                self.list.config(height=22)
                self.list.bind('<Double-1>', self.play_song) 

                self.scrollbar.config(command=self.list.yview)
                self.list.grid(row=0, column=1, rowspan=5)

            def retrieve_songs(self):

                con=mysql.connect(host="localhost", user="root", password="Aman@123", database="music_player")
                cursor=con.cursor()
                cursor.execute("truncate table music")
                cursor.execute("commit");

                con.close();

                
                self.songlist = []
                directory = filedialog.askdirectory()
                for root_, dirs, files in os.walk(directory):
                        for file in files:
                                if os.path.splitext(file)[1] == '.mp3':
                                        path = (root_ + '/' + file).replace('\\','/')
                                        self.songlist.append(path)

                with open('songs.pickle', 'wb') as f:
                    pickle.dump(self.songlist, f)
                self.playlist = self.songlist
                self.tracklist['text'] = f'PlayList - {str(len(self.playlist))}'
                self.list.delete(0, END)
                self.enumerate_songs()
                

                

            def enumerate_songs(self):
                for index, song in enumerate(self.playlist):
                    
                    self.list.insert(index, os.path.basename(song))

                
                    con=mysql.connect(host="localhost", user="root", password="Aman@123", database="music_player")
                    cursor=con.cursor()
                    cursor.execute("insert into music values('"+ str(index) +"','"+ os.path.basename(song) +"')")
                    cursor.execute("commit");
                    

                
                    con.close();
                    
                    

                    

                    

            def play_pause_song(self, event):
                if self.paused:
                    self.play_song()
                else:
                    self.pause_song()

            def play_song(self, event=None):
                if event is not None:
                    self.current = self.list.curselection()[0]
                    for i in range(len(self.playlist)):
                        self.list.itemconfigure(i, bg="white")

                print(self.playlist[self.current])
                mixer.music.load(self.playlist[self.current])
                self.songtrack['anchor'] = 'w' 
                self.songtrack['text'] = os.path.basename(self.playlist[self.current])

                self.pause['image'] = play
                self.paused = False
                self.played = True
                self.list.activate(self.current) 
                self.list.itemconfigure(self.current, bg='sky blue')

                mixer.music.play()

            def pause_song(self):
                if not self.paused:
                    self.paused = True
                    mixer.music.pause()
                    self.pause['image'] = pause
                else:
                    if self.played == False:
                        self.play_song()
                    self.paused = False
                    mixer.music.unpause()
                    self.pause['image'] = play

            def prev_song(self, event=None):
                self.master.focus_set()
                if self.current > 0:
                    self.current -= 1
                else:
                    self.current = 0
                self.list.itemconfigure(self.current + 1, bg='white')
                self.play_song()

            def next_song(self, event=None):
                self.master.focus_set()
                if self.current < len(self.playlist) - 1:
                    self.current += 1
                else:
                    self.current = 0
                self.list.itemconfigure(self.current - 1, bg='white')
                self.play_song()

            def change_volume(self, event=None):
                self.v = self.volume.get()
                mixer.music.set_volume(self.v / 10)

            def logout(self,event=None):

                con=mysql.connect(host="localhost", user="root", password="Aman@123", database="music_player")
                cursor=con.cursor()
                cursor.execute("truncate table music")
                cursor.execute("commit");

                con.close();

                app.destroy()
                screen.destroy()
                messagebox.showinfo('Logout Status',"You've been successfully logged out.");


            #def search(self,event=None):
                #find=search.get()

                #if find in self.tracklist:
                    #self.songlist.replace(find)

                #else:
                    #messagebox.showerror('Invalid Song','This song is not in the list');
                    

# Music Player GUI .....................................

        if __name__ == '__main__':
            screen =Toplevel(root)
            screen.geometry('700x400+200+100')
            screen.title('Music Player')

            img = PhotoImage(file='icons/music.gif')
            next_=PhotoImage(file='icons/next.gif')
            prev = PhotoImage(file='icons/previous.gif')
            play = PhotoImage(file='icons/play.gif')
            pause = PhotoImage(file='icons/pause.gif')

            app = Player(master=screen)
            app.mainloop()
            

#Music Player Code Ends ..................................

    elif username =='Username' and password =='Password':
        messagebox.showerror('Invalid','Both fields are required')

    elif username in output and password not in output:
        messagebox.showerror('Invalid','Invalid password')

    elif username not in output and password in output:
        messagebox.showerror('Invalid','Invalid username')
        
    else:
        messagebox.showerror('Invalid','Invalid username or password')
    
#Sign Up Code Begins ...................................................
def signup_command():
    window=Toplevel(root)
    window.title('SignUp')
    window.geometry("925x500+300+200")
    window.configure(bg="#fff")
    window.resizable(False,False)

    def signup():
        username=user.get()
        password=code.get()
        confirm_password=confirm_code.get()

        if(username=="" or password=="" or confirm_password==""):
            messagebox.showinfo("Invalid","All fields are required")

        elif(confirm_password!=password):
            messagebox.showerror("Invalid","Both passwords should match")
    
        else:
            con=mysql.connect(host="localhost", user="root", password="Aman@123", database="music_player")
            cursor=con.cursor()
            cursor.execute("insert into user values('"+ username +"','"+ password +"')")
            cursor.execute("commit");

            messagebox.showinfo("Insert Status","Successfully sign up!!");
            con.close();

    def sign():
        window.destroy()

    img=PhotoImage(file='signup.png')
    Label(window,image=img,bg='white').place(x=100,y=150)

    frame=Frame(window,width=350,height=390,bg='white')
    frame.place(x=480,y=50)

    heading=Label(frame,text='Sign up',fg='#57a1f8',bg='white',font=('Arial',23,'bold'))
    heading.place(x=100,y=5)

    #####################-------------------------------------------------------

    def on_enter(e):
        user.delete(0,'end')

    def on_leave(e):
        name=user.get()
        if name=="":
            user.insert(0,'Username')


    user=Entry(frame,width=25,fg='black',border=0,bg='white',font=('Arial',11))
    user.place(x=30,y=80)
    user.insert(0,'Username')
    user.bind('<FocusIn>',on_enter)
    user.bind('FocusOut>',on_leave)

    Frame(frame,width=295,height=2,bg='black').place(x=25,y=107)

    ####################--------------------------------------------------------

    def on_enter(e):
        code.delete(0,'end')

    def on_leave(e):
        name=code.get()
        if name=="":
            code.insert(0,'Password')



    code=Entry(frame,width=25,fg='black',border=0,bg='white',font=('Arial',11))
    code.place(x=30,y=150)
    code.insert(0,'Password')
    code.bind('<FocusIn>',on_enter)
    code.bind('FocusOut>',on_leave)

    Frame(frame,width=295,height=2,bg='black').place(x=25,y=177)

    #############################################################
    def on_enter(e):
        confirm_code.delete(0,'end')

    def on_leave(e):
        name=confirm_code.get()
        if name=="":
            confirm_code.insert(0,'Password')



    confirm_code=Entry(frame,width=25,fg='black',border=0,bg='white',font=('Arial',11))
    confirm_code.place(x=30,y=220)
    confirm_code.insert(0,'Confirm Password')
    confirm_code.bind('<FocusIn>',on_enter)
    confirm_code.bind('FocusOut>',on_leave)

    Frame(frame,width=295,height=2,bg='black').place(x=25,y=247)
    #############################################################

    Button(frame,width=39,pady=7,text='Sign up',bg='#57a1f8',fg='white',border=0,command=signup).place(x=35,y=280)
    label=Label(frame,text="I have an account",fg='black',bg='white',font=('Arial',9))
    label.place(x=90,y=340)

    sign_in=Button(frame,width=6,text='Sign in',border=0,bg='white',cursor='hand2',fg='#57a1f8',command=sign)
    sign_in.place(x=200,y=340)

    window.mainloop()


#Sign Up Code Ends ............................................................................................                                       
    
img=PhotoImage(file='login.png')
Label(root,image=img,bg='white').place(x=40,y=-50)

frame=Frame(root,width=350,height=350,bg='white')
frame.place(x=480,y=70)

heading=Label(frame,text='Sign In',fg='#57a1f8',bg='white',font=('Arial',23,'bold'))
heading.place(x=100,y=5)
#####################-------------------------------------------------------

def on_enter(e):
    user.delete(0,'end')

def on_leave(e):
    name=user.get()
    if name=="":
        user.insert(0,'Username')


user=Entry(frame,width=25,fg='black',border=0,bg='white',font=('Arial',11))
user.place(x=30,y=80)
user.insert(0,'Username')
user.bind('<FocusIn>',on_enter)
user.bind('FocusOut>',on_leave)

Frame(frame,width=295,height=2,bg='black').place(x=25,y=107)

####################--------------------------------------------------------

def on_enter(e):
    code.delete(0,'end')

def on_leave(e):
    name=code.get()
    if name=="":
        code.insert(0,'Password')

def show_hide_password():
    if code['show']=='*':
        code.configure(show='')
        show_hide_btn.configure(text=show_face)
    else:
        code.configure(show='*')
        show_hide_btn.configure(text=hide_face)

hide_face='?'
show_face='?'

code=Entry(frame,width=25,fg='black',border=0,bg='white',font=('Arial',11),show='*')
code.place(x=30,y=150)

show_hide_btn=Button(frame, text=hide_face, font=('Bold', 15), bd=0,command=show_hide_password)
show_hide_btn.place(x=320,y=150)

code.insert(0,'Password')
code.bind('<FocusIn>',on_enter)
code.bind('FocusOut>',on_leave)

Frame(frame,width=295,height=2,bg='black').place(x=25,y=177)

#############################################################

Button(frame,width=39,pady=7,text='Sign in',bg='#57a1f8',fg='white',border=0,command=signin).place(x=35,y=204)
label=Label(frame,text="Don't have an account?",fg='black',bg='white',font=('Arial',9))
label.place(x=75,y=270)

sign_in=Button(frame,width=6,text='Sign up',border=0,bg='white',cursor='hand2',fg='#57a1f8',command=signup_command)
sign_in.place(x=215,y=270)


root.mainloop()

