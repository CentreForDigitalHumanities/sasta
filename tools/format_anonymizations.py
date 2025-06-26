# flake8: noqa: E501
import json
import pathlib

ANON_FP = pathlib.Path(__file__).parent.parent.parent.resolve() / 'backend' / 'anonymization.json'

def format_anons(anons):
    for spec in anons:
        codes = ', '.join([f'`{code}`' for code in spec['codes']])
        common = ', '.join([f'`{com}`' for com in spec['common']])
        example = f'`{spec["example"][0]}` -> `{spec["example"][1]}`'

        l1 = f'- categorie: {spec["label-nl"]}'
        l2 = f'    - codes: {codes}'
        l3 = f'    - vervangingen: {common}'
        l4 = f'    - voorbeeld: {example}'

        total = [l1, l2, l3, l4]
        print(*total, sep='\n')


def main():
    with open(ANON_FP, 'r') as f:
        content = json.load(f)
        format_anons(content)


if __name__ == '__main__':
    main()
