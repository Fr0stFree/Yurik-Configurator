from collections import namedtuple


LOOKING_VALUE = 'FB_SHPS_S'

SEVERITY_SIGNALS = {"Тушение": 1, "Пожар": 2, "Порог 2": 3, "Авария": 4, "Тревога": 5,
                    "Порог 1": 6, "Предупреждение": 8, "Недостоверность": 10,
                    "Неисправность": 12, "Отключение": 13, "Ремонт": 14, "Имитация": 16,
                    "Телесигнализация": 18, "Команда оператора": 20, "Информация": 22}

Field = namedtuple('Field', 'name, column, key')

NAME = Field(name='name', column='D', key='name')
STYPE = Field(name='SensorType', column='N', key='stype')
COLOR_ON = Field(name='ColorOn', column='Q', key='color_on')
GP = Field(name='GeneralPlan', column='J', key='gp')
SOUND_ON = Field(name='SoundOn', column='P', key='sound_on')
MESSAGE_ON = Field(name='MessageOn', column='O', key='message_on')
DESCRIPTION = Field(name='Description', column='E', key='description')
SEVERITY = Field(name='SeverityOn', column='P', key='severity')
IVXX_TP = Field(name='IVXX_TP', column='Y', key='ivxx_tp')

NON_EMPTY_FIELDS = [NAME, STYPE, GP, SEVERITY]
