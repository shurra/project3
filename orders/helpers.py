def search_in_list_of_dicts(search_list, key, value):
    for item in search_list:
        if item[key] == value:
            return item
