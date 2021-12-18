#! /usr/bin/python3
import jinja2
import requests
from bs4 import BeautifulSoup
import urllib3
from cpe import CPE
import nvdlib
import ast


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
YOU_TRACK_TOKEN = 1


def parsing_opencve():
    URL1 = 2
    URL = 3
    USERNAME = 4
    PASSWORD = 5
    csrf_token = ''
    s = requests.Session()
    response = s.get(URL1)
    soup = BeautifulSoup(response.text, 'lxml')

    # Get CSRF
    for a in soup.find_all('meta'):
        if 'name' in a.attrs:
            if a.attrs['name'] == 'csrf-token':
                csrf_token = a.attrs['content']

    # Authentication
    login = s.post(
        URL,
        data={
            'username': USERNAME,
            'password': PASSWORD,
            'csrf_token': csrf_token,
        },
        headers={'referer': 'https://www.opencve.io/login'},
        verify=False
    )

    # Get new CVE
    cve_line = []
    parse = BeautifulSoup(login.text, 'lxml')
    for cve in parse.find_all('h3', class_='timeline-header'):
        if 'is a new CVE' in cve.text:
            cve_line.append(cve.text.replace(' is a new CVE', ''))
    return cve_line


def get_cve_data(cve):
    template = """
### Описание

{{d.cve}}

### Дата публикации

{{d.lastModifiedDate}}

### Дата выявления

{{d.publishedDate}}

### Продукт, вендор

{% for vendor in d.product_vendor_list %}{{vendor}}
{% endfor %}


### CVSSv3 Score

{{d.score}}

### CVSSv3 Vector

{{d.vector}}

### CPE

{% if d.configurations.nodes %}
{% for conf in d.configurations.nodes %}

#### Configuration {{ loop.index }}
{% if conf.operator == 'AND'%}{% set children = conf.children %}{% else %}{% set children = [conf] %}{% endif %}{% if children|length > 1 %}
**AND:**{% endif %}{% for child in children %}{% if child.cpe_match|length > 1 %}**OR:**{% endif %}{% for cpe in child.cpe_match %}
{{ cpe.cpe23Uri | replace("*", "\*") }}{% endfor %}{% endfor %}{% endfor %}
{% endif %}
### Links

{% for link in d.links %}{{ link }}
{% endfor %}

{% if d.exploit_links %}
### Exploit
{% for exploit in d.exploit_links %}{{exploit}}
{% endfor %}
{% endif %}
    """

    YOU_TRACK_PROJECT_ID = 6
    YOU_TRACK_BASE_URL = 7
    URL = 8
    pattern = ['Stack-based buffer overflow', 'Arbitrary command execution', 'Obtain sensitive information', 'Local privilege escalation', 'Security Feature Bypass', 'Out-of-bounds read', 'Out of bounds read', 'Denial of service', 'Denial-of-service', 'Execute arbitrary code', 'Expose the credentials', 'Cross-site scripting (XSS)', 'Privilege escalation', 'Reflective XSS Vulnerability', 'Execution of arbitrary programs', 'Server-side request forgery (SSRF)', 'Stack overflow', 'Execute arbitrary commands', 'Obtain highly sensitive information', 'Bypass security', 'Remote Code Execution', 'Memory Corruption', 'Arbitrary code execution', 'CSV Injection', 'Heap corruption', 'Out of bounds memory access', 'Sandbox escape', 'NULL pointer dereference', 'Remote Code Execution']

    r = nvdlib.getCVE(cve, cpe_dict=False)

    cve_cpe_nodes = r.configurations.nodes
    cpe_nodes = ast.literal_eval(str(r.configurations))
    score = str(r.v3score) + " - "
    links = []
    exploit_links = []
    links.append(r.url)
    
    for t in r.cve.references.reference_data:
        links.append(t.url)
        if 'Exploit' in t.tags:
            exploit_links.append(t.url)
            
    cpe_for_product_vendors = []
    if cpe_nodes:
        for conf in cve_cpe_nodes:
            if conf.operator == 'AND':
                children = [conf.children[0]]
            else:
                children = [conf]
            for child in children:
                for cpe in child.cpe_match:
                    cpe_for_product_vendors.append(cpe.cpe23Uri)

#parse CPE--------------------------------------------------------------------------------------------------------------
    product_vendor_list = []
    product_image_list = []
    version_list = []
    for cpe in cpe_for_product_vendors:
        cpe_parsed = CPE(cpe)
        product = cpe_parsed.get_product()
        vendor = cpe_parsed.get_vendor()
        product_vendor = vendor[0] + " " + product[0] if product != vendor else product
        product_vendor_list.append(product_vendor)
        product_image_list.append(product[0])
        version = cpe_parsed.get_version()
        if (version[0] != '-' and version[0] != '*'):
            version_list.append(version[0])

    temp1 = []
    for item in version_list:
        if item not in temp1:
            temp1.append(item)
            
    versions = []
    for item in temp1:
        ver = {"name": item}
        versions.append(ver)

    prod = []
    for item in product_image_list:
        if item not in prod:
            prod.append(item)

    content = []
    for item in product_vendor_list:
        con = {"name": item}
        content.append(con)

    value = "Да"
    if not exploit_links:
        value = "Нет"

#check regex in cve-----------------------------------------------------------------------------------------------------
    cve_name = ''
    cve_info = r.cve.description.description_data[0].value
    for item in pattern:
        if item.upper() in cve_info.upper():
            cve_name = cve + " - " + item
            break
        else:
            cve_name = cve
#message----------------------------------------------------------------------------------------------------------------
    data = {
        'cve': cve_info,
        'lastModifiedDate': r.lastModifiedDate[:-7],
        'publishedDate': r.publishedDate[:-7],
        'configurations': cpe_nodes,
        'score': score,
        'vector': r.v3vector,
        'links': links,
        'product_vendor_list': prod,
        'exploit_links': exploit_links
    }
    message = jinja2.Template(template).render(d=data)

#check for product_vendor-----------------------------------------------------------------------------------------------
    URL_get_products = 9
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(YOU_TRACK_TOKEN),
        "Content-Type": "application/json"
    }
    data_prod = requests.get(URL_get_products, headers=headers).json()

    upload_prod = []
    for buff in product_vendor_list:
        upload_prod.append(buff)

    prod_vend = []
    for i in data_prod:
        prod_vend.append(i['name'])

    temp = []
    for iter in upload_prod:
        if iter not in prod_vend:
            temp.append(iter)

    for upload in temp:
        payload = {
            "id": "0",
            "&type": "FieldStyle",
            "name": upload
        }
        requests.post(URL_get_products, headers=headers, json=payload)

# check for versions----------------------------------------------------------------------------------------------------
    URL_get_vetsions = 10
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(YOU_TRACK_TOKEN),
        "Content-Type": "application/json"
    }
    data_ver = requests.get(URL_get_vetsions, headers=headers).json()

    ver_list = []
    for i in data_ver:
        ver_list.append(i['name'])

    temp2 = []
    for iter in temp1:
        if iter not in ver_list:
            temp2.append(iter)

    for upload in temp2:
        payload = {
            "id": "0",
            "&type": "FieldStyle",
            "name": upload
        }
        requests.post(URL_get_vetsions, headers=headers, json=payload)

# upload information on cve---------------------------------------------------------------------------------------------
    request_payload = {
        "project": {
            "id": YOU_TRACK_PROJECT_ID
        },
        "summary": cve_name,
        "description": message,
        "tags": [
            {
                "name": "OpenCVE",
                "id": "6-20",
                "$type": "IssueTag"
            }
        ],
        "customFields": [
            {
                "name": "Продукт (пакет)",
                "$type": "MultiEnumIssueCustomField",
                "value": content
            },
            {
                "name": "Есть эксплоит",
                "$type": "SingleEnumIssueCustomField",
                "value": {"name": value}
            },
            {
                "name": "Affected versions",
                "$type": "MultiEnumIssueCustomField",
                "value": versions
            },
        ]
    }
    #print(request_payload) #DEBUG
    print(requests.post(URL, headers=headers, json=request_payload).json()) # Выгрузка инфы о cve в YouTrack

if __name__ == '__main__':
    # MAIN
    URL = 11
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(YOU_TRACK_TOKEN),
        "Content-Type": "application/json"
    }
    list_summary = requests.get(URL, headers=headers).json() # Получение последних 500 задач с YouTrack
    cve_line = parsing_opencve() # Получение списка новых cve с сайта opencve.io
    # Удаление cve, информация о которых уже есть в YouTrack
    sum_list = []
    for n in range(len(list_summary)):
        sum_list.append(list_summary[n]['summary'])
        
    repeat_list = []
    for item in cve_line:
        for n in sum_list:
            index = n.find(item)
            if index != -1:
                repeat_list.append(item)
                
    vuln_list = []
    for item in cve_line:
        if item not in repeat_list:
            vuln_list.append(item)

    for cve in vuln_list:
        get_cve_data(cve)


    # DEBUG
    #get_cve_data('CVE-2021-43808')






