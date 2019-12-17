from athena.consts import EnumObject


class Sex(EnumObject):
    female = 0
    male = 1
    unknown = 2
    __transaction__ = dict(female='女', male='男', unknown='未知')


class OpenidType(EnumObject):
    phone = 1
    email = 2
    __transaction__ = dict(phone='手机', email='邮箱')

