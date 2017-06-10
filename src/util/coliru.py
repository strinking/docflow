import aiohttp
import json

LANGS = {
    'c': 'mv main.cpp main.c && gcc -std=c11 -Wall -Wextra -pthread main.c && ./a.out',
    'cpp': 'g++ -std=c++1z -Wall -Wextra -pthread main.cpp && ./a.out',
    'sh': 'sh main.cpp',
    'py': 'python3 main.cpp',
    'ruby': 'ruby main.cpp'
}


async def post(cmd: str, src: str):
    data = json.dumps({'cmd': cmd, 'src': src})
    async with aiohttp.ClientSession() as cs:
        async with cs.post('http://coliru.stacked-crooked.com/compile', data=data) as r:
            return await r.text()


async def evaluate(lang: str, src: str):
    """
    Evaluate Code using the Coliru API.

    `lang` is the syntax highlighter used for the codeblock, and `src` the contents.
    """
    lang_cmd = LANGS.get(lang, None)
    if lang_cmd is None:
        return None
    return await post(lang_cmd, src)
