import multiprocessing
import threading
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

login = "" #Логин
password = "" #Пароль
fireFoxPath = r'C:\Program Files\Mozilla Firefox\firefox.exe' #Путь к Firefox браузеру
threadsAmount = 6 #Количество потоков

class Driver(object):
    def __init__(self, login, password, fireFoxPath): #Инициализация класса
        self.login = login
        self.password = password
        self.fireFoxPath = fireFoxPath
        self.options = Options()
        self.options.binary_location = fireFoxPath
        #self.options.add_argument(
        #    "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36")
        self.options.add_argument("--headless")
        self.service = Service(r'geckodriver.exe')
        self.driver = webdriver.Firefox(service=self.service, options=self.options)


    def auth(self): #Авторизация
        self.driver.get('https://ok.ru/')
        self.driver.find_element(by=By.NAME, value="st.email").send_keys(login)
        self.driver.find_element(by=By.NAME, value="st.password").send_keys(password)
        self.driver.find_element(by=By.XPATH, value=".//input[@class='button-pro __wide']").click()


    def visitPage(self, id): #Посещение страницы
        self.driver.get('https://ok.ru/profile/' + str(id) + "/")
        try:
            self.driver.find_element(by=By.CLASS_NAME, value='p404_w')
            print(str(id) + " — 404")
        except:
            print(str(id) + " — 200")


    def closeDriver(self):  # Закрытие драйвера
        self.driver.close()


def makeThread(numberOfThread): #Создать экземпляр потока
    driver = Driver(login, password, fireFoxPath)
    driver.auth()
    for i in range((numberOfThread-1)*1000000000+1, numberOfThread*1000000000): #Распределение данных по потокам
        driver.visitPage(i)
    driver.closeDriver()

def makeThreads(amountOfThreads, numberOfProcess): #Создать все потоки
    threads = []
    for i in range(1, amountOfThreads+1):
        t = threading.Thread(target=makeThread, args=(i,)) #Создать поток
        threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        t.join()

def makeProcesses(amountOfProcesses): #Выкинуть все потоки в отдельный процесс
    processes = []
    for i in range(1, amountOfProcesses+1):
        p = multiprocessing.Process(target=makeThreads, args=(threadsAmount,i))
        processes.append(p)
    for p in processes:
        p.start()
    for p in processes:
        p.join()

def main(): #Реализация методов и логирование
    makeProcesses(1)


if (__name__) == ('__main__'):
    main()
