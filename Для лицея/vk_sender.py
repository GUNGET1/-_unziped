import vk
import random


def send_message(id, text):
    token = '''TOKEN'''
    session = vk.Session(access_token=token)
    vka = vk.API(session, v=5.8)


    if type(id) == int:
        vka.messages.send(user_id=id, message=text, random_id=random.randint(0, 2 ** 64), access_token=token)
    else:
        name = vka.users.get(access_token=token, user_ids=id)
        vka.messages.send(user_id=name[0]['id'], message=text)