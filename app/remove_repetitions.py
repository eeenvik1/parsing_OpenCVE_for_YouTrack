import requests
import re
from dotenv import dotenv_values
config = dotenv_values(".env")

YOU_TRACK_TOKEN = config.get("YOU_TRACK_TOKEN")

main_url = config.get("main_url")
headers = {
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(YOU_TRACK_TOKEN),
        "Content-Type": "application/json"
    }
list_summary = requests.get(URL, headers=headers).json()

buff_cve_list = []
buff_id_list = []
for i in range(len(list_summary)):
    regex = re.search(r'CVE-\d{4}-\d{4,6}', str(list_summary[i]['summary']))
    if regex != None:
        buff_cve_list.append(str(regex.group()))
        buff_id_list.append(list_summary[i]['id'])

no_repeat_list = []
repeat_list = []
for i in range(len(buff_cve_list)):
    if buff_cve_list[i] not in no_repeat_list:
        no_repeat_list.append(buff_cve_list[i])
    else:
        repeat_list.append(buff_id_list[i])

for n, name in enumerate(repeat_list, start = 1):
    URL1 = f'https://vm-proval.myjetbrains.com/youtrack/api/issues/{name}'
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(YOU_TRACK_TOKEN),
        "Content-Type": "application/json"
    }
    requests.delete(URL1, headers=headers)
    print(f'{n} / {len(repeat_list)}')

