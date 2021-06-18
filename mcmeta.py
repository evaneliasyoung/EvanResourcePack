#!/usr/bin/env python3
"""
@file      mcmeta.py
@brief     Represents the MCMeta file.

@author    Evan Elias Young
@date      2021-06-17
@date      2021-06-17
@copyright Copyright 2021 Evan Elias Young. All rights reserved.
"""

from typing import Dict, Literal, TypedDict

PackFormat = Literal[1,  # 1.6.1  - 1.8.9
                     2,  # 1.9    - 1.10.2
                     3,  # 1.11   - 1.12.2
                     4,  # 1.13   - 1.14.4
                     5,  # 1.15   - 1.16.1
                     6,  # 1.16.2 - 1.16.5
                     7,  # 1.17
                     ]


class MCPack(TypedDict):
    """Holds base resource pack information.
    """
    pack_format: PackFormat  # Pack version.
    description: str  # Text shown below the pack name in the resource pack menu.


class MCLanguage(TypedDict):
    """Language information to add to the language menu.
    """
    name: str  # The full name of the language.
    region: str  # The country or region name.
    bidirectional: bool  # If true, the language reads right to left.


class MCMeta(TypedDict):
    """Represents a resource pack in Minecraft.
    """
    pack: MCPack  # Holds resource pack information.
    language: Dict[
        str,
        MCLanguage]  # Contains additional languages to add to the language menu.
