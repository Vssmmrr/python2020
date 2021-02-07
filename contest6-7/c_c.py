import traceback


def force_load(file_name):
    with open(file_name + '.py', 'rt') as f:
        code = f.readlines()
    funcs = {}
    while code:
        try:
            exec(''.join(code), globals(), funcs)
        except Exception as e:
            error = traceback.format_exc().split('\n')
            while not ' '.join(error[-1].split()).startswith('File'):
                error.pop(-1)
            try:
                str_no = int(error[-1].split()[3])
            except ValueError:
                str_no = int(error[-1].split()[3][:-1])
            code.pop(str_no - 1)
            funcs = {}
        else:
            break
    return funcs


m = force_load('broken_module')
print(m['foo']())
