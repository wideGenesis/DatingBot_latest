import random

from settings.conf import AZURE_STORAGE_CONF

LANG_CHOICE = {
    0: "Українська",
    1: "ru",
}

GENDER_CHOICE = {
    0: "👱🏻‍♂️ Чоловік",
    1: "👩🏼‍🦱 Жінка",
}

LOOKING_GENDER_CHOICE = {
    0: "👱🏻‍♂️ Чоловіків",
    1: "👩🏼‍🦱 Жінок",
    2: "👱🏻‍♂️ 👩🏼‍🦱 Чоловіків та Жінок",
    3: "👫 Пару МЖ",
    4: "👬 Пару ММ",
    5: "👭 Пару ЖЖ",
    6: "☯️ Інші гендерні ідентичності",
}

LOOKING_FOR_CHOICE = {
    0: "🥰 Відносини, сім'я",
    1: "😏 Секс без зобов'язань",
    2: "🤗 Спілкування, пошук друзів",
    3: "😉 Усе по трохи",
}

TIER_CHOICE = {
    0: "free",
    1: "basic",
    2: "advanced",
    3: "premium",
}

PHOTO_TYPE_CHOICE = {
    0: "Доступно",
    1: "Приховано",
}

BOT_MESSAGES = {
    "choose_language": "Choose language: ",
    "reprompt": "Зробіть вибір, натиснувши на відповідну кнопку вище",
    "next": "далі",
    "choose_sex": "Вкажіть вашу стать: ",
    "looking_for_sex": "Кого шукаємо? (Ця інформація буде прихованою і не буде відображатися у вашому профілі) ",
    "age": "Надрукуйте цифрами свій вік (у діапазоні 18 - 69) ",
    "age_reprompt": "Ваш фактичний вік має бути в діапазоні 18 - 69 ",
    "prefer_age": "Надрукуйте цифрами вік партнера (в діапазоні 18 - 69) \n  \nНаприклад: 20 - 45 ",
    "prefer_age_reprompt": "Фактичний вік має бути в діапазоні 18 - 69",
    "looking_for": "Мене цікавить: ",
    "phone_request": "🤖 ➡️ ❌ Підтвердьте, що ви людина за допомогою телефонного номера, натиснувши кнопку нижче ⬇️",
    "phone_error": "Підтвердіть свою особу, натиснувши кнопку Підтвердити на клавіатурі нижче",
    "phone_verified": "🙊 Ваш номер телефону не буде доступний іншим користувачам \n  \nДякуємо!",
    "contact_not_my_phone": "Бот не може підтвердити, що контакт, який ви надіслали є вашим \n  \n"
    "Вислати свій номер телефону можна лише натиснувши кнопку ✅ Підтвердити",
    "location_request": "🔍 Для пошуку профілів та оголошень необхідно визначити ваше місто, натиснувши кнопку нижче ⬇ ",
    "location_error": "Дані про ваше розташування будуть використані для визначення міста та області "
    "та залишаться недоступними для інших користувачів \n  \nНатисніть на кнопку визначити місто",
    "location_verified": "✅ Місто визначено \n  \n😊 Дякуємо!",
    "upload_file": "Файли, які ви завантажите, будуть доступні для перегляду тільки якщо ви надасте дозвіл "
    "для цього (Меню ➡️ Мої фото ➡️ Редагувати фото)\n \n"
    "⚠️ Файл розміром більше 4МB не буде збережено\n \n"
    "Будь ласка, додайте зображення/відео, натисніть на скріпку та виберіть файл"
    " (або введіть будь-яке повідомлення, щоб пропустити цей крок)",
    "file_uploaded": "✅ Файл завантажено",
    "file_bad_format": "❌ Можна завантажити лише файли форматів: jpg, png, mp4",
    "file_limit_reached": "❌ Ви завантажили максимальну кількість файлів (4)  \n  \n"
    "Видаліть непотрібні файли та спробуйте ще раз",
    "file_not_uploaded": "Вкладень не отримано. Продовжуємо далі...",
    "main_menu": "Головне меню",
    "buy": "👋🏼 До побачення! Якщо потрібно продовжити, наберіть будь-яке повідомлення",
    "prompt_otp": "На ваш телефон та пошту надійшов 4-х значний код в SMS. Вкажіть його ",
    "self_delete": "Ваш запис у базі даних було видалено, флоу буде перезапущено ",
    "otp_failed": "Ви вказали невірний код, спробуйте ще раз",
    "verification_succeeded": "Авторизація пройшла успішно! Відтепер щотижня будете отримувати запит для "
    "підтвердження того, що ви на зв'язку та доступні \n  \n"
    "Додатково щотижня у той самий час просимо вказавати населений пункт або місто, "
    "де ви перебуваєте в поточний момент\n  \n"
    "Важливо: ми не отримуємо доступу до вашої геолокації, вся надана "
    "інформація надійно захищена згідно з політикою Метінвесту",
    "error": "Невідома помилка! \n  \nВведіть будь-яке повідомлення: ",
    "exceptions_occurs": "Зовнішній сервіс повідомив про помилку❗️  \n  \n"
    "Зачекайте кілька хвилин і надрукуйте повідомлення, "
    "щоб перезапустити діалог🔄  \n  \nЯкщо помилка повторюватиметься, зв'яжіться з розробниками "
    "(telegram @ )",
    "incoming_message": "Ви маєте одне нове повідомлення",
    "bye": "Вдалих пошуків!",
    "agreement": "Продовжуючи, ви погоджуєтесь з політикою конфіденційності https://zodier.com/policy.html",
}

LOCALES = {"en": {}, "ua": {}, "es": {}, "ru": {}}


def image_rotation(category: str) -> list:
    if category == "straight":
        c_list = ["s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10"]
    elif category == "gay":
        c_list = ["g1", "g2", "g3", "g4", "g5", "g6," "g7", "g8", "g9", "g10"]
    elif category == "friends":
        c_list = ["f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10"]
    elif category == "lesbian":
        c_list = ["l1", "l2", "l3", "l4", "l5", "l6", "l7", "l8", "l9", "l10"]
    else:
        raise ValueError("Category not found")
    random.shuffle(c_list)
    return c_list


CHOOSE_LANG = {
    "method": "sendPhoto",
    "parameters": {
        "caption": f"{BOT_MESSAGES['agreement']} \n \n{BOT_MESSAGES['choose_language']}",
        "photo": f"https://{AZURE_STORAGE_CONF.STORAGE_ACCOUNT_NAME}.blob.core.windows.net/media/logo.jpg",
        "protect_content": True,
        "disable_notification": True,
        "reply_markup": {
            "inline_keyboard": [
                [
                    {"text": "English", "callback_data": "KEY_CALLBACK:0"},
                    {"text": "Українська", "callback_data": "KEY_CALLBACK:1"},
                    {"text": "Español", "callback_data": "KEY_CALLBACK:2"},
                    {"text": "російська", "callback_data": "KEY_CALLBACK:3"},
                ],
            ]
        },
    },
}

CHOOSE_SEX_KB = {
    "method": "sendPhoto",
    "parameters": {
        "caption": f"{BOT_MESSAGES['choose_sex']}",
        "photo": f"https://{AZURE_STORAGE_CONF.STORAGE_ACCOUNT_NAME}.blob.core.windows.net/media/"
        f"{image_rotation('friends')[0]}.jpg",
        "protect_content": True,
        "disable_notification": True,
        "reply_markup": {
            "inline_keyboard": [
                [
                    {"text": "👱🏻‍♂️ Чоловік", "callback_data": "KEY_CALLBACK:Man"},
                    {"text": "👩🏼‍🦱 Жінка", "callback_data": "KEY_CALLBACK:Woman"},
                ],
            ]
        },
    },
}

MY_AGE_KB = {
    "method": "sendPhoto",
    "parameters": {
        "caption": f"{BOT_MESSAGES['age']}",
        "photo": f"https://{AZURE_STORAGE_CONF.STORAGE_ACCOUNT_NAME}.blob.core.windows.net/media/"
        f"{image_rotation('friends')[1]}.jpg",
        "protect_content": True,
        "disable_notification": True,
        "reply_markup": {"force_reply": True},
    },
}

UPLOAD_FILE_KB = {
    "method": "sendPhoto",
    "parameters": {
        "caption": f"{BOT_MESSAGES['upload_file']}",
        "photo": f"https://{AZURE_STORAGE_CONF.STORAGE_ACCOUNT_NAME}.blob.core.windows.net/media/upload.png",
        "reply_markup": {"force_reply": True},
    },
}

PREFER_AGE_KB = {
    "method": "sendPhoto",
    "parameters": {
        "caption": f"{BOT_MESSAGES['prefer_age']}",
        "photo": f"https://{AZURE_STORAGE_CONF.STORAGE_ACCOUNT_NAME}.blob.core.windows.net/media/3_prefer_age.jpg",
        "reply_markup": {"force_reply": True},
    },
}

LOOKING_FOR_SEX_KB = {
    "method": "sendPhoto",
    "parameters": {
        "caption": f"{BOT_MESSAGES['looking_for_sex']}",
        "photo": f"https://{AZURE_STORAGE_CONF.STORAGE_ACCOUNT_NAME}.blob.core.windows.net/media/"
        f"{image_rotation('friends')}.jpg",
        "protect_content": True,
        "disable_notification": True,
        "reply_markup": {
            "inline_keyboard": [
                [{"text": "👱🏻‍♂️ Чоловіків", "callback_data": "KEY_CALLBACK:Man"}],
                [{"text": "👩🏼‍🦱 Жінок", "callback_data": "KEY_CALLBACK:Woman"}],
                [
                    {
                        "text": "👱🏻‍♂️ 👩🏼‍🦱 Чоловіків та Жінок",
                        "callback_data": "KEY_CALLBACK:Both",
                    }
                ],
                [{"text": "☯️ Інші варіанти", "callback_data": "KEY_CALLBACK:Other"}],
            ]
        },
    },
}

LOOKING_FOR_KB = {
    "method": "sendPhoto",
    "parameters": {
        "caption": f"{BOT_MESSAGES['looking_for']}",
        "photo": f"https://{AZURE_STORAGE_CONF.STORAGE_ACCOUNT_NAME}.blob.core.windows.net/media/4_looking_for_a.jpg",
        "reply_markup": {
            "inline_keyboard": [
                [
                    {
                        "text": "🥰 Відносини, сім'я",
                        "callback_data": "KEY_CALLBACK:relationships",
                    }
                ],
                [
                    {
                        "text": "😏 Секс без зобов'язань",
                        "callback_data": "KEY_CALLBACK:sex_fun",
                    }
                ],
                [
                    {
                        "text": "🤗 Спілкування, пошук друзів",
                        "callback_data": "KEY_CALLBACK:talking_friends",
                    }
                ],
                [
                    {
                        "text": "😉 Усе по трохи",
                        "callback_data": "KEY_CALLBACK:all_in_one",
                    }
                ],
            ]
        },
    },
}

MAIN_MENU_KB = {
    "method": "sendMessage",
    "parameters": {
        "text": f"{BOT_MESSAGES['main_menu']}",
        "reply_markup": {
            "inline_keyboard": [
                [
                    {
                        "text": "🌍 Пошук людей поруч",
                        "callback_data": "KEY_CALLBACK:nearby_people",
                    }
                ],
                [
                    {
                        "text": "💌 Пошук за оголошеннями",
                        "callback_data": "KEY_CALLBACK:adv_search",
                    }
                ],
                [{"text": "📂 Профіль", "callback_data": "KEY_CALLBACK:my_profile"}],
                [{"text": "📸 Мої файли", "callback_data": "KEY_CALLBACK:files"}],
            ]
        },
    },
}


def profile_kb(message: str) -> dict:
    return {
        "method": "sendMessage",
        "parameters": {
            "text": f"{message}",
            "reply_markup": {
                "inline_keyboard": [
                    [
                        {
                            "text": "🔄 Редагувати профіль",
                            "callback_data": "KEY_CALLBACK:Редагувати профіль",
                        }
                    ],
                    [{"text": "↩️ Назад", "callback_data": "KEY_CALLBACK:Назад"}],
                ]
            },
        },
    }


USER_FILES_KB = {
    "method": "sendMessage",
    "parameters": {
        "text": "Керування файлами",
        "reply_markup": {
            "inline_keyboard": [
                [
                    {
                        "text": "⬆️ Завантажити файл",
                        "callback_data": "KEY_CALLBACK:upload",
                    }
                ],
                [
                    {
                        "text": "⚙️ Менеджер файлів",
                        "callback_data": "KEY_CALLBACK:access",
                    }
                ],
                [{"text": "↩️ Назад", "callback_data": "KEY_CALLBACK:back"}],
            ]
        },
    },
}

REQUEST_GEO = {
    "method": "sendMessage",
    "parameters": {
        "text": f"{BOT_MESSAGES['location_request']}",
        "reply_markup": {
            "one_time_keyboard": True,
            "resize_keyboard": True,
            "keyboard": [[{"text": "✅ Визначити місто", "request_location": True}]],
        },
    },
}


def send_photo_kb(file: str, privacy_type: int) -> dict:
    if privacy_type == 0:
        msg = "Приватний файл"
    else:
        msg = "Файл доступний користувачам"

    return {
        "method": "sendPhoto",
        "parameters": {
            "protect_content": True,
            "caption": f"{msg}",
            "photo": f"https://{AZURE_STORAGE_CONF.STORAGE_ACCOUNT_NAME}.blob.core.windows.net/media/{file}",
        },
    }


def send_video_kb(file: str, privacy_type: int) -> dict:
    if privacy_type == 0:
        msg = "Файл доступний користувачам"
    else:
        msg = "Приватний файл"
    return {
        "method": "sendVideo",
        "parameters": {
            "protect_content": True,
            "caption": f"{msg}",
            "video": f"https://{AZURE_STORAGE_CONF.STORAGE_ACCOUNT_NAME}.blob.core.windows.net/media/{file}",
        },
    }


SEND_MEDIA_KB = {
    "method": "sendMessage",
    "parameters": {
        "protect_content": True,
        "parse_mode": "MarkdownV2",
        "text": "Зробіть вибір:",
        "reply_markup": {
            "inline_keyboard": [
                [
                    {
                        "text": "🔐 Відкрити (Приховати)",
                        "callback_data": "KEY_CALLBACK:file_open_hidden",
                    }
                ],
                [{"text": "🗑 Видалити файл", "callback_data": "KEY_CALLBACK:file_rm"}],
                [{"text": "➡️ Далі", "callback_data": "KEY_CALLBACK:next"}],
            ]
        },
    },
}

ADV_MENU_KB = {
    "method": "sendMessage",
    "parameters": {
        "text": "Управління оголошеннями",
        "reply_markup": {
            "inline_keyboard": [
                [
                    {
                        "text": "📬 Вхідні повідомлення",
                        "callback_data": "KEY_CALLBACK:income_adv",
                    }
                ],
                [
                    {
                        "text": "📭 Опубліковані оголошення",
                        "callback_data": "KEY_CALLBACK:review_adv",
                    }
                ],
                [
                    {
                        "text": "📝 Створити оголошення",
                        "callback_data": "KEY_CALLBACK:create_adv",
                    }
                ],
                [{"text": "↩️ Назад", "callback_data": "KEY_CALLBACK:back"}],
            ]
        },
    },
}

SEND_ADV_KB = {
    "method": "sendMessage",
    "parameters": {
        "text": "Зробіть вибір:",
        "reply_markup": {
            "inline_keyboard": [
                [
                    {
                        "text": "📬 Вхідні повідомлення",
                        "callback_data": "KEY_CALLBACK:income_adv",
                    }
                ],
                [
                    {
                        "text": "📭 Опубліковані оголошення",
                        "callback_data": "KEY_CALLBACK:review_adv",
                    }
                ],
                [
                    {
                        "text": "📝 Створити оголошення",
                        "callback_data": "KEY_CALLBACK:create_adv",
                    }
                ],
                [
                    {
                        "text": "🗑 Видалити оголошення",
                        "callback_data": "KEY_CALLBACK:adv_rm",
                    }
                ],
                [{"text": "↩️️ Назад", "callback_data": "KEY_CALLBACK:back"}],
            ]
        },
    },
}

CREATE_AREA_KB = {
    "method": "sendMessage",
    "parameters": {
        "text": "Вкажіть регіон пошуку (можна використовувати регіон, вказаний при "
        "реєстрації з профілю або вказати інший регіон)",
        "reply_markup": {
            "inline_keyboard": [
                [
                    {
                        "text": "📂 Регіон з профілю",
                        "callback_data": "KEY_CALLBACK:profile_region",
                    }
                ],
                [
                    {
                        "text": "🔍 Вказати інший регіон",
                        "callback_data": "KEY_CALLBACK:find_region",
                    }
                ],
            ]
        },
    },
}

relationships_buttons = [
    [{"text": "🏡 Сім'я", "callback_data": "KEY_CALLBACK:family"}],
    [{"text": "🥰 Відносини", "callback_data": "KEY_CALLBACK:relationships"}],
    [{"text": "❤️ Зустрічі, побачення", "callback_data": "KEY_CALLBACK:dating"}],
    [{"text": "🧸 Народження дітей", "callback_data": "KEY_CALLBACK:children"}],
    [
        {"text": "✅ Всі цілі додані", "callback_data": "KEY_CALLBACK:ready"},
    ],
]

friends_buttons = [
    [{"text": "❤️ Зустрічі, побачення", "callback_data": "KEY_CALLBACK:dating"}],
    [{"text": "🤗 Прогулянки, спілкування", "callback_data": "KEY_CALLBACK:talking"}],
    [
        {"text": "✅ Всі цілі додані", "callback_data": "KEY_CALLBACK:ready"},
    ],
]

sex_buttons = [
    [{"text": "Петтинг, мастурбация", "callback_data": "KEY_CALLBACK:4"}],
    [{"text": "Оральный секс (делают мне)", "callback_data": "KEY_CALLBACK:5"}],
    [{"text": "Оральный секс (делаю я)", "callback_data": "KEY_CALLBACK:6"}],
    [{"text": "Секс (Классический гетеро)", "callback_data": "KEY_CALLBACK:7"}],
    [{"text": "Анальный секс (я)", "callback_data": "KEY_CALLBACK:8"}],
    [{"text": "Анальный секс (меня)", "callback_data": "KEY_CALLBACK:9"}],
    [{"text": "Анилингус (делают мне)", "callback_data": "KEY_CALLBACK:10"}],
    [{"text": "Анилингус (делаю я)", "callback_data": "KEY_CALLBACK:11"}],
    [{"text": "Массаж (делают мне)", "callback_data": "KEY_CALLBACK:14"}],
    [{"text": "Массаж (делаю я)", "callback_data": "KEY_CALLBACK:15"}],
    [{"text": "Эскорт (предлагаю)", "callback_data": "KEY_CALLBACK:17"}],
    [{"text": "Эскорт (ищу)", "callback_data": "KEY_CALLBACK:16"}],
    [{"text": "Фетиши, ролевые игры и другое", "callback_data": "KEY_CALLBACK:12"}],
    [
        {"text": "✅ Всі цілі додані", "callback_data": "KEY_CALLBACK:ready"},
    ],
]

all_in_one_buttons = [
    [{"text": "🥰 відносини", "callback_data": "KEY_CALLBACK:relationships"}],
    [{"text": "❤️ Зустрічі, побачення", "callback_data": "KEY_CALLBACK:dating"}],
    [{"text": "🤗 Прогулянки, спілкування", "callback_data": "KEY_CALLBACK:talking"}],
    [{"text": "😏 Регулярный секс", "callback_data": "KEY_CALLBACK:"}],
    [
        {"text": "✅ Всі цілі додані", "callback_data": "KEY_CALLBACK:ready"},
    ],
]


def goals_kb(buttons: list, call_back):
    n = 0

    if call_back is not None:
        for item in buttons:
            if item["callback_data"] == call_back:
                item.pop(n)
                n += 1

    return {
        "method": "sendMessage",
        "parameters": {
            "text": "Зробіть вибір:",
            "reply_markup": {
                "inline_keyboard": buttons,
            },
        },
    }


MAILS_MAPPING = {
    "report": {
        "subject": "Новое сообщение от _bot",
        "text": "<h2>Здравствуйте</h2> "
        "<br>"
        "Отчет за последний интервал опроса"
        "<br><br>"
        '<font size="-2">Это сообщение было отправлено автоматически. '
        "Ваш ответ на письмо не требуется.</font>",
        "format": "otp",
    },
    "otp": {
        "subject": "Новое сообщение от Nazv'yazku Bot",
        "text": "<h2>Здравствуйте</h2> "
        "<br>"
        "Ваш проверочный код: {}"
        "<br>"
        "Код действителен 24 часа."
        "<br><br>"
        '<font size="-2">Это сообщение было отправлено автоматически. '
        "Ваш ответ на письмо не требуется.</font>",
        "format": "otp",
    },
}
