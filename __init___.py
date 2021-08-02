import time
from gtts import gTTS
from playsound import playsound
import speech_recognition as sr
import selenium.webdriver as webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

def ouvir_microfone():
    microfone = sr.Recognizer()
    with sr.Microphone() as source:
        microfone.adjust_for_ambient_noise(source)
        print("Diga alguma coisa: ")    
        audio = microfone.listen(source)    
    
    try:
        frase = microfone.recognize_google(audio,language='pt-BR')
        print("Você disse: " + frase)
        return frase
    except :
        print("Não entendi")
        ouvir_microfone()
def pesquisaGoogle(audio):
    chrome_option = Options()
    chrome_option.headless = True
    chrome = webdriver.Chrome('./chromedriver', chrome_options=chrome_option)

    pesquisa = chrome.get("https://www.google.com/")
    pesquisa = chrome.find_element_by_name('q')
    pesquisa.send_keys(audio)
    pesquisa.send_keys(Keys.RETURN)
    time.sleep(5)
    teste = ''
    pesquisa = chrome.find_elements_by_tag_name('h3')
    for c in range(0,len(pesquisa)):
        if 'Descri' in pesquisa[c].text:
            teste = pesquisa[c].find_element_by_xpath('..')
            teste = teste.find_element_by_tag_name('span')
    return teste.text



def cria_audio(audio):

    tts = gTTS(audio,lang='pt-br')

    tts.save('hello.mp3')

    playsound('hello.mp3')

frase = ouvir_microfone()
resultado = pesquisaGoogle(frase)
cria_audio(resultado)