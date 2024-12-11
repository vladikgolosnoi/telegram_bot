import re


def escape_markdown(text):
    pattern = r'```(.*?)(```|$)'
    for match in re.finditer(pattern, text, flags=re.DOTALL):
        ending = match.group(2)

        if ending != '```':
            # Блок не закрыт, удаляем его
            start, end = match.span()
            text = text[:start] + text[end:]
            return escape_markdown(text)

    return text
