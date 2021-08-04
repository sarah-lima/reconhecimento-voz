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
    local_pesquisa = False
    pesquisa = chrome.find_elements_by_tag_name('h3')
    for c in range(len(pesquisa)):
        # google descrição
        if 'Descri' in pesquisa[c].text:
            local_pesquisa = False
            teste = pesquisa[c].find_element_by_xpath('..')
            teste = teste.find_element_by_tag_name('span').text
        else:
            local_pesquisa = True
    if local_pesquisa:
        pesquisa = chrome.find_elements_by_tag_name('h2')
        teste = pesquisa[0].find_element_by_xpath('..')
        # google link
        if '› ' in teste.find_element_by_tag_name('span').text:
            teste = teste.text
        # google clima
        elif 'clima' in pesquisa[0].text:
            teste += "°C"
        # google tradutor
        elif 'Inglês' in teste.find_element_by_tag_name('span').text:
            teste = teste.find_element_by_id('tw-target-text-container').text
        # google descrição
        else:
           teste = teste.find_element_by_tag_name('span').text
    return teste



def cria_audio(audio):

    tts = gTTS(audio,lang='pt-br')

    tts.save('hello.mp3')

    playsound('hello.mp3')

frase = ouvir_microfone()
resultado = pesquisaGoogle(frase)
cria_audio(resultado)