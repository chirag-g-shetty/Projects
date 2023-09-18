import matplotlib.pyplot as plt
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

def speak(text):
    import pyttsx3
    ts = pyttsx3.init()
    ts.setProperty('rate', 120)
    ts.setProperty('voice','HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')
    ts.say(text)
    ts.runAndWait()

def stats():
    uri=client=db=collection=0
    try:
        from params import gmail
        uri = "mongodb+srv://CGSMongo:gIWkRYRpnQBnCxeT@mongocluster.zo51ngp.mongodb.net/?retryWrites=true&w=majority"
        client = MongoClient(uri, server_api=ServerApi('1'))
        db = client['JustGest']
        collection = db['Users']
        _doc = collection.find_one({'gmail': gmail})
        data = _doc['l_t']
        if not any(data):
            speak('The data is empty')
            return
        plt.title('Your usage')
        plt.xlabel('Features →')
        plt.ylabel('Duration (min) →')
        plt.ylim(top= int(max(data)*1.5)+.5)
        plt.xticks(range(4),['Hand Mouse', 'Commands', 'Slang Code', 'Gameplay'])
        bars = plt.bar(range(4),data)
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, yval, round(yval, 2), ha='center', va='bottom')
        manager = plt.get_current_fig_manager()
        manager.window.geometry('+550+120')
        manager.window.title('Stats')
        plt.show()
    except:
        speak('Please check your internet connection')
