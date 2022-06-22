from botbuilder.core import CardFactory
from botbuilder.schema import ActionTypes, Attachment, HeroCard, CardAction, CardImage

import config.conf as conf
from ms_bot.lib.messages import BOT_MESSAGES


def welcome_hero_card() -> Attachment:
    card = HeroCard(
        title=f"{BOT_MESSAGES['welcome']}",
        images=[
            CardImage(
                url=f"https://{conf.AZURE_STORAGE_HOST}.blob.core.windows.net/media/0_online-dating.jpg",
            )
        ],
        buttons=[
            CardAction(
                type=ActionTypes.im_back,
                title="Українська",
                value="0",
            ),
            CardAction(
                type=ActionTypes.im_back,
                title="російська",
                value="1",
            ),
        ],
    )
    return CardFactory.hero_card(card)


def gender_hero_card() -> Attachment:
    card = HeroCard(
        title=f"{BOT_MESSAGES['gender']}",
        images=[
            CardImage(
                url=f"https://{configuration.AZURE_STORAGE_HOST}.blob.core.windows.net/media/1_gender_a.jpg",
            )
        ],
        buttons=[
            CardAction(
                type=ActionTypes.im_back,
                title="👱🏻‍♂️ Чоловік",
                value="0",
            ),
            CardAction(
                type=ActionTypes.im_back,
                title="👩🏼‍🦱 Жінка",
                value="1",
            ),
        ],
    )
    return CardFactory.hero_card(card)


def looking_gender_hero_card() -> Attachment:
    card = HeroCard(
        title=f"{BOT_MESSAGES['looking_gender']}",
        images=[
            CardImage(
                url=f"https://{configuration.AZURE_STORAGE_HOST}.blob.core.windows.net/media/1_gender.jpg",
            )
        ],
        buttons=[
            CardAction(
                type=ActionTypes.im_back,
                title="👱🏻‍♂️ Чоловіків",
                value="0",
            ),
            CardAction(
                type=ActionTypes.im_back,
                title="👩🏼‍🦱 Жінок",
                value="1",
            ),
            CardAction(
                type=ActionTypes.im_back,
                title="👱🏻‍♂️ 👩🏼‍🦱 Чоловіків та Жінок",
                value="2",
            ),
            CardAction(
                type=ActionTypes.im_back,
                title="👫 Пару МЖ",
                value="3",
            ),
            CardAction(
                type=ActionTypes.im_back,
                title="👬 Пару ММ",
                value="4",
            ),
            CardAction(
                type=ActionTypes.im_back,
                title="👭 Пару ЖЖ",
                value="5",
            ),
        ],
    )
    return CardFactory.hero_card(card)


def age_hero_card() -> Attachment:
    card = HeroCard(
        title=f"{BOT_MESSAGES['age']}",
        images=[
            CardImage(
                url=f"https://{configuration.AZURE_STORAGE_HOST}.blob.core.windows.net/media/2_age.jpg",
            )
        ],
    )
    return CardFactory.hero_card(card)


def prefer_age_hero_card() -> Attachment:
    card = HeroCard(
        title=f"{BOT_MESSAGES['prefer_age']}",
        images=[
            CardImage(
                url=f"https://{configuration.AZURE_STORAGE_HOST}.blob.core.windows.net/media/3_prefer_age.jpg",
            )
        ],
    )
    return CardFactory.hero_card(card)


def looking_for_hero_card() -> Attachment:
    card = HeroCard(
        title=f"{BOT_MESSAGES['looking_for']}",
        images=[
            CardImage(
                url=f"https://{configuration.AZURE_STORAGE_HOST}.blob.core.windows.net/media/4_looking_for_a.jpg",
            )
        ],
        buttons=[
            CardAction(
                type=ActionTypes.im_back,
                title="🥰 Відносини, сім'я",
                value="0",
            ),
            CardAction(
                type=ActionTypes.im_back,
                title="😏 Секс без зобов'язань",
                value="1",
            ),
            CardAction(
                type=ActionTypes.im_back,
                title="🤗 Спілкування, пошук друзів",
                value="2",
            ),
            CardAction(
                type=ActionTypes.im_back,
                title="😉 Усе по трохи",
                value="3",
            )
        ],
    )
    return CardFactory.hero_card(card)


def upload_photo_hero_card() -> Attachment:
    card = HeroCard(
        title=f"{BOT_MESSAGES['upload_photo']}",
        images=[
            CardImage(
                url=f"https://{configuration.AZURE_STORAGE_HOST}.blob.core.windows.net/media/6_upload.png",
            )
        ]
    )
    return CardFactory.hero_card(card)


def main_menu_hero_card() -> Attachment:
    card = HeroCard(
        title=f"{BOT_MESSAGES['main_menu']}",
        buttons=[
            CardAction(
                type=ActionTypes.im_back,
                title="📂 Профіль",
                value="📂 Профіль",
            ),
            CardAction(
                type=ActionTypes.im_back,
                title="📸 Мої фото",
                value="📸 Мої фото",
            ),
            CardAction(
                type=ActionTypes.im_back,
                title="💌 Мої оголошення",
                value="💌 Мої оголошення",
            ),
            CardAction(
                type=ActionTypes.im_back,
                title="⚙️ Налаштування",
                value="⚙️ Налаштування",
            ),
        ],
    )
    return CardFactory.hero_card(card)
