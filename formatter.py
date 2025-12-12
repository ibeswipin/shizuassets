# ░██████╗░██████╗░██╗░░░░░███╗░░░███╗███████╗██████╗░██████╗░
# ██╔════╝██╔═══██╗██║░░░░░████╗░████║██╔════╝██╔══██╗██╔══██╗
# ╚█████╗░██║██╗██║██║░░░░░██╔████╔██║█████╗░░██████╔╝██████╔╝
# ░╚═══██╗╚██████╔╝██║░░░░░██║╚██╔╝██║██╔══╝░░██╔══██╗██╔══██╗
# ██████╔╝░╚═██╔═╝░███████╗██║░╚═╝░██║███████╗██║░░██║██║░░██║
# ╚═════╝░░░░╚═╝░░░╚══════╝╚═╝░░░░░╚═╝╚══════╝╚═╝░░╚═╝╚═╝░░╚═╝
# ---------------------------------------------------------------------------------------------
# Name: AutoFormatter
# Description: Automatically formats the text of your messages | Автоматически форматирует текст ваших сообщений | Check The Config | Загляните в конфиг
# Author: sqlmerr
# Commands:
# .textformat
# ---------------------------------------------------------------------------------------------

# meta icon: https://github.com/sqlmerr/hikka_mods/blob/main/assets/icons/autoformatter.png?raw=true
# meta banner: https://github.com/sqlmerr/sqlmerr/blob/main/assets/hikka_mods/sqlmerrmodules_autoformatter.png?raw=true
# meta developer: @sqlmerr_m
# only hikka


import pyrogram
from pyrogram.types import Message

import logging


from shizu import loader, utils


logger = logging.getLogger(__name__)


@loader.module(name="AutoFormatter", author="sqlmerr")
class AutoFormatter(loader.Module):
    """Automatically formats the text of your messages | Check The Config"""

    strings = {
        "name": "AutoFormatter",
        "status": "Module enabled or disabled",
        "format": "Text format. Where {} is the original message text",
        "type": "Formatting Type",
        "exceptions": "This is exceptions, this text is not formated",
        "disabled": "Module is now disabled",
        "enabled": "Module is now enabled",
    }
    strings_ru = {
        "status": "Включен или выключен модуль",
        "format": "Формат текста. Где {} это исходный текст сообщения",
        "type": "Тип форматирования",
        "exceptions": "Это исключения, этот текст не будет форматироваться",
        "disabled": "Модуль сейчас выключен",
        "enabled": "Модуль сейчас включен",
    }

    def __init__(self):
        self.m__telethon = False  # Explicitly mark as Pyrogram module
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "status",
                False,
                lambda: self.strings("status"),
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "format",
                "<b>{}</b>",
                lambda: self.strings("format"),
                validator=loader.validators.String(),
            ),
            loader.ConfigValue(
                "exceptions",
                [],
                lambda: self.strings("exceptions"),
                validator=loader.validators.Series(loader.validators.String()),
            ),
        )

    async def watcher(self, app, message: Message):
        if not self.config.get("status", False):
            return
        
        if not message.from_user:
            return

        tg_id = getattr(self, "tg_id", None)
        if not tg_id or message.from_user.id != tg_id:
            return

        if message.outgoing:
            return

        print("format")

        exc = self.config["exceptions"]
        f = self.config["format"]
        text = message.text
        
        if not text:
            return
        
        if exc and exc != [None]:
            for e in exc:
                if str(e).strip() == text.strip():
                    return
        else:
            if f in text:
                return

        await utils.answer(message, f"{f.format(text)}")

    @loader.command(ru_doc="Включить/выключить модуль")
    async def textformat(self, app: pyrogram.Client, message: Message):
        """Turn on/off The Module"""
        self.config["status"] = not self.config["status"]
        enable = self.strings("enabled")
        disable = self.strings("disabled")
        status = (
            f"<emoji document_id=5447644880824181073>⚠️</emoji> {enable}"
            if self.config["status"]
            else f"<emoji document_id=5447644880824181073>⚠️</emoji> {disable}"
        )

        await utils.answer(message, "<b>{}</b>".format(status))
