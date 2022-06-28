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
