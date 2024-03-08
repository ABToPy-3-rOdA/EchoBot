from aiogram import Router, F, types

router = Router(name=__name__)


@router.message(F.photo, ~F.caption)
async def handle_photo_without_caption(message: types.Message):
    caption = "I can't see, sorry. Could you describe it, please?"
    await message.reply_photo(
        photo=message.photo[-1].file_id,
        caption=caption,
    )


@router.message(F.photo, F.caption.contains("please"))
async def handle_photo_with_please_caption(message: types.Message):
    await message.reply("Don't beg me. I can't see, sorry.")


any_media_filter = F.photo | F.video | F.document


@router.message(any_media_filter, ~F.caption)
async def handle_any_media_without_caption(message: types.Message):
    if message.document:
        await message.reply_document(
            document=message.document.file_id,
        )
    elif message.video:
        await message.reply_video(
            video=message.video.file_id,
        )
    else:
        await message.reply("I can't see.")


@router.message(any_media_filter, F.caption)
async def handle_any_media_with_caption(message: types.Message):
    await message.reply(f"Something is on media. Your text: {message.caption!r}")
