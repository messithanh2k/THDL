import pandas as pd
import datetime

AREA_RANGES = {'nhà trong hẻm':  [40, 55, 70, 80, 90, 100, 150],
               'căn hộ chung cư': [40, 55, 70, 80, 90, 100, 120],
               'nhà mặt tiền': [50, 70, 90, 110, 140, 180, 230],
               'biệt thự': [70, 100, 130, 165, 200, 250, 300],
               'đất nền': [80, 210, 360, 700, 1000, 1400, 1900],
               'loại hình khác': [120, 500, 2500, 4000, 6200, 8500, 11000],
               'khách sạn, cửa hàng': [80, 120, 170, 260, 350, 490, 620],
               'văn phòng': [120, 300, 550, 780, 1000, 1500, 1900],
               'phòng trọ, nhà trọ': [50, 65, 80, 95, 110, 130, 160]}

PRICE_RANGES = {'nhà trong hẻm':      [3000000000 , 4000000000 , 5000000000 , 7000000000 , 9000000000  , 12000000000 , 15000000000 ],
               'căn hộ chung cư':     [600000000  , 1200000000 , 2000000000 , 3500000000 , 5000000000  , 7500000000  , 10000000000 ],
               'nhà mặt tiền':        [3000000000 , 7000000000 , 15000000000, 20000000000, 35000000000 , 45000000000 , 80000000000 ],
               'biệt thự':            [5000000000 , 8000000000 , 14000000000, 20000000000, 35000000000 , 50000000000 , 60000000000 ],
               'đất nền':             [1500000000 , 6000000000 , 10000000000, 15000000000, 20000000000 , 30000000000 , 80000000000 ],
               'loại hình khác':      [4000000000 , 8000000000 , 12000000000, 20000000000, 40000000000 , 60000000000 , 80000000000 ],
               'khách sạn, cửa hàng': [19000000000, 40000000000, 70000000000, 95000000000, 200000000000, 400000000000, 600000000000],
               'văn phòng':           [10000000000, 20000000000, 30000000000, 65000000000, 100000000000, 180000000000, 260000000000],
               'phòng trọ, nhà trọ':  [2000000000 , 5000000000 , 7500000000 , 10000000000, 13000000000 , 17000000000 , 25000000000]}

def get_timestamp(stime):
    return datetime.datetime.strptime(stime, "%d/%m/%Y").timestamp()

def get_area_str(value):
  if value < 1000:
    return "%d m2" %value
  value = value/1000
  return "%.1f ha" %value

def get_price_str(value):
  if value>=1000000000:
    value = value/1000000000
    return "%.1f tỷ" %value
  value = value/1000000
  return "%d triệu" %value

def area_encode(item):
  area_ranges = AREA_RANGES[item["property_type"]]
  value = item["property_area"]
  for i in range(len(area_ranges)):
    if value<=area_ranges[i]:
      if i==0:
        return pd.Series(["Nhỏ hơn " + get_area_str(area_ranges[0]),0, area_ranges[0]])
      return pd.Series(["Từ " + get_area_str(area_ranges[i-1]) + " đến " +  get_area_str(area_ranges[i]), area_ranges[i-1], area_ranges[i]])
  return pd.Series(["Lớn hơn " + get_area_str(area_ranges[-1]), area_ranges[-1], -1])

def price_encode(item):
  price_ranges = PRICE_RANGES[item["property_type"]]
  value = item["property_price"]
  for i in range(len(price_ranges)):
    if value<=price_ranges[i]:
      if i==0:
        return pd.Series(["Nhỏ hơn " + get_price_str(price_ranges[0]), 0, price_ranges[0]])
      return pd.Series(["Từ " + get_price_str(price_ranges[i-1]) + " đến " +  get_price_str(price_ranges[i]), price_ranges[i-1], price_ranges[i]])
  return pd.Series(["Lớn hơn " + get_price_str(price_ranges[-1]), price_ranges[-1], -1])

def day_extract(value):
  value = value.split("/")
  return pd.Series([int(value[0]), int(value[1]), int(value[2])])

def sumup_data(data: pd.DataFrame) -> pd.DataFrame:
    data[["property_day", "property_month", "property_year"]] = data["property_date"].apply(day_extract)
    data[["property_area_type", "property_min_area", "property_max_area"]] = data.apply(area_encode, axis=1)
    data[["property_price_type", "property_min_price", "property_max_price"]] = data.apply(price_encode, axis=1)
    sumup = data.groupby(["property_province", "property_district", "property_ward",
                          "property_type", "property_day", "property_month",
                          "property_year", "property_date",
                          "property_area_type", "property_min_area", "property_max_area",
                          "property_price_type", "property_min_price", "property_max_price"]).agg({"_id": "count", "property_area": "sum", "property_price": "sum"})
    sumup.rename(columns={"_id": "count", "property_area": "sum_area", "property_price": "sum_price"}, inplace=True)
    sumup.reset_index(inplace=True)
    sumup["property_linux"] = sumup["property_date"].apply(get_timestamp)
    return sumup