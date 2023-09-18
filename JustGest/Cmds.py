import pyautogui as pag
shortcuts = {'action': 'win+a', 'record': 'win+alt+r', 'board': 'win+v', 'shot': 'win+shift+s', 'mini': 'alt+space+n',
             'all': 'win+m', 'type': 'win+h', 'explore': 'win+e', 'run': 'win+r', 'news': 'win+w',
             'notification': 'win+n',
             'setting': 'win+i', 'close': 'alt+f4', 'shut': 'win+x+u+u', 'sleep': 'win+x+u+s', 'sign': 'win+x+u+i',
             'restart': 'win+x+u+r'}

def search_google(query):
    import webbrowser as web
    url = f"https://www.google.com/search?q={query}"
    web.open(url)

def speak(text):
    import pyttsx3
    ts = pyttsx3.init()
    ts.setProperty('rate', 120)
    ts.setProperty('voice','HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')
    ts.say(text)
    ts.runAndWait()

def speak_delay():
    import time
    time.sleep(0.5)
    speak('Go ahead')

def return_audio_text():
    import speech_recognition as sr
    import pyaudio as pa
    import _thread as tdd
    FORMAT = pa.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = 8
    audio = pa.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,rate=RATE,
                        input=True,frames_per_buffer=CHUNK) # audio stream used to record audio
    frames = []
    tdd.start_new_thread(speak_delay,())
    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    stream.stop_stream()
    stream.close()
    audio.terminate()
    recognizer = sr.Recognizer()
    audio_data = sr.AudioData(b''.join(frames), RATE, 2) #Joining of frames into a continuous byte stream being
                                                         #converted to AudioData object which is an intermediate
                                                         #representation of audio
    try:
        return recognizer.recognize_google(audio_data).lower()
    except:
        try:
            speak('Command not recognized')
        except: pass
def quick_actions():
    query = return_audio_text()
    if query is not None:
        speak('Command accepted')
        map_to_key(query)
def map_to_key(query):
    query = query.replace('go','')
    query = query.replace('ahead','')
    if 'google' in query or 'ogle' in query:
        query=query.replace('google','')
        query=query.replace('ogle','')
        search_google(query)
    elif 'lock' in query:
        import ctypes
        user32 = ctypes.windll.user32
        user32.LockWorkStation()
    else:
        cmd = ''
        for i in query.split():
            cmd += i
        buttons = []
        f = 0
        for i in shortcuts.keys():
            if i in cmd:
                f+=1
                buttons = shortcuts[i].split('+')
                break
        if not f:
            pag.press('win')
            pag.sleep(2)
            pag.typewrite(query)
            pag.press('enter')
        else: run_cmd(tuple(buttons))


def run_cmd(buttons):
    pag.FAILSAFE=False
    if len(buttons) == 4:
        pag.hotkey(buttons[0], buttons[1])
        pag.sleep(0.225)
        pag.press(buttons[2])
        pag.sleep(0.225)
        pag.press(buttons[3])
    else:
        pag.hotkey(buttons)

quick_actions()