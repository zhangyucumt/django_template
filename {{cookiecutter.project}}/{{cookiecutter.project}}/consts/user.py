from {{cookiecutter.project}}.consts import EnumObject


class Sex(EnumObject):
    female = 0
    make = 1
    unknown = 2


class OpenidType(EnumObject):
    phone = 1
    email = 2
