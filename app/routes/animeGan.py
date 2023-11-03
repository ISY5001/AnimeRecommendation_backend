#@title Define functions
#@markdown Select model version and run.
from flask import request, send_file, send_from_directory
import onnxruntime as ort
import time, cv2, PIL
import numpy as np
from tqdm import tqdm
import os
from glob import glob
import logging

# data path
data_path = os.path.join(os.getcwd(), 'app/data')
models_path = os.path.join(data_path, 'models')
in_dir = os.path.join(data_path, 'content/in')
out_dir = os.path.join(data_path, 'content/outputs')

pic_form = ['.jpeg','.jpg','.png','.JPEG','.JPG','.PNG']

providers = ['CoreMLExecutionProvider']
# device_name = ort.get_device()

# if device_name == 'cpu':
#     providers = ['CPUExecutionProvider']
# elif device_name == 'GPU':
#     providers = ['CUDAExecutionProvider', 'CPUExecutionProvider']
# @param ['AnimeGAN_Hayao','AnimeGANv2_Hayao','AnimeGANv2_Shinkai','AnimeGANv2_Paprika']

# model =  request.form['style']
model = 'AnimeGANv2_Paprika'
# load model
model_path = os.path.join(models_path, f'{model}.onnx') 
# /Users/chenzhiwei/Downloads/AnimeRecommendation_backend/app/data/models/AnimeGANv2_Paprika.onnx
# /Users/chenzhiwei/Downloads/AnimeRecommendation_backend/app/data/models/AnimeGANv2_Paprika.onnx
print("\033[1;35m model_path: ", model_path, "\033[0m")
session = ort.InferenceSession(model_path, providers=providers)

def process_image(img, x32=True):
    h, w = img.shape[:2]
    if x32: # resize image to multiple of 32s
        def to_32s(x):
            return 256 if x < 256 else x - x%32
        img = cv2.resize(img, (to_32s(w), to_32s(h)))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB).astype(np.float32)/ 127.5 - 1.0
    return img

def load_test_data(image_path):
    img0 = cv2.imread(image_path).astype(np.float32)
    img = process_image(img0)
    img = np.expand_dims(img, axis=0)
    return img, img0.shape[:2]

def Convert(img, scale):
    x = session.get_inputs()[0].name
    y = session.get_outputs()[0].name
    fake_img = session.run(None, {x : img})[0]
    images = (np.squeeze(fake_img) + 1.) / 2 * 255
    images = np.clip(images, 0, 255).astype(np.uint8)
    output_image = cv2.resize(images, (scale[1],scale[0]))
    return cv2.cvtColor(output_image, cv2.COLOR_RGB2BGR)
    
def clear_directory(directory_path):
    try:
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
        print(f"Successfully cleared all files in {directory_path}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    
def process(upload=True, clear_dir=True):
    if clear_dir:
        clear_directory(in_dir)
        clear_directory(out_dir)

    if 'image' not in request.files or not upload:
        print('\nNo files were uploaded. Try again..\n')
        return

    uploaded_file = request.files['image']
    in_file_path = os.path.join(in_dir, uploaded_file.filename)
    
    if not uploaded_file.filename:
        print('\nNo files were uploaded. Try again..\n')
        return

    uploaded_file.save(in_file_path)
    
    in_files = sorted(glob(f'{in_dir}/*'))
    in_files = [x for x in in_files if os.path.splitext(x)[-1] in pic_form]
    print(in_files)
    for ims in tqdm(in_files):
        out_name = f"{out_dir}/{ims.split('/')[-1].split('.')[0]}.jpg"
        mat, scale = load_test_data(ims)
        res = Convert(mat, scale)
        cv2.imwrite(out_name, res)

def get_output_images():
    out_files = sorted(glob(f'{out_dir}/*.jpg'))
    if out_files:
        return out_files[0]  
    else:
        return None  

def handle_animeGan():
    try:
        global model, model_path, providers, session
        model =  request.form['style']
        print("\033[1;35mmodel changed to ", model, "\033[0m")
        model_path = os.path.join(models_path, f'{model}.onnx') 
        providers = ['CoreMLExecutionProvider']
        session = ort.InferenceSession(model_path, providers=providers)
        uploaded_file = request.files['image']
        process(uploaded_file)
        output_image = get_output_images()
        filename = os.path.basename(output_image) if output_image else None
        if output_image:
            with open(output_image, 'rb') as img_file:
                img_data = img_file.read()
            return {
                'status': 'success',
                'message': 'Image uploaded and processed successfully',
                'image_data': img_data.decode('latin1'),
                'filename': filename  
            }, 200
        else:
            return {
                'status': 'success',
                'message': 'Image uploaded and processed successfully',
                'image_data': None,
                'filename': None
            }, 200
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e)
        }, 400


if __name__ == '__main__':
    process()
    get_output_images()