#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from typing import Optional

import pyrogram
from pyrogram import enums, raw, types


class AnswerGuestQuery:
    async def answer_guest_query(
        self: "pyrogram.Client", guest_query_id: str, result: "types.InlineQueryResult"
    ):
        """Use this method to reply to a received guest message.

        .. include:: /_includes/usable-by/bots.rst

        Parameters:
            guest_query_id (``str``):
                Unique identifier for the answered query.

            result (:obj:`~pyrogram.types.InlineQueryResult`):
                A result for the guest query.

        Returns:
            :obj:`~pyrogram.types.SentGuestMessage`: On success, a :obj:`~pyrogram.types.SentGuestMessage` object is returned.

        Example:
            .. code-block:: python

                from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent

                await app.answer_guest_query(
                    guest_query_id,
                    result=InlineQueryResultArticle(
                        "Title",
                        InputTextMessageContent("Message content")
                    ),
                )
        """
        r = await self.invoke(
            raw.functions.messages.SetBotGuestChatResult(
                query_id=int(guest_query_id),
                result=await result.write(self),
            )
        )

        return await types.SentGuestMessage._parse(r)

    async def answer_guest_text(
        self: "pyrogram.Client",
        guest_query_id: str,
        text: str,
        parse_mode: Optional["enums.ParseMode"] = None,
    ):
        """Convenience method to reply to a guest message with simple text.

        Wraps the text in an :obj:`~pyrogram.types.InlineQueryResultArticle` with
        :obj:`~pyrogram.types.InputTextMessageContent` and calls :meth:`~pyrogram.Client.answer_guest_query`.

        Parameters:
            guest_query_id (``str``):
                Unique identifier for the answered query.

            text (``str``):
                Text of the message to be sent.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

        Returns:
            :obj:`~pyrogram.types.SentGuestMessage`: On success, a :obj:`~pyrogram.types.SentGuestMessage` object is returned.
        """
        return await self.answer_guest_query(
            guest_query_id,
            types.InlineQueryResultArticle(
                title="Response",
                input_message_content=types.InputTextMessageContent(
                    message_text=text,
                    parse_mode=parse_mode,
                ),
            ),
        )
