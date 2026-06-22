import pyrogram


class GetBotApiMe:
    async def get_bot_api_me(
        self: "pyrogram.Client",
    ):
        """Get the bot's information via the Bot API.

        This method calls the Bot API ``getMe`` method to retrieve the bot's information,
        including the ``supports_guest_queries`` field which is not available via MTProto.

        Requires a bot token with Bot API access enabled.

        Returns:
            ``dict``: A dictionary containing the bot's information as returned by the Bot API.

        Raises:
            RuntimeError: In case Bot API support is not available.
        """
        if not getattr(self, "bot_api", None):
            raise RuntimeError("get_bot_api_me requires Bot API support and a bot token")

        return await self.bot_api.request("getMe")
