import asyncio
import logging

import pyrogram
from pyrogram.handlers import GuestMessageHandler

log = logging.getLogger(__name__)


class GuestPoller:
    def __init__(self, client: "pyrogram.Client"):
        self.client = client
        self.offset = 0
        self.running = False
        self.task = None

    async def start(self):
        if self.running:
            return

        self.running = True
        self.task = asyncio.create_task(self._run())

    async def stop(self):
        self.running = False

        if self.task:
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass
            self.task = None

    async def _run(self):
        log.info("[guest] Bot API guest poller started")

        while self.running:
            try:
                updates = await self.client.bot_api.request(
                    "getUpdates",
                    {
                        "offset": self.offset,
                        "timeout": 30,
                        "allowed_updates": ["guest_message"],
                    },
                )

                for update in updates:
                    self.offset = max(self.offset, update["update_id"] + 1)

                    data = update.get("guest_message")
                    if not data:
                        continue

                    await self._dispatch_guest_message(data)

            except asyncio.CancelledError:
                raise
            except Exception:
                log.exception("[guest] guest poller error")
                await asyncio.sleep(3)

    async def _dispatch_guest_message(self, data: dict):
        message = await pyrogram.types.Message._parse(
            self.client,
            None,
            {},
            {},
            guest_query_id=data.get("guest_query_id"),
        )
        message.guest_query_id = data.get("guest_query_id")
        message.text = data.get("text")
        message.caption = data.get("caption")
        message.photo = data.get("photo")
        message.document = data.get("document")
        message.date = data.get("date")
        message.raw = data

        for group in self.client.dispatcher.groups.values():
            for handler in group:
                if not isinstance(handler, GuestMessageHandler):
                    continue

                try:
                    if await handler.check(self.client, message):
                        await handler.callback(self.client, message)
                        return
                except Exception:
                    log.exception("[guest] handler error")
