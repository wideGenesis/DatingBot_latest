import random

from settings.conf import AZURE_STORAGE_CONF

LANG_CHOICE = {
    'en': "English",
    'ua': "Українська",
    'es': "Español",
    'ru': "російська",
}

SEX_CHOICE = {
    'man': "👱🏻‍♂️ Чоловік",
    'woman': "👩🏼‍🦱 Жінка",
}

# LOOKING_GENDER_CHOICE = {
#     0: "👱🏻‍♂️ Чоловіків",
#     1: "👩🏼‍🦱 Жінок",
#     2: "👱🏻‍♂️ 👩🏼‍🦱 Чоловіків та Жінок",
#     3: "👫 👱🏻‍♂️ 👩🏼‍🦱 Компанію",
# }


PHOTO_TYPE_CHOICE = {
    0: "Доступно",
    1: "Приховано",
}

BOT_MESSAGES = {
    "choose_language": "Choose language: ",
    "reprompt": "Зробіть вибір, натиснувши на відповідну кнопку вище",
    "next": "далі",
    "choose_sex": "Вкажіть вашу стать: ",
    "looking_for_sex": "Кого шукаємо? (Ця інформація буде прихованою і не буде відображатися у вашому профілі) \n  \n"
                       " Ви можете вказати ту стать, яку ви насправді шукаєте",
    "age": "Надрукуйте цифрами свій вік (у діапазоні 18 - 69) ",
    "age_reprompt": "Ваш фактичний вік має бути в діапазоні 18 - 69 ",
    "prefer_age": "Надрукуйте цифрами вік партнера (в діапазоні 18 - 69) \n  \nНаприклад: 20 - 45 ",
    "prefer_age_reprompt": "Фактичний вік має бути в діапазоні 18 - 69",
    "looking_for": "Мене цікавлять: ",
    "date_place": "Місце для зустрічей: ",
    "date_time": "У мене є час для зустрічей: ",
    "date_day": "Я можу зустрітися у: ",
    "adv_text": "Текст оголошення: ",
    "money_support": "фінансова підтримка",
    "phone_is_hidden": "Опублікувати ваш телефон?",
    "email_is_hidden": "Опублікувати ваш email?",
    "tg_is_hidden": "Опублікувати ваш telegram?",


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
    "file_uploaded_success": "✅ Файл завантажено! Обробка у процесі",
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
    "files_not_found": "У вас немає завантажених файлів",
}

LOCALES = {"en": {}, "ua": {}, "es": {}, "ru": {}}


def image_rotation(category: str) -> list:
    if category == "straight":
        c_list = ["s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10"]
    elif category == "gay":
        c_list = ["g1", "g2", "g3", "g4", "g5", "g6," "g7", "g8", "g9", "g10"]
    elif category == "friends":
        c_list = ["f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11",
                  "f12", "f13", "f14", "f15", "f16", "f17", "f18"]
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
                    {
                        "text": "English", "callback_data": "KEY_CALLBACK:en"
                    }

                ],
                [
                    {
                        "text": "Українська", "callback_data": "KEY_CALLBACK:ua"
                    }
                ],
                [
                    {
                        "text": "Español", "callback_data": "KEY_CALLBACK:es"
                    }
                ],
                [
                    {
                        "text": "російська", "callback_data": "KEY_CALLBACK:ru"
                    }
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
                    {
                        "text": "👱🏻‍♂️ Чоловік", "callback_data": "KEY_CALLBACK:man"
                    },
                    {
                        "text": "👩🏼‍🦱 Жінка", "callback_data": "KEY_CALLBACK:woman"
                    },
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

MAIN_MENU_KB = {
    "method": "sendMessage",
    "parameters": {
        "text": f"{BOT_MESSAGES['main_menu']}",
        "reply_markup": {
            "inline_keyboard": [
                [
                    {
                        "text": "📝 Створити оголошення",
                        "callback_data": "KEY_CALLBACK:create_adv",
                    }
                ],
                [
                    {
                        "text": "🔥 Опубліковані оголошення",
                        "callback_data": "KEY_CALLBACK:review_adv",
                    }
                ],
                [
                    {
                        "text": "🗣 Розмови",
                        "callback_data": "KEY_CALLBACK:conversations",
                    }
                ],
                [
                    {
                        "text": "📂 Профіль",
                        "callback_data": "KEY_CALLBACK:my_profile",
                    }
                ],
                [
                    {
                        "text": "📸 Мої файли",
                        "callback_data": "KEY_CALLBACK:files",
                    }
                ],
            ]
        },
    },
}

LOOKING_FOR_KB = {
    "method": "sendPhoto",
    "parameters": {
        "caption": f"{BOT_MESSAGES['looking_for']}",
        "photo": f"https://{AZURE_STORAGE_CONF.STORAGE_ACCOUNT_NAME}.blob.core.windows.net/media/"
                 f"{image_rotation('friends')[2]}.jpg",
        "protect_content": True,
        "disable_notification": True,
        "reply_markup": {
            "inline_keyboard": [
                [{"text": "👱🏻‍♂️ Чоловіки", "callback_data": "KEY_CALLBACK:man"}],
                [{"text": "👩🏼‍🦱 Жінки", "callback_data": "KEY_CALLBACK:woman"}],
                [{"text": "🧔‍♂️ 👩‍🦰 Чоловіки та Жінки", "callback_data": "KEY_CALLBACK:both"}],
                [{"text": "🎭 Компанія (розваги, спілкування)", "callback_data": "KEY_CALLBACK:friendship"}],
            ]
        },
    },
}

HAS_PLACE_KB = {
    "method": "sendPhoto",
    "parameters": {
        "caption": f"{BOT_MESSAGES['date_place']}",
        "photo": f"https://{AZURE_STORAGE_CONF.STORAGE_ACCOUNT_NAME}.blob.core.windows.net/media/"
                 f"{image_rotation('friends')[2]}.jpg",
        "protect_content": True,
        "disable_notification": True,
        "reply_markup": {
            "inline_keyboard": [
                [{"text": "🟢 У мене", "callback_data": "KEY_CALLBACK:mine"}],
                [{"text": "🟡 Швидше за все, у мене", "callback_data": "KEY_CALLBACK:sometimes"}],
                [{"text": "❓ У тебе", "callback_data": "KEY_CALLBACK:yours"}],
                [{"text": "🏩 Знімемо (50/50)", "callback_data": "KEY_CALLBACK:fifty_fifty"}],
                [{"text": "🍕 Iнше", "callback_data": "KEY_CALLBACK:other"}],
            ]
        },
    },
}

DATING_TIME = {
    "method": "sendPhoto",
    "parameters": {
        "caption": f"{BOT_MESSAGES['date_time']}",
        "photo": f"https://{AZURE_STORAGE_CONF.STORAGE_ACCOUNT_NAME}.blob.core.windows.net/media/"
                 f"{image_rotation('friends')[3]}.jpg",
        "protect_content": True,
        "disable_notification": True,
        "reply_markup": {
            "inline_keyboard": [
                [{"text": "☕️ Вранці", "callback_data": "KEY_CALLBACK:morning"}],
                [{"text": "🌞 Вдень", "callback_data": "KEY_CALLBACK:day"}],
                [{"text": "🍷 Увечері", "callback_data": "KEY_CALLBACK:evening"}],
                [{"text": "🌔 Вночі", "callback_data": "KEY_CALLBACK:night"}],
            ]
        },
    },
}

DATING_DAY = {
    "method": "sendPhoto",
    "parameters": {
        "caption": f"{BOT_MESSAGES['date_day']}",
        "photo": f"https://{AZURE_STORAGE_CONF.STORAGE_ACCOUNT_NAME}.blob.core.windows.net/media/"
                 f"{image_rotation('friends')[5]}.jpg",
        "protect_content": True,
        "disable_notification": True,
        "reply_markup": {
            "inline_keyboard": [
                [{"text": "💚 будь-який день", "callback_data": "KEY_CALLBACK:any"}],
                [{"text": "💛 сьогодні", "callback_data": "KEY_CALLBACK:today"}],
                [{"text": "💜 у вихідні", "callback_data": "KEY_CALLBACK:weekend"}],
            ]
        },
    },
}

MONEY_SUPPORT = {
    "method": "sendMessage",
    "parameters": {
        "text": f"{BOT_MESSAGES['money_support']}",
        "reply_markup": {
            "inline_keyboard": [
                [
                    {
                        "text": "🟢 Так",
                        "callback_data": "KEY_CALLBACK:money_yes",
                    }
                ],
                [
                    {
                        "text": "🔴 Нi",
                        "callback_data": "KEY_CALLBACK:money_no",
                    }
                ],
            ]
        },
    },
}

ADV_TEXT = {
    "method": "sendMessage",
    "parameters": {
        "text": f"{BOT_MESSAGES['adv_text']}",

    },
}

PREFER_AGE_KB = {
    "method": "sendPhoto",
    "parameters": {
        "caption": f"{BOT_MESSAGES['prefer_age']}",
        "photo": f"https://{AZURE_STORAGE_CONF.STORAGE_ACCOUNT_NAME}.blob.core.windows.net/media/"
                 f"{image_rotation('friends')[3]}.jpg",
        "reply_markup": {"force_reply": True},
    },
}

PHONE_IS_HIDDEN = {
    "method": "sendMessage",
    "parameters": {
        "text": f"{BOT_MESSAGES['phone_is_hidden']}",
        "reply_markup": {
            "inline_keyboard": [
                [
                    {
                        "text": "🟢 Так",
                        "callback_data": "KEY_CALLBACK:phone_yes",
                    }
                ],
                [
                    {
                        "text": "🔴 Нi",
                        "callback_data": "KEY_CALLBACK:phone_no",
                    }
                ],
            ]
        },
    },
}

EMAIL_IS_HIDDEN = {
    "method": "sendMessage",
    "parameters": {
        "text": f"{BOT_MESSAGES['email_is_hidden']}",
        "reply_markup": {
            "inline_keyboard": [
                [
                    {
                        "text": "🟢 Так",
                        "callback_data": "KEY_CALLBACK:email_yes",
                    }
                ],
                [
                    {
                        "text": "🔴 Нi",
                        "callback_data": "KEY_CALLBACK:email_no",
                    }
                ],
            ]
        },
    },
}

TG_IS_HIDDEN = {
    "method": "sendMessage",
    "parameters": {
        "text": f"{BOT_MESSAGES['tg_is_hidden']}",
        "reply_markup": {
            "inline_keyboard": [
                [
                    {
                        "text": "🟢 Так",
                        "callback_data": "KEY_CALLBACK:tg_yes",
                    }
                ],
                [
                    {
                        "text": "🔴 Нi",
                        "callback_data": "KEY_CALLBACK:tg_no",
                    }
                ],
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
                            "callback_data": "KEY_CALLBACK:edit_profile",
                        }
                    ],
                    [{"text": "↩️ Назад", "callback_data": "KEY_CALLBACK:back"}],
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

GLOBAL_GOALS_KB = {
    "method": "sendPhoto",
    "parameters": {
        "caption": f"{BOT_MESSAGES['looking_for']}",
        "photo": f"https://{AZURE_STORAGE_CONF.STORAGE_ACCOUNT_NAME}.blob.core.windows.net/media/"
                 f"{image_rotation('friends')[10]}.jpg",
        "protect_content": True,
        "disable_notification": True,
        "reply_markup": {
            "inline_keyboard": [
                [{"text": "🥰 Сім'я та відносини", "callback_data": "KEY_CALLBACK:relationships"}],
                [{"text": "😏 Побачення, секс без зобов'язань", "callback_data": "KEY_CALLBACK:dating"}],
                [{"text": "🤗 Зустрічі, прогулянки, спілкування", "callback_data": "KEY_CALLBACK:friendship"}],
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


def send_file_kb(member_id: str, file: str, privacy_type: int) -> dict:
    if privacy_type == "hidden":
        msg = "Приватний файл"
    else:
        msg = "Файл доступний користувачам"
    file = f"https://{AZURE_STORAGE_CONF.STORAGE_ACCOUNT_NAME}.blob.core.windows.net/media/{member_id}/{file}"
    return {
        "method": "sendPhoto",
        "parameters": {
            "caption": f"{msg}",
            "photo": file,
            "protect_content": True,
            "disable_notification": True,
            "reply_markup": {
                "inline_keyboard": [
                    [
                        {"text": "🔐", "callback_data": "KEY_CALLBACK:file_open_hidden"},
                        {"text": "🗑", "callback_data": "KEY_CALLBACK:file_rm"},
                        {"text": "➡️", "callback_data": "KEY_CALLBACK:next"},
                    ],
                    [{"text": "↩️ меню", "callback_data": "KEY_CALLBACK:menu"}],
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

sex_buttons = [
    [{"text": "Петтинг, мастурбация", "callback_data": "KEY_CALLBACK:petting"}],
    [{"text": "Оральный секс (делают мне)", "callback_data": "KEY_CALLBACK:oral_to_me"}],
    [{"text": "Оральный секс (делаю я)", "callback_data": "KEY_CALLBACK:oral_to_you"}],
    [{"text": "Секс (Классический)", "callback_data": "KEY_CALLBACK:hetero_fuck"}],
    [{"text": "Анальный секс (я)", "callback_data": "KEY_CALLBACK:anal_to_you"}],
    [{"text": "Анальный секс (меня)", "callback_data": "KEY_CALLBACK:anal_to_me"}],
    [{"text": "Анилингус (делают мне)", "callback_data": "KEY_CALLBACK:rim_to_me"}],
    [{"text": "Анилингус (делаю я)", "callback_data": "KEY_CALLBACK:rim_to_you"}],
    [{"text": "Массаж (делают мне)", "callback_data": "KEY_CALLBACK:massage_to_me"}],
    [{"text": "Массаж (делаю я)", "callback_data": "KEY_CALLBACK:massage_to_you"}],
    [{"text": "Эскорт (предлагаю)", "callback_data": "KEY_CALLBACK:for_pay_offer"}],
    [{"text": "Эскорт (ищу)", "callback_data": "KEY_CALLBACK:for_pay_looking"}],
    [{"text": "Фетиши, ролевые игры и другое", "callback_data": "KEY_CALLBACK:fetishes"}],
    [{"text": "Вiрт", "callback_data": "KEY_CALLBACK:virt"}],
    [
        {"text": "✅ Всі цілі додані", "callback_data": "KEY_CALLBACK:ready"},
    ],
]

relationships_buttons = [
    [{"text": "Створення родини", "callback_data": "KEY_CALLBACK:31"}],
    [{"text": "Народження дітей", "callback_data": "KEY_CALLBACK:32"}],
    [{"text": "Спільне проживання", "callback_data": "KEY_CALLBACK:33"}],
    [{"text": "Серйозні стосунки", "callback_data": "KEY_CALLBACK:34"}],
    [
        {"text": "✅ Всі цілі додані", "callback_data": "KEY_CALLBACK:ready"},
    ],
]

walking_buttons = [
    [{"text": "Спільні походи у кіно", "callback_data": "KEY_CALLBACK:51"}],
    [{"text": "Спільний відпочинок", "callback_data": "KEY_CALLBACK:52"}],
    [{"text": "Заняття спортом", "callback_data": "KEY_CALLBACK:53"}],
    [{"text": "Спілкування", "callback_data": "KEY_CALLBACK:54"}],
    [{"text": "Прогулянки", "callback_data": "KEY_CALLBACK:55"}],
    [{"text": "Дружба", "callback_data": "KEY_CALLBACK:56"}],
    [
        {"text": "✅ Всі цілі додані", "callback_data": "KEY_CALLBACK:ready"},
    ],
]


def goals_kb(buttons: list):
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
