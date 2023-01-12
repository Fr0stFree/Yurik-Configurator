from collections import namedtuple


class FB_SHPS_S:

SEVERITY_SIGNALS = {"Тушение": 1, "Пожар": 2, "Порог 2": 3, "Авария": 4, "Тревога": 5,
                    "Порог 1": 6, "Предупреждение": 8, "Недостоверность": 10,
                    "Неисправность": 12, "Отключение": 13, "Ремонт": 14, "Имитация": 16,
                    "Телесигнализация": 18, "Команда оператора": 20, "Информация": 22}

Field = namedtuple('Field', 'name, column, key')

NAME = Field(name='name', column='D', key='name')
SENSOR_TYPE = Field(name='SensorType', column='N', key='sensor_type')
#COLOR_OFF = Field(name='ColorOff', column='???', key='color_off')
#COLOR_OFF-отсутствует в таблице, по умолчанию "серый" поставил
COLOR_ON = Field(name='ColorOn', column='Q', key='color_on')
GP = Field(name='GeneralPlan', column='J', key='gp')
SOUND_ON = Field(name='SoundOn', column='P', key='sound_on')
MESSAGE_ON = Field(name='MessageOn', column='O', key='message_on')
DESCRIPTION = Field(name='Description', column='E', key='description')
SEVERITY = Field(name='SeverityOn', column='P', key='severity')
IVXX_TP = Field(name='IVXX_TP', column='Y', key='ivxx_tp')

NON_EMPTY_FIELDS = [NAME, SENSOR_TYPE, GP, SEVERITY]

class FB_SHOP_S:

SEVERITY_SIGNALS = {"Тушение": 1, "Пожар": 2, "Порог 2": 3, "Авария": 4, "Тревога": 5,
                        "Порог 1": 6, "Предупреждение": 8, "Недостоверность": 10,
                        "Неисправность": 12, "Отключение": 13, "Ремонт": 14, "Имитация": 16,
                        "Телесигнализация": 18, "Команда оператора": 20, "Информация": 22}

Field = namedtuple('Field', 'name, column, key')

NAME = Field(name='name', column='D', key='name')
SIREN_TYPE = Field(name='SirenType', column='N', key='siren_type')
COLOR_ON = Field(name='ColorOn', column='Q', key='color_on')
GP = Field(name='GeneralPlan', column='J', key='gp')
SOUND_ON = Field(name='SoundOn', column='P', key='sound_on')
DESCRIPTION = Field(name='Description', column='E', key='description')
SEVERITY = Field(name='SeverityOn', column='P', key='severity')
IVXX_TP = Field(name='IVXX_TP', column='Y', key='ivxx_tp')

NON_EMPTY_FIELDS = [NAME, SIREN_TYPE, GP]


class FB_QSA_S:

Field = namedtuple('Field', 'name, column, key')

NAME = Field(name='name', column='D', key='name')
E_UNIT = Field(name='EUnit', column='L', key='e_unit')
#FRAC_DIGITS = Field(name='FracDigits', column='???', key='frac_digits')
#FRAC_DIGITS - задает сколько цифр будет после запятой у аналоговых  датчиков, пока по умолчанию ставлю 2
SENSOR_POSITION = Field(name='Sensor_Position', column='N', key='sensor_position')
SENSOR_TYPE = Field(name='Sensor_Type', column='O', key='sensor_type')
DESCRIPTION = Field(name='Description', column='E', key='description')
IVXX_TP = Field(name='IVXX_TP', column='Y', key='ivxx_tp')
SUBSTANCE = Field(name='Substance', column='N', key='substance')
GP = Field(name='GeneralPlan', column='J', key='gp')
IFEX_TP = Field(name='IFEX_TP', column='AD', key='ifex_tp')
IT1X_TP = Field(name='IT1X_TP', column='Z', key='it1x_tp')
IT2X_TP = Field(name='IT2X_TP', column='AA', key='it2x_tp')

NON_EMPTY_FIELDS = [NAME, SENSOR_TYPE, GP]


class FB_DI_S:

SEVERITY_SIGNALS = {"Тушение": 1, "Пожар": 2, "Порог 2": 3, "Авария": 4, "Тревога": 5,
                    "Порог 1": 6, "Предупреждение": 8, "Недостоверность": 10,
                    "Неисправность": 12, "Отключение": 13, "Ремонт": 14, "Имитация": 16,
                    "Телесигнализация": 18, "Команда оператора": 20, "Информация": 22}

Field = namedtuple('Field', 'name, column, key')

NAME = Field(name='name', column='D', key='name')
#COLOR_OFF = Field(name='ColorOff', column='???', key='color_off')
#COLOR_OFF-отсутствует в таблице, по умолчанию "серый" поставил
COLOR_ON = Field(name='ColorOn', column='Q', key='color_on')
MESSAGE_ON = Field(name='MessageOn', column='O', key='message_on')
SEVERITY = Field(name='SeverityOn', column='P', key='severity')
SOUND_ON = Field(name='SoundOn', column='P', key='sound_on')
DESCRIPTION = Field(name='Description', column='E', key='description')
GP = Field(name='GeneralPlan', column='J', key='gp')
SENSOR_TYPE = Field(name='Sensor_Type', column='N', key='sensor_type')
IVXX_TP = Field(name='IVXX_TP', column='Y', key='ivxx_tp')

NON_EMPTY_FIELDS = [NAME, SENSOR_TYPE, GP, SEVERITY]


class FB_DO_S:

SEVERITY_SIGNALS = {"Тушение": 1, "Пожар": 2, "Порог 2": 3, "Авария": 4, "Тревога": 5,
                    "Порог 1": 6, "Предупреждение": 8, "Недостоверность": 10,
                    "Неисправность": 12, "Отключение": 13, "Ремонт": 14, "Имитация": 16,
                    "Телесигнализация": 18, "Команда оператора": 20, "Информация": 22}

Field = namedtuple('Field', 'name, column, key')

NAME = Field(name='name', column='D', key='name')
GP = Field(name='GeneralPlan', column='J', key='gp')
COLOR_ON = Field(name='ColorOn', column='Q', key='color_on')
SOUND_ON = Field(name='SoundOn', column='P', key='sound_on')
DESCRIPTION = Field(name='Description', column='E', key='description')
SEVERITY = Field(name='SeverityOn', column='P', key='severity')
OXON_TP = Field(name='OXON_TP', column='AE', key='oxon_tp')

NON_EMPTY_FIELDS = [NAME, SENSOR_TYPE, GP, SEVERITY]


class FB_AI_S:

Field = namedtuple('Field', 'name, column, key')

NAME = Field(name='name', column='D', key='name')
E_UNIT = Field(name='EUnit', column='L', key='e_unit')
#FRAC_DIGITS = Field(name='FracDigits', column='????', key='frac_digits')
PAR_NAME = Field(name='ParName', column='K', key='par_name')
SENSOR_POSITION = Field(name='Sensor_Position', column='N', key='sensor_position')
SENSOR_TYPE = Field(name='Sensor_Type', column='O', key='sensor_type')
DESCRIPTION = Field(name='Description', column='E', key='description')
IVXX_TP = Field(name='IVXX_TP', column='Y', key='ivxx_tp')
GP = Field(name='GeneralPlan', column='J', key='gp')

NON_EMPTY_FIELDS = [NAME, SENSOR_TYPE, GP]


class FB_UPG_S:

Field = namedtuple('Field', 'name, column, key')

NAME = Field(name='name', column='D', key='name')
DESCRIPTION = Field(name='Description', column='E', key='description')
SECOND_QUEUE = Field(name='SecondQueue', column='E', key='second_queue')
GP = Field(name='GeneralPlan', column='J', key='gp')

NON_EMPTY_FIELDS = [NAME, SENSOR_TYPE, GP]

