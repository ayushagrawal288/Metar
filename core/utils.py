def qs_to_dict(data):
    if data == '':
        return dict()
    data = data.split('&')
    dic = dict()
    for item in data:
        item = item.split('=')
        dic.update({item[0]: item[1]})
    return dic
