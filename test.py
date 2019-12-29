
import requests

res = requests.get("https://cn.bing.com/images/async?q=%E7%BE%8E%E5%A5%B3&first=0&count=35&relp=35&lostate=r&mmasync=1&dgState=x*175_y*848_h*199_c*1_i*106_r*0")
print(res.text)
