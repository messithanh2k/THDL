# alomuabannhadat
item = {}
if (item['square'] != 'UNKNOW' and item['square'] != ''):
    item['square'] = float(
        item['square'].replace('m2', '').replace(',', '.'))

if ('tỷ' in item['price'].lower() and 'triệu' in item['price'].lower()):
    item['price'] = float(item['price'].split(
        'tỷ')[0].strip()) * 1000 + float(item['price'].split(
            'tỷ')[1].replace('triệu', '').strip())
elif 'tỷ' in item['price'].lower():
    item['price'] = float(item['price'].replace('tỷ', '').strip())*1000
else:
    item['price'] = float(item['price'].replace('triệu').strip())


# batdongsan
if (item['square'] != '---' and item['square'] != ''):
    item['square'] = float(
        item['square'].replace('m', '').replace(',', '.'))
if ('tỷ' in item['price'].lower()):
    item['price'] = float(item['price'].split(
        ' ')[0].strip().replace(',', '.')) * 1000
elif 'triệu/m' in item['price'].lower():
    item['price'] = float(item['price'].split(
        ' ')[0].strip()) * float(item['square'])
else:
    item['price'] = float(item['price'].split(' ')[0].strip())


# alonhadat
if (item['square'] != '---' and item['square'] != ''):
    item['square'] = float(item['square'].replace('m', '').replace('.', '').replace(
        ',', '.'))

if ('tỷ' in item['price'].lower()):
    item['price'] = float(item['price'].split(
        ' ')[0].strip().replace(',', '.')) * 1000
elif 'triệu/' in item['price'].lower().strip():
    item['price'] = float(item['price'].split(
        ' ')[0].strip().replace(',', '.')) * float(item['square'])
else:
    item['price'] = float(item['price'].split(' ')[0].strip())

# i-batdongsan

if (item['square'] != '---' and item['square'] != ''):
    item['square'] = float(
        item['square'].replace('m', '').replace(',', '.'))

if ('tỷ' in item['price'].lower()):
    item['price'] = float(item['price'].split(
        ' ')[0].strip().replace(',', '.')) * 1000
elif 'triệu/' in item['price'].lower().strip():
    item['price'] = float(item['price'].split(
        ' ')[0].strip().replace(',', '.')) * float(item['square'])
else:
    item['price'] = float(item['price'].split(' ')[0].strip())
