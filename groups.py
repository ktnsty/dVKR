import requests
import json
import time
import networkx
import collections
import re
import io

token_file = open('token.txt')
for line in token_file:
    token = line
ACCESS_TOKEN = token
token_file.close()

group_file = open('mig_last2.txt', 'r')


group_get_members = "https://api.vk.com/method/groups.getMembers?group_id={}&offset={}&v=5.103&access_token={}"
# id,offset,token

group_get_count = "https://api.vk.com/method/groups.getById?group_id={}&fields=members_count&v=5.103&access_token={}"
#id, token

# открываем файл с названиями групп, выкачиваем id групп в массив
group_list = []
for line in group_file:
    group = line.split('/')[3].split('\n')[0].replace(' ', '')
    if re.fullmatch(r'club\d+', group):
        group = group[4:]
    if re.fullmatch(r'public\d+', group):
        group = group[6:]
    group_list.append(group)

full_number = len(group_list)

group_file.close()
# получаем количество участников группы


def getGroupNameAndCount(group_id):
    json_resp = requests.get(
        group_get_count.format(group_id, ACCESS_TOKEN)).json()
    time.sleep(0.33)
    if json_resp.get('error'):
        print('error')
        return ('error', 0)
    elif json_resp['response'][0]['name'] == 'Частная группа':
        print('private group error')
        return 'error', 0
    elif 'deactivated' in json_resp['response'][0]:
        print('deactivated')
        return 'error', 0
    elif 'members_count' in json_resp['response'][0]:
        print(json_resp['response'][0]['name'],
              json_resp['response'][0]['members_count'])
        return (json_resp['response'][0]['name'], json_resp['response'][0]['members_count'])
    else:
        print('unhandled error')
        return 'error', 0


namecount = io.open('namecount_miglast2.csv', 'a', encoding='utf8')


def getAllGroupMembers(group_id):
    name, group_count = getGroupNameAndCount(group_id)
    namecount.write(str(name)+','+str(group_count)+'\n')
    if group_count == 0:
        return list()
    offset = 0
    members = []
    cnt = 0
    while(cnt*25000 < group_count):
        code = '''
        var offset = ''' + str(offset) + '''; 
        var group_id= "''' + str(group_id) + '''"; 
        var members; 
        var requests = 0; 
        var ret = [];
        while (requests<25) {
            members = API.groups.getMembers({"group_id": group_id, "offset": offset, "count": 1000});
            ret = ret + members.items;
            requests = requests+1;
            offset = offset+1000;
        }
        return ret;'''
        payload = {
            "code": code,
            "access_token": ACCESS_TOKEN,
            "v": '5.103',
        }
        req = requests.post('https://api.vk.com/method/execute', data=payload)
        cnt += 1
        members += req.json()['response']
        offset += 25000
        time.sleep(0.33)
    return members


result = io.open('table_miglast2.csv', 'a')



for group in group_list:

    members = getAllGroupMembers(group)
    for member in members:
        result.write(str(group)+','+str(member)+'\n')

result.close()
namecount.close()
