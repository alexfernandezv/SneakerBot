# File to create the Base Url
# https://www.adidas.ca/en/gazelle-shoes/BB5478.html?forceSelSize=BB5478_530 Size=4
# What sizes are currently available
# Add to Cart Button
# Checkout Pop up
# Checkout complete
# Payment complete

import math
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from config import keys


def CheckSizes(myUrl):

          driver.get(myUrl)
          WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "product_addtocart_form")))
          elementoTallas = driver.find_element_by_class_name('product-options-wrapper')
          todasTallas = elementoTallas.find_elements_by_class_name('swatch-option')  #todas las tallas
          tallasNoDisponibles= elementoTallas.find_elements_by_class_name('disabled')

          tallasComprar = []
          auxList=[]
          for talla in todasTallas:
              if talla not in tallasNoDisponibles:
               tallasComprar.append(talla.get_attribute('innerHTML'))
              auxList.append(talla.get_attribute('innerHTML'))

          aux=str(myUrl).split("/")
          print("----------------------------------------")
          print("Tallas disponibles para "+ aux[-1]+ " :")
          for sizes in tallasComprar:
                    print("Talla "+sizes )
          print("----------------------------------------")

          size = float(random.choice(tallasComprar))
          frac, whole = math.modf(size)
          if frac == 0.0:
              size = int(whole)

          print("Talla escogida---> " + str(size))

          divPosition=auxList.index(str(size))

          return size,divPosition,aux[-1]

def agregarCarrito(myUrl,size,divPosition):


          driver.get(myUrl)
          aux= driver.find_element_by_class_name('product-options-wrapper')
          s1=str("//*[contains(text(), '{0}')]").format(size)

          aux2=driver.find_elements_by_xpath(s1)
          selector=str("div[index='{0}']").format(divPosition)
          s = aux.find_element_by_css_selector(selector)
          driver.execute_script("arguments[0].click();", s)

          webElement= driver.find_element_by_id("product-addtocart-button")
          driver.execute_script("arguments[0].click();", webElement)

          WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//A[@data-bind='attr: { href: window.checkout.checkoutUrl }']")))
          driver.find_element_by_xpath("//A[@data-bind='attr: { href: window.checkout.checkoutUrl }']").click()
          WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//INPUT[@id='customer-email']")))
          driver.find_element_by_xpath("//INPUT[@id='customer-email']").send_keys(keys['email'])
          driver.find_element_by_xpath("//INPUT[@name='firstname']").send_keys(keys['first_name'])
          driver.find_element_by_xpath("//INPUT[@name='lastname']").send_keys(keys['last_name'])
          driver.find_element_by_xpath("//INPUT[@name='street[0]']").send_keys(keys['street_address'])
          driver.find_element_by_xpath("//INPUT[@name='city']").send_keys(keys['city'])
          driver.find_element_by_xpath("//SELECT[@name='region_id']").click()
          provincia=str("//OPTION[@data-title='{0}']").format(keys['province'])
          driver.find_element_by_xpath(provincia).click()
          driver.find_element_by_xpath("//INPUT[@name='postcode']").send_keys(keys['postal_code'])
          driver.find_element_by_xpath("//INPUT[@name='telephone']").send_keys(keys['phone_number'])
          WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//BUTTON[@data-role='opc-continue']")))
          driver.find_element_by_xpath("//BUTTON[@data-role='opc-continue']").click()


          WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//DIV[@class='payment-group']")))
          """
       
          # paypal
          driver.find_element_by_xpath("//INPUT[@id='braintree_paypal']").click()
          elmnt=driver.find_element_by_xpath("//INPUT[@id='policies-braintree_paypal']")
          driver.execute_script("arguments[0].click();", elmnt)
          driver.find_element_by_xpath("//DIV[@data-container='paypal-button']").click()   """
          #targeta credito
          WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//INPUT[@id='braintree']")))
          driver.find_element_by_xpath("//INPUT[@id='braintree']").click()
          WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//IFRAME[@name='braintree-hosted-field-number']")))
          frame=driver.find_element_by_xpath("//IFRAME[@name='braintree-hosted-field-number']")
          driver.switch_to.frame(frame)
          WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//INPUT[@id='credit-card-number']")))
          driver.find_element_by_xpath("//INPUT[@id='credit-card-number']").send_keys(keys['card_number'])
          driver.switch_to.default_content()

          frame1=driver.find_element_by_xpath("//IFRAME[@name='braintree-hosted-field-expirationMonth']")
          driver.switch_to.frame(frame1)
          WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//INPUT[@id='expiration-month']")))
          driver.find_element_by_xpath("//INPUT[@id='expiration-month']").send_keys(keys['expiration_month'])
          driver.switch_to.default_content()

          frame2 = driver.find_element_by_xpath("//IFRAME[@name='braintree-hosted-field-expirationYear']")
          driver.switch_to.frame(frame2)
          WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//INPUT[@id='expiration-year']")))
          driver.find_element_by_xpath("//INPUT[@id='expiration-year']").send_keys(keys['expiration_year'])
          driver.switch_to.default_content()

          frame3 = driver.find_element_by_xpath("//IFRAME[@name='braintree-hosted-field-cvv']")
          driver.switch_to.frame(frame3)
          WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//INPUT[@id='cvv']")))
          driver.find_element_by_xpath("//INPUT[@id='cvv']").send_keys(keys['card_cvv'])
          driver.switch_to.default_content()

          elmnt = driver.find_element_by_xpath("//INPUT[@id='policies-braintree']")
          driver.execute_script("arguments[0].click();", elmnt)
          checkbox=driver.find_element_by_xpath("//INPUT[@id='billing-address-same-as-shipping-shared']").is_selected()
          checkEl=driver.find_element_by_xpath("//INPUT[@id='billing-address-same-as-shipping-shared']")
          if checkbox==False:
              driver.execute_script("arguments[0].click();", checkEl)

          lastButton = driver.find_element_by_xpath("(//BUTTON[@class='action primary checkout'])")
          driver.execute_script("arguments[0].click();", lastButton)



"""""
          WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='mini-cart']/div/div[4]/div/div")))
          #driver.switch_to.frame(driver.find_element_by_class_name("zoid-component-frame"))
          driver.implicitly_wait(10)
          pay=driver.find_element_by_xpath("//*[@id='mini-cart']/div/div[4]/div/div")
          driver.execute_script("arguments[0].click();", pay)
          #driver.execute_script("arguments[0].click();", driver.find_element_by_class_name("zoid-outlet"))
          """
if __name__ == '__main__':

     driver = webdriver.Chrome() ##inicializamos chrome
     driver.maximize_window()
     #productoURL=str(input("Introduce la URL del producto a comprar (espacio y intro para confirmar): "))

     productoURL=str(input("Introduce la URL del producto a comprar (pulsa ESPACIO + INTRO para confirmar): "))
     size,divPos,prod=CheckSizes(productoURL)
     agregarCarrito(productoURL,size,divPos)
     print("Tu " + prod + "ha sido comprado satisfactoriamente, comprueba el correo")
