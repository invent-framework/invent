import pyodide_http
import requests

pyodide_http.patch_all()


def ask_the_overlords(context="", ai_launcher_port=8765):
    """Ask the overlords!"""

    url = f"http://127.0.0.1:{ai_launcher_port}/v1/chat/completions"

    content = f"""
    Given the context of the following documents:
    
    {context}
        
    Please summarize in no more than 30 words in the style of an 18th century
    pirate.

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

