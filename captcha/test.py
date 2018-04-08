#author:mukever
import os
import requests
from PIL import Image
from keras.models import model_from_json
from keras.utils.vis_utils import plot_model
from vocab import *
loginurl = 'https://ln.122.gov.cn/m/login'
captchaurl = 'https://ln.122.gov.cn/captcha?nocache='


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model = model_from_json(open(BASE_DIR+'/model/CNN.json').read())



model.load_weights(BASE_DIR+'/model/CNN.h5')

plot_model(model, to_file='./model.png', show_shapes=True, show_layer_names=True)

gov_session = requests.session()

login = gov_session.get(loginurl)
img = gov_session.get(captchaurl)
temp_img = img.content
fp = open(BASE_DIR+"/temp.jpg","wb")
fp.write(temp_img)
fp.close()
image = Image.open(BASE_DIR+"/temp.jpg")
wide, high = image.size
for j in range(wide):
    image.putpixel((j, 0), (255, 255, 255))
for j in range(high):
    image.putpixel((0, j), (255, 255, 255))
X_ = np.empty((1, 32, 90, 3), dtype='float32')

X_[0] = np.array(image) / 255
Y_pred = model.predict(X_, 1, 1)
Pred_text = Vocab().one_hot_to_text(Y_pred[0])
print(Pred_text)