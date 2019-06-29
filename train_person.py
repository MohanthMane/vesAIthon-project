important_objects = ['laptop','keyboard','bottle','tv','person']

def generate_mappings(category_index):
    a = list(category_index.keys())
    names = []
    for i in range(len(a)):
        names.append(category_index[a[i]]['name'])
    
    object_mappings = {}

    for i in range(len(names)):
        if i == 63 or i==66:
            object_mappings[names[i]] = '111101111'
        elif i == 39:
            object_mappings[names[i]] = '000111000'
        elif i == 62:
            object_mappings[names[i]] = '100111100'
        elif i == 0:
            object_mappings[names[i]] = '010010010'

        else:
            if i == int('111101111',2):
                object_mappings[names[i]] = '001100001'

            elif i == int('000111000',2):
                object_mappings[names[i]] = '001100010'

            elif i == int('100111100',2):
                object_mappings[names[i]] = '001100011'

            elif i == int('010010010',2):
                object_mappings[names[i]] = '001100100'

            else:
                object_mappings[names[i]] = bin(i)[2:]
                prefix = '0' * (9-len((object_mappings[names[i]])))
                object_mappings[names[i]] = prefix + object_mappings[names[i]]

    print(object_mappings)
    return object_mappings

