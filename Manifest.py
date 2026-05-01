import sys
import time
import os
import requests

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
    "Referer": "https://manifest.steam.run/"
}

if getattr(sys, 'frozen', False):
    base_path = os.path.dirname(sys.executable)
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

appid = int(input("请输入游戏appid:"))
depots_url = f"https://manifest.steam.run/api/depot/{appid}"
depots = requests.get(url=depots_url,headers=headers).json()
time.sleep(1)
ls_depots = depots.get('depots',[])
print(f"共查询到{len(ls_depots)}个清单文件")
if len(ls_depots) != 0:
    print("正在进行文件下载")

    #获取depotid,manifestid
    for i in range(0,len(ls_depots),3):
        split =ls_depots[i:i+3]
        for depot in split:
            depot_id = depot['depotid']
            manifest_id = depot['manifestid']
            content_url = f"https://manifest.steam.run/api/manifest/{manifest_id}"
            time.sleep(1)
            res_content = requests.get(url=content_url,headers=headers).json()
            final_content = res_content.get('content')

            if final_content:
                try:
                    cdn_url = f"https://steampipe.akamaized.net/depot/{depot_id}/manifest/{manifest_id}/5/{final_content}"
                    print(f"正在请求{depot_id}...")
                    manifest_file = requests.get(url=cdn_url,headers=headers,timeout=10)

                    if manifest_file.status_code == 200:
                        file_path = os.path.join(base_path,"Manifest")
                        if not os.path.exists(file_path):
                            os.makedirs(file_path)
                        file_name = f"{depot_id}.manifest"
                        final_path = os.path.join(file_path,file_name)
                        with open(final_path,"wb") as f:
                            f.write(manifest_file.content)
                        print(f"✅ {file_name}已保存到{file_path}")
                    else:
                        print(f"❌ 文件保存失败,请重试! error_code:{manifest_file.status_code}")
                except:
                    print("未能获取有效参数,请检查网络是否畅通...")

        time.sleep(1)
    print(f"{len(ls_depots)} 个清单文件已下载完成!✅")

else:
    print("❌ 未找到有效的清单文件，请检查appid是否正确...")
input("\n按下回车键退出程序...")