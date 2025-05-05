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
    boton1= driver.find_element(By.ID,"Boton-Crear-Cuenta")
    boton1.click()
    boton2= driver.find_element(By.ID,"CrearCuentaEstudiante")
    boton2.click()
    Apellidos=driver.find_element(By.ID,"Apellidos")
    Nombres=driver.find_element(By.ID,"Nombres")
    CI=driver.find_element(By.ID,"CI")
    Complemento=driver.find_element(By.ID,"Complemento")
    Expedido=driver.find_element(By.ID,"Expedido")
    status = "EXISTE ✅" if exists else "NO EXISTE ❌"
    if():
        print("")
    time.sleep(4)

if __name__ == '__main__':
    main()
