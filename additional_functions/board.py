def load_move(data):
    if data == 'None':
        return False
    print(f'{data} = data')

    data = data.split('%')
    last = int(data[0]), int(data[1])
    new = list(map(int, data[2:]))
    new = [(new[i], new[i + 1]) for i in range(0, len(new), 2)]
    return last, new


def send_move(last, new):
    new = '%'.join('%'.join([str(i[0]), str(i[1])]) for i in new)
    return '%'.join([str(last[0]), str(last[1]), new])