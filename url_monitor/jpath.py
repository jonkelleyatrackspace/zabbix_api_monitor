#!/usr/bin/python

import json

PATH_SEPARATOR = '/'
CURRENT_NODE = '.'
LIST_INDEX_INDICATORS = ('[', ']')


def jpath(json_str, path, throw_error_or_mark_none='none'):
    """

    :param json_str:
    :param path:
    :param throw_error_or_mark_none:
    :return:
    """
    value = json.loads(json_str.strip())

    path_list = path.split(PATH_SEPARATOR)
    if path_list and path_list[0] == CURRENT_NODE:
        path_list = path_list[1:]

    for key in path_list:
        index = None
        if key[-1] == LIST_INDEX_INDICATORS[1]:
            left_indicator = key.rfind(LIST_INDEX_INDICATORS[0])
            if left_indicator > -1:
                index = int(key[left_indicator + 1:-1])
                key = key[:left_indicator]

        if key not in value:
            if throw_error_or_mark_none == 'none':
                value = None
            else:
                raise KeyError
        else:
            value = value.get(key)

        if index:
            try:
                value = value[index]
            except:
                if throw_error_or_mark_none == 'none':
                    value = None
                else:
                    raise

        if value is None:
            break

    return value
