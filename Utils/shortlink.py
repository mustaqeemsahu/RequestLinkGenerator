import random
import string

from database import channels_db


class ShortLink:

    @staticmethod
    def _clean(text: str) -> str:
        """
        Keep only letters and numbers.
        """

        if not text:
            return "CH"

        text = "".join(
            c for c in text
            if c.isalnum()
        )

        return text.upper()

    @staticmethod
    def _prefix(username=None, title=None):

        if username:

            username = username.replace("@", "")

            username = ShortLink._clean(username)

            return username[:3]

        title = ShortLink._clean(title)

        return title[:3]

    @staticmethod
    def _random():

        letters = random.choice(
            string.ascii_uppercase
        )

        number = random.choice(
            string.digits
        )

        return f"{number}{letters}"

    @classmethod
    async def generate(
        cls,
        username=None,
        title=None,
    ):

        prefix = cls._prefix(
            username=username,
            title=title,
        )

        while True:

            code = prefix + cls._random()

            exists = await channels_db.get_channel_by_code(
                code
            )

            if not exists:
                return code


shortlink = ShortLink()
