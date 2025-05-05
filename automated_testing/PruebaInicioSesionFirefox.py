from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
import time 

def initialize_driver():
    gecko_path = "E:/Usuarios/INTELPC/Documents/GitHub/EventMaker/test/geckodriver.exe"
    service = Service(executable_path=gecko_path)
    driver = webdriver.Firefox(service=service)
    return driver

def click_InicioSesion():
    
    return 0

def main():
    driver = initialize_driver()
    driver.get("http://127.0.0.1:5000")
    boton1= driver.find_element(By.ID,"Boton-Iniciar-Sesion")
    boton1.click()
    Correo_electronico=driver.find_element(By.ID,"Correo-Electronico")
    Correo_electronico.send_keys("add@adm.com")
    Contraseña=driver.find_element(By.ID,"Contraseña")
    Contraseña.send_keys("12345678")
    boton2= driver.find_element(By.ID,"Boton-Iniciar-Sesion2")
    boton2.click()
    time.sleep(4)

if __name__ == '__main__':
    main()
