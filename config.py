# DataBase Item BDS

class BDSDatabaseConfig:
    MONGO_URI = "mongodb+srv://root:123@cluster0.wnpz9.mongodb.net/PropertiesDatabase?retryWrites=true&w=majority"
    DATABASE_NAME = 'PropertiesDatabase'
    COLLECTION_BDS_NAME = 'MediatedCleanData'

    NAME_ID = '_id'
    NAME_PROPERTY_WARD = 'property_ward'
    NAME_PROPERTY_DISTRICT = 'property_district'
    NAME_PROPERTY_PROVINCE = 'property_province'
    NAME_PROPERTY_TYPE = 'property_type'
    NAME_PROPERTY_TITLE = 'property_title'
    NAME_PROPERTY_DETAIL = 'property_detail'
    NAME_PROPERTY_PRICE = 'property_price'
    NAME_PROPERTY_AREA = 'property_area'
    NAME_PROPERTY_ADDRESS = 'property_address'
    NAME_PROPERTY_DATE = 'property_date'
    NAME_PROPERTY_LINK = 'property_link'
    NAME_PROPERTY_IMAGES = 'property_images'
    NAME_PROPERTY_LINUX = 'property_linux'
    NAME_PROPERTY_SEARCH = 'property_search'


class StatisticDatabaseConfig:
    MONGO_URI = 'mongodb+srv://root:123@cluster0.wnpz9.mongodb.net/StatDatabase?retryWrites=true&w=majority'
    DATABASE_NAME = 'StatDatabase'
    COLLECTION_TOTAL_PRICE_ON_CITY = 'TotalPriceOnCity'
    COLLECTION_TOTAL_PRICE_ON_DISTRICT = 'TotalPriceOnDistrict'
    COLLECTION_TOTAL_PRICE_ON_WARD = 'TotalPriceOnWard'
    COLLECTION_DENSITY_ON_DISTRICT = 'TotalDensityOnDistrict'
    COLLECTION_DENSITY_ON_WARD = 'TotalDensityOnWard'


class UserDatabaseConfig:
    MONGO_URI = "mongodb+srv://root:123@cluster0.wnpz9.mongodb.net/UserDatabase?retryWrites=true&w=majority"
    DATABASE_NAME = "UserDatabase"
    COLLECTION_ACCOUNT = "Account"
    COLLECTION_LOG = "Log"
