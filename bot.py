import requests
import vk_api
from vk_api.utils import get_random_id
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
import time
from utils import *

group_token = 'vk1.a.spx6PyqlNUTXe67P7GSGQCR7bCyzWdOIsixvpKOmUEsrSmZ4EkSGGkhotXlVVbPkOesdn8u9bdSft0HeyAcwh1hP594VhHpycSPeT0_9EwMLqy46x67iiRohQJxRCGUlGDNGL_lCpvwrjD183t9lT5Qortl4Mef2BeaWEjza7DgiUI8aFuBLUAwHESx5xBV1_34AOFGpFDpojEJFgPRvsw'
# vk_session = vk_api.VkApi(token=group_token)
upload = VkUpload(vk_session)

values = requests.get('https://api.vk.com/method/groups.getLongPollServer', params={'access_token': group_token, 'v': 5.131, 'group_id': 219274632}).json()['response']
server = values['server']
key = values['key']
ts = values['ts']

while True:
    print(ts)
    req = requests.get(f'{server}?act=a_check&key={key}&ts={ts}&wait=30')
    data = req.json()
    if 'updates' in data:
        if data['updates'] != []:
            ts = int(ts) + 1
            for event in data['updates']:
                if event['type'] == 'message_new':
                    print(f"new message from: {event['object']['message']['from_id']}")
                    if event['object']['message']['attachments'] != []:
                        print(f"work photo from {event['object']['message']['from_id']}")
                        user_id = event['object']['message']['from_id']
                        # photo_url = event['object']['message']['attachments'][0]['photo']['sizes'][7]['url']
                        photo_info = event['object']['message']['attachments'][0]['photo']['sizes']
                        photo_url = ''
                        for photo in photo_info:
                            if photo['type'] == 'z':
                                photo_url = photo['url']

                        image_name = save_get_image(photo_url, user_id)

                        reformat_image(image_name, user_id)

                        uploads_images = upload.photo_messages(photos=[f'images/reformat/results/ava_{user_id}.png'])

                        images = ''
                        for image in uploads_images:
                            images += 'photo{}_{}'.format(image['owner_id'], image['id'])

                        send_images(user_id, images)

                    else:
                        print(f"work text from {event['object']['message']['from_id']}")
                        if event['object']['message']['text'] != '':
                            user_id = event['object']['message']['from_id']

                            user_photo = get_photo_url(user_id)
                            image_name = save_user_avatar(user_photo['url'], user_id)
                            reformat_image(image_name, user_id)

                            uploads_images = upload.photo_messages(photos=[f'images/sourse/cat.jpg', f'images/reformat/results/ava_{user_id}.png'])

                            images = ''
                            for image in uploads_images:
                                images += 'photo{}_{}'.format(image['owner_id'], image['id']) + ','

                            send_images(user_id, images)

