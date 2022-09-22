# Pass CAPTCHA v1.0
# Libs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import os
import time, requests

delayTime = 2
audioTextDelay = 3
filename = '../PassCaptcha/audio.mp3'
url = 'https://www.ipva.fazenda.sp.gov.br/ipvanet_consulta/consulta.aspx'
watsonLink = 'https://speech-to-text-demo.ng.bluemix.net/'
option = webdriver.ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-logging'])
option.add_argument("--window-size=800,750")


def audioToText(mp3):
    driver.execute_script('''window.open("","_blank");''')
    driver.switch_to.window(driver.window_handles[-1])
    print("3. Iniciando o Serviço IBM Watson Speech to Text")
    driver.get(watsonLink)
    print("3.1 Upload do Áudio -> Conversão Áudio - Texto")
    time.sleep(1)
    #root = driver.find_element(By.ID, 'root').find_elements(By.CLASS_NAME, 'dropzone _container _container_large')
    button = driver.find_element(By.XPATH, '//*[@id="root"]/div/input')
    button.send_keys('C:\\Users\\linol\\Documents\\pythonProjects\\PassCaptcha\\audio.mp3')
    #time.sleep(delayTime)
    time.sleep(audioTextDelay)
    texto = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[7]/div/div/div').find_elements(By.TAG_NAME, 'span')
    result = " ".join([each.text for each in texto])
    print("4. Conversão Finalizada")
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    return result


def saveFile(content, filename):
    with open(filename, "wb") as handle:
        for data in content.iter_content():
            handle.write(data)


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)
driver.get(url)
driver.set_window_position(566, 10, windowHandle='current')
print('1. Iniciando')
time.sleep(1)
print("2. Identificando Elementos da Página")
googleClass = driver.find_elements(By.CLASS_NAME, 'g-recaptcha')[0]
time.sleep(1)
outerIframe = googleClass.find_element(By.TAG_NAME, 'iframe')
time.sleep(1)
outerIframe.click()
time.sleep(1)
allIframesLen = driver.find_elements(By.TAG_NAME, 'iframe')
time.sleep(1)
audioBtnFound = False
audioBtnIndex = -1
for index in range(len(allIframesLen)):
    driver.switch_to.default_content()
    iframe = driver.find_elements(By.TAG_NAME, 'iframe')[index]
    driver.switch_to.frame(iframe)
    driver.implicitly_wait(delayTime)
    try:
        audioBtn = driver.find_element(By.ID, 'recaptcha-audio-button') or driver.find_element(By.ID,
                                                                                               'recaptcha-anchor')
        audioBtn.click()
        audioBtnFound = True
        audioBtnIndex = index
        break
    except Exception as e:
        pass
if audioBtnFound:
    try:
        while True:
            href = driver.find_element(By.ID, 'audio-source').get_attribute('src')
            response = requests.get(href, stream=True)
            saveFile(response, filename)
            response = audioToText(os.getcwd() + '/' + filename)
            driver.switch_to.default_content()
            iframe = driver.find_elements(By.TAG_NAME, 'iframe')[audioBtnIndex]
            driver.switch_to.frame(iframe)
            inputBtn = driver.find_element(By.ID, 'audio-response')
            print("5. Validando o Texto: " + response)
            inputBtn.send_keys(response)
            inputBtn.send_keys(Keys.ENTER)
            time.sleep(1)
            errorMsg = driver.find_elements(By.CLASS_NAME, 'rc-audiochallenge-error-message')[0]
            if errorMsg.text == "" or errorMsg.value_of_css_property('display') == 'none':
                print("6. Captcha Validado com Sucesso!")
                break
    except Exception as e:
        print(e)
        print('Necessário alterar o proxy!')
else:
    print('Botão não localizado!')
