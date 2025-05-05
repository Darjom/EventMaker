from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def initialize_driver():
    chrome_path = "C:/Users/ARACELI/OneDrive/Documentos/GitHub/EventMaker/automated_testing/chromedriver.exe"
    service = Service(executable_path=chrome_path)
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")  # Maximiza la ventana
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def main():
    driver = initialize_driver()
    driver.get("http://127.0.0.1:5000")
    
    try:
        # Esperar y hacer clic en el botón de inicio de sesión
        boton1 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "Boton-Iniciar-Sesion"))
        )
        boton1.click()
        
        # Rellenar campos con esperas
        Correo_electronico = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "Correo-Electronico"))
        )
        Correo_electronico.send_keys("ledezma@gmail.com")
        
        Contraseña = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "Contraseña"))
        )
        Contraseña.send_keys("Brunomars0131.")
        
        boton2 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "Boton-Iniciar-Sesion2"))
        )
        boton2.click()
        
    except Exception as e:
        print(f"Error: {str(e)}")
    
    finally:
        input("Presiona Enter para cerrar el navegador...")
        driver.quit()

if __name__ == '__main__':
    main()