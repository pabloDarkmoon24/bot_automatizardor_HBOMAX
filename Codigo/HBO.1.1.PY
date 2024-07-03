from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as chromeService
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tkinter import *
import time
from selenium.webdriver.common.keys import Keys
from tkinter import ttk

texto_deseado = 'Disfruta'
resultados = []
webdrivers = []


# Leer el archivo Excel y crear el diccionario de datos
nombre_archivo_excel = 'cuentas.xlsx'  
da = pd.read_excel(nombre_archivo_excel)  
diccionario_datos = da.set_index('correo')['contraseña'].to_dict()


def comando_total():
    for usuario, clave in diccionario_datos.items():
        driver = webdriver.Chrome(service=chromeService(ChromeDriverManager().install()))
        webdrivers.append(driver)
        validar_cuentas(driver, usuario, clave)



def validar_cuentas(driver, usuario, clave):
    global cuenta
    cuenta = 0
    try:
        driver = webdriver.Chrome()
        driver.get('https://play.hbomax.com/signIn')
        driver.implicitly_wait(6)

        search_mail = driver.find_element(by=By.ID, value="EmailTextInput")
        search_password = driver.find_element(by=By.ID, value="PasswordTextInput")
        search_button = driver.find_element(by=By.XPATH, value='//div[@data-testid="SignInButton"]')

        search_mail.send_keys(usuario)
        search_password.send_keys(clave)

        search_button.click()

        
        driver.implicitly_wait(10)

        # PROCESO DE RECICLAJE 
        # Esperar a que los elementos AvatarContentPressableContainer sean visibles
        perfiles = WebDriverWait(driver, 10).until(
        EC.visibility_of_all_elements_located((By.XPATH, '//div[@data-testid="AvatarContentPressableContainer"]'))
        )
        numero_de_perfiles = len(perfiles)
        cuenta = 1

        while numero_de_perfiles > 1:
            # Hacer clic en "Editar perfiles"
            elemento_editar_perfiles = driver.find_element(by=By.XPATH, value='//div[@data-testid="ProfileSelectScreenDoneManageProfilesButton"]/div/div[@dir="auto" and contains(text(), "Administrar perfiles")]')
            elemento_editar_perfiles.click()
            
            time.sleep(1)
            # Esperar a que el segundo perfil sea clicable
            perfil2 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '(//div[@data-testid="AvatarContentPressableContainer"])[2]')))
            perfil2.click()


            # Hacer clic en eliminar, para eliminar el perfil
            driver.implicitly_wait(6)
            eliminar_perfil = driver.find_element(by=By.XPATH, value='//div[@data-testid="AddEditProfileScreenDeleteButton"]')
            eliminar_perfil.click()
            

            # Hacer clic en eliminar, para confirmar eliminación
            driver.implicitly_wait(6)
            confirmar_eliminar_perfil = driver.find_element(by=By.XPATH, value='//div[@data-testid="DeleteProfileScreenDeleteButton"]')
            confirmar_eliminar_perfil.click()
            
            #breve espera, se refresca la pagina para que recargue el codigo, se resta un perfil eliminado 
            time.sleep(1)
            driver.refresh()
            numero_de_perfiles = numero_de_perfiles-1

#Proceso para cambiar de nombre el perfil

        # Hacer clic en "Editar perfiles"
        elemento_editar_perfiles = driver.find_element(by=By.XPATH, value='//div[@data-testid="ProfileSelectScreenDoneManageProfilesButton"]/div/div[@dir="auto" and contains(text(), "Administrar perfiles")]')
        elemento_editar_perfiles.click()

        time.sleep(1)
        # Esperar a que el segundo perfil sea clicable
        perfil1 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '(//div[@data-testid="AvatarContentPressableContainer"])[1]')))
        perfil1.click()

        nombre_perfil_input = driver.find_element(by=By.XPATH, value='//input[@data-testid="AddEditProfileScreenInputProfileNameTextInput"]')

        # Borra el contenido

        # Obtener el valor actual
        valor_actual = nombre_perfil_input.get_attribute('value')

        # Limpiar el campo enviando una combinación de teclas (selecciona todo y presiona BACKSPACE)
        nombre_perfil_input.send_keys(Keys.CONTROL + 'a', Keys.BACKSPACE)

        # Ingresa el nuevo valor
        nuevo_valor = 'hbo'
        nombre_perfil_input.send_keys(nuevo_valor)

        #boton guardar
        guardar = driver.find_element(by=By.XPATH, value='//div[@data-testid="AddEditProfileScreenNextSaveButton"]')
        guardar.click()

        time.sleep(2)
        driver.refresh()
        
        #entrar al perfil 1
        perfil1 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '(//div[@data-testid="AvatarContentPressableContainer"])[1]')))
        perfil1.click()

        #validar si en la pagina existe la palabra  disfruta
        wait = WebDriverWait(driver, 10)
        elemento_con_texto = wait.until(EC.visibility_of_element_located((By.XPATH, f'//*[contains(text(), "{texto_deseado}")]')))
        texto = elemento_con_texto.text

        if texto == "¡Disfruta de HBO Max!":

            # menu
            search_button3 = driver.find_element(by=By.XPATH, value='//*[@id="root"]/div[1]/div/div[3]/div[1]/div[2]/div[4]/div/div[1]')
            search_button3.click()

            driver.implicitly_wait(6)
            # cerrar sesión
            search_button4 = driver.find_element(by=By.XPATH, value='//*[@id="dropdown-1-3"]')
            search_button4.click()

            driver.implicitly_wait(6)
            resultados.append([usuario, clave, "Ingresa, Pero ya está caída"])


            # Crear un DataFrame a partir de la lista de resultados
            df_resultados = pd.DataFrame(resultados, columns=['Usuario', 'Contraseña', 'Resultado'])

            # Guardar el DataFrame en un archivo Excel
            df_resultados.to_excel('resultados.xlsx', index=False)

        else:
            # menu
            search_button3 = driver.find_element(by=By.XPATH, value='//*[@id="root"]/div[1]/div/div[3]/div[1]/div[2]/div[4]/div/div[1]')
            search_button3.click()

            # ajustes
            ajustes = driver.find_element(by=By.XPATH, value='//*[@aria-label="Ajustes"]')
            ajustes.click()

            # administrar perfiles
            administrar_perfiles = driver.find_element(by=By.XPATH, value='//*[@data-testid="Link"]')
            administrar_perfiles.click()

            # cerrar sesion en los dispositivos
            close_session = driver.find_element(by=By.XPATH, value='//*[@aria-label="Cerrar sesión en todos los dispositivos"]')
            close_session.click()

            time.sleep(1)
            # cerrar sesion en los dispositivos confirmacion
            close_dispositivos = driver.find_element(by=By.XPATH, value='//div[contains(@class, "css-175oi2r") and contains(@class, "r-1awozwy") and contains(@class, "r-zs9c5m") and contains(@class, "r-42olwf") and contains(@class, "r-z2wwpe") and contains(@class, "r-d045u9") and contains(@class, "r-18u37iz") and contains(@class, "r-1777fci") and contains(@class, "r-peo1c") and contains(@class, "r-xb9fkz") and contains(@class, "r-kzbkwu") and contains(@class, "r-d9fdf6") and contains(@class, "r-1b3ntt7")]//div[@style="color: rgb(0, 0, 0); font-family: StreetLCG2; font-weight: 600; font-style: normal; font-size: 14px; letter-spacing: 0px; line-height: 21px;"]')
            close_dispositivos.click()

            driver.implicitly_wait(6)
            resultados.append([usuario, clave, "Cuenta funcional"])

            # Crear un DataFrame a partir de la lista de resultados
            df_resultados = pd.DataFrame(resultados, columns=['Usuario', 'Contraseña', 'Resultado'])

            # Guardar el DataFrame en un archivo Excel
            df_resultados.to_excel('resultados.xlsx', index=False)

    except Exception as e:
        # En caso de error, verificar si es un error de contraseña incorrecta
        if cuenta == 1:
            resultados.append([usuario, clave, "Ha ocurrido un error"])
            df_resultados = pd.DataFrame(resultados, columns=['Usuario', 'Contraseña', 'Resultado'])
            # Guardar el DataFrame en un archivo Excel
            df_resultados.to_excel('resultados.xlsx', index=False)
        else:      
        # Crear un DataFrame a partir de la lista de resultados
            resultados.append([usuario, clave, "Contraseña incorrecta"])
            df_resultados = pd.DataFrame(resultados, columns=['Usuario', 'Contraseña', 'Resultado'])
            # Guardar el DataFrame en un archivo Excel
            df_resultados.to_excel('resultados.xlsx', index=False)

        


    

def cerrar_navegadores_y_salir():
    root.destroy()

root = Tk()
root.iconbitmap("MPANTALLA.ico")
root.title("Validador HBO")
root.configure(bg="#f4f3fb")

# Configurar la imagen
imagen_path = "validador.png"
imagen = PhotoImage(file=imagen_path)

root.configure(bg="#f4f3fb")



# Obtener las dimensiones de la pantalla
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calcular el tamaño deseado del Canvas
canvas_width = screen_width // 3.9
canvas_height = screen_height // 1.4


# Configurar el Canvas con dimensiones calculadas
canvas = Canvas(root, width=canvas_width, height=canvas_height, bg="#f4f3fb")
canvas.pack()

# Dibujar la imagen en el Canvas y ajustar el tamaño
canvas.create_image(0, 0, anchor=NW, image=imagen, tags="imagen")

# Configurar los botones
boton_validar = ttk.Button(root, text="VALIDAR CUENTAS", command=comando_total, style="TButton")
boton_validar.pack(side="left", padx=(40, 10), pady=10)

boton_cerrar = ttk.Button(root, text="CERRAR", command=cerrar_navegadores_y_salir, style="TButton")
boton_cerrar.pack(side="left", padx=(10, 10), pady=10)

# Crear estilo para los botones
style = ttk.Style()
style.configure("TButton", font=("Arial", 10, "bold"), background="#a740f6", foreground="black", borderwidth=0, padding=10)
style.map("TButton", background=[("active", "#cb8fff")])  # Cambiar el color al hacer clic

# Llamar a cerrar_navegadores() al cerrar la ventana de Tkinter
root.mainloop()