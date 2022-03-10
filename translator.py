import requests
from bs4 import BeautifulSoup
import argparse
import sys

LANGS = ['Arabic', 'German', 'English', 'Spanish', 'French', 'Hebrew', 'Japanese',
         'Dutch', 'Polish', 'Portuguese', 'Romanian', 'Russian', 'Turkish']


def get_req(usr_lang, target_lang, word):
    url = f'https://context.reverso.net/translation/{usr_lang}-{target_lang}/{word}'
    headers = {'User-Agent': 'Mozilla/5.0'}

    return requests.get(url, headers=headers)


def writeto_file(word, req, lang):
    if req.status_code == 200:  # Got response
        file = open(f'{word}.txt', 'a', encoding='utf-8')
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
    elif req.status_code == 404:
        print(f'Sorry, unable to find{word}')
        sys.exit(0)
    else:
        print('Something wrong with your internet connection')
        sys.exit(0)


def main():
    # Take command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", nargs=3)
    args = parser.parse_args()

    usr_lang, target_lang, word = args.inputs[0], args.inputs[1], args.inputs[2]

    if usr_lang.capitalize() not in LANGS:
        print(f"Sorry, the program doesn't support {usr_lang}")
        sys.exit(0)
    elif target_lang.capitalize() not in LANGS and target_lang != 'all':
        print(f"Sorry, the program doesn't support {target_lang}")
        sys.exit(0)

    if target_lang == 'all':  # Translate into all available languages
        for lang in LANGS:
            target_lang = lang.lower()
            if usr_lang == target_lang:
                continue

            req = get_req(usr_lang, target_lang, word)
            writeto_file(word, req, lang)
    else:  # Translate into target language
        req = get_req(usr_lang, target_lang, word)
        writeto_file(word, req, target_lang)

    file = open(f'{word}.txt', 'r', encoding='utf-8')
    content = file.readlines()
    for line in content:
        print(line.strip())
    file.close()


if __name__ == '__main__':
    main()
