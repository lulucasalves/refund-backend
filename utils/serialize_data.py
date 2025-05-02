def serialize_array(data):
    listItems = []
    for item in data:
        item_data = {
            key: value
            for key, value in item.__dict__.items()
            if not key.startswith("_")
        }
        listItems.append(item_data)

    return listItems
