from aiogram.types import Message, CallbackQuery
from app import hdvb, views_counter
import templates, config


async def show_watch_btn(c: CallbackQuery):
    kp_id: int = int(c.data.split('|')[1])
    film = await hdvb.find_by_kp_id(kp_id)

    if film.kinopoisk_id:
        views_counter.increment_day_views()

        await c.bot.edit_message_reply_markup(
            chat_id=c.from_user.id,
            message_id=c.message.message_id,
            reply_markup=templates.btn_search_film(
                film.iframe_url,
                film.kinopoisk_id,
                more_btn=False
            )
        )
        await hdvb.up_film_rating(film)
    else:
        c.answer('Ошибка')


async def film_info(c: CallbackQuery):
    kp_id = int(c.data.split('|')[1])
    film_info = await hdvb.get_film_info(kp_id)

    if not film_info.description:
        film_info.description = 'Отсутсвует'

    new_caption = c.message.caption \
        + f'\n\n⏳ Время: {film_info.length} (часы) \n\n🎥 Жанры: {", ".join(film_info.genres)} \n\n📙 Описание: {film_info.description}'

    await c.answer('Описание получено 👌')

    await c.bot.edit_message_caption(
        c.from_user.id,
        c.message.message_id,
        caption=new_caption,
        reply_markup=templates.btn_search_film('', kp_id, more_btn=False)
    )
