import math
import random
import os
import sys
import time

from functionalities import autobuyer

bot_title="""   _____  __      __  _____      ____            _   
  / ____| \ \    / / |  __ \    |  _ \          | |  
 | (___    \ \  / /  | |  | |   | |_) |   ___   | |_ 
  \___ \    \ \/ /   | |  | |   |  _ <   / _ \  | __|
  ____) |    \  /    | |__| |   | |_) | | (_) | | |_ 
 |_____/      \/     |_____/    |____/   \___/   \__|   
"""

def menu():
    clear_screen()
    print(bot_title)
    print("\n")
    print("MENU:")

    menu_options = ["Auto-buyer", "Monitor","Discord WebHook Settings", "Exit"]

    for i, option in enumerate(menu_options):
        print("{}) {}".format(i + 1, option))

    print("\n")
    sel = choose(menu_options, "Select an option: ")

    if sel == 1:
        autobuyer_run()
    elif sel == 2:
        monitor_run()
    elif sel == 3:
        webhook_options()
    elif sel == 4:
        sys.exit()

def choose(choices, message):
    while True:
        try:
            sel = int(input(message + " [1-{}]: ".format(len(choices))))
            if 1 <= sel <= len(choices):
                break
            else:
                print("!!!!Selection must be in range!!!!")
        except ValueError:
            print("!!!!Input must be integer!!!!")
    return sel

def clear_screen():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def autobuyer_run():
    try:
        with open("webhook.txt", "r") as f:
            webhook_link = f.read()
    except FileNotFoundError:
        print("[-] Error: File 'webhook.txt' not found")
        webhook_link=""

    productURL = str(input("Intro the URL of the product to purchase (SPACE + INTRO to confirm): "))
    bot=autobuyer.AutoBuyer(productURL,webhook_link)
    driver =bot.createDriver()
    driver.get(productURL)
    size, divPos, prod = bot.CheckSizes(productURL, driver)
    if size != 0:
        bot.agregarCarrito(size, divPos, driver,prod)
def monitor_run():

def webhook_options():
    clear_screen()
    print(bot_title)
    print("\n")
    print("Discord Webhook settings")
    print("\n")

    menu_options = ["Set webhook link", "Clear webhook link", "Show current webhook link", "Back"]
    for i, option in enumerate(menu_options):
        print("{}) {}".format(i + 1, option))
    sel = choose(menu_options, "Select one of the options: ")
    print("\n")
    if sel == 1:
        webhook_link = input("Insert webhook link: ")
        webhook_link = webhook_link[: -1]
        with open("webhook.txt", "w") as f:

            f.write(webhook_link)
        print("Webhook link successfully updated")
    elif sel == 2:
        with open("webhook.txt", "w") as f:
            f.write("")
        print("Webhook link successfully cleared")
    elif sel == 3:
        try:
            with open("webhook.txt", "r") as f:
                webhook_link = f.read()
            print("Webhook link:\n{}".format(webhook_link))
        except FileNotFoundError:
            print("[-] Error: File 'webhook.txt' not found")
    elif sel == 4:
        menu()
    input("Press enter...")
    webhook_options()

if __name__ == '__main__':
    menu()
