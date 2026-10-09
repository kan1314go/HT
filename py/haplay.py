# -*- coding: utf-8 -*-
# 哈TV 影視壳 Python Spider
# 修正：1. get_prefix 異常防護與超時 2. 列表參數相容性 3. homeVideoContent 正常輸出

import sys
import re
import requests
import xml.etree.ElementTree as ET

sys.path.append('..')
from base.spider import Spider


class Spider(Spider):

    def __init__(self):
        super().__init__()

        self.name = "哈TV"

        # 哈TV Prefix API
        self.prefix_url = (
            "http://58.99.33.12:8080/"
            "csr_mobile_client_web/"
            "Cloud_Account_ProcessAction.do"
            "?method=getVersionCode"
            "&ott_status="
            "&move_type=0"
            "&token_value="
            "&source_service_type="
            "&time="
            "&id="
            "&date="
            "&name="
        )

        self.channels = []
        self.prefix = ""

        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Linux; Android 10) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/131.0.0.0 Mobile Safari/537.36"
            )
        }

        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def getName(self):
        return self.name

    def init(self, extend):
        pass

    def get_channels(self):
        if self.channels:
            return self.channels

        channels = []

        main_channels = {
            "民視": 5, "CNNI HD": 6, "台視": 7, "中視": 9, "大愛電視台": 10,
            "華視": 11, "動物星球": 12, "公視(HD)": 13, "公視台語台": 14, "好消息衛星電視台": 15,
            "原住民族電視台": 16, "客家電視台": 17, "BBC Earth HD": 18, "DISCOVERY": 19, "中台灣生活網": 20,
            "TLC旅遊生活頻道": 21, "Cartoon Network": 22, "CARTOONITO": 23, "MOMO親子台": 24, "東森幼幼台": 25,
            "緯來綜合台": 26, "八大第一台": 27, "八大綜合台": 28, "三立台灣台": 29, "三立都會台": 30,
            "壹電視資訊綜合台": 31, "東森綜合台": 32, "超視": 33, "東森購物2台": 34, "MOMO 2": 35,
            "中天綜合台": 36, "東風衛視": 37, "年代MUCH TV": 38, "AXN": 39, "東森戲劇台": 40,
            "八大戲劇台": 41, "TVBS歡樂台": 42, "緯來戲劇台": 43, "高點電視台": 44, "JET綜合台": 45,
            "東森購物3台": 46, "東森購物1台": 47, "MOMO一台": 48, "壹電視新聞台": 49, "年代新聞台": 50,
            "東森新聞台": 51, "華視新聞資訊台": 52, "民視新聞台": 53, "三立新聞台": 54, "TVBS新聞台": 55,
            "TVBS": 56, "東森財經新聞台": 57, "非凡新聞台": 58, "VIVA1台": 59, "東森購物5台": 60,
            "CATCHPLAY電影台": 61, "東森電影台": 62, "緯來電影台": 63, "冠軍電視台": 64, "HBO": 65,
            "東森洋片台": 66, "中天娛樂台": 67, "好萊塢電影台": 68, "amc電影台": 69, "美麗人生購物台": 70,
            "CINEMAX": 71, "緯來體育台": 72, "DAZN 1": 73, "DAZN 2": 74, "MOMO綜合台": 75,
            "博斯運動一台": 76, "海豚綜合台": 77, "中投地方采風": 78, "緯來日本台": 79, "國興衛視": 80,
            "冠軍夢想台": 81, "信吉電視台": 82, "中投生活資訊": 83, "中投民俗才藝": 84, "寰宇新聞台": 85,
            "信大電視台": 86, "緯來育樂台": 87, "三立財經新聞台": 88, "雙子衛視": 89, "靖天購物一台": 90,
            "台灣綜合台": 91, "LS Time電影台": 92, "SBN全球財經台": 93, "誠心電視台": 94, "非凡商業台": 95,
            "台灣藝術台": 96, "運通財經綜合台": 97, "Z頻道": 98, "霹靂台灣台": 99, "MTV綜合台HD": 100,
            "BBC Lifestyle HD": 101, "十方法界": 102, "華藏衛視": 103, "ANIMAX": 104, "佛衛慈悲台": 105,
            "八大娛樂台": 106, "全大電視台": 107, "華藝台灣台": 108, "正德電視台": 109, "天良綜合台": 110,
            "番薯電視台": 111, "富立電視台": 112, "樂視台": 113, "三聖電視台": 114, "新天地民俗台": 115,
            "紅豆電視台": 116, "威達超舜生活台": 117, "天美麗電視台": 118, "大立電視台": 119, "大愛二台": 121,
            "智林體育台": 122, "國會頻道1": 123, "國會頻道2": 124, "幸福空間居家台": 125, "高點育樂台": 126,
            "華視教育體育文化台": 127, "希望綜合台": 131, "高雄都會台": 133, "NHK WORLD PREMIUM": 135,
            "唯心電視台": 140, "Global Trekker 探索世界": 145, "ROCK Action": 146, "TRACE Sport Stars": 147,
            "美食星球HD": 148, "寰宇財經HD": 149, "民視第一台": 151, "民視台灣台": 152, "台視新聞台": 155,
            "台視財經台": 156, "台視綜合台": 157, "公視兒少台HD": 159, "中視新聞台": 161, "TaiwanPlus": 163,
            "BBC News": 164, "CNA": 165, "FRANCE24 英文台": 166, "A-One體育台": 167, "LOVE NATURE": 168,
            "TV5MONDE": 170, "Arirang TV HD": 171, "亞洲旅遊台": 172
        }

        package_channels = {
            "Discovery Asia": 200, "Discovery 科學頻道": 201, "DMAX": 202, "Dreamworks": 207,
            "Cbeebies": 209, "亞洲美食頻道": 211, "EVE": 215, "HBO HD": 220, "HBO Signature": 221,
            "HBO Family": 222, "HBO Hits": 223, "tvN": 225, "博斯高球一台": 242, "博斯網球台": 243,
            "博斯運動二台": 244, "博斯高球二台": 245, "博斯無限台": 246, "博斯無限二台": 247, "博斯魅力網": 248
        }

        adult_channels = {
            "玩家頻道": 401, "HAPPY": 402, "Hot": 403, "松視4台": 404, "松視1台": 405,
            "松視2台": 406, "松視3台": 407, "彩虹頻道": 408, "樂活頻道": 410, "潘朵啦高畫質玩美台": 411,
            "潘朵啦高畫質粉紅台": 412, "驚豔成人電影台": 413, "香蕉台": 414
        }

        for name, chid in main_channels.items():
            channels.append({"id": str(chid), "name": name, "category": "哈TV頻道", "logo": ""})

        for name, chid in package_channels.items():
            channels.append({"id": str(chid), "name": name, "category": "哈TV套餐頻道", "logo": ""})

        for name, chid in adult_channels.items():
            channels.append({"id": str(chid), "name": name, "category": "成人頻道", "logo": ""})

        self.channels = channels
        return channels

    def get_prefix(self):
        if self.prefix:
            return self.prefix

        try:
            # 降速與極短 timeout 避免影視壳載入時卡死
            response = self.session.get(self.prefix_url, timeout=4)
            if response.status_code == 200:
                root = ET.fromstring(response.content)
                node = root.find(".//ad_url")
                if node is not None and node.text:
                    match = re.search(r"liveedge2/([^_/]+)_", node.text.strip())
                    if match:
                        self.prefix = match.group(1)
                        return self.prefix
        except Exception:
            pass

        return ""

    def get_channel_url(self, chid):
        chid = str(chid)
        prefix = self.get_prefix()
        if not prefix:
            return ""

        return (
            f"http://58.99.33.2:1935/liveedge2/{prefix}_{chid}_1/chunklist_w.m3u8"
            "?checkCode=37050688asdfsdfsadf&aa=60999&as=2018&dr=&mmmm="
        )

    def isVideoFormat(self, url):
        if not url:
            return False
        return any(ext in url.lower() for ext in [".m3u8", ".mp4", ".ts", ".flv"])

    def manualVideoCheck(self):
        return False

    def homeContent(self, filter):
        self.get_channels()
        classes = [
            {"type_name": "全部頻道", "type_id": "all"},
            {"type_name": "哈TV頻道", "type_id": "哈TV頻道"},
            {"type_name": "哈TV套餐頻道", "type_id": "哈TV套餐頻道"},
            {"type_name": "成人頻道", "type_id": "成人頻道"}
        ]
        return {"class": classes}

    def homeVideoContent(self):
        channels = self.get_channels()
        videos = []
        for item in channels:
            videos.append({
                "vod_id": item["id"],
                "vod_name": item["name"],
                "vod_pic": item.get("logo", ""),
                "vod_remarks": item["category"],
                "vod_year": "",
                "vod_area": "",
                "vod_actor": "",
                "vod_director": "",
                "vod_content": "哈TV直播頻道"
            })
        return {"list": videos}

    def categoryContent(self, tid, page, filter, ext):
        channels = self.get_channels()
        videos = []
        tid = str(tid)

        for item in channels:
            if tid != "all" and item["category"] != tid:
                continue

            videos.append({
                "vod_id": item["id"],
                "vod_name": item["name"],
                "vod_pic": item.get("logo", ""),
                "vod_remarks": "直播",
                "vod_year": "",
                "vod_area": "",
                "vod_actor": "",
                "vod_director": "",
                "vod_content": item["category"]
            })

        return {
            "list": videos,
            "page": 1,
            "pagecount": 1,
            "limit": len(videos),
            "total": len(videos)
        }

    def detailContent(self, array):
        if not array:
            return {"list": []}

        chid = str(array[0])
        channels = self.get_channels()
        channel_name = f"頻道 {chid}"
        logo = ""
        category = ""

        for item in channels:
            if str(item["id"]) == chid:
                channel_name = item["name"]
                logo = item.get("logo", "")
                category = item.get("category", "")
                break

        url = self.get_channel_url(chid)

        return {
            "list": [
                {
                    "vod_id": chid,
                    "vod_name": channel_name,
                    "vod_pic": logo,
                    "vod_remarks": "直播",
                    "vod_year": "",
                    "vod_area": category,
                    "vod_content": "哈TV直播頻道",
                    "vod_play_from": "哈TV",
                    "vod_play_url": f"播放${url}"
                }
            ]
        }

    def searchContent(self, key, quick, page="1"):
        if not key:
            return {"list": []}

        key = str(key).lower()
        channels = self.get_channels()
        videos = []

        for item in channels:
            if key not in item["name"].lower():
                continue

            videos.append({
                "vod_id": item["id"],
                "vod_name": item["name"],
                "vod_pic": item.get("logo", ""),
                "vod_remarks": "直播",
                "vod_content": item["category"]
            })

        return {"list": videos}

    def searchContentPage(self, keywords, quick, page):
        return self.searchContent(keywords, quick, page)

    def playerContent(self, flag, pid, vipFlags):
        if not pid:
            return {"parse": 0, "playUrl": "", "url": "", "header": {}}

        return {
            "parse": 0,
            "playUrl": "",
            "url": pid,
            "header": {
                "User-Agent": (
                    "Mozilla/5.0 (Linux; Android 10) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/131.0.0.0 Mobile Safari/537.36"
                ),
                "Referer": "http://58.99.33.12/"
            }
        }

    def liveContent(self, url):
        channels = self.get_channels()
        lines = ["#EXTM3U"]
        for item in channels:
            play_url = self.get_channel_url(item["id"])
            if not play_url:
                continue
            lines.append(
                f'#EXTINF:-1 tvg-logo="{item.get("logo", "")}" group-title="{item["category"]}",{item["name"]}'
            )
            lines.append(play_url)
        return "\n".join(lines)

    def localProxy(self, params):
        return {}

    def destroy(self):
        try:
            self.session.close()
        except Exception:
            pass
        return "正在Destroy"


if __name__ == "__main__":
    pass
