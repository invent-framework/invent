import json
from pyscript import fetch


async def summarize(context=""):
    """Ask the overlords!"""

    user_message = f"""
    Given the context of the following documents:

    {context}

    Please summarize them in no more than 30 words in the style of a very articulate
    business analyst.

    """

    ai_client = AIClient("http://127.0.0.1:8765/v1")

    return await ai_client.completions(user_messages=[user_message])


class AIClient:
    def __init__(self, url):
        """An OpenAI compatible AI client."""

        self.url = url

    async def completions(self, user_messages=None, system_messages=None):
        """OpenAI completions endpoint."""

        messages = []
        if system_messages:
            messages.extend([
                {"role": "system", "content": system_message}

                for system_message in system_messages
            ])

        if user_messages:
            messages.extend([
                {"role": "user", "content": user_message}

                for user_message in user_messages
            ])

        result = await fetch(
            f"{self.url}/chat/completions",
            method="POST",
            headers={
                "Content-Type": "application/json"
            },
            body=json.dumps({
                "model": "gpt-3.5-turbo",
                "messages": messages,
                "temperature": 0.7
            }),
        ).json()

        return result["choices"][0]["message"]["content"]
