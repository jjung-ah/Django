import cv2
import numpy as np
import tensorflow as tf
import os

current_dir = os.path.dirname( os.path.abspath( __file__ ) )

def getImglist(path):
    img_path = current_dir + path

    file_list = os.listdir(img_path)
    img_list = [file for file in file_list if file.endswith(".png")]
    return img_list


def process(path, model_path):
    password = ""
    img_path = current_dir + path
    img_list = getImglist(path)

    # 폴더 안에 있는 모든 이미지에 대해 전처리
    for img in img_list:
        img_input = cv2.imread(img_path + img)
        gray = cv2.cvtColor(img_input, cv2.COLOR_BGR2GRAY)
        gray = cv2.resize(gray, (28, 28), interpolation=cv2.INTER_AREA)

        (thresh, img_binary) = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

        h,w = img_binary.shape

        ratio = 100 / h
        new_h = 100
        new_w = w * ratio

        img_temp = np.zeros((110,110), dtype=img_binary.dtype)
        img_binary = cv2.resize(img_binary, (int(new_w), int(new_h)), interpolation=cv2.INTER_AREA)
        img_temp[:img_binary.shape[0], :img_binary.shape[1]] = img_binary

        img_binary = img_temp

        cnts = cv2.findContours(img_binary.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 컨투어의 무게중심 좌표를 구합니다. 
        M = cv2.moments(cnts[0][0])
        center_x = (M["m10"] / M["m00"])
        center_y = (M["m01"] / M["m00"])

        # 무게 중심이 이미지 중심으로 오도록 이동시킵니다. 
        height,width = img_binary.shape[:2]
        shiftx = width/2-center_x
        shifty = height/2-center_y

        Translation_Matrix = np.float32([[1, 0, shiftx],[0, 1, shifty]])
        img_binary = cv2.warpAffine(img_binary, Translation_Matrix, (width,height))

        img_binary = cv2.resize(img_binary, (28, 28), interpolation=cv2.INTER_AREA)
        img_binary = img_binary.reshape(1, 28, 28, 1)
        img_binary = tf.cast(img_binary, tf.float16)

        # 모델에 전처리 된 이미지를 넘겨주고 리턴받은 값을 password에 덧붙인다.
        password += str(mnist_predict(img_binary, model_path))

    return password

def mnist_predict(img, path):
    # 모델 불러올 경로 설정
    model_path = current_dir + path

    # 모델 불러오기
    model = tf.keras.models.load_model(model_path)

    # 모델에 이미지를 넣고 예측한 값(클래스)을 리턴
    prediction = model.predict_classes(img)
    return prediction[0]


if __name__ == "__main__":
    getImglist()