import pyodide_http
import requests

pyodide_http.patch_all()


def read_document(url):
    """Read a text-based document from the specified URL."""

    proxy_url = f"https://mchilvers.pyscriptapps.com/my/api-proxies/the-web"

    response = requests.get(proxy_url, headers={"-url": url})
    if response.status_code != 200:
        raise ValueError("Can't read that URL")

    return response.text()


def ask_the_overlords(prompt, use_ai_launcher=True, ai_launcher_port=8765):
    """Ask the overlords!"""

    if use_ai_launcher:
        url = f"http://127.0.0.1:{ai_launcher_port}/v1/chat/completions"

    else:
        url = "https://mchilvers.pyscriptapps.com/my/api-proxies/openai-completions"

    content = f"""
    Respond as an 18th century pirate.

    {prompt}
    """

    response = requests.post(
        url,
        headers={
            "Content-Type": "application/json"
        },
        json={
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": content}],
            "temperature": 0.7},
    )

    if response.status_code == 200:
        result = response.json()
        answer = result["choices"][0]["message"]["content"]

    else:
        answer = "Oops, computer says 'No!'"
        print(response.status_code)

    return answer

