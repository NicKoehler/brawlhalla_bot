import en

SUPPORTED_LANGUAGES = {
    "it": "it_IT",
    "en": "en_US",
    "es": "es_ES",
}


def parse_strings(text: str):
    """
    Parse all the words inside curly brackets in the given text without dupplicates.
    """
    seen = set()
    words = []
    start = -1
    while True:
        start = text.find("{", start + 1)
        if start == -1:
            break
        end = text.find("}", start + 1)
        if end == -1:
            break
        word = text[start + 1 : end]
        if word not in seen:
            seen.add(word)
            words.append(word)
    return words


print(
    """# THIS CODE IS AUTOGENERATED BY src/locales/generate_locales.py
# DO NOT EDIT THIS FILE DIRECTLY.
"""
)

print("from typing import Iterator")
print(f"from locales import {', '.join(SUPPORTED_LANGUAGES)}\n\n")

print(f"SUPPORTED_LANGUAGES = {SUPPORTED_LANGUAGES}\n\n")

print(
    """class Translator:
    def __init__(self, locale, locale_str) -> None:
        self.locale = locale
        self.locale_str = locale_str
"""
)

strings = [item for item in dir(en) if not item.startswith("__")]
for string in strings:
    args = parse_strings(en.__dict__[string])
    docstring = getattr(en, string).replace("\n", "\n        ")
    if not args:
        print(f"    def {string.lower()}(self) -> str:")
        print(f'        """\n        {docstring}\n        """')
        print(f"        return self.locale.{string}\n")
    else:
        args_str = ",\n".join(f"        {arg}" for arg in args)
        args_kwargs = ",\n".join(f"            {arg}={arg}" for arg in args)
        print(f"    def {string.lower()}(")
        print("        self,")
        print(f"{args_str}")
        print("    ) -> str:")
        print(f'        """\n        {docstring}\n        """')
        print(
            f"        return self.locale.{string}.format(\n{args_kwargs}\n        )\n"
        )

print(
    "\nclass Localization:\n"
    "    def __init__(self) -> None:\n"
    "        self._strings = {\n"
    + "\n".join(
        f'            "{k}": Translator({k}, "{v}"),'
        for k, v in SUPPORTED_LANGUAGES.items()
    )
    + "\n        }\n"
)
print(
    "    def get_translator(self, lang: str) -> Translator:\n"
    "        if lang not in self._strings:\n"
    '            return self._strings["en"]\n'
    "        return self._strings[lang]\n\n"
    "    def __iter__(self) -> Iterator[Translator]:\n"
    "        return iter(self._strings.values())"
)
