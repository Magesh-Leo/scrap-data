from fastapi import FastAPI
from pydantic import BaseModel
from time import sleep
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver


class Item(BaseModel):
    url: str


app = FastAPI()

@app.post("/")
def create_item(item: Item):
    print(f'{item.url}')
    try: #https://selenium-standalone-chrome-zlzujd3glq-em.a.run.app
        web = DesiredCapabilities.CHROME
        driver = webdriver.Remote(
            command_executor='http://127.0.0.1:4444/wd/hub', 
            desired_capabilities=web,)
        driver.get('www.python.org')
        driver.save_screenshot('demo.png')
        driver.quit()
        return "Sent Successfully..."
    except Exception as e:
        return e