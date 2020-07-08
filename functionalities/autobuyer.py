

import math
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from config import keys
from threading import Thread
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from discord_webhook import DiscordWebhook, DiscordEmbed

class AutoBuyer():
    def __init__(self,url,webhooklink):
        self.prodURL=url
        self.WebHookLink=webhooklink

    def run_webhook(self, title, message):

        web_hook = DiscordWebhook(url=self.WebHookLink)
        embed = DiscordEmbed(title=title, description=message, color=int("36b54b", 16))
        web_hook.add_embed(embed)
        response = web_hook.execute()


    def CheckSizes(self,myUrl, driver):
        while True:
            try:
                form = driver.find_element_by_id("product_addtocart_form")
                break
            except NoSuchElementException:
                print("Product is not available yet. Retrying...")
                driver.refresh()
                continue

        if self.WebHookLink != "":
            self.run_webhook(title="Product is available. Buying...",message="")
        else:
            print("Product is available. Buying...")
        # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "product_addtocart_form")))
        elementoTallas = driver.find_element_by_class_name('product-options-wrapper')
        todasTallas = elementoTallas.find_elements_by_class_name('swatch-option')  # todas las tallas
        tallasNoDisponibles = elementoTallas.find_elements_by_class_name('disabled')

        tallasComprar = []
        auxList = []
        for talla in todasTallas:
            if talla not in tallasNoDisponibles:
                tallasComprar.append(talla.get_attribute('innerHTML'))
            auxList.append(talla.get_attribute('innerHTML'))

        aux = str(myUrl).split("/")

        if len(tallasComprar) == 0:
            if self.WebHookLink != "":
                msg="Sizes for "+aux[-1]
                self.run_webhook(title="msg", message="No pairs available")
            else:
                print("No pairs available " + aux[-1])
            self.CheckSizes(myUrl,driver)
        else:
            if self.WebHookLink != "":
                msg = "Available sizes for " + aux[-1]
                txt=""
                for sizes in tallasComprar:
                    txt=txt+(sizes+"\n")
                self.run_webhook(title=msg, message=txt)
            else:
                print("----------------------------------------")
                print("Available sizes for " + aux[-1] + " :")
                for sizes in tallasComprar:
                    print("Size " + sizes)
                print("----------------------------------------")

            size = float(random.choice(tallasComprar))
            frac, whole = math.modf(size)
            if frac == 0.0:
                size = int(whole)
            if self.WebHookLink != "":
                self.run_webhook(title="Chosen size", message=str(size))
            else:
                print("Chosen size ---> " + str(size))

            divPosition = auxList.index(str(size))

            return size, divPosition, aux[-1]


    def agregarCarrito(self,size, divPosition, driver, productoURL):
        ##driver.get(myUrl)
        aux = driver.find_element_by_class_name('product-options-wrapper')
        s1 = str("//*[contains(text(), '{0}')]").format(size)

        aux2 = driver.find_elements_by_xpath(s1)
        selector = str("div[index='{0}']").format(divPosition)
        s = aux.find_element_by_css_selector(selector)
        driver.execute_script("arguments[0].click();", s)

        webElement = driver.find_element_by_id("product-addtocart-button")
        driver.execute_script("arguments[0].click();", webElement)

        WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.XPATH, "//A[@data-bind='attr: { href: window.checkout.checkoutUrl }']")))
        driver.find_element_by_xpath("//A[@data-bind='attr: { href: window.checkout.checkoutUrl }']").click()
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//INPUT[@id='customer-email']")))
        driver.find_element_by_xpath("//INPUT[@id='customer-email']").send_keys(keys['email'])
        driver.find_element_by_xpath("//INPUT[@name='firstname']").send_keys(keys['first_name'])
        driver.find_element_by_xpath("//INPUT[@name='lastname']").send_keys(keys['last_name'])
        driver.find_element_by_xpath("//INPUT[@name='street[0]']").send_keys(keys['street_address'])
        driver.find_element_by_xpath("//INPUT[@name='city']").send_keys(keys['city'])
        driver.find_element_by_xpath("//SELECT[@name='region_id']").click()
        provincia = str("//OPTION[@data-title='{0}']").format(keys['province'])
        driver.find_element_by_xpath(provincia).click()
        driver.find_element_by_xpath("//INPUT[@name='postcode']").send_keys(keys['postal_code'])
        driver.find_element_by_xpath("//INPUT[@name='telephone']").send_keys(keys['phone_number'])
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//BUTTON[@data-role='opc-continue']")))
        continueEL = driver.find_element_by_xpath("//BUTTON[@data-role='opc-continue']")
        driver.execute_script("arguments[0].click();", continueEL)

        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//DIV[@class='payment-group']")))
        """
    
        # paypal
        driver.find_element_by_xpath("//INPUT[@id='braintree_paypal']").click()
        elmnt=driver.find_element_by_xpath("//INPUT[@id='policies-braintree_paypal']")
        driver.execute_script("arguments[0].click();", elmnt)
        driver.find_element_by_xpath("//DIV[@data-container='paypal-button']").click()   """
        # targeta credito
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//INPUT[@id='braintree']")))
        driver.find_element_by_xpath("//INPUT[@id='braintree']").click()
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//IFRAME[@name='braintree-hosted-field-number']")))
        frame = driver.find_element_by_xpath("//IFRAME[@name='braintree-hosted-field-number']")
        driver.switch_to.frame(frame)
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//INPUT[@id='credit-card-number']")))
        driver.find_element_by_xpath("//INPUT[@id='credit-card-number']").send_keys(keys['card_number'])
        driver.switch_to.default_content()

        frame1 = driver.find_element_by_xpath("//IFRAME[@name='braintree-hosted-field-expirationMonth']")
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
        checkbox = driver.find_element_by_xpath("//INPUT[@id='billing-address-same-as-shipping-shared']").is_selected()
        checkEl = driver.find_element_by_xpath("//INPUT[@id='billing-address-same-as-shipping-shared']")
        if checkbox == False:
            driver.execute_script("arguments[0].click();", checkEl)

        lastButton = driver.find_element_by_xpath("(//BUTTON[@class='action primary checkout'])")
        driver.execute_script("arguments[0].click();", lastButton)
        driver.maximize_window()

        if self.WebHookLink != "":
            msg="Your " + productoURL + "has been purchased succesfully."
            self.run_webhook(title=msg, message="")
        else:
            print("Your " + productoURL + "has been purchased succesfully.")



    def createDriver(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.headless = False
        driver = webdriver.Chrome(r"C:\Users\Nuria\PycharmProjects\SneakerBot\chromedriver.exe", options=chrome_options)
        driver.create_options()
        driver.minimize_window()
        return driver