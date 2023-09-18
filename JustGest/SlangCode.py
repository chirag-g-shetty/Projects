def speak(text):
    import pyttsx3
    ts = pyttsx3.init()
    ts.setProperty('rate', 120)
    ts.setProperty('voice','HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')
    ts.say(text)
    ts.runAndWait()
def return_query():
    import speech_recognition as sr,os
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        speak('Go Ahead')
        audio = r.listen(source,phrase_time_limit=10)
        speak('Understanding the program')
        return r.recognize_google(audio)

def return_code(query):
    from bardapi import Bard
    import os
    os.environ['_BARD_API_KEY']='agioS7E3MYSMSH4dv1btHWyfDnohz3Te7V_EFU3iCo-yZL3Xcr5PQ29UtrsLUUflyr39hQ.'
    speak('Coding the program')
    code=Bard().get_answer(query)['content']
    code=code.split('```')
    code = code[1]
    return code[code.find('\n'):]

def type_em(s):
    import time
    from pynput.keyboard import Controller
    keyB = Controller()
    s = s.split('\n')
    speak('Here you go')
    for i in s:
        keyB.type(i.lstrip(' ')+'\n')

