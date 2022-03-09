#from webbrowser import get
from fastapi import FastAPI
from pydantic import BaseModel
from time import sleep
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
from google.cloud import storage


class Item(BaseModel):
    url: str


app = FastAPI()

@app.post("/")
def create_item(item: Item):
    print(f'{item.url}')
    try:
        web = DesiredCapabilities.CHROME
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-dev-shm-usage")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        '''driver = webdriver.Remote(
            command_executor=SELENIUM_API_ENDPOINT,
            desired_capabilities=web,
            options=options)'''
        driver = webdriver.Remote(
            command_executor='https://standalone-chrome-zlzujd3glq-em.a.run.app/wd/hub',
            desired_capabilities=web, 
            options=options)
        driver.implicitly_wait(5)
        driver.get(f'{item.url}')
        content = driver.find_element_by_tag_name('body').text    #scrapping content
        print('get successfully')
        #driver.save_screenshot('screen-shot.png')
        fTitle = item.url.split('/')[-1]     # split url for set file name to store gcp
        client = storage.Client()
        bucket = client.get_bucket('mydemo-bucket-ts')
        new_blob = bucket.blob(f'remote/path/{fTitle}.txt')
        new_blob.upload_from_string(content)
        driver.quit()
        return item
    except Exception as e:
        print("Error Occured")
        return e
    

@app.get('/items')
def getItem():
    return 'Item scrapped successfully...'
