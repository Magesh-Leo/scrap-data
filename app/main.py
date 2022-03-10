#from webbrowser import get
from fastapi import FastAPI
from pydantic import BaseModel
from time import sleep
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
from google.cloud import storage
from google.cloud import tasks_v2
from google.protobuf import timestamp_pb2    
import datetime
import json


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
        # Create a client.
        client = tasks_v2.CloudTasksClient()

        # TODO(developer): Uncomment these lines and replace with your values.
        project = 'demoapp-containerize'      #'my-project-id'
        queue = 'demo-queue'
        location = 'asia-south1'
        payload = 'hello' # or {'param': 'value'} for application/json
        in_seconds = 180 # in_seconds = None

        # Construct the fully qualified queue name.
        parent = client.queue_path(project, location, queue)

        # Construct the request body.
        task = {
                'app_engine_http_request': {  # Specify the type of request.
                    'http_method': tasks_v2.HttpMethod.POST,
                    'relative_uri': '/'
                }
        }
        if payload is not None:
            if isinstance(payload, dict):
                # Convert dict to JSON string
                payload = json.dumps(payload)
                # specify http content-type to application/json
                task["app_engine_http_request"]["headers"] = {"Content-type": "application/json"}
            # The API expects a payload of type bytes.
            converted_payload = payload.encode()

            # Add the payload to the request.
            task['app_engine_http_request']['body'] = converted_payload

        if in_seconds is not None:
            # Convert "seconds from now" into an rfc3339 datetime string.
            d = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(seconds=in_seconds)

            # Create Timestamp protobuf.
            timestamp = timestamp_pb2.Timestamp()
            timestamp.FromDatetime(d)

            # Add the timestamp to the tasks.
            task['schedule_time'] = timestamp

        # Use the client to build and send the task.
        response = client.create_task(parent=parent, task=task)

        print('Created task {}'.format(response.name))

        return item
    except Exception as e:
        print("Error Occured")
        return e
    

@app.get('/items')
def getItem():
    return 'Item scrapped successfully...'
