from flask import Flask, render_template
from collections import Counter
import leancloud
import requests
import random
import jieba
import re

leancloud.init("LwmvjzvHzUxmJDK6QeAlflA4-MdYXbMMI", "CsDY3h7a7GYktVFH3yO8vpsd")

app = Flask(__name__)

querylist = [
        'id',
        'title',
        'video_link',
        'time',
        'date',
        'play_num',
        'like_num',
        'coin_num',
        'danmu_num',
        'collect_num',
        'share_num',
        'taglist']

# 从leancould获取数据

# 时间序列数据排序
def getleanclouddatatime(order,number):
    Bilidata = leancloud.Object.extend('bilidata')
    query = Bilidata.query
    query.select(querylist)
    query.descending(order)
    query.limit(number)
    query_list = query.find()
    dataoutput = []
    datalist = []
    for item in query_list:
        data = []
        data.append(item.get('id'))
        data.append(item.get('title'))
        data.append(item.get('video_link'))
        data.append(item.get('time'))
        data.append(item.get('date'))
        data.append(item.get('play_num'))
        data.append(item.get('like_num'))
        data.append(item.get('coin_num'))
        data.append(item.get('danmu_num'))
        data.append(item.get('collect_num'))
        data.append(item.get('share_num'))
        data.append(item.get('taglist'))
        dataoutput.append(data)
    k1 = 0
    for i in dataoutput:
        if i[querylist.index(order)] == 0:
            break
        item = []
        k1 = k1 + 1
        str = i[3]
        str1 = str[0:2]
        item.append(k1)
        item.append(str1)
        datalist.append(item)
    return datalist

# top列表排序
def getleanclouddataorder(order,number):
    Bilidata = leancloud.Object.extend('bilidata')
    query = Bilidata.query
    query.select(querylist)
    query.descending(order)
    query.limit(number)
    query_list = query.find()
    dataoutput = []
    datalist = []
    for item in query_list:
        data = []
        data.append(item.get('id'))
        data.append(item.get('title'))
        data.append(item.get('video_link'))
        data.append(item.get('time'))
        data.append(item.get('date'))
        data.append(item.get('play_num'))
        data.append(item.get('like_num'))
        data.append(item.get('coin_num'))
        data.append(item.get('danmu_num'))
        data.append(item.get('collect_num'))
        data.append(item.get('share_num'))
        data.append(item.get('taglist'))
        dataoutput.append(data)
    for item in dataoutput:
        items = []
        items.append(item[1])
        items.append(item[querylist.index(order)])
        items.append(item[2])
        imagelink = item[2].replace('https://www.bilibili.com/video/', '')
        #imagelink = getpic(imagelink)
        imagelink ='https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fimg.mp.itc.cn%2Fq_70%2Cc_zoom%2Cw_640%2Fupload%2F20160903%2Fd1ed32e2adcb4a93bb76ad1f2d322399_th.jpeg&refer=http%3A%2F%2Fimg.mp.itc.cn&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1613485663&t=85d654cc0e9d042828ea62d164c146e4'
        items.append(imagelink)
        datalist.append(items)
    return datalist

# 基础数据获取
def getleanclouddata():
    Bilidata = leancloud.Object.extend('bilidata')
    query = Bilidata.query
    query.select(querylist)
    query.limit(1000)
    query_list = query.find()
    dataoutput = []
    for item in query_list:
        data = []
        data.append(item.get('id'))
        data.append(item.get('title'))
        data.append(item.get('video_link'))
        data.append(item.get('time'))
        data.append(item.get('date'))
        data.append(item.get('play_num'))
        data.append(item.get('like_num'))
        data.append(item.get('coin_num'))
        data.append(item.get('danmu_num'))
        data.append(item.get('collect_num'))
        data.append(item.get('share_num'))
        data.append(item.get('taglist'))
        dataoutput.append(data)
    return dataoutput


# 临时通过api获取图片链接
def getpic(urlid):
    url = 'https://api.bilibili.com/x/web-interface/view?bvid=' + urlid
    r = requests.get(url)
    r.encoding = 'utf-8'
    datajson = r.json()
    return datajson['data']['pic']

@app.route('/word-infection')
def word():
    taglist = []
    wordlist = []
    titlelist = getleanclouddata()
    for index, item in enumerate(titlelist):
        title = item[1]
        titlere = re.sub(r"[0-9\s+\.\!\/_,$%^*()?;；:-【】+\"\']+|[+——！，;:\-丨｜：～。？、~@#￥%……&*（）]+", "", title)
        seg_list = jieba.cut(titlere, cut_all=False)
        wordlist.extend(seg_list)
        taglist.extend(item[11].split(","))
    # dict = collections.Counter(wordlist)
    word_dict_list = {key: value for key, value in dict(Counter(wordlist)).items() if value > 10 and len(key) > 1}
    word_dictkey_list = list(tuple(word_dict_list.keys()))
    word_dictvalue_list = list(tuple(word_dict_list.values()))

    tag_dict_list = {key: value for key, value in dict(Counter(taglist)).items() if value > 10 and value < 500}
    tag_dictkey_list = list(tuple(tag_dict_list.keys()))
    tag_dictvalue_list = list(tuple(tag_dict_list.values()))

    return render_template('./charts_word.html',
                           word_dictkey_list=word_dictkey_list,
                           word_dictvalue_list=word_dictvalue_list,
                           tag_dictkey_list=tag_dictkey_list,
                           tag_dictvalue_list=tag_dictvalue_list,
                           )

@app.route('/interact-infection')
def interact():
    data = getleanclouddata()
    listmost = [0,0,0,0,0]
    listmin = [0, 0, 0, 0, 0]
    zero =[0, 0, 0, 0, 0]
    thousand = [0, 0, 0, 0, 0]
    hundred = [0, 0, 0, 0, 0]
    play_coll_list = []
    play_like_list = []
    play_share_list = []
    play_coin_list = []
    play_danmu_list = []
    coll_like_list = []
    for dataitem in data:
        num = 0
        maxnumlist = []
        minnumlist = []
        transplay = dataitem[5]/1000
        like_play = [transplay, dataitem[6]]
        coll_play = [transplay, dataitem[9]]
        share_play = [transplay, dataitem[10]]
        coin_play = [transplay, dataitem[7]]
        danmu_play = [transplay, dataitem[8]]
        coll_like=  [dataitem[9], dataitem[6]]
        test = [dataitem[6], dataitem[7], dataitem[8],dataitem[9], dataitem[10]]
        for index, item in enumerate(test):
            if item > 100:
                hundred[index] += 1
            if item > 1000:
                thousand[index] += 1
        if dataitem[9] < 1000 and dataitem[5] < 15000:
            play_coll_list.append(coll_play)
        if dataitem[6] < 400 and dataitem[5] < 15000:
            play_like_list.append(like_play)
        if dataitem[10] < 200 and dataitem[5] < 15000:
            play_share_list.append(share_play)
        if dataitem[7] < 200 and dataitem[5] < 15000:
            play_coin_list.append(coin_play)
        if dataitem[8] < 100 and dataitem[5] < 15000:
            play_danmu_list.append(danmu_play)
        if dataitem[9] < 1000 and dataitem[6] < 1000:
            coll_like_list.append(coll_like)
        maxnum = max(dataitem[6], dataitem[7], dataitem[8],dataitem[9], dataitem[10])
        minnum = min(dataitem[6], dataitem[7], dataitem[8], dataitem[9], dataitem[10])
        for index, item in enumerate(dataitem):
            if index > 5 and item == maxnum:
                num = index - 6
                maxnumlist.append(num)
            if index > 5 and item == minnum:
                num = index - 6
                minnumlist.append(num)
                if minnum == 0:
                    zero[num] = zero[num] + 1
        randommaxnum = random.choice(maxnumlist)
        listmost[randommaxnum] = listmost[randommaxnum] + 1
        randomminnum = random.choice(minnumlist)
        listmin[randomminnum] = listmin[randomminnum] + 1

    return render_template('./charts_action.html',
                           actionmost=listmost,
                           actionmin=listmin,
                           zero=zero,
                           thousand=thousand,
                           hundred=hundred,
                           play_coll_list=play_coll_list,
                           play_like_list=play_like_list,
                           play_share_list=play_share_list,
                           play_coin_list=play_coin_list,
                           play_danmu_list=play_danmu_list,
                           coll_like_list=coll_like_list
                           )


@app.route('/toplist')
def toplist():
    datalist = getleanclouddataorder('play_num', 10)
    datalist1 = getleanclouddataorder('like_num', 10)
    datalist2 = getleanclouddataorder('coin_num', 10)
    datalist3 = getleanclouddataorder('collect_num', 10)
    datalist4 = getleanclouddataorder('share_num', 10)
    datalist5 = getleanclouddataorder('danmu_num', 10)
    return render_template('./toplist.html',
                           play=datalist,
                           like=datalist1,
                           coin=datalist2,
                           coll=datalist3,
                           share=datalist4,
                           danmu=datalist5
                           )


@app.route('/time-infection')
def time():
    list_day_time = []
    data4 = getleanclouddata()
    for item in data4:
        str = item[3]
        str1 = str[0:2]
        list_day_time.append(str1)
    ranklist = []
    rankid = 0
    for ranktime in list_day_time:
        item = []
        rankid = rankid + 1
        item.append(rankid)
        item.append(ranktime)
        ranklist.append(item)
    timecount = Counter(list_day_time)
    timecountkeys = sorted(list(timecount.keys()))
    timedata = []
    for i in range(len(timecountkeys)):
        item = []
        keys = timecountkeys[i]
        item.append(keys + ':00')
        value = timecount[keys]
        item.append(value)
        timedata.append(item)
    # timelike = getleanclouddatatime('like_num', 1000)
    # timecoin = getleanclouddatatime('coin_num', 1000)
    # timecollect = getleanclouddatatime('collect_num', 1000)
    # timeshare = getleanclouddatatime('share_num', 1000)
    # timedanmu = getleanclouddatatime('danmu_num', 1000)
    return render_template('./charts.html',
                           dataall=data4,
                           time=timedata,
                           rank=ranklist,
                           # like=timelike,
                           # coin=timecoin,
                           # coll=timecollect,
                           # share=timeshare,
                           # danmu=timedanmu
                           )


@app.route('/database')
def database():
    dataall = []
    data3 = getleanclouddata()
    for item in data3:
        data = []
        for i in range(len(item)):
            if i == 1:
                str = '<a rel="+' + item[1] + '" href="' + item[2] + '">' + item[1] + '</a>'
                data.append(str)
                continue
            if i == 2:
                continue
            data.append(item[i])
        dataall.append(data)
    return render_template('./tables.html', alldata=dataall)


@app.route('/')
def homepage():
    # 获取时间
    dateall = getleanclouddata()
    datelist=[]
    for item in dateall:
        datelist.append(item[4].replace("-", "/"))
    data_list = []
    data2_list = []
    data3_list = []
    data4_list = []
    data5_list = []
    data6_list = []
    data7_list = []
    data8_list = []
    data9_list = []
    data10_list = []
    data11_list = []
    data12_list = []
    data13_list = []
    for item in dateall:
        data_rank = []
        data_title = []
        data_like = []
        data_coin = []
        data_danmu = []
        data_collect = []
        data_share = []
        data_title.append(item[0])
        data_rank.append(item[0])
        data_like.append(item[0])
        data_coin.append(item[0])
        data_danmu.append(item[0])
        data_collect.append(item[0])
        data_share.append(item[0])
        data_rank.append(item[5])
        data_title.append(item[1])
        data_like.append(item[6])
        data_coin.append(item[7])
        data_danmu.append(item[8])
        data_collect.append(item[9])
        data_share.append(item[10])
        data2_list.append(data_rank)
        data3_list.append(data_title)
        data4_list.append(data_like)
        data5_list.append(data_coin)
        data6_list.append(data_danmu)
        data7_list.append(data_collect)
        data8_list.append(data_share)
        data9_list.extend(item[11].split(","))
        data10_list = {key: value for key, value in dict(Counter(data9_list)).items() if value > 20 and value < 508}
        data11_list = list(tuple(data10_list.keys()))
        data12_list = list(tuple(data10_list.values()))
    return render_template("./index.html",
                           dateall=dateall,
                           datelist=datelist,
                           bili_video_date=data_list,
                           bili_video_rank=data2_list,
                           bili_video_title=data3_list,
                           bili_video_like=data4_list,
                           bili_video_coin=data5_list,
                           bili_video_danmu=data6_list,
                           bili_video_collect=data7_list,
                           bili_video_share=data8_list,
                           bili_video_tag1=data11_list,
                           bili_video_tag2=data12_list,
                           bili=data13_list
                           )
if __name__ == '__main__':
    app.run()
