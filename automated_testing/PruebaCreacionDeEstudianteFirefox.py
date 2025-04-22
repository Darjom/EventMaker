from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from datetime import datetime 
fecha = datetime(2025, 5, 20)
fecha_str = fecha.strftime("%Y-%m-%d")
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
    Expedido=driver.find_element(By.ID,"Expedido")
    Fecha_nacimiento=driver.find_element(By.ID,"Fecha_nacimiento")
    Número=driver.find_element(By.ID,"Número")
    Curso=driver.find_element(By.ID,"Curso")
    Colegio=driver.find_element(By.ID,"Colegio")
    Departamento=driver.find_element(By.ID,"Departamento")
    Provincia=driver.find_element(By.ID,"Provincia")
    Correo=driver.find_element(By.ID,"Correo")
    password=driver.find_element(By.ID,"password")
    confirm_password=driver.find_element(By.ID,"confirm_password")
    checkbox=driver.find_element(By.ID,"checkbox")
    Inscribirse=driver.find_element(By.ID,"Inscribirse")
    Apellidos.send_keys("Pérez")
    Nombres.send_keys("Juan")
    CI.send_keys("12345678 b")
    Expedido.send_keys("CBBA")
    Fecha_nacimiento.send_keys(fecha_str)
    Número.send_keys(987654321)
    Curso.send_keys("Ingeniería de Software")
    Colegio.send_keys("1")
    Departamento.send_keys("La Paz")
    Provincia.send_keys("Murillo")
    Correo.send_keys("jjissopusauffe-5213@yopmail.com")
    password.send_keys("6zU43U%#tiv}")
    confirm_password.send_keys("6zU43U%#tiv}")
    checkbox.click()
    Inscribirse.click()


if __name__ == '__main__':
    main()
