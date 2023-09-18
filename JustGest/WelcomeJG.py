import traceback,sys,subprocess,re,Gmail_OTP as gmo,time,_thread as td,tkinter as tk,params as pm,FaceVerification as fv,HandMouse as hm,Analysis as ana
from tkinter import messagebox
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

with open('LogFile','a') as fp:
    try:
        x = pm.gmail
        fp.write('Logging in at '+time.ctime()+'\n')
    except: fp.write('Signing up in at '+time.ctime()+'\n')

t_hm=t_cmd=t_sd=t_gp=0

def display_image_for_seconds(image_path, duration):
    window = tk.Tk()
    window.geometry('750x270')
    window.geometry('+585+285')
    window.title("Welcome")
    img = tk.PhotoImage(file=image_path)
    label = tk.Label(window, image=img)
    label.place(x=0, y=0, relwidth=1, relheight=1)
    window.after(duration, window.destroy)
    window.mainloop()

td.start_new_thread(display_image_for_seconds,('IntroImg.png', 5700))

def speak(text):
    import pyttsx3
    ts = pyttsx3.init()
    ts.setProperty('rate', 120)
    ts.setProperty('voice','HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')
    ts.say(text)
    ts.runAndWait()

def stop_mouse():
    hm.mouse_in_action=False
    time.sleep(1)
    hm.mouse_in_action=True



client=0
uri = "mongodb+srv://CGSMongo:gIWkRYRpnQBnCxeT@mongocluster.zo51ngp.mongodb.net/?retryWrites=true&w=majority"
try:
    client = MongoClient(uri, server_api=ServerApi('1'))
except Exception as e:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    filename = exc_traceback.tb_frame.f_code.co_filename
    line_number = exc_traceback.tb_lineno
    print(f"Exception occurred: {e} in {filename} at line {line_number}")
    speak('Please check your internet connection')
    exit(1)

collection = client['JustGest']['Users']
def putter():
    global t_hm,t_cmd,t_sd,t_gp
    s=_s=0
    with open('params.py','r') as fp:
        s = fp.readlines()[0]
        _s = f'l_t = [{round(t_hm/60,2)},{round(t_cmd/60,2)},{round(t_sd/60,2)},{round(t_gp/60,2)}]'
    with open('params.py','w') as fp:
        fp.writelines([s,_s])
def updater():
    global collection
    gmail = pm.gmail
    n_l = pm.l_t
    _doc = collection.find_one({'gmail':gmail})
    p_l = _doc['l_t']
    for i in range(4):
        p_l[i]+=n_l[i]
    collection.update_one({'gmail':gmail},{'$set':{'l_t':p_l}})
    s=_s=0
    with open('params.py', 'r') as fp:
        s = fp.readlines()[0]
        _s = 'l_t = [0,0,0,0]'
    with open('params.py', 'w') as fp:
        fp.writelines([s, _s])

try:
    with open('params.py','r') as fffp:
        if len(fffp.read())>2:
            updater()
        else: speak('Welcome, nice to meet you, my name is Just Gest')
except Exception as e:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    filename = exc_traceback.tb_frame.f_code.co_filename
    line_number = exc_traceback.tb_lineno
    print(f"Exception occurred: {e} in {filename} at line {line_number}")
    speak('Please check your internet connection')
    import sys
    sys.exit(1)

def menu_bar():
    window = tk.Tk()
    window.geometry('187x180')
    window.geometry('+850+350')
    window.place_slaves()
    window.title('C')
    window.iconbitmap('Logo.ico')

    def hand_mouse_click():
        speak('Show me your hand')
        try:
            td.start_new_thread(hm.the_h_mouse,())
        except:
            speak('Oops!There was a glitch, please try again')

    def commands_click():
        global t_cmd
        t1=time.time()
        import Cmds as cd
        try:
            cd.quick_actions()
        except: speak('Please check your internet connection')
        t_cmd+=(time.time()-t1)
    def slang_code_click():
        global t_sd
        t1=time.time()
        import SlangCode as sd
        try:
            sd.type_em(sd.return_code(sd.return_query()))
        except: speak('Oops!There was a glitch, please try again')
        t_sd+=(time.time()-t1)
    def gameplay_click():
        global t_gp
        speak("Let's Play")
        speak("Please adjust your head for neutral alignment to have an enjoyable time playing")
        t1=time.time()
        import GamePlay
        t_gp+=(time.time()-t1)
        speak("Gameplay stopped. If you want to play for unlimited time, upgrade to professional version")
    def analysis_click():
        speak("Let's see the statistics")
        ana.stats()
    def stop_click():
        global t_hm
        td.start_new_thread(stop_mouse,())
        t_hm += hm.r_sec
        hm.r_sec=0
        speak('Process stopped')

    def exit_click():
        global t_hm
        td.start_new_thread(stop_mouse, ())
        t_hm += hm.r_sec
        speak('Signing off, see you next time')
        window.destroy()

    hand_mouse_button = tk.Button(window, text="Hand Mouse", command=hand_mouse_click, width=10, height=1)
    commands_button = tk.Button(window, text="Commands", command=commands_click, width=10, height=1)
    slang_code_button = tk.Button(window, text="Slang Code", command=slang_code_click, width=10, height=1)
    gameplay_button = tk.Button(window, text="Gameplay", command=gameplay_click, width=10, height=1)
    analysis_button = tk.Button(window, text="Analysis", command=analysis_click, width=10, height=1)
    stop_button = tk.Button(window, text="Stop", command=stop_click, width=10, height=1)
    exit_button = tk.Button(window, text="Exit", command=exit_click, width=10, height=1)

    hand_mouse_button.place(x=5, y=5)
    commands_button.place(x=5, y=40)
    slang_code_button.place(x=5, y=75)
    gameplay_button.place(x=5, y=110)
    analysis_button.place(x=5, y=145)
    stop_button.place(x=95, y=55)
    exit_button.place(x=95, y=95)

    window.mainloop()
def get_gmail():
    gmail__ = {'gmail':''}
    window = tk.Tk()
    window.geometry('300x100')
    window.geometry('+800+350')
    window.title('JustGest')
    window.iconbitmap('Logo.ico')
    tk.Label(window, text="Gmail:").pack()
    gmail_entry = tk.Entry(window)
    gmail_entry.pack()

    def on_next_button_click():
        gmail__['gmail'] = gmail_entry.get()
        window.destroy()

    next_button = tk.Button(window, text="Next", command=on_next_button_click)
    next_button.pack()
    window.mainloop()
    return gmail__['gmail']


def get_otp():
    otp__= {'otp':''}

    window = tk.Tk()
    window.geometry('300x105')
    window.geometry('+800+350')
    window.title("OTP")
    window.iconbitmap('Logo.ico')
    tk.Label(window, text="OTP:").pack()
    otp_entry = tk.Entry(window)
    otp_entry.pack()

    def on_next_button_click():
        otp__['otp'] = otp_entry.get()
        window.destroy()

    next_button = tk.Button(window, text="Next", command=on_next_button_click)
    next_button.pack()
    window.mainloop()
    return otp__['otp']


otp = ''
data =0
with open('params.py', 'r') as  fp:
    data = fp.read()

if '1' in data:
    gmail__ = get_gmail()
    if collection.find_one({'gmail': gmail__}) != None:
        messagebox.showerror('Account Creation Failed', 'Account already exists')
    else:
        try:
            otp = gmo.mailer(gmail__)
            if (get_otp() == otp):
                speak('Show me your face so that I can recognize you next time')
                fv.cap_N_save()
                collection.insert_one(
                    {'gmail': gmail__, 'time_s': time.ctime(),
                     'otp': otp,'l_t':[0,0,0,0]})
                with open('params.py', 'w') as ffp:
                    ffp.writelines(["gmail=" + "'" + gmail__ + "'", "\nl_t = [0,0,0,0]"])
                messagebox.showinfo('Validation Success', 'Go ahead and explore!')
                try:
                    speak('Welcome to Just Gest')
                    menu_bar()
                    putter()
                except:
                    putter()
                    speak('Oops!There was a glitch, please try again')
            else:messagebox.showerror('Validation Failed', 'OTP invalid')
        except KeyboardInterrupt:
            putter()
            pass
        except Exception as e:
            putter()
            exc_type, exc_value, exc_traceback = sys.exc_info()
            filename = exc_traceback.tb_frame.f_code.co_filename
            line_number = exc_traceback.tb_lineno
            print(f"Exception occurred: {e} in {filename} at line {line_number}")
            messagebox.showerror('Account Creation Failed', 'Gmail invalid')
    client.close()
else:
    fp.close()
    try:
        _doc_ = collection.find_one({'gmail': pm.gmail})
        speak('Let me verify whether it is you')
        _allow_=fv.verify()
        client.close()
        if _allow_:
            name = pm.gmail.rstrip('com')
            name = name.replace('gmail','')
            name = re.sub(r'[^A-Za-z]', '', name)
            speak('Welcome back '+name)
            menu_bar()
            putter()
        else:
            speak('You are not recognized')
    except Exception as e :
        putter()
        exc_type, exc_value, exc_traceback = sys.exc_info()
        filename = exc_traceback.tb_frame.f_code.co_filename
        line_number = exc_traceback.tb_lineno
        print(f"Exception occurred: {e} in {filename} at line {line_number}")
        speak('Oops!There was a glitch, please try again')


