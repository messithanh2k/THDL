import pymongo
import pandas as pd

client = pymongo.MongoClient("mongodb+srv://chimeyrock999:admin123@congthongtinbatdongsan.19hdj.mongodb.net/?retryWrites=true&w=majority")
db = client["PropertiesDatabase"]
data = db["MediatedSchemaData"]
df = pd.DataFrame(list(data.find()))

df.drop(columns=["_id"], inplace=True)

def preprocessing(x):
  x = x.lower()
  x = x.replace('bán ', '')
  return x
df['type'] = df['type'].apply(preprocessing)

label_mapping = {'nhà mặt tiền': 'nhà mặt tiền',
                 'đất nền - đất ở - đất thổ cư': 'đất nền',
                'nhà trong hẻm': 'nhà trong hẻm',
                'nhà ngõ, hẻm': 'nhà trong hẻm',
                'đất': 'đất nền',
                'đất thổ cư, đất ở': 'đất nền',
                'nhà mặt phố': 'nhà phố',
                'biệt thự, nhà liền kề': 'biệt thự',
                 'biệt thự phố': 'biệt thự',
                'đất nông, lâm nghiệp': 'loại hình khác',
                 'căn hộ cao cấp': 'căn hộ chung cư',
                 'nhà biệt thự, liền kề': 'biệt thự',
                 'đất nền thổ cư': 'đất nền',
                'nhà hàng, khách sạn': 'khách sạn, cửa hàng',
                 'đất nền, phân lô': 'đất nền',
                 'đất dự án': 'đất nền',
                 'đất nền, liền kề, đất dự án': 'đất nền',
                 'nhà': 'nhà riêng',
                  'các loại khác': 'loại hình khác',
                 'shophouse': 'khách sạn, cửa hàng',
                'shop, kiot, quán': 'khách sạn, cửa hàng',
                'kho, xưởng': 'loại hình khác',
                 'phòng trọ': 'phòng trọ, nhà trọ',
                'mặt bằng': 'đất nền',
                'trang trại': 'loại hình khác',
                 'căn hộ chung cư mini': 'căn hộ chung cư',
                 'nhà hàng - khách sạn': 'khách sạn, cửa hàng',
                 'căn hộ giá rẻ': 'căn hộ chung cư',
                 'căn hộ tập thể': 'căn hộ chung cư',
                 'đất vàng': 'đất nền',
                 'căn hộ trung cấp': 'căn hộ chung cư',
                 'cửa hàng, kiot': 'khách sạn, cửa hàng',
                 'luxury home': 'khách sạn, cửa hàng',
                 'đất nền dự án': 'đất nền',
                 'tòa nhà văn phòng': 'văn phòng',
                 'nhà xưởng': 'loại hình khác',
                 'kho, nhà xưởng': 'loại hình khác',
                 'bđs thương mại': 'loại hình khác',
                 'sàn thương mại': 'loại hình khác',
                 'bđs nông nghiệp': 'loại hình khác'}

def typestandard(x):
  x = label_mapping[x] if x in list(label_mapping.keys()) else x
  return x
df['type'] = df['type'].apply(typestandard)

import re
import numpy as np
def area_extract(area):
    if not isinstance(area, str):
        area = str(area)
    area = area.replace(" ", "").replace(".", "").replace(",", ".").lower()
    result = 0
    square = re.findall("(\d+[\.]?\d*)m2", area)
    if square:
        result += float(square[0])
    square = re.findall("(\d+[\.]?\d*)m", area)
    if square:
        result += float(square[0])
    square = re.findall("(\d+[\.]?\d*)ha", area)
    if square:
        result += float(square[0]) * 1000
    if result > 0:
        return result
    else:
        return np.nan

def transform(df):
    df["square"] = df["square"].apply(area_extract)
    df.dropna(subset=["square"], inplace=True)
    return df
df = transform(df)

def price_extract(item):
    price = 0
    value = str(item["price"]).replace(" ", "").replace(".", "").replace(",", ".").lower()

    billion = re.findall("(\d+[\.]?\d*)tỷ", value)
    if billion:
        price += float(billion[0]) * 1000000000
    million = re.findall("(\d+[.]?\d*)triệu", value)
    if million:
        price += float(million[0]) * 1000000
    thousand = re.findall("(\d+[.]?\d*)nghìn", value)
    if thousand:
        price += float(thousand[0]) * 1000
    try:
        if value.endswith("/m2"):
            price = price * item["square"]
        elif value.endswith("/ha"):
            price = price * item["square"] / 1000
    except:
        price = 0
    if price == 0:
        return np.nan
    else:
        return int(price)

def transformprice(df):
    df["price"] = df.apply(price_extract, axis=1)
    df.dropna(subset=["price"], inplace=True)
    return df
df = transformprice(df)

df = df[df.city == 'Hà Nội']

df = df[df.address != '---']

wards = ['Phường Dịch Vọng', 'Phường Thanh Lương', 'Phường Hoàng Liệt',
       'Phường Xuân La', 'Phường Chương Dương', 'Phường Cống Vị',
       'Xã Dân Hòa', 'Phường Thụy Phương', 'Phường Thanh Trì',
       'Phường Bạch Đằng', 'Phường Cửa Đông', 'Xã Hồng Vân',
       'Phường Phúc Tân', 'Phường Kim Liên', 'Phường Cự Khối',
       'Thị trấn Trâu Quỳ', 'Phường Kim Giang', 'Phường Đồng Tâm',
       'Phường Minh Khai', 'Phường Phú Thượng', 'Phường Phúc La',
       'Phường Hoàng Văn Thụ', 'Xã Tân Triều', 'Phường Thịnh Quang',
       'Phường Vĩnh Tuy', 'Phường Nhật Tân', 'Phường Thành Công',
       'Phường Cửa Nam', 'Phường Yên Phụ', 'Phường Bách Khoa',
       'Phường Ngã Tư Sở', 'Xã Tiên Dương', 'Phường Xuân Đỉnh',
       'Xã Di Trạch', 'Phường Trung Tự', 'Phường Biên Giang',
       'Xã Phú Cát', 'Phường Cầu Diễn', 'Phường Mễ Trì',
       'Phường Lê Đại Hành', 'Phường Thanh Xuân Bắc', 'Xã Đức Giang',
       'Xã Nguyên Khê', 'Phường Thanh Xuân Trung', 'Xã Kim Sơn',
       'Xã Đông Hội', 'Phường Quán Thánh', 'Phường Kiến Hưng',
       'Phường Thụy Khuê', 'Phường Phố Huế', 'Phường Đại Mỗ',
       'Xã Tân Lập', 'Xã An Khánh', 'Xã Tiến Xuân', 'Phường Kim Mã',
       'Phường Yên Hoà', 'Xã Tả Thanh Oai', 'Phường Đồng Mai',
       'Phường Khâm Thiên', 'Phường Đại Kim', 'Phường Mai Dịch',
       'Phường Giáp Bát', 'Xã Vân Hòa', 'Xã Yên Trung', 'Phường Quảng An',
       'Phường Đồng Nhân', 'Phường Bồ Đề', 'Phường Phú Lương',
       'Phường Tân Mai', 'Phường Quang Trung', 'Phường Nhân Chính',
       'Phường Mộ Lao', 'Phường Giang Biên', 'Thị trấn Văn Điển',
       'Xã Đặng Xá', 'Phường Đội Cấn', 'Phường Phúc Đồng',
       'Phường Phúc Xá', 'Phường Nghĩa Tân', 'Xã Hải Bối',
       'Phường Mai Động', 'Phường Cát Linh', 'Xã Tân Phú', 'Xã Vân Hà',
       'Phường Mỹ Đình 2', 'Phường Khương Mai', 'Xã Bắc Hồng',
       'Xã Đồng Tâm', 'Phường Bưởi', 'Xã Dũng Tiến', 'Phường Ô Chợ Dừa',
       'Phường Phúc Lợi', 'Phường Trung Hoà', 'Phường Phú La',
       'Phường Hàng Gai', 'Phường Việt Hưng', 'Xã Bắc Sơn',
       'Phường Phương Liên', 'Phường Lý Thái Tổ', 'Phường Ngọc Thụy',
       'Phường Thanh Xuân Nam', 'Phường Liên Mạc', 'Phường Trung Liệt',
       'Phường Phú Đô', 'Phường Cổ Nhuế 2', 'Phường Mỹ Đình 1',
       'Xã Ninh Sở', 'Phường Ngọc Hà', 'Xã Đa Tốn', 'Phường Phương Canh',
       'Đại Kim', 'Phường Hạ Đình', 'Phường Xuân Khanh', 'Phường Phú Lãm',
       'Phường Nguyễn Trãi', 'Phường Đông Ngạc', 'Xã Đỗ Động',
       'Xã Thanh Mỹ', 'Phường Đồng Xuân', 'Phường Sài Đồng',
       'Xã Thanh Liệt', 'Phường Khương Trung', 'Phường Thượng Đình',
       'Phường Trần Hưng Đạo', 'Phường Tây Mỗ', 'Xã Xuân Sơn',
       'Phường Long Biên', 'Phường Giảng Võ', 'Xã Liên Ninh',
       'Phường Vĩnh Hưng', 'Xã Quang Tiến', 'Xã Đồng Trúc',
       'Phường Khương Đình', 'Phường Ngọc Lâm', 'Phường Dương Nội',
       'Phường Yên Nghĩa', 'Xã Kim Chung', 'Phường Thịnh Liệt',
       'Phường Hà Cầu', 'Phường Phương Mai', 'Phường La Khê',
       'Phường Vĩnh Phúc', 'Phường Liễu Giai', 'Xã Minh Phú',
       'Phường Trần Phú', 'Xã Tứ Hiệp', 'Phường Phúc Diễn',
       'Phường Nguyễn Du', 'Phường Quan Hoa', 'Xã Vân Nội', 'Xã Đông Dư',
       'Xã Đắc Sở', 'Phường Nghĩa Đô', 'Xã Nam Sơn', 'Phường Phương Liệt',
       'Xã Đông Mỹ', 'Xã Tân Tiến', 'Phường Trương Định',
       'Phường Văn Chương', 'Phường Yên Sở', 'Phường Nam Đồng',
       'Phường Thổ Quan', 'Phường Hàng Bột', 'Phường Văn Quán',
       'Xã Vạn Phúc', 'Xã Xuân Nộn', 'Xã Quất Động', 'Trung Hoà',
       'Phường Phú Diễn', 'Xã Dương Xá', 'Phường Hàng Bồ',
       'Xã Vĩnh Quỳnh', 'Phường Khương Thượng', 'Phường Trung Văn',
       'Phường Láng Thượng', 'Phường Thạch Bàn', 'Xã Duyên Thái',
       'Phường Cổ Nhuế 1', 'Xã Vân Côn', 'Thị trấn Xuân Mai',
       'Phường Tứ Liên', 'Xã Song Phượng', 'Phường Cầu Dền', 'Xã Hà Hồi',
       'Xã Đông Yên', 'Phường Định Công', 'Thị trấn Đông Anh',
       'Phường Tương Mai', 'Khương Trung', 'Xã Kiêu Kỵ',
       'Xã Phương Trung', 'Xã Tản Lĩnh', 'Phường Láng Hạ',
       'Phường Bạch Mai', 'Phường Lĩnh Nam', 'Phường Thanh Nhàn',
       'Phường Vạn Phúc', 'Phường Thượng Thanh', 'Xã Vân Canh',
       'Phường Yết Kiêu', 'Xã Bình Minh', 'Xã Phú Cường',
       'Phường Đống Mác', 'Phường Quỳnh Mai', 'Phường Hàng Trống',
       'Xã Ba Trại', 'Phường Xuân Tảo', 'Xã Yên Bình', 'Xã Lại Yên',
       'Phường Tràng Tiền', 'Phường Xuân Phương', 'Xã Phú Thị',
       'Phường Hàng Bông', 'Phường Trung Sơn Trầm', 'Xã Ngũ Hiệp',
       'Phường Ngọc Khánh', 'Phường Quỳnh Lôi', 'Phường Đức Thắng',
       'Xã Phù Lỗ', 'Xã Minh Trí', 'Xã Bình Yên', 'Xã Thạch Hoà',
       'Xã Tam Hiệp', 'Xã Tân Xã', 'Thị trấn Trạm Trôi', 'Xã Đại áng',
       'Xã Phụng Thượng', 'Phố Huế', 'Xã Sơn Đông', 'Thị trấn Quang Minh',
       'Thị trấn Chúc Sơn', 'Phường Tây Tựu', 'Xã Vĩnh Ngọc',
       'Xã Tự Nhiên', 'Xã Song Phương', 'Xã Đức Thượng', 'Xã Tiên Dược',
       'Phường Gia Thụy', 'Xã Đồng Tháp', 'Xã Thanh Văn', 'Xã Hòa Thạch',
       'Xã Hữu Hoà', 'Xã Ngọc Hồi', 'Phường Nguyễn Trung Trực',
       'Xã Nhị Khê', 'Xã Hiền Ninh', 'Phường Trúc Bạch', 'Xã Cổ Đông',
       'Phường Đức Giang', 'Xã Vân Tảo', 'Phường Hàng Mã',
       'Phường Quốc Tử Giám', 'Quảng An', 'Xã Thư Phú', 'Xuân La',
       'Xã Cổ Bi', 'Xã Hạ Bằng', 'Xã Yên Bài', 'Xã Đông Xuân',
       'Xã Phú Mãn', 'Xã Thắng Lợi', 'Xã Uy Nỗ', 'Xã Cổ Loa',
       'Xã Yên Viên', 'Phường Văn Miếu', 'Xã Nam Phương Tiến',
       'Phường Điện Biên', 'Xã Đại Thịnh', 'Xã Mai Lâm', 'Xã Nam Hồng',
       'Xã Chương Dương', 'Thị trấn Thường Tín', 'Xã La Phù',
       'Xã Mai Đình', 'Xã Đại Xuyên', 'Xã Tòng Bạt', 'Phường Thượng Cát',
       'Xã Phụng Châu', 'Xã Xuân Canh', 'Hà Cầu', 'Xã Lệ Chi',
       'Xã Minh Quang', 'Xã Hoàng Văn Thụ', 'Xã Ba Vì', 'Xã Hồng Minh',
       'Phường Sơn Lộc', 'Xã Dục Tú', 'Xã Dương Quang', 'Xã Lại Thượng',
       'Xã Vân Từ', 'Xã Bích Hòa', 'Xã Phú Nghĩa', 'Đồng Tâm',
       'Xã Đồng Lạc', 'Xã Thuỵ Lâm', 'Phường Hàng Đào',
       'Xã Thủy Xuân Tiên', 'Phường Phan Chu Trinh', 'Hạ Đình',
       'Xã Tích Giang', 'Xã Đông La', 'Xã Ngọc Tảo', 'Xã Sài Sơn',
       'Xã Vật Lại', 'Xã Mỹ Lương', 'Xã Phúc Hòa', 'Xã Tân Minh',
       'Thị trấn Phú Minh', 'Xã Ninh Hiệp', 'Quan Hoa', 'Xã Thượng Mỗ',
       'Thị trấn Phùng', 'Xã Võng La', 'Cửa Nam', 'Xã Yên Mỹ',
       'Xã Khánh Hà', 'Xã Phù Linh', 'Xã Tô Hiệu', 'Xã Tri Trung',
       'Xã Văn Bình', 'Xã Cự Khê', 'Xã Văn Hoàng', 'Xã Trung Giã',
       'Xã Cẩm Lĩnh', 'Xã Tân Dân', 'Xã Yên Thường', 'Xã Trần Phú',
       'Văn Điển', 'Xã An Thượng', 'Thị trấn Kim Bài', 'Phú Diễn',
       'Xã Tiền Phong', 'Xã Kim An', 'Xã Mỹ Hưng', 'Xã Tiên Phương',
       'Hàng Bột', 'Vạn Phúc', 'Xã Đường Lâm', 'Mộ Lao',
       'Xã Đông Phương Yên', 'Láng Hạ', 'Xã Thanh Cao', 'Xã Nguyễn Trãi',
       'Xã Thụy Hương', 'Xã Việt Hùng', 'Xã Duyên Hà', 'Xã Ngọc Mỹ',
       'Thị trấn Vân Đình', 'Xã Võng Xuyên', 'Tương Mai', 'Xã Liệp Tuyết',
       'Thanh Liệt', 'Xã Liên Phương', 'Xã Thọ Lộc', 'Xã Ngọc Hòa',
       'Xã Mê Linh', 'Xã Đại Cường', 'Xã Đại Mạch', 'Xã Khánh Thượng',
       'Xã Thanh Mai', 'Xã Đan Phượng', 'Giáp Bát', 'Gia Thụy',
       'Xã Hiệp Thuận', 'Thị trấn Chi Đông', 'Vĩnh Hưng', 'Ngọc Lâm',
       'Xã Tam Hưng', 'Xã Kim Quan', 'Lĩnh Nam', 'Xã Thụy An', 'Trung Tự',
       'Phường Phú Thịnh', 'Xã Thạch Xá', 'Xã Bát Tràng', 'Xuân Đình',
       'Xã Kim Nỗ', 'Xã Liên Hà', 'Xã Phú Minh', 'Xã Hiền Giang',
       'Xã Dương Hà', 'Xã Phương Đình', 'Xã An Phú', 'Xã Hợp Đồng',
       'Nhân Chính', 'Phương Mai', 'Thanh Nhàn', 'Thị trấn Sóc Sơn',
       'Thị trấn Phúc Thọ', 'Kiến Hưng', 'Xã Trạch Mỹ Lộc', 'Xã Đông Sơn']
wards_lower = list(map(lambda x: x.lower(), wards))
wards_lower_short = []
for ward in wards_lower:
   wards_lower_short.append(ward.replace("xã ", "").replace("phường ", "").replace("thị trấn ", ""))

import regex as re
 
uniChars = "àáảãạâầấẩẫậăằắẳẵặèéẻẽẹêềếểễệđìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵÀÁẢÃẠÂẦẤẨẪẬĂẰẮẲẴẶÈÉẺẼẸÊỀẾỂỄỆĐÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴÂĂĐÔƠƯ"
unsignChars = "aaaaaaaaaaaaaaaaaeeeeeeeeeeediiiiiooooooooooooooooouuuuuuuuuuuyyyyyAAAAAAAAAAAAAAAAAEEEEEEEEEEEDIIIOOOOOOOOOOOOOOOOOOOUUUUUUUUUUUYYYYYAADOOU"
 
 
def loaddicchar():
    dic = {}
    char1252 = 'à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ'.split(
        '|')
    charutf8 = "à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ".split(
        '|')
    for i in range(len(char1252)):
        dic[char1252[i]] = charutf8[i]
    return dic
 
 
dicchar = loaddicchar()
 
 
def covert_unicode(txt):
    return re.sub(
        r'à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ',
        lambda x: dicchar[x.group()], txt)

def extract_ward(text):
  text = covert_unicode(text)
  text = text.lower()
  for i in range(len(wards_lower_short)):
    hasWard = re.findall(wards_lower_short[i], text)
    if hasWard:
      return wards[i]
df['ward'] = df['address'].apply(extract_ward)

from datetime import datetime
def compute_time(x):
    if not isinstance(x, str):
        x = str(x)
    try:
      if x.find(':')>0:
        x = x.split()[0]
        time_object = datetime.strptime(x, "%Y-%m-%d")
      elif x.find('-')>0:
        time_object = datetime.strptime(x, "%d-%m-%Y")
      elif x.find('/')>0:
        time_object = datetime.strptime(x, "%d/%m/%Y")
      else:
        return
      return time_object.timestamp()
    except:
      print(x)
      return 0

def transformTime(df):
    df["postedTime"] = df["postedTime"].apply(compute_time)
    df.dropna(subset=["postedTime"], inplace=True)
    return df
df = transformTime(df)

df.drop(df[df['price'] > 10e13].index, inplace = True)

data_ = df.to_dict("records")
target_db = client["PropertiesDatabase"]
target_collection = target_db["MediatedCleanDataDuplicate"]
target_collection.insert_many(data_)
