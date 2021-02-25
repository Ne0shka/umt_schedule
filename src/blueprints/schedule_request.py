from loguru import logger
from vkbottle.bot import Blueprint, Message
from vkbottle.exception_factory import VKAPIError

from src.services.schedule_handler import get_schedule
from src.services.schedule_keyboard import generate_keyboard

bp = Blueprint(name="Расписание")
message_del_api_err = 924


@bp.on.message(payload_contains={"command": "start"})
@bp.on.message(text=["Расписание", "расписание", "!расписание", "/расписание"])
async def schedule_command_handler(message: Message):
    await message.answer(
        "{0} {1}".format(
            "&#128218; Выберите ваш курс с помощью клавиатуры",
            "или напишите номер курса вручную",
        ),
        keyboard=generate_keyboard(),
    )


@bp.on.message(text=["1", "2", "3", "4"])
@bp.on.message(text=["1 курс", "2 курс", "3 курс", "4 курс"])
@bp.on.message(payload_contains={"command": "schedule_request"})
async def schedule_keyboard_handler(message: Message):
    message_id = await message.answer("&#8987; Загрузка расписания...")
    payload = message.get_payload_json()
    if payload:
        course = payload.get("course")
    else:
        course = message.text
    if course in {"1", "2", "3", "4"}:
        course = "{0} курс".format(course)
    logger.info("[{0}] Запрос расписания {1}а.".format(message.id, course))
    logger.info("[{0}] User: id{1} - ChatID: {2}".format(
        message.id,
        message.from_id,
        message.peer_id,
    ))
    text, images_links = await get_schedule(message.peer_id, bp.api, course)
    await message.answer(
        "&#128218; {0}".format(text),
        attachment=",".join(images_links),
    )
    logger.info("[{0}] Расписание отправлено!".format(message.id))
    if message_id:
        try:
            await bp.api.messages.delete(
                message_ids=message_id,
                delete_for_all=1,
            )
        except VKAPIError(message_del_api_err):
            logger.warning("Ошибка удаления сообщения!")
            logger.warning(message)
