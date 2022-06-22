from botbuilder.core import ConversationState, MessageFactory, CardFactory, UserState
from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
    PromptOptions,
    TextPrompt, ChoicePrompt
)
from botbuilder.schema import HeroCard, CardAction, ActionTypes, InputHints
from ms_bot.bots_models.models import CustomerProfile

from setup.logger import CustomLogger


logger = CustomLogger.get_logger('bot')


class UtilsDialog(ComponentDialog):
    def __init__(
            self,
            conversation_state: ConversationState,
            user_state: UserState,
            dialog_id: str = None
    ):
        super(UtilsDialog, self).__init__(dialog_id or UtilsDialog.__name__)

        self.user_state = user_state
        self.user_profile_accessor = self.user_state.create_property("CustomerProfile")

        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(
            WaterfallDialog(
                "UtilsDialog",
                [
                    self.bot_input,
                    self.integrity_check,
                    self.customer_prompt,
                    self.customer_search
                ]
            )
        )

        self.initial_dialog_id = "UtilsDialog"
        self.conversation_state = conversation_state

    async def bot_input(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        logger.debug('bot_input %s', UtilsDialog.__name__)
        user_data: CustomerProfile = await self.user_profile_accessor.get(step_context.context, CustomerProfile)
        activity_ids = []
        prompt_text = MessageFactory.list([])
        prompt_text.attachments.append(self._create_hero_card())

        resource_response = await step_context.context.send_activity(prompt_text)
        activity_ids.append(resource_response.id)

        user_data.activity_ids = activity_ids

        prompt_message = MessageFactory.text('⏳', InputHints.expecting_input)
        return await step_context.prompt(TextPrompt.__name__, PromptOptions(prompt=prompt_message))

    async def integrity_check(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        logger.debug('integrity_check %s', UtilsDialog.__name__)
        user_data: CustomerProfile = await self.user_profile_accessor.get(step_context.context, CustomerProfile)

        found_choice = step_context.result

        for activity_id in user_data.activity_ids:
            await step_context.context.delete_activity(activity_id)

        if found_choice == 'Кількість у бд':
            result = await _count_all()
            await step_context.context.send_activity(result)
            return await step_context.replace_dialog(UtilsDialog.__name__)

        elif found_choice == 'Кількість у боті':
            result = await _count_reg()
            await step_context.context.send_activity(result)
            return await step_context.replace_dialog(UtilsDialog.__name__)

        elif found_choice == 'Кількість надісланих гео':
            result = await _count_broadcast_geo()
            await step_context.context.send_activity(result)
            return await step_context.replace_dialog(UtilsDialog.__name__)

        elif found_choice == 'Кількість відповідей на гео':
            result = await _count_replies_received()
            await step_context.context.send_activity(result)
            return await step_context.replace_dialog(UtilsDialog.__name__)

        elif found_choice == 'Ті, хто видалили бота':
            result = await _search_banned()
            await step_context.context.send_activity(result)
            return await step_context.replace_dialog(UtilsDialog.__name__)

        elif found_choice == 'Пошук співробітника':
            return await step_context.next([])

        elif found_choice == '❤️ Response time':
            result = ping_message()
            await step_context.context.send_activity(result)
            return await step_context.replace_dialog(UtilsDialog.__name__)

        elif found_choice == '🗑 Видалити свій запис':
            await _self_delete(self.conversation_state, step_context)
            await step_context.context.send_activity('Видалено')
            return await step_context.replace_dialog(UtilsDialog.__name__)

        elif found_choice == '🔙 Вихід':
            await step_context.cancel_all_dialogs(True)

        else:
            return await step_context.cancel_all_dialogs(True)

        return await step_context.cancel_all_dialogs(True)

    async def customer_prompt(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        logger.debug('customer_prompt %s', UtilsDialog.__name__)

        prompt_options = PromptOptions(
            prompt=MessageFactory.text('🔍 Введіть табельний номер користувача (8 цифр)')
        )
        return await step_context.prompt(TextPrompt.__name__, prompt_options)

    async def customer_search(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        logger.debug('customer_search %s', UtilsDialog.__name__)

        found_choice: str = step_context.result
        if len(found_choice) == 8:
            result = await _search(found_choice)
            await step_context.context.send_activity(result)
        return await step_context.replace_dialog(UtilsDialog.__name__)

    def _create_hero_card(self):
        card = HeroCard(
            text='🤠',
            buttons=[
                CardAction(
                    type=ActionTypes.im_back,
                    title='Кількість у бд',
                    value='Кількість у бд',
                ),
                CardAction(
                    type=ActionTypes.im_back,
                    title='Кількість у боті',
                    value='Кількість у боті',
                ),
                CardAction(
                    type=ActionTypes.im_back,
                    title='Кількість надісланих гео',
                    value='Кількість надісланих гео',
                ),
                CardAction(
                    type=ActionTypes.im_back,
                    title='Кількість відповідей на гео',
                    value='Кількість відповідей на гео',
                ),
                CardAction(
                    type=ActionTypes.im_back,
                    title='Ті, хто видалили бота',
                    value='Ті, хто видалили бота',
                ),
                CardAction(
                    type=ActionTypes.im_back,
                    title='Пошук співробітника',
                    value='Пошук співробітника',
                ),
                CardAction(
                    type=ActionTypes.im_back,
                    title='🗑 Видалити свій запис',
                    value='🗑 Видалити свій запис',
                ),
                CardAction(
                    type=ActionTypes.im_back,
                    title='❤️ Response time',
                    value='❤️ Response time',
                ),
                CardAction(
                    type=ActionTypes.im_back,
                    title='🔙 Вихід',
                    value='🔙 Вихід',
                )
            ],
        )
        return CardFactory.hero_card(card)


async def _count_all() -> str:
    from . import Customer
    try:
        customer = Customer.objects.filter(employeeId__isnull=False).count()
    except Exception as e:
        logger.exception('_count_all error')
        customer = 'db error' + str(e)
    return 'Общее количество всех пользователей: ' + str(customer)


async def _count_reg() -> str:
    from . import Customer
    try:
        customer = Customer.objects.filter(member_id__isnull=False).count()
    except Exception as e:
        logger.exception('_count_reg error')
        customer = 'db error' + str(e)
    return 'Общее количество пользователей пришедших через бота: ' + str(customer)


async def _count_broadcast_geo() -> str:
    from . import Customer
    try:
        customer = Customer.objects.filter(is_current_state_message_send=True).count()
    except Exception as e:
        logger.exception('_count_broadcast_geo error')
        customer = 'db error' + str(e)
    return 'Общее количество пользователей получивших запрос геолокации: ' + str(customer)


async def _count_replies_received() -> str:
    from . import Customer
    try:
        customer = Customer.objects.filter(is_current_state_reply_received=True).count()
    except Exception as e:
        logger.exception('_count_replies_received error')
        customer = 'db error' + str(e)
    return 'Общее количество пользователей ответивших на запрос геолокации: ' + str(customer)


async def _search(employeeId: str):
    from v.models import Customer
    try:
        customer = Customer.objects.get(employeeId=employeeId)
    except Exception:
        customer = None

    if customer:
        message = f'Id: {customer.id} \n  \n' \
                  f'employeeId: {customer.employeeId} \n  \n' \
                  f'displayName: {customer.displayName} \n  \n' \
                  f'mobilePhone: {customer.mobilePhone} \n  \n' \
                  f'userPrincipalName: {customer.userPrincipalName} \n  \n' \
                  f'mail: {customer.mail} \n  \n' \
                  f'department: {customer.department} \n  \n' \
                  f'company: {customer.company} \n  \n' \
                  f'company_id: {customer.company_id} \n  \n' \
                  f'country: {customer.country} \n  \n' \
                  f'country_id: {customer.country_id} \n  \n' \
                  f'region: {customer.region} \n  \n' \
                  f'region_id: {customer.region_id} \n  \n' \
                  f'city: {customer.city} \n  \n' \
                  f'city_id: {customer.city_id} \n  \n' \
                  f'operator_displayName: {customer.operator_displayName} \n  \n' \
                  f'member_id: {customer.member_id} \n  \n' \
                  f'is_current_state_message_send: {customer.is_current_state_message_send} \n  \n' \
                  f'is_current_state_reply_received: {customer.is_current_state_reply_received} \n  \n' \
                  f'last_reply_received_at: {customer.last_reply_received_at} \n  \n' \
                  f'created_at: {customer.created_at} \n  \n' \
                  f'updated_at: {customer.updated_at}'
    else:
        message = 'Customer not found'

    return message


async def _search_banned():
    from . import Customer
    try:
        customers = Customer.objects.filter(operator_displayName='bot was banned')
    except Exception:
        logger.exception('DB error while getting filter(operator_displayName=bot was banned)')
        customers = None
    count = customers.count()

    if customers:
        return f'Количество сотрудников, забанивших бота: {count}'
    else:
        return 'Сотрудников удаливших бота, не обнаружено'


async def _self_delete(
        conversation_state,
        step_context: WaterfallStepContext
) -> bool:
    from . import Customer
    member_id = step_context.context.activity.from_property.id
    result = None
    select_result = None
    conversation_state_result = None

    try:
        await conversation_state.delete(step_context.context)
        conversation_state_result = True
    except Exception:
        logger.exception('conversation_state.delete %s error', member_id)

    try:
        customer = Customer.objects.get(member_id=member_id)
    except Exception:
        logger.exception('Customer.objects.get %s error', member_id)
        customer = None
    try:
        customer.delete()
    except Exception:
        logger.exception('customer.delete() %s error', member_id)

    try:
        customer = Customer.objects.get(member_id=member_id)
    except Exception:
        logger.warning('SELECT AFTER Customer.objects.get %s object not found', member_id)
        select_result = True

    if select_result and conversation_state_result:
        result = True
    else:
        result = False

    if result:
        logger.warning('<<< self >>> %s', result)
        logger.warning('completed for %s', member_id)
    return bool(result)


def ping_message():
    result = get_ping_statistics()

    try:
        now_d = round(result["now"][0], ndigits=2)
    except Exception:
        now_d = 1.00

    try:
        a10_d = round(result["a10"], ndigits=2)
    except Exception:
        a10_d = 10.00

    try:
        a60_d = round(result["a60"], ndigits=2)
    except Exception:
        a60_d = 10.00

    if a10_d <= now_d <= a60_d:
        text = '🟡 Помірне навантаження'
    elif a10_d <= now_d >= a60_d:
        text = '🔴 Високе навантаження'
    elif a10_d >= now_d <= a60_d:
        text = '🟢 Навантаження відсутнє'

    else:
        text = '⚠️ Навантаження не може бути розраховане (Not enough data)'

    now = str(now_d).replace('.', ',')
    a10 = str(a10_d).replace('.', ',')
    a60 = str(a60_d).replace('.', ',')

    message = f'Час відповіді вказано у мс (1 сек = 1000 мс) \n  \n' \
              f'Поточний час відповіді: {now} мс \n  \n' \
              f'Середній час відповіді за 10 хв: {a10} мс \n  \n' \
              f'Середній час відповіді за годину: {a60} мс \n  \n' \
              f'Статус: {text} \n  \n'

    return message
