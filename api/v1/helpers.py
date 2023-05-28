#!/usr/bin/python3
"""A module containing helper functions for the api"""


def del_keys(keys_list, data):
    """
    Delete keys from a dictionary if exists.

    Args:
    keys_list: A list of keys to delete
    data: The dictionary to delete the keys from

    Return:
    None
    """
    for k in keys_list:
        try:
            del data[k]
        except KeyError:
            continue
