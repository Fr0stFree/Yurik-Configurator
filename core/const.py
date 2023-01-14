from collections import namedtuple

# | Яч.+переменная     | Атрибут                       | Пример           | Блоки               | Комментарий                |
# | ------------------ |:----------------------------- |:---------------- | ------------------- | -------------------------- |
# | [D**]NAME**        | Имя датчика                   | GPA_QT_100       | Все                 |                            |
# | [N]SIREN_TYPE      | Тип оповещателя               | Свет             | SHOP                |                            |
# | [Q]COLOR_ON        | Цвет при сработке             | Красный          | SHPS SHOP DI DO     |                            |
# | [J]GP              | Мнемосхема                    | ГПА31            | Все                 |                            |
# | [P]SOUND_ON        | Звук при сработке             | Пожар            | SHPS SHOP DI DO     | Под вопросом нужно или нет |
# | [E]DESCRIPTION     | Описание                      | ГПА-31.Г-р QT202 | Все                 |                            |
# | [-]SEVERITY        | Важность при сработке         | 2                | SHPS SHOP DI DO     | Формируется из SOUND_ON    |
# | [Y]IVXX_TP         | Входн. знач./Адр. подкл.      | 2+7              | SHPS SHOP QSA DI AI |                            |
# | [L]E_UNIT          | Единицы измерения             | %                | QSA AI              |                            |
# | [N]SENSOR_POSITION | Позиция датчика               | QT100            | QSA AI              |                            |
# | [O,N]SENSOR_TYPE   | Тип датчика                   | КТД-50           | SHPS QSA DI AI      | 2 SHPS AI проверить        |
# | [N]SUBSTANCE       | Тип вещества                  | Метан            | QSA                 |                            |
# | [AD]IFEX_TP        | Неисправность   пер.          | 3+1              | QSA                 | (3 модуль TREI, 1 канал)   |
# | [Z]IT1X_TP         | 1 порог                       | 3+2              | QSA                 |                            |
# | [AA]IT2X_TP        | 2 порог                       | 3+3              | QSA                 |                            |
# | [O]MESSAGE_ON      | Сообщение при сработке        | .Пожар           | SHPS DI             |                            |
# | [K]PAR_NAME        | Обозначение пар-ра в СИ       | T                | AI                  | Тип.изм.(P,L,dP,F)         |
# | [N]SECOND_QUEUE    | Нал. второй оч. г. туш.       | 1                | UPG                 |                            |
# | [-]FRAC_DIGITS     | кол-во цифр после зап. у ан-х | 2                | QSA AI              | По умолч. в функц - 2      |

#   <ct:object name="DO" access-level="public" uuid="54cd6969-f334-4893-b36b-dc9293cd4cba">
#       <attribute type="unit.Server.Attributes.NodeRelativePath" />
#       <attribute type="unit.Server.Attributes.IsObject" value="false" />

#  Эти строчки создают папку в DevStudio, для определенного типа устройств в данном случае DO.
#  Они необходимы только в первом блоке набора одного типа датчиков.


class FB_SHPS_S:
#SOUND_ON должен смотреть и вставлять в Severity
SEVERITY_SIGNALS = {"Тушение": 1, "Пожар": 2, "Порог 2": 3, "Авария": 4, "Тревога": 5,
                    "Порог 1": 6, "Предупреждение": 8, "Недостоверность": 10,
                    "Неисправность": 12, "Отключение": 13, "Ремонт": 14, "Имитация": 16,
                    "Телесигнализация": 18, "Команда оператора": 20, "Информация": 22}

Field = namedtuple('Field', 'name, column, key')

NAME = Field(name='name', column='D', key='name')
SENSOR_TYPE = Field(name='SensorType', column='N', key='sensor_type')
#COLOR_OFF-отсутствует в таблице, по умолчанию в функции установил пар-тр "Серый"
COLOR_ON = Field(name='ColorOn', column='Q', key='color_on')
GP = Field(name='GeneralPlan', column='J', key='gp')
SOUND_ON = Field(name='SoundOn', column='P', key='sound_on')
MESSAGE_ON = Field(name='MessageOn', column='O', key='message_on')
DESCRIPTION = Field(name='Description', column='E', key='description')
SEVERITY = Field(name='SeverityOn', column='???', key='severity') # SEVERITY формируется из SOUND_ON,
# если в SOUND_ON значение пожар, слдовательно в Severity будет значение "2"
IVXX_TP = Field(name='IVXX_TP', column='Y', key='ivxx_tp')

NON_EMPTY_FIELDS = [NAME, SENSOR_TYPE, GP, SOUND_ON, MESSAGE_ON, DESCRIPTION]

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
SOUND_ON = Field(name='SoundOn', column='P', key='sound_on')# под вопросом нужно или нет
DESCRIPTION = Field(name='Description', column='E', key='description')
SEVERITY = Field(name='SeverityOn', column='???', key='severity')# SEVERITY формируется из SOUND_ON
IVXX_TP = Field(name='IVXX_TP', column='Y', key='ivxx_tp')

NON_EMPTY_FIELDS = [NAME, SIREN_TYPE, GP, SOUND_ON, DESCRIPTION]


class FB_QSA_S:

Field = namedtuple('Field', 'name, column, key')

NAME = Field(name='name', column='D', key='name')
E_UNIT = Field(name='EUnit', column='L', key='e_unit')
#FRAC_DIGITS = Field(name='FracDigits', column='???', key='frac_digits')
#FRAC_DIGITS - задает сколько цифр будет после запятой у аналоговых  датчиков, пока по умолчанию ставлю 2 в функции cоздания omx
SENSOR_POSITION = Field(name='Sensor_Position', column='N', key='sensor_position')
SENSOR_TYPE = Field(name='Sensor_Type', column='O', key='sensor_type')
DESCRIPTION = Field(name='Description', column='E', key='description')
IVXX_TP = Field(name='IVXX_TP', column='Y', key='ivxx_tp')
SUBSTANCE = Field(name='Substance', column='N', key='substance')
GP = Field(name='GeneralPlan', column='J', key='gp')
IFEX_TP = Field(name='IFEX_TP', column='AD', key='ifex_tp')
IT1X_TP = Field(name='IT1X_TP', column='Z', key='it1x_tp')
IT2X_TP = Field(name='IT2X_TP', column='AA', key='it2x_tp')

NON_EMPTY_FIELDS = [NAME, GP, SUBSTANCE, E_UNIT, DESCRIPTION]


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
SEVERITY = Field(name='SeverityOn', column='P', key='severity_on')# SEVERITY формируется из SOUND_ON
SOUND_ON = Field(name='SoundOn', column='P', key='sound_on')
DESCRIPTION = Field(name='Description', column='E', key='description')
GP = Field(name='GeneralPlan', column='J', key='gp')
SENSOR_TYPE = Field(name='Sensor_Type', column='N', key='sensor_type')
IVXX_TP = Field(name='IVXX_TP', column='Y', key='ivxx_tp')

NON_EMPTY_FIELDS = [NAME, SENSOR_TYPE, GP, SOUND_ON, MESSAGE_ON, DESCRIPTION]


class FB_DO_STB_S:
#SEVERITY_SIGNALS сделать глобальной
SEVERITY_SIGNALS = {"Тушение": 1, "Пожар": 2, "Порог 2": 3, "Авария": 4, "Тревога": 5,
                    "Порог 1": 6, "Предупреждение": 8, "Недостоверность": 10,
                    "Неисправность": 12, "Отключение": 13, "Ремонт": 14, "Имитация": 16,
                    "Телесигнализация": 18, "Команда оператора": 20, "Информация": 22}

Field = namedtuple('Field', 'name, column, key')

NAME = Field(name='name', column='D', key='name')
GP = Field(name='GeneralPlan', column='J', key='gp')
COLOR_ON = Field(name='ColorOn', column='Q', key='color_on')
SOUND_ON = Field(name='SoundOn', column='P', key='sound_on')# под впоросом, нужен ли он. Узнать!
DESCRIPTION = Field(name='Description', column='E', key='description')
SEVERITY = Field(name='SeverityOn', column='???', key='severity')#вычисляется значение из SOUND_ON
OXON_TP = Field(name='OXON_TP', column='AE', key='oxon_tp')

NON_EMPTY_FIELDS = [NAME, GP, SOUND_ON, DESCRIPTION]


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

NON_EMPTY_FIELDS = [NAME, SENSOR_TYPE, GP, PAR_NAME, E_UNIT, DESCRIPTION]


class FB_UPG_S:

Field = namedtuple('Field', 'name, column, key')

NAME = Field(name='name', column='D', key='name')
DESCRIPTION = Field(name='Description', column='E', key='description')
SECOND_QUEUE = Field(name='SecondQueue', column='N', key='second_queue')
GP = Field(name='GeneralPlan', column='J', key='gp')

NON_EMPTY_FIELDS = [NAME, GP, DESCRIPTION, SECOND_QUEUE]


class FB_UPP_S:
# пенное тушение
Field = namedtuple('Field', 'name, column, key')

NAME = Field(name='name', column='D', key='name')
DESCRIPTION = Field(name='Description', column='E', key='description')
GP = Field(name='GeneralPlan', column='J', key='gp')

NON_EMPTY_FIELDS = [NAME, GP, DESCRIPTION]

