import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import random
from urllib.parse import quote
from songs_data import songs

# ВСТАВЬТЕ СВОЙ ТОКЕН МЕЖДУ КАВЫЧКАМИ
TOKEN = "vk1.a.Yzm1-vv6_VcEoXlLJaBLqIob0XVMgl0NoQ8OTiRIUENoeewESqs7FgiSUqhQxkaoLYkdcVIgj0XYmoEJKQ7kSGeVvcRxQNMtKR0p5nudlwuw7mXmTbtKED4__wrgLIAO41bk0s8zKJcsFzSVVgUGKdIxWgQIKGd-0Z1SObfoRC7X-RuqAVKS_aC85mRdIXVCH9VJOhF7LzJtpGTxHOjHOQ"
vk_session = vk_api.VkApi(token=TOKEN)
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

print("Бот запущен. Доступные года:", sorted(songs.keys()))

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        text = event.text.lower().strip()
        user_id = event.user_id

        if text.startswith("песня"):
            parts = text.split()
            if len(parts) == 2 and parts[1].isdigit():
                year = int(parts[1])
                if year in songs:
                    hit = random.choice(songs[year])
                    # Формируем поисковую ссылку ВК
                    query = f"{hit['artist']} {hit['name']}"
                    vk_url = f"https://vk.com/search?c%5Baudio%5D=1&c%5Bq%5D={quote(query)}"
                    msg = (f"🎵 {hit['artist']} – {hit['name']}\n\n"
                           f"📖 {hit['fact']}\n\n"
                           f"🎧 Слушать: {vk_url}")
                else:
                    years_list = ", ".join(str(y) for y in sorted(songs.keys()))
                    msg = f"❌ Нет песен за {year}. Доступны: {years_list}"
            else:
                msg = "📅 Напиши: песня 1985\nПример: песня 1971"
        else:
            years_list = ", ".join(str(y) for y in sorted(songs.keys()))
            msg = (f"🎶 Архив забытых хитов\n\n"
                   f"Доступные года: {years_list}\n"
                   f"Пример команды: песня 1990")

        vk.messages.send(user_id=user_id, message=msg, random_id=0)