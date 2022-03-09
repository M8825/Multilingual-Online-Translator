import requests
from bs4 import BeautifulSoup

LANGS = ['Arabic', 'German', 'English', 'Spanish', 'French', 'Hebrew', 'Japanese',
         'Dutch', 'Polish', 'Portuguese', 'Romanian', 'Russian', 'Turkish']


def get_list(lst):
    return [i.text.strip() for i in lst]


def get_req(usr_lang, target_lang, word):
    url = f'https://context.reverso.net/translation/{usr_lang}-{target_lang}/{word}'
    headers = {'User-Agent': 'Mozilla/5.0'}

    return requests.get(url, headers=headers)


def writeto_file(word, req, lang):
    file = open(f'{word}.txt', 'a', encoding='utf-8')

    if req.status_code == 200:  # Got response
        soup = BeautifulSoup(req.content, 'html.parser')

        file.write(f'\n{lang} Translations:\n')
        example = soup.find('a', {'class': 'dict'})
        file.write(example.text.strip() + '\n')

        file.write(f'\n{lang} Examples:\n')
        base_examples = soup.find('div', {'class': 'src ltr'})
        trg_examples = soup.find('div', {'class': 'trg'})

        file.write(base_examples.text.strip() + '\n')
        file.write(trg_examples.text.strip() + '\n')

    file.close()


def get_inputs():
    usr_lang = LANGS[int(input('Type the number of your language:\n')) - 1].lower()
    target_lang = int(input("Type the number of a language you want to translate to or '0' to translate to all languages:\n"))
    word = input('Type the word you want to translate:\n')

    return usr_lang, target_lang, word


def main():
    print("Hello, you're welcome to the translator. Translator supports: ")
    for i, lang in enumerate(LANGS):
        print(f'{i + 1}. {lang}')

    usr_lang, target_lang, word = get_inputs()

    if target_lang == 0:  # Translate into all available languages
        for lang in LANGS:
            target_lang = lang.lower()

            if usr_lang == target_lang:
                continue

            req = get_req(usr_lang, target_lang, word)
            writeto_file(word, req, lang)
    else:  # Translate into target language
        target_lang = LANGS[target_lang - 1].lower()  # Assign target language from list
        req = get_req(usr_lang, target_lang, word)
        writeto_file(word, req, target_lang)

    file = open(f'{word}.txt', 'r', encoding='utf-8')
    content = file.readlines()
    for line in content:
        print(line.strip())
    file.close()


if __name__ == '__main__':
    main()
