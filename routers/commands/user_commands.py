import asyncio
import csv
import io

import aiohttp
from aiogram import Router, types
from aiogram.enums import ParseMode, ChatAction
from aiogram.filters import Command
from aiogram.utils import markdown
from aiogram.utils.chat_action import ChatActionSender

router = Router(name=__name__)


@router.message(Command("code", prefix="/!"))  # code
async def handle_command_code(message: types.Message):
    text = markdown.text(
        "Here's Python code:",
        "",
        markdown.markdown_decoration.pre_language(
            markdown.text(
                "print('Hello world!')",
                "",
                "def foo():\n  return 'bar'",
                sep='\n'
            ),
            language='python',
        ),
        "And here's some JS:",
        "",
        markdown.markdown_decoration.pre_language(
            markdown.text(
                "console.log('Hello world!')",
                "\n",
                "function foo() {\n  return 'bar'\n}",
                sep="\n",
            ),
            language="javascript",
        ),
        sep="\n",
    )
    await message.answer(text=text, parse_mode=ParseMode.MARKDOWN_V2)


@router.message(Command("pic"))
async def handle_command_pic(message: types.Message):
    url = "https://avatars.dzeninfra.ru/get-zen_doc/8074369/pub_64735556da735e595528014f_6473564c85e81a0f78973c68/scale_2400"
    await message.reply_photo(
        photo=url,
        caption="Gojo Satoru"
    )


@router.message(Command("file"))
async def handle_command_file(message: types.Message):
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.UPLOAD_DOCUMENT,
    )
    file_path = "C:\PythonProjects\TestGame\icon.png"
    await message.reply_document(
        document=types.FSInputFile(
            path=file_path,
            filename="Python.png"
        ),
    )


@router.message(Command("text"))
async def send_txt_file(message: types.Message):
    file = io.StringIO()
    file.write("Hello, world!\n")
    file.write("This is a text file.\n")
    await message.reply_document(
        document=types.BufferedInputFile(
            file=file.getvalue().encode("utf-8"),
            filename="text.txt"
        ),
    )


@router.message(Command("csv"))
async def send_csv_file(message: types.Message):
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.TYPING,
    )
    file = io.StringIO()
    csv_writer = csv.writer(file)
    csv_writer.writerow([
        ["Name", "Age", "City"],
        ["Jane Doe", "34", "London"],
        ["John Smith", "28", "New York"],
        ["Petr Ivanov", "15", "Moscow"],
    ])
    await message.reply_document(
        document=types.BufferedInputFile(
            file=file.getvalue().encode("utf-8"),
            filename="people.csv"
        ),
    )


async def send_big_file(message: types.Message):
    await asyncio.sleep(4)
    file = io.BytesIO()
    url = "https://i.pinimg.com/564x/6e/0c/34/6e0c34b96426d43bd575483c3d33594f.jpg"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            result_bytes = await response.read()

    file.write(result_bytes)
    await message.reply_document(
        document=types.BufferedInputFile(
            file=result_bytes,
            filename="Killua.jpg"
        ),
    )


@router.message(Command("pic_file"))
async def send_pic_file_buffered(message: types.Message):
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.UPLOAD_DOCUMENT,
    )
    async with ChatActionSender.upload_document(
            bot=message.bot,
            chat_id=message.chat.id
    ):
        await send_big_file(message)
