def process(row):
    id_ = row['customer_id']
    if id_[-1:]=='d':
        o = 1
    else:
        o = 0
    return o
