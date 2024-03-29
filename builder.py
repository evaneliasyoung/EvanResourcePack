#!/usr/bin/env python3
"""
@file      builder.py
@brief     Builds my custom language resource pack.

@author    Evan Elias Young
@date      2019-08-29
@date      2021-06-17
@copyright Copyright 2019-2020 Evan Elias Young. All rights reserved.
"""

from mcmeta import MCMeta, PackFormat
from os.path import join
import os
import json
from io import BytesIO
from zipfile import ZipFile, ZIP_DEFLATED
from typing import List, Dict, Any, TypedDict, Union


class SimplePack(TypedDict):
    name: str  # The name for the resource pack addition.
    code: str  # The internal codename for the addition.
    version: str  # The interal version of the addition.
    data: Dict[str, str]  # The underlying language data.


class ComplexPack(SimplePack):
    content: List[str]  # The additional files to include.


PACK_NAME: str = "Evan's Language"
PACK_VER: str = '4.1.1'
PACK_FORMAT: PackFormat = 7
SPLASHES: List[str] = ['01000101', 'eey.pw', 'Open Source!']
PACK_DATA: MCMeta = {
    'pack': {
        'pack_format': PACK_FORMAT,
        'description': f"Evan's Custom Language! V{PACK_VER}"
    },
    'language': {
        'en_ev': {
            'name': "Evan's English",
            'region': "Evan's House",
            'bidirectional': False
        }
    }
}
SEP: str = os.sep
PackCollection = Dict[str, Union[SimplePack, ComplexPack]]


def load_complex() -> Dict[str, ComplexPack]:
    """Loads all the complex data packs.

    Returns:
        Dict[str, ComplexPack] -- The collection of complex data packs.
    """
    complex_files: List[str] = [
        f for f in os.listdir('complex') if os.path.isdir(join('complex', f))
    ]
    complex_json: List[ComplexPack] = [
        json.load(open(join('complex', f, f'{f}.json'))) for f in complex_files
    ]
    complex_data: Dict[str, ComplexPack] = {}
    for j in complex_json:
        complex_data[j['code']] = j
    return complex_data


def load_simple() -> Dict[str, SimplePack]:
    """Loads all the simple data packs.

    Returns:
        Dict[str, SimplePack] -- The collection of simple data packs.
    """
    simple_files: List[str] = [
        f for f in os.listdir('simple') if f.endswith('.json')
    ]
    simple_json: List[ComplexPack] = [
        json.load(open(join('simple', f))) for f in simple_files
    ]
    simple_data: Dict[str, SimplePack] = {}
    for j in simple_json:
        simple_data[j['code']] = j
    return simple_data


def build_selected(zipf: ZipFile, selected: PackCollection) -> None:
    """Builds the selected data packs into a file.

    Args:
        zipf (ZipFile): The zip file of the data pack.
        selected (PackCollection): The selected packs to combine.
    """
    st: str = 'Selected Packs:\n'
    st += '\n'.join([f'  {p} - {selected[p]["version"]}' for p in selected])
    zipf.writestr('selected.txt', st)


def build_content(zipf: ZipFile, selected: PackCollection):
    """Builds the selected data packs and their contents into the data pack.

    Args:
        zipf (ZipFile): The zip file of the data pack.
        selected (PackCollection): The selected packs to combine.
    """
    comp: Dict[str, ComplexPack] = load_complex()
    rev: Dict[str, ComplexPack] = [s for s in selected if s in comp]
    for p in rev:
        for c in comp[p]['content']:
            for root, _, files in os.walk(join('complex', p, c)):
                for f in files:
                    zipf.write(
                        join(root, f),
                        join('assets', 'minecraft',
                             SEP.join(root.split(SEP)[2:]), f))


def build_base(zipf: ZipFile) -> None:
    """Builds the base structure for the data pack.

    Args:
        zipf (ZipFile): The zip file of the data pack.
    """
    zipf.write(join('assets', 'pack.png'), 'pack.png')
    zipf.writestr('pack.mcmeta', json.dumps(PACK_DATA, indent=4))
    zipf.writestr(join('assets', 'minecraft', 'texts', 'splashes.txt'),
                  '\n'.join(SPLASHES))


def build_lang(zipf: ZipFile, selected: PackCollection) -> None:
    """Builds the language files into the data pack.

    Args:
        zipf (ZipFile): The zip file of the data pack.
        selected (PackCollection): The selected packs to combine.
    """
    lang: Dict[str, str] = json.load(open(join('assets', 'base.json')))
    for p in selected:
        lang.update(selected[p]['data'])
    zipf.writestr(join('assets', 'minecraft', 'lang', 'en_ev.json'),
                  json.dumps(lang, indent=2))

if __name__ == '__main__':
    selected: PackCollection = {}
    allData: PackCollection = {}
    allData.update(load_simple())
    allData.update(load_complex())

    for p in allData:
        ans: str = ''
        while not (ans == 'Y' or ans == 'N'):
            print(allData[p]['name'])
            ans = input('Y/n ').upper()
        if ans == 'Y':
            selected[p] = allData[p]

    zipbytes: BytesIO = BytesIO()
    zipf: ZipFile = ZipFile(zipbytes, 'w', ZIP_DEFLATED, False)

    build_base(zipf)
    build_selected(zipf, selected)
    build_lang(zipf, selected)
    build_content(zipf, selected)

    zipf.close()
    open(f'{PACK_NAME}.zip', 'wb').write(zipbytes.getvalue())
