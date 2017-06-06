import aiohttp
import json

LANGS = {
    'cpp': 'g++ -std=c++1z -Wall -Wextra -pthread main.cpp && ./a.out',
    'py': 'python3 main.cpp'
}


async def post(cmd: str, src: str):
    data = json.dumps({'cmd': cmd, 'src': src})
    async with aiohttp.ClientSession() as cs:
        async with cs.post('http://coliru.stacked-crooked.com/compile', data=data) as r:
            print(await r.text())
            return await r.json()


async def evaluate(lang: str, src: str):
    """
    Evaluate Code using the Coliru API.

    `lang` is the syntax highlighter used for the codeblock, and `src` the contents.
    """
    lang_cmd = LANGS.get(lang, None)
    if lang_cmd is None:
        return None
    return await post(lang_cmd, src)