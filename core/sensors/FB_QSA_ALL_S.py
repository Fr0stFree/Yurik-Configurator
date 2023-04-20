# <ct:object name="QSA_ALL" access-level="public" access-scope="global" uuid="843d91cc-c360-422f-a890-7a0c50896379">
#     <attribute type="unit.Server.Attributes.NodeRelativePath" />
#     <attribute type="unit.Server.Attributes.IsObject" value="false" />
#     <ct:object name="GP001_QSA_01" base-type="Types.FB_QSA_ALL.FB_QSA_ALL_PLC" access-level="public" access-scope="global" aspect="Aspects.PLC" uuid="fc18af05-0d22-4a81-8e72-9a547a61b638">
#       <attribute type="unit.System.Attributes.Description" value="ГП 1. Помещение пробкоуловителей" />
#       <attribute type="Attributes.GeneralPlan" value="ГП001" />
#     </ct:object>
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!НОВЫЙ ДАТЧИК! ОБЯЗАТЕЛЬНО ВСЁ ПРОВЕРИТЬ!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
from core.validators import value_is_not_none_or_empty
from core.fields import Field, SeverityField
from .sensor import Sensor


class FB_QSA_ALL(Sensor):
    """
    Класс для работы с датчиками типа FB_QSA_ALL. Поле Severity отсутствует в таблице, его значение
    рассчитывается на основе значения в поле SOUND_ON.
    """
    BASE_TYPE = 'Types.FB_QSA_ALL.FB_QSA_ALL_PLC'
    CLASS_NAME = 'QSA_ALL'
    Name = Field(name='name', column='D', validators=[value_is_not_none_or_empty])
    Description = Field(name='Description', column='E', validators=[value_is_not_none_or_empty])
    GP = Field(name='GeneralPlan', column='J', validators=[value_is_not_none_or_empty])

    def to_omx(self) -> str:
        omx_block = (
            f'    <ct:object {self.Name.name}="{getattr(self, self.Name.key)}" base-type="{self.BASE_TYPE}" aspect="Aspects.PLC" access-level="public" uuid="{self.pk}">\n'
            f'      <attribute type="unit.System.Attributes.{self.Description.name}" value="{getattr(self, self.Description.key)}"/>\n'
            f'      <attribute type="Attributes.{self.GP.name}" value="{getattr(self, self.GP.key)}"/>\n'
            f'    </ct:object>\n'
        )
        return omx_block
