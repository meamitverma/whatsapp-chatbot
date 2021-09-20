import pyautogui as pt
import pyperclip as pc
import requests
from bs4 import BeautifulSoup
from pynput.mouse import Button, Controller
from time import sleep

pt.FAILSAFE = True
mouse = Controller()

#Nav to any image
def nav_to_image(image, clicks, off_x = 0, off_y = 0):
    position = pt.locateCenterOnScreen(image, confidence = 0.8)

    if position is None:
        print(f'{image} not found...')
        return 0
    else:
        pt.moveTo(position, duration=0.3)
        pt.moveRel(off_x, off_y, duration=0.2)
        pt.click(clicks=clicks, interval=0.1)


def get_message():
    nav_to_image('whatsapp-chatbot/images/paperclip.png', 0, off_y=-85)
    mouse.click(Button.left, 3)
    pt.rightClick()

    copy = nav_to_image('whatsapp-chatbot/images/copy.png', 1)
    sleep(0.5)

    return pc.paste() if copy != 0 else 0

def send_message(msg):
    nav_to_image('whatsapp-chatbot/images/paperclip.png', 2, off_x=100)
    pt.typewrite(msg, interval=0.05)
    pt.typewrite('\n')

def close_reply_box():
    nav_to_image('whatsapp-chatbot/images/exit.png', 2)

def process_message(msg):
    raw_msg = msg.lower()
    
    user_query = raw_msg

    URL = "https://www.google.co.in/search?q=" + user_query

    headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.57'
    }

    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    result = soup.find(class_='Z0LcW XcVN5d').get_text()

    return result

# Loop the code
delay = 10
last_message = ''

sleep(3)
while True:
    # Check for new messages
    nav_to_image('whatsapp-chatbot/images/green_circle.png', 2, off_x=-100) #1
    close_reply_box() #2

    message = get_message() #3
    
    if message != 0 and message != last_message:
        last_message = message
        try:
            send_message(process_message(message))
            #print(process_message('toughest of them all'))
        except Exception:
            send_message("Please be clear.")
            #print('please be cl')
            

    else:
        print('No new messages...')
    
    sleep(10)


