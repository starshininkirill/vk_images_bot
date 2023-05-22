# from bot import vk_session, user_vk_session
from PIL import Image, ImageChops
import requests
import vk_api
from vk_api.utils import get_random_id
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType


group_token = 'vk1.a.spx6PyqlNUTXe67P7GSGQCR7bCyzWdOIsixvpKOmUEsrSmZ4EkSGGkhotXlVVbPkOesdn8u9bdSft0HeyAcwh1hP594VhHpycSPeT0_9EwMLqy46x67iiRohQJxRCGUlGDNGL_lCpvwrjD183t9lT5Qortl4Mef2BeaWEjza7DgiUI8aFuBLUAwHESx5xBV1_34AOFGpFDpojEJFgPRvsw'
user_token = 'vk1.a.bSY2W5b5QV12o8YqsZNvZBDlRBeUON2pmaQGEFQm19y8CLM9x31gdz2PZb-RHa0juRVkgN97iIl9viBlOeRN5ex4afc57e7s18drKsDFecwpslyeiKGBW2Bs2JSN4MyRtgkLbz5kfkm26cT0GhVYZtc_MHInyVxsYFjdQ9aI7Xazjml61oT1-7rts2h7xWlposjwIJOkFoFP-6qUdYyw8g'

vk_session = vk_api.VkApi(token=group_token)
user_vk_session = vk_api.VkApi(token=user_token)

upload = VkUpload(vk_session)


def send_message(uid, message):
    vk_session.method('messages.send', {'user_id': uid, 'message': message, 'random_id': get_random_id()})


def send_images(user_id, images):
    vk_session.method('messages.send', {'user_id': user_id, 'random_id': get_random_id(), 'attachment': images})


def get_photo_url_by_photo_id(photo_id):
    print(photo_id)
    # photo = user_vk_session.method('photos.get', {'owner_id': photo_id.split('_')[0], 'photo_ids': photo_id.split('_')[1], 'album_id': 'saved'})['items'][0]['sizes']
    # photo = user_vk_session.method('photos.get',
    #                                {'owner_id': photo_id.split('_')[0], 'photo_ids': photo_id.split('_')[1],
    #                                 'album_id': 'saved'})
    photo = user_vk_session.method('photos.getById', {'photos': f'{photo_id}'})[0]['sizes']
    print(photo)

    # res_photo = []ы
    # for p in photo:
    #     if p['type'] == 'z':
    #         res_photo.append(p)
    #
    # return res_photo[0]['url']


def get_photo_url(user_id):
    photo_id = vk_session.method('users.get', {'user_ids': user_id, 'fields': 'photo_id', 'name_case': 'nom'})[0]['photo_id']
    # photo = user_vk_session.method('photos.get',
    #                                {'owner_id': photo_id.split('_')[0],
    #                                 'photo_ids': photo_id.split('_')[1],
    #                                 'album_id': 'profile'})['items'][0]['sizes']

    photo = user_vk_session.method('photos.getById', {'photos': f'{photo_id}'})[0]['sizes']
    res_photo = []
    for p in photo:
        if p['type'] == 'z':
            res_photo.append(p)
    return res_photo[0]


def save_user_avatar(url, user_id):
    response = requests.get(url, stream=True).raw
    image = Image.open(response)
    # image = image.resize((800, 800))
    image_name = f'ava_{user_id}.jpg'
    image.save(f'images/upload/{image_name}')

    return image_name


def save_get_image(url, user_id):
    response = requests.get(url, stream=True).raw
    img = Image.open(response)
    image_name = f'photo_{user_id}.jpg'
    img.save(f'images/upload/{image_name}', 'jpeg')

    return image_name


def reformat_image(image_name, user_id):
    main_image = Image.open(f'images/upload/{image_name}')
    background_image = Image.open('images/sourse/ram.png').resize(main_image.size)

    mask_im = Image.open('images/sourse/ram.png').resize(main_image.size)
    mask_im = ImageChops.invert(mask_im)

    mask_im.save(f'images/reformat/masks/mask_{user_id}.png')

    background_image.paste(main_image, (0, 0), mask_im)
    background_image.save(f'images/reformat/results/ava_{user_id}.png')
