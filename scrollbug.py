import json

import requests

out_path = "G:\\pixiv2\\"
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
url_pic = "https://www.pixiv.net/ajax/illust/%s"


def getPaintByPaintID(id):
    headers["referer"] = url_pic % id
    pic_result = requests.get(url_pic % id, proxies=proxies, headers=headers).json()
    if pic_result["error"]: return
    images_urls = pic_result["body"]["urls"]
    headers["referer"] = images_urls["original"]
    image = requests.get(images_urls["original"], proxies=proxies, headers=headers)
    with open(sources_path + id + ".jpg", "wb+") as fp:
        fp.write(image.content)
    with open(sources_path + id + ".json", "w+", encoding='utf-8') as fp:
        fp.write(json.dumps(pic_result, ensure_ascii=False))
    print("geted paint id %s" % id)


for i in range(100000000):
    id=str(i)
    getPaintByPaintID(id)
