from settings.conf import AZURE_STORAGE_CONF

LANG_CHOICE = {
    0: 'Українська',
    1: 'ru',
}

GENDER_CHOICE = {
    0: '👱🏻‍♂️ Чоловік',
    1: '👩🏼‍🦱 Жінка',
}

LOOKING_GENDER_CHOICE = {
    0: '👱🏻‍♂️ Чоловіків',
    1: '👩🏼‍🦱 Жінок',
    2: '👱🏻‍♂️ 👩🏼‍🦱 Чоловіків та Жінок',
    3: '👫 Пару МЖ',
    4: '👬 Пару ММ',
    5: '👭 Пару ЖЖ',
    6: '☯️ Інші гендерні ідентичності',
}

LOOKING_FOR_CHOICE = {
    0: "🥰 Відносини, сім'я",
    1: "😏 Секс без зобов'язань",
    2: '🤗 Спілкування, пошук друзів',
    3: '😉 Усе по трохи',
}

TIER_CHOICE = {
    0: 'free',
    1: 'basic',
    2: 'advanced',
    3: 'premium',
}

PHOTO_TYPE_CHOICE = {
    0: 'Доступно',
    1: 'Приховано',
}

BOT_MESSAGES = {
    'welcome_without_lang': 'Вітаю!',
    'welcome': 'Вітаю! Оберіть мову спілкування з ботом: ',
    'next': 'далі',
    'gender': 'Вкажіть вашу стать: ',
    'looking_gender': 'Кого шукаємо? (Ця інформація буде прихованою і не буде відображатися у вашому профілі) ',
    'age': 'Надрукуйте цифрами свій вік (у діапазоні 18 - 69) ',
    'age_reprompt': 'Ваш фактичний вік має бути в діапазоні 18 - 69 ',
    'prefer_age': 'Надрукуйте цифрами вік партнера (в діапазоні 18 - 69) \n  \nНаприклад: 20 - 45 ',
    'prefer_age_reprompt': 'Фактичний вік має бути в діапазоні 18 - 69',
    'looking_for': 'Мене цікавить: ',
    'upload_file': 'Файли, які ви завантажите, будуть доступні для перегляду тільки якщо ви надасте дозвіл '
                   'для цього (Меню ➡️ Мої фото ➡️ Редагувати фото)\n \n'
                   '⚠️ Файл розміром більше 4МB не буде збережено\n \n'
                   'Будь ласка, додайте зображення/відео (або введіть будь-яке повідомлення, щоб пропустити цей крок)',

    'phone_request': '🤖 ➡️ ❌ Підтвердьте, що ви людина за допомогою телефонного номера, натиснувши кнопку нижче ⬇️',
    'phone_error': 'Підтвердіть свою особу, натиснувши кнопку Підтвердити на клавіатурі нижче',
    'phone_verified': '🙊 Ваш номер телефону не буде доступний іншим користувачам \n  \nДякуємо!',
    'contact_not_my_phone': 'Бот не може підтвердити, що контакт, який ви надіслали є вашим \n  \n'
                            'Вислати свій номер телефону можна лише натиснувши кнопку ✅ Підтвердити',
    'location_request': '🔍 Для пошуку профілів та оголошень необхідно визначити ваше місто, натиснувши кнопку нижче ⬇ ',
    'location_error': 'Дані про ваше розташування будуть використані для визначення міста та області '
                      'та залишаться недоступними для інших користувачів \n  \nНатисніть на кнопку визначити місто',
    'location_verified': '✅ Місто визначено \n  \n😊 Дякуємо!',
    'file_uploaded': '✅ Файл завантажено',
    'file_bad_format': '❌ Можна завантажити лише файли форматів: jpg, png, mp4',
    'file_limit_reached': '❌ Ви завантажили максимальну кількість файлів (4)  \n  \n' \
                          'Видаліть непотрібні файли та спробуйте ще раз',

    'main_menu': 'Головне меню',
    'buy': '👋🏼 До побачення! Якщо потрібно продовжити, наберіть будь-яке повідомлення',

    'prompt_otp': 'На ваш телефон та пошту надійшов 4-х значний код в SMS. Вкажіть його ',
    'self_delete': 'Ваш запис у базі даних було видалено, флоу буде перезапущено ',
    'otp_failed': 'Ви вказали невірний код, спробуйте ще раз',

    'verification_succeeded': 'Авторизація пройшла успішно! Відтепер щотижня будете отримувати запит для '
                              'підтвердження того, що ви на зв\'язку та доступні \n  \n'
                              'Додатково щотижня у той самий час просимо вказавати населений пункт або місто, '
                              'де ви перебуваєте в поточний момент\n  \n'
                              'Важливо: ми не отримуємо доступу до вашої геолокації, вся надана '
                              'інформація надійно захищена згідно з політикою Метінвесту',
    'agreement': 'Я ознайомився з формами про збір та обробку персональних даних, розміщеними за посиланням '
                 'https://bit\.ly/3JTcVi5 та даю свою згоду',

    'error': 'Невідома помилка! \n  \nВведіть будь-яке повідомлення: ',
    'exceptions_occurs': 'Зовнішній сервіс повідомив про помилку❗️  \n  \n'
                         'Зачекайте кілька хвилин і надрукуйте повідомлення, '
                         'щоб перезапустити діалог🔄  \n  \nЯкщо помилка повторюватиметься, зв\'яжіться з розробниками '
                         '(telegram @ )',
    'incoming_message': 'Ви маєте одне нове повідомлення',

}

WITHOUT_LANG_WELCOME_KB = {
    'method': 'sendPhoto',
    'parameters': {
        'caption': f"{BOT_MESSAGES['welcome_without_lang']}",
        'photo': f"https://{AZURE_STORAGE_CONF.STORAGE_ACCOUNT_NAME}.blob.core.windows.net/media/0_online-dating.jpg",
        'reply_markup': {
            'inline_keyboard': [
                [
                    {
                        'text': '➡️ далі',
                        'callback_data': 'KEY_CALLBACK:0'
                    },
                ],
            ]
        }
    }
}

WELCOME_KB = {
    'method': 'sendPhoto',
    'parameters': {
        'caption': f"{BOT_MESSAGES['welcome']}",
        'photo': f"https://{AZURE_STORAGE_CONF.STORAGE_ACCOUNT_NAME}.blob.core.windows.net/media/0_online-dating.jpg",
        'reply_markup': {
            'inline_keyboard': [
                [
                    {
                        'text': 'Українська',
                        'callback_data': 'KEY_CALLBACK:0'
                    },
                    {
                        'text': 'російська',
                        'callback_data': 'KEY_CALLBACK:1'
                    }
                ],
            ]
        }
    }
}

GENDER_KB = {
    'method': 'sendPhoto',
    'parameters': {
        'caption': f"{BOT_MESSAGES['gender']}",
        'photo': f"https://{AZURE_STORAGE_CONF.STORAGE_ACCOUNT_NAME}.blob.core.windows.net/media/1_gender_a.jpg",
        'reply_markup': {
            'inline_keyboard': [
                [
                    {
                        'text': '👱🏻‍♂️ Чоловік',
                        'callback_data': 'KEY_CALLBACK:Man'
                    },
                    {
                        'text': '👩🏼‍🦱 Жінка',
                        'callback_data': 'KEY_CALLBACK:Woman'
                    }
                ],
            ]
        }
    }
}

LOOKING_GENDER_KB = {
    'method': 'sendPhoto',
    'parameters': {
        'caption': f"{BOT_MESSAGES['looking_gender']}",
        'photo': f"https://{AZURE_STORAGE_CONF.STORAGE_ACCOUNT_NAME}.blob.core.windows.net/media/1_gender.jpg",
        'reply_markup': {
            'inline_keyboard': [
                [
                    {
                        'text': '👱🏻‍♂️ Чоловіків',
                        'callback_data': 'KEY_CALLBACK:Man'
                    }
                ],
                [
                    {
                        'text': '👩🏼‍🦱 Жінок',
                        'callback_data': 'KEY_CALLBACK:Woman'
                    }
                ],
                [
                    {
                        'text': '👱🏻‍♂️ 👩🏼‍🦱 Чоловіків та Жінок',
                        'callback_data': 'KEY_CALLBACK:Both'
                    }
                ],
                [
                    {
                        'text': '☯️ Інші варіанти',
                        'callback_data': 'KEY_CALLBACK:Other'
                    }
                ]
            ]
        }
    }
}

MY_AGE_KB = {
    'method': 'sendPhoto',
    'parameters': {
        'caption': f"{BOT_MESSAGES['age']}",
        'photo': f"https://{AZURE_STORAGE_CONF.STORAGE_ACCOUNT_NAME}.blob.core.windows.net/media/2_age.jpg",
        'reply_markup': {
            'force_reply': True
        }
    }
}

PREFER_AGE_KB = {
    'method': 'sendPhoto',
    'parameters': {
        'caption': f"{BOT_MESSAGES['prefer_age']}",
        'photo': f"https://{AZURE_STORAGE_CONF.STORAGE_ACCOUNT_NAME}.blob.core.windows.net/media/3_prefer_age.jpg",
        'reply_markup': {
            'force_reply': True
        }
    }
}

LOOKING_FOR_KB = {
    'method': 'sendPhoto',
    'parameters': {
        'caption': f"{BOT_MESSAGES['looking_for']}",
        'photo': f"https://{AZURE_STORAGE_CONF.STORAGE_ACCOUNT_NAME}.blob.core.windows.net/media/4_looking_for_a.jpg",
        'reply_markup': {
            'inline_keyboard': [
                [
                    {
                        'text': "🥰 Відносини, сім'я",
                        'callback_data': 'KEY_CALLBACK:relationships'
                    }
                ],
                [
                    {
                        'text': "😏 Секс без зобов'язань",
                        'callback_data': 'KEY_CALLBACK:sex_fun'
                    }
                ],
                [
                    {
                        'text': '🤗 Спілкування, пошук друзів',
                        'callback_data': 'KEY_CALLBACK:talking_friends'
                    }
                ],
                [
                    {
                        'text': '😉 Усе по трохи',
                        'callback_data': 'KEY_CALLBACK:all_in_one'
                    }
                ]
            ]
        }
    }
}

UPLOAD_FILE_KB = {
    'method': 'sendPhoto',
    'parameters': {
        'caption': f"{BOT_MESSAGES['upload_file']}",
        'photo': f"https://{AZURE_STORAGE_CONF.STORAGE_ACCOUNT_NAME}.blob.core.windows.net/media/6_upload.png",
        'reply_markup': {
            'force_reply': True
        }
    }
}

MAIN_MENU_KB = {
    'method': 'sendMessage',
    'parameters': {
        'text': f"{BOT_MESSAGES['main_menu']}",
        'reply_markup': {
            'inline_keyboard': [
                # [
                #     {
                #         'text': '📂 Профіль',
                #         'callback_data': 'KEY_CALLBACK:Профіль'
                #     }
                # ],
                [
                    {
                        'text': '📸 Мої файли',
                        'callback_data': 'KEY_CALLBACK:Мої файли'
                    }
                ],
                [
                    {
                        'text': '💌 Мої оголошення',
                        'callback_data': 'KEY_CALLBACK:Мої оголошення'
                    }
                ],
                [
                    {
                        'text': '⚙️ Налаштування',
                        'callback_data': 'KEY_CALLBACK:Налаштування'
                    }
                ]
            ]
        }
    }
}


def profile_kb(message: str) -> dict:
    return {
        'method': 'sendMessage',
        'parameters': {
            'text': f'{message}',
            'reply_markup': {
                'inline_keyboard': [
                    [
                        {
                            'text': '🔄 Редагувати профіль',
                            'callback_data': 'KEY_CALLBACK:Редагувати профіль'
                        }
                    ],
                    [
                        {
                            'text': '↩️ Назад',
                            'callback_data': 'KEY_CALLBACK:Назад'
                        }
                    ]
                ]
            }
        }
    }


USER_FILES_KB = {
    'method': 'sendMessage',
    'parameters': {
        'text': 'Керування файлами',
        'reply_markup': {
            'inline_keyboard': [
                [
                    {
                        'text': '⬆️ Завантажити файл',
                        'callback_data': 'KEY_CALLBACK:Завантажити файл'
                    }
                ],
                [
                    {
                        'text': '⚙️ Менеджер файлів',
                        'callback_data': 'KEY_CALLBACK:доступ'
                    }
                ],
                [
                    {
                        'text': '↩️ Назад',
                        'callback_data': 'KEY_CALLBACK:Назад'
                    }
                ]
            ]
        }
    }
}


def send_photo_kb(file: str, privacy_type: int) -> dict:
    if privacy_type == 0:
        msg = 'Приватний файл'
    else:
        msg = 'Файл доступний користувачам'

    return {
        'method': 'sendPhoto',
        'parameters': {
            'protect_content': True,
            'caption': f'{msg}',
            'photo': f"https://{AZURE_STORAGE_CONF.STORAGE_ACCOUNT_NAME}.blob.core.windows.net/media/{file}",
        }
    }


def send_video_kb(file: str, privacy_type: int) -> dict:
    if privacy_type == 0:
        msg = 'Файл доступний користувачам'
    else:
        msg = 'Приватний файл'
    return {
        'method': 'sendVideo',
        'parameters': {
            'protect_content': True,
            'caption': f'{msg}',
            'video': f"https://{AZURE_STORAGE_CONF.STORAGE_ACCOUNT_NAME}.blob.core.windows.net/media/{file}",
        }
    }


SEND_MEDIA_KB = {
    'method': 'sendMessage',
    'parameters': {
        'protect_content': True,
        'parse_mode': 'MarkdownV2',
        'text': 'Зробіть вибір:',
        'reply_markup': {
            'inline_keyboard': [
                [
                    {
                        'text': '🔐 Відкрити (Приховати)',
                        'callback_data': 'KEY_CALLBACK:file_open_hidden'
                    }
                ],
                [
                    {
                        'text': '🗑 Видалити файл',
                        'callback_data': 'KEY_CALLBACK:file_rm'
                    }
                ],
                [
                    {
                        'text': '➡️ Далі',
                        'callback_data': 'KEY_CALLBACK:next'
                    }
                ],
            ]
        }
    }
}

ADV_MENU_KB = {
    'method': 'sendMessage',
    'parameters': {
        'text': "Управління оголошеннями",
        'reply_markup': {
            'inline_keyboard': [
                [
                    {
                        'text': '📬 Вхідні повідомлення',
                        'callback_data': 'KEY_CALLBACK:income_adv'
                    }
                ],
                [
                    {
                        'text': '📭 Опубліковані оголошення',
                        'callback_data': 'KEY_CALLBACK:review_adv'
                    }
                ],
                [
                    {
                        'text': '📝 Створити оголошення',
                        'callback_data': 'KEY_CALLBACK:create_adv'
                    }
                ],
                [
                    {
                        'text': '↩️ Назад',
                        'callback_data': 'KEY_CALLBACK:back'
                    }
                ],
            ]
        }
    }
}

SEND_ADV_KB = {
    'method': 'sendMessage',
    'parameters': {
        'text': 'Зробіть вибір:',
        'reply_markup': {
            'inline_keyboard': [
                [
                    {
                        'text': '📬 Вхідні повідомлення',
                        'callback_data': 'KEY_CALLBACK:income_adv'
                    }
                ],
                [
                    {
                        'text': '📭 Опубліковані оголошення',
                        'callback_data': 'KEY_CALLBACK:review_adv'
                    }
                ],
                [
                    {
                        'text': '📝 Створити оголошення',
                        'callback_data': 'KEY_CALLBACK:create_adv'
                    }
                ],
                [
                    {
                        'text': '🗑 Видалити оголошення',
                        'callback_data': 'KEY_CALLBACK:adv_rm'
                    }
                ],
                [
                    {
                        'text': '↩️️ Назад',
                        'callback_data': 'KEY_CALLBACK:back'
                    }
                ],
            ]
        }
    }
}

CREATE_AREA_KB = {
    'method': 'sendMessage',
    'parameters': {
        'text': 'Вкажіть регіон пошуку (можна використовувати регіон, вказаний при '
                'реєстрації з профілю або вказати інший регіон)',
        'reply_markup': {
            'inline_keyboard': [
                [
                    {
                        'text': '📂 Регіон з профілю',
                        'callback_data': 'KEY_CALLBACK:profile_region'
                    }
                ],
                [
                    {
                        'text': '🔍 Вказати інший регіон',
                        'callback_data': 'KEY_CALLBACK:find_region'
                    }
                ]
            ]
        }
    }
}

relationships_buttons = [
    [
        {
            'text': '🏡 Сім\'я',
            'callback_data': 'KEY_CALLBACK:family'
        }
    ],
    [
        {
            'text': '🥰 Відносини',
            'callback_data': 'KEY_CALLBACK:relationships'
        }

    ],

    [
        {
            'text': '❤️ Зустрічі, побачення',
            'callback_data': 'KEY_CALLBACK:dating'
        }
    ],
    [
        {
            'text': '🧸 Народження дітей',
            'callback_data': 'KEY_CALLBACK:children'
        }
    ],
    [
        {
            'text': '✅ Всі цілі додані',
            'callback_data': 'KEY_CALLBACK:ready'
        },
    ]
]

friends_buttons = [
    [
        {
            'text': '❤️ Зустрічі, побачення',
            'callback_data': 'KEY_CALLBACK:dating'
        }
    ],
    [
        {
            'text': '🤗 Прогулянки, спілкування',
            'callback_data': 'KEY_CALLBACK:talking'
        }
    ],
    [
        {
            'text': '✅ Всі цілі додані',
            'callback_data': 'KEY_CALLBACK:ready'
        },
    ]
]

sex_buttons = [
    [
        {
            'text': 'Петтинг, мастурбация',
            'callback_data': 'KEY_CALLBACK:4'
        }
    ],
    [
        {
            'text': 'Оральный секс (делают мне)',
            'callback_data': 'KEY_CALLBACK:5'
        }
    ],
    [

        {
            'text': 'Оральный секс (делаю я)',
            'callback_data': 'KEY_CALLBACK:6'
        }
    ],
    [

        {
            'text': 'Секс (Классический гетеро)',
            'callback_data': 'KEY_CALLBACK:7'
        }
    ],
    [

        {
            'text': 'Анальный секс (я)',
            'callback_data': 'KEY_CALLBACK:8'
        }
    ],
    [

        {
            'text': 'Анальный секс (меня)',
            'callback_data': 'KEY_CALLBACK:9'
        }
    ],
    [

        {
            'text': 'Анилингус (делают мне)',
            'callback_data': 'KEY_CALLBACK:10'
        }
    ],
    [

        {
            'text': 'Анилингус (делаю я)',
            'callback_data': 'KEY_CALLBACK:11'
        }
    ],
    [

        {
            'text': 'Массаж (делают мне)',
            'callback_data': 'KEY_CALLBACK:14'
        }
    ],
    [

        {
            'text': 'Массаж (делаю я)',
            'callback_data': 'KEY_CALLBACK:15'
        }
    ],
    [

        {
            'text': 'Эскорт (предлагаю)',
            'callback_data': 'KEY_CALLBACK:17'
        }
    ],
    [

        {
            'text': 'Эскорт (ищу)',
            'callback_data': 'KEY_CALLBACK:16'
        }
    ],
    [

        {
            'text': 'Фетиши, ролевые игры и другое',
            'callback_data': 'KEY_CALLBACK:12'
        }
    ],
    [
        {
            'text': '✅ Всі цілі додані',
            'callback_data': 'KEY_CALLBACK:ready'
        },
    ]
]

all_in_one_buttons = [
    [
        {
            'text': '🥰 відносини',
            'callback_data': 'KEY_CALLBACK:relationships'
        }]
    ,
    [
        {
            'text': '❤️ Зустрічі, побачення',
            'callback_data': 'KEY_CALLBACK:dating'
        }]
    ,
    [
        {
            'text': '🤗 Прогулянки, спілкування',
            'callback_data': 'KEY_CALLBACK:talking'
        }]
    ,
    [
        {
            'text': '😏 Регулярный секс',
            'callback_data': 'KEY_CALLBACK:'
        }
    ],
    [
        {
            'text': '✅ Всі цілі додані',
            'callback_data': 'KEY_CALLBACK:ready'
        },
    ]
]


def goals_kb(buttons: list, call_back):
    n = 0

    if call_back is not None:
        for item in buttons:
            if item['callback_data'] == call_back:
                item.pop(n)
                n += 1

    return {
        'method': 'sendMessage',
        'parameters': {
            'text': 'Зробіть вибір:',
            'reply_markup': {
                'inline_keyboard': buttons,
            }
        }
    }


MAILS_MAPPING = {
    'report': {
        'subject': 'Новое сообщение от _bot',
        'text': '<h2>Здравствуйте</h2> '
                '<br>'
                'Отчет за последний интервал опроса'
                '<br><br>'
                '<font size="-2">Это сообщение было отправлено автоматически. '
                'Ваш ответ на письмо не требуется.</font>',
        'format': 'otp'
    },
    'otp': {
        'subject': 'Новое сообщение от Nazv\'yazku Bot',
        'text': '<h2>Здравствуйте</h2> '
                '<br>'
                'Ваш проверочный код: {}'
                '<br>'
                'Код действителен 24 часа.'
                '<br><br>'
                '<font size="-2">Это сообщение было отправлено автоматически. '
                'Ваш ответ на письмо не требуется.</font>',
        'format': 'otp'
    },
}