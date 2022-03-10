from google.cloud import storage
import json

filename='python'
client = storage.Client()
#list blob 
'''for blob in client.list_blobs('mydemo-bucket-ts',prefix='remote/path'):
    print(str(blob))
'''
url = 'mydemo-bucket-ts/remote/path/python.txt'
file_name = url.split('/')[-1]
bucket_name = url.split('/')[0]
path = url.split('/')[1:]
file_path='/'.join(path)
bucket = client.get_bucket(bucket_name)
blob = bucket.get_blob(file_path)
jfile = {}
jfile['text']=str(blob.download_as_text())
out_file = open(f"{file_name}.json", "w")
json.dump(jfile, out_file)
out_file.close()
