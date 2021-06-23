from azure.storage.blob import BlobClient
import requests,uuid
import matplotlib.image as mpimg
import time

from flask import Flask, flash, request, redirect, url_for, render_template

from werkzeug.utils import secure_filename

app = Flask(__name__)

app.secret_key = "secret key"

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png','jpg'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/', methods=['POST','GET'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        id = str(uuid.uuid1())
        blob = BlobClient.from_connection_string(
            conn_str="DefaultEndpointsProtocol=https;AccountName=imgclass;AccountKey=jwli+rbvjB2Y2VB8jRfuR0ZknUiPJYuxFBDLl6hC1GawM47zJqSFebJr+7P4s6o023GPDfLSMcB9pZmY4i643Q==;EndpointSuffix=core.windows.net",
            container_name="image", blob_name=id)
        blob.upload_blob(file)
        filename = secure_filename(file.filename)
        img = mpimg.imread(file)
        img = img / 255
        img = img.reshape(784)

        input_data = "{\"data\": [" + str(list(img)) + "]}"
        headers = {'Content-Type': 'application/json'}

        key = '9yqdKWb1llA06MBfdlO4KmU8MfGbDgKa'

        headers = {'Content-Type': 'application/json'}
        headers['Authorization'] = f'Bearer {key}'
        service = 'http://1101520b-7cac-4e8e-b29d-7ca073cc4561.centralus.azurecontainer.io/score'
        resp = requests.post(service, input_data, headers=headers)
        m = resp.text
        flash('The predicted number is: ' + m[1])
        s = 'https://imgclass.blob.core.windows.net/image/' + str(id)
        print ( time.localtime(time.time()) )
        return render_template('index.html', filename = s)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)



# if __name__ == "__main__":
#     app.run()

