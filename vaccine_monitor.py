import requests
import schedule
import time

areas = [
    {
        'name': '南山区',
        'code': '440305',
    },
    {
        'name': '宝安区',
        'code': '440306',
    }
]

headers = {
    'Host': 'xgsz.szcdc.net',
    'appId': 'app569d18f5',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-cn',
    'Accept-Encoding': 'gzip, deflate, br',
    'token': '-t-Pce-rxMTcnGdsP7dqvV0A339Z0EeMdatyfRTs6GdUxxKyHi8wi1vXSG3uw5Zx1L8',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://xgsz.szcdc.net',
    'Content-Length': '110',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148/openweb=paschybrid/SZSMT_IOS,VERSION:3.3.1',
    'selfAppId': 'TbqkLoGN',
    'Cache-Control': 'no-cache',
    'Referer': 'https://xgsz.szcdc.net/crmobile/other/?appId=app569d18f5&token=-t-Pce-rxMTcnGdsP7dqvV0A339Z0EeMdatyfRTs6GdUxxKyHi8wi1vXSG3uw5Zx1L8&cardNo=BA79827AE2FB723E3020DC2B88914B963AAEEE3AD9637F8354CC5064BD25C0A4&reservationToken=-t-kZB5EJPQ_4mwGCp8CocouIGHy4nzFHjzNNVAH9DjHdRKyHi8wi1vXbweA8emjANm&vaccineCode=5601&mzt=mzt&selfAppId=TbqkLoGN',
    'Connection': 'keep-alive',
    'mzt': 'mzt',
    'reservationToken': '-t-kZB5EJPQ_4mwGCp8CocouIGHy4nzFHjzNNVAH9DjHdRKyHi8wi1vXbweA8emjANm',
}

data = {
    'pageNum': '1',
    'numPerPage': '10',
    'bactCode': '5601',
    'outpName': '',
    'outpMapLongitude': '',
    'outpMapLatitude': ''
}


def query():
    results = []
    
    for area in areas:
        data['areaCode'] = area['code']
        response = requests.post(
            'https://xgsz.szcdc.net/crmobile/outpatient/nearby', headers=headers, data=data)
        # print(response.json())
        listData = response.json()["data"]["list"]
        for item in listData:
            # print(item["outpName"], '有号：', item['status'], '有疫苗：', item['nums'])
            if int(item['status']) == 1 and int(item['nums']) > 0:
                result = area['name'] + ' ' + item['outpName']
                print(result)
                results.append(result)

    if len(results) > 0:
        resultStr = '\n\n'.join(results)
        url = "https://sc.ftqq.com/SCU40394T1a3987b8483010e9b1cc1c64435757025c3bef2fbd9e9.send?text=放号提醒&desp=\n\n"+resultStr
        # print('推送: ', url)
        response = requests.get(url)
        print('推送结果: ', response)
    else:
        print('空')


schedule.every(1).minutes.do(query)

while True:
    schedule.run_pending()   # 运行所有可以运行的任务
    time.sleep(1)
