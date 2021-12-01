import json

import requests

out_path = "G:\\pixiv\\"
sources_path = out_path + "src\\"
checkpoint_path = out_path + "checkpoint\\"
proxies = {
    'https': 'http://localhost:29758',
    'http': 'http://localhost:29758'
}
headers = {
    "cookie": 'first_visit_datetime_pc=2021-11-15+17%3A34%3A27; '
              'p_ab_id=9; p_ab_id_2=4; p_ab_d_id=401914293; '
              'yuid_b=KYeRcA; _gcl_au=1.1.1918950531.1637342631; '
              'c_type=19; a_type=0; b_type=2; ki_r=; '
              'ki_s=214908%3A0.0.0.0.2%3B214994%3A0.0.0.0.2%3B215190%3A0.0.0.0.2%3B220959%3A0.0.0.0.2; '
              'login_ever=yes; '
              'tag_view_ranking=4QveACRzn3~-aje4qKLpW~DvpBcdQm5q~LJo91uBPz4~9ODMAZ0ebV~_Jc3XITZqL~RTJMXD26Ak'
              '~65aiw_5Y72~Lt-oEicbBr~HLWLeyYOUF~kGYw4gQ11Z~Itu6dbmwxu~a810h_CYms~Cj_Gcw9KR1~qkC-JF_MXY~e3YKQbOrfa'
              '~kzLMCKtPl3~epvz6rmYIS~TF54ZguWG3; '
              'user_language=zh; '
              'ki_t=1637342899464%3B1637342899464%3B1637352903310%3B1%3B22',
    "accept": "text/html,application/xhtml+xml,application/xml;"
              "q=0.9,image/avif,image/webp,image/apng,*/*;"
              "q=0.8,application/signed-exchange;"
              "v=b3;q=0.9",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
}
# url = 'https://www.pixiv.net/artworks/93902830'
url_user = "https://pixiv.net/ajax/user/%s/profile/all?lang=zh"
url_recommend = "https://www.pixiv.net/ajax/illust/%s/recommend/init?limit=30&lang=zh"
url_get_info = "https://www.pixiv.net/ajax/illust/recommend/illusts?" \
               "illust_ids%5B%5D=93707358" \
               "&illust_ids%5B%5D=94069522" \
               "&illust_ids%5B%5D=94105924" \
               "&illust_ids%5B%5D=84899204" \
               "&illust_ids%5B%5D=93738885" \
               "&illust_ids%5B%5D=94059540" \
               "&illust_ids%5B%5D=93576901" \
               "&illust_ids%5B%5D=92301569" \
               "&illust_ids%5B%5D=93061504" \
               "&illust_ids%5B%5D=93558857" \
               "&illust_ids%5B%5D=93979591" \
               "&illust_ids%5B%5D=93627877" \
               "&illust_ids%5B%5D=90499755" \
               "&illust_ids%5B%5D=93697192" \
               "&illust_ids%5B%5D=93957504" \
               "&illust_ids%5B%5D=93536953" \
               "&illust_ids%5B%5D=93780826" \
               "&illust_ids%5B%5D=93812849" \
               "&lang=zh"
url_main = "https://www.pixiv.net/ajax/top/illust"
url_top = "https://www.pixiv.net/ranking.php?p=%s&format=json"
url_full = "https://www.pixiv.net/ajax/user/160522?full=1&lang=zh"
url_last = "https://www.pixiv.net/ajax/user/160522/works/latest?lang=zh"
url_pic = "https://www.pixiv.net/ajax/illust/%s"

getedPaint = []
getedPainter = []
findedPainter = []


def getPaintByPaintID(id):
    if getedPaint.count(id) > 0: return
    headers["referer"] = url_pic % id
    pic_result = requests.get(url_pic % id, proxies=proxies, headers=headers).json()
    images_urls = pic_result["body"]["urls"]
    headers["referer"] = images_urls["original"]
    image = requests.get(images_urls["original"], proxies=proxies, headers=headers)
    with open(sources_path + id + ".jpg", "wb+") as fp:
        fp.write(image.content)
    with open(sources_path + id + ".json", "w+", encoding='utf-8') as fp:
        fp.write(json.dumps(pic_result, ensure_ascii=False))
    print("geted paint id %s" % id)
    getedPaint.append(id)
    painterId = pic_result["body"]["userId"]
    if getedPainter.count(painterId) == 0 and findedPainter.count(painterId) == 0:
        print("finded painter id %s" % painterId)
        findedPainter.append(painterId)


def clearFindedPainter():
    for painterId in findedPainter:
        paintList = getListByPainterID(painterId)
        for paint in paintList["illusts"]:
            getPaintByPaintID(paint)
            recommendList = getRecommendByPaintID(paint)
            for res in recommendList:
                getPaintByPaintID(res["id"])
        getedPainter.append(painterId)
    findedPainter.clear()


def getRecommendByPaintID(id):
    headers["referer"] = url_recommend % id
    recommend = requests.get(url_recommend % id, proxies=proxies, headers=headers).json()
    return recommend["body"]["illusts"]


def getListByPainterID(id):
    headers["referer"] = url_user % id
    lists = requests.get(url_user % id, proxies=proxies, headers=headers).json()
    return lists["body"]


for i in range(1, 10):
    headers["referer"] = url_top % str(i)
    top_list = requests.get(url_top % str(i), proxies=proxies, headers=headers).json()
    for res in top_list["contents"]:
        res = str(res["illust_id"])
        getPaintByPaintID(res)
        recommendList = getRecommendByPaintID(res)
        for res in recommendList:
            if "isAdContainer" not in res:
                getPaintByPaintID(res["id"])
    print(top_list)
    clearFindedPainter()
# json1=getListByPainterID("32709571")

# getRecommendByPaintID("66555623")
