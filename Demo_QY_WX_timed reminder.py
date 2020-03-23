#! -*- coding: utf-8 -*-
"""
Author: ZhenYuSha
Create type_time: 2020-2-24
Info: 定期向企业微信推送消息

Amended by: Ge Zhi
Amend time: 2020-3-22
修订内容: 从原代码每分钟发布一次提醒改成在设定时间点发送提醒，可以实现多时间点发布不同内容提醒信息并@所有人
"""
import requests, json
import datetime
import time

wx_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=9c3ae4ed-c95b-4fed-a853-aaaaaaaaaaa"    # 测试机器人1号    将此网址替换成你的群聊机器人Webhook地址
send_message1 = "内容1，内容1，内容1！"
send_message2 = "内容2，内容2，内容2！"


def get_current_time():
    """获取当前时间，当前时分秒"""
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    hour = datetime.datetime.now().strftime("%H")
    mm = datetime.datetime.now().strftime("%M")
    ss = datetime.datetime.now().strftime("%S")
    return now_time, hour, mm, ss


def sleep_time(hour, m, sec):
    """返回总共秒数"""
    return hour * 3600 + m * 60 + sec


def send_msg(content):
    """@全部，并发送指定信息"""
    data = json.dumps({"msgtype": "text", "text": {"content": content, "mentioned_list":["@all"]}})
    r = requests.post(wx_url, data, auth=('Content-Type', 'application/json'))
    print(r.json)

def every_time_send_msg(interval_h=0, interval_m=0, interval_s=31, special_h1="08",special_h2="12", special_m="00", mode="special"):    #此处定义了每多长时间重复一次此指令，在这里我设置的是每31秒重复一次。且此处设置定时发送消息的时间点（24小时制），在这里我设置的是8点和12点整。
    """每天指定时间发送指定消息"""

    # 设置自动执行间隔时间
    second = sleep_time(interval_h, interval_m, interval_s)
    # 循环
    while True:
        # 获取当前时间和当前时分秒
        c_now, c_h, c_m, c_s = get_current_time()
        print("当前时间：", c_now, c_h, c_m, c_s)
        if c_h == special_h1 and c_m == special_m:
            print('正在发送提醒')
            send_msg(send_message1)
        else:
            print('未到早8点提醒时间')
        # 下午3点报送一次体温
        
        if c_h == special_h2 and c_m == special_m:
            print('正在发送提醒')
            send_msg(send_message2)
        else:
            print('未到中午12点提醒时间')
        # 下午5点报送一次轨迹
        
        print("每隔" + str(interval_h) + "小时" + str(interval_m) + "分" + str(interval_s) + "秒执行一次")
        # 延时
        time.sleep(second)
        
if __name__ == '__main__':
    every_time_send_msg(mode="no")
