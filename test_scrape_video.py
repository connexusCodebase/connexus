import time
from selenium import webdriver
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import image as mpimg
import base64
import scipy.ndimage

def getPic(driver):
    #driver.get('http://96.39.107.90:8082/')
    driver.get(WEBSITE)
    driver.save_screenshot("tmp.png")
    img = mpimg.imread("tmp.png")
    #img = scaleFrameToSize(img)
    print(img.shape)
    return img

def getFrameDiff(frames,i,j):
    try:
        return np.average(np.average(np.average((frames[j]-frames[i])**2)))
    except:
        print('frames size inconsistent: '+str(frames[i].shape))
        return 0

def scaleFrameToSize(img):
    print(img.shape)
    return scipy.ndimage.zoom(img,(HEIGHT/len(img),WIDTH/len(img[0]),1))

def plotFrames(i):
    plt.imshow(frames[i])
    plt.show()

def clickOnScreen(actions):
    actions.click()
    actions.perform()

def convertToGray(img):
    grayImg = np.zeros((HEIGHT,WIDTH))
    for i in range(HEIGHT):
        for j in range(WIDTH):
            grayImg[i][j] = np.average(img[i][j])
    return grayImg

WIDTH = 425.0
HEIGHT = 300.0
WEBSITE = 'http://96.39.107.90:8090/default.htm'

br = webdriver.PhantomJS()

br.set_window_position(0, 0)
br.set_window_size(HEIGHT, WIDTH)
#br.maximize_window()
print(br.get_window_size())
br.get(WEBSITE)
#br.get('http://96.39.107.90:8082/') #second best
#br.get('http://www.earthcam.com/usa/oklahoma/vinita/?cam=route66west')
#br.get('http://www.earthcam.com/usa/newyork/highline/?cam=highline')
#actions = webdriver.ActionChains(br)
#br.get('https://www.timeanddate.com/worldclock/usa/boston') #clock
time.sleep(30)

frames = []
times = []
start = time.time()
frames.append(getPic(br))
times.append(time.time()-start)

frames.append(getPic(br))
times.append(time.time()-start)

i = 1
diff = getFrameDiff(frames,0,1)

time.sleep(30)
while diff<.003:
    br.set_window_size(HEIGHT, WIDTH)
    frames[0] = frames[1]
    times[0] = times[1]
    frames[1] = getPic(br)
    times[1] = time.time()-start
    diff = getFrameDiff(frames,0,1)
    print(diff)
    
for i in range(2,10):
    br.set_window_size(HEIGHT, WIDTH)
    frames.append(getPic(br))
    times.append(time.time()-start)

br.quit



