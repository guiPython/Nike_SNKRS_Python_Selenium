from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import time as time 
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('disable-infobars')
options.add_argument("--disable-extensions")

info = {}
try:
    manipulador = open('config.txt', 'r', encoding ='utf-8')
    for linha in manipulador:
        valor = linha[6::].strip()
        chave = linha[0:5].strip()
        info[chave] = valor
    manipulador.close()
except FileNotFoundError:
    print('O arquivo de configuração não foi encontrado.')
    input()
    
driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(),chrome_options=options)
driver.get('https://www.nike.com.br')
WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.ID,'anchor-acessar'))).click()
driver.maximize_window()

def login_form(driver):
    email = driver.find_element_by_name("emailAddress")
    senha = driver.find_element_by_name("password")
    return [email ,senha]
[email , senha ] = WebDriverWait(driver,30).until(login_form)
time.sleep(2)
driver.execute_script("arguments[0].setAttribute('value','{}')".format(info['email']),email)
driver.execute_script("arguments[0].setAttribute('value','{}')".format(info['senha']),senha)
WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[9]/div/div/div[2]/div[5]/form/div[4]/label"))).click()
WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[9]/div/div/div[2]/div[5]/form/div[6]/input'))).click()
time.sleep(5.7)
driver.get('https://www.nike.com.br/Snkrs/Produto/{}'.format(info['model']))
driver.execute_script('window.scrollTo(0,300)')
time.sleep(0.5)
WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"//label[contains(text(),'{}')]".format(info['sizeM'])))).click()
time.sleep(0.1)
WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"/html/body/main/div/div[1]/div[3]/div/div[2]/div[4]/div/div[2]/button[1]"))).click()
'''WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"/html/body/main/div[4]/div/div[1]/div[1]/div[2]/div[2]/label"))).click()'''
WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"/html/body/main/div[4]/div/div[4]/a"))).click()
time.sleep(0.5)
WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"/html/body/main/div/div[3]/div[4]/div[5]/button"))).click()
time.sleep(0.7)
try:
    WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[13]/div/div/div[3]/button[1]"))).click()
except TimeoutException as exception:
    try:
        WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[15]/div/div/div[3]/button[1]"))).click()
    except TimeoutException as exception:
        WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[12]/div/div/div[3]/button[1]"))).click()
driver.execute_script('window.scrollTo(0,200)')
time.sleep(0.6)
WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.ID,"politica-trocas-label"))).click()
'WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[13]/div/div/div[3]/button"))).click()'
WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.ID,"confirmar-pagamento"))).click()
time.sleep(6)
driver.save_screenshot('Comprovantes/{}_Comprovante.png'.format(info['model'].split('/')[0]))
driver.quit()
print('Sucesso , verifique a pasta Comprovantes.')
input()