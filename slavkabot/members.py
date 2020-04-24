from collections import namedtuple
from typing import Union

Member = namedtuple('Member', ('name', 'vk_id', 'tg_id'))


VkId2Name = {
    22381381: 'Евгин',
    188533876: 'Антоха',
    221859240: 'Жак',
    275079864: 'Борз',
    19492291: 'Степан',
    320669384: 'Славка',
    322472465: 'Игорь',
    179007104: 'Марти',
    234706017: 'Паша'
}

TeleId2Name = {
    24077164: 'Евгин',
    75144556: 'Антоха',
    687124937: 'Жак',
    225315032: 'Борз',
    422842018: 'Степан',
    1016732841: 'Cлавка',
    # 1088798978: 'Bot'
    178499692: 'Игорь',
    354275035: 'Марти',
    716452309: 'Паша'
}


def _members():
    members = {}
    for vk_id, name in VkId2Name.items():
        tg_id = None
        for id_, name_ in TeleId2Name.items():
            if name_ == name:
                tg_id = id_
                break
        members[name] = Member(name=name, vk_id=vk_id, tg_id=tg_id)
    return members


members = _members()
del _members


def get_member(key: Union[int, str]) -> Member:
    if key in members:
        # key is member name
        return members[key]

    for id_, name in VkId2Name.items():
        # search key in VK IDs
        if id_ == key:
            return members[name]

    for id_, name in TeleId2Name.items():
        # search key in Tg IDs
        if id_ == key:
            return members[name]

    # raise KeyError('Member not found')
    # TODO: create default member
    # For now Жак will be default member

    return members['Жак']
