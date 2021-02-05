import loguru
from vkbottle.bot import Blueprint, Message
from vkbottle.exception_factory import VKAPIError

from src.services.schedule_handler import get_schedule
from src.services.schedule_keyboard import generate_keyboard

bp = Blueprint(name="Расписание")
message_del_api_err = 924


@bp.on.message(text=["Расписание", "расписание", "!расписание", "/расписание"])
async def schedule_command_handler(message: Message):
    await message.answer(
        "&#128218; Выберите ваш курс с помощью клавиатуры",
        keyboard=generate_keyboard(),
    )


@bp.on.message(payload_contains={"command": "schedule_request"})
async def schedule_keyboard_handler(message: Message):
    message_id = await message.answer("&#8987; Загрузка расписания...")
    course = message.get_payload_json()["course"]
    text, images_links = await get_schedule(message.peer_id, bp.api, course)
    await message.answer(
        "&#128218; {}".format(text),
        attachment=",".join(images_links),
    )
    if message_id:
        try:
            await bp.api.messages.delete(
                message_ids=message_id,
                delete_for_all=1,
            )
        except VKAPIError(message_del_api_err):
            loguru.error("Ошибка удаления сообщения!")
            loguru.error(message)
