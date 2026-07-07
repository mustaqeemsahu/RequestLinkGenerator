import random
import string

from database import channels_db


class ShortCodeGenerator:

    @staticmethod
    def _clean(text: str) -> str:
        if not text:
            return "CH"

        text = "".join(
            c for c in text
            if c.isalnum()
        ).upper()

        return text

    @classmethod
    def _prefix(cls, username=None, title=None):

        if username:
            username = username.replace("@", "")
            username = cls._clean(username)
            return username[:4]

        title = cls._clean(title)

        return title[:4]

    @staticmethod
    def _suffix(length=3):

        return "".join(
            random.choices(
                string.ascii_uppercase + string.digits,
                k=length,
            )
        )

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

            code = f"{prefix}{cls._suffix()}"

            exists = await channels_db.get_by_short_code(
                code
            )

            if not exists:
                return code


shortcode = ShortCodeGenerator()
