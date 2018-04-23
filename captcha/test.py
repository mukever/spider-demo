#author:mukever
import json
import os
import requests
from PIL import Image
from keras.models import model_from_json
from keras.utils.vis_utils import plot_model
from vocab import *
loginurl = 'https://ln.122.gov.cn/m/login'
captchaurl = 'https://ln.122.gov.cn/captcha?nocache=123456789'
posturl = 'https://ln.122.gov.cn/m/publicquery/scores/?jszh=sadasd&dabh=123456789012&captcha=%s'
header = {
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Referer':'https://ln.122.gov.cn/views/inquiry.html',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',

}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model = model_from_json(open(BASE_DIR+'/model/CNN.json').read())
model.load_weights(BASE_DIR+'/model/CNN.h5')

# plot_model(model, to_file='./model.png', show_shapes=True, show_layer_names=True)

gov_session = requests.session()
right = 0
for i in range(50000):
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
    print(str(i+1)+'  ======>  '+Pred_text)
    temp_url = posturl % (Pred_text)
    reconvene = gov_session.post(temp_url ,headers= header)
    code = json.loads(reconvene.content.decode('utf8'))['code']
    print(reconvene.content.decode('utf8'))
    ####('1', '正确'), ('0', '错误')
    if code ==404:
        right+=1
        save_path = '/Users/diamond/deep_learn/data/'
        img_name = Pred_text + '.jpg'
        image.save(save_path + img_name)
        print("\033[1;31;40m 正确率：:",right*1.0/(i+1),"\033[0m")
    else:
      pass
