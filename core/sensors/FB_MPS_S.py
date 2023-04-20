# <ct:object name="MPS" access-level="public" access-scope="global" uuid="25c8e6ee-b54f-4199-a249-a5d158e36b09">
#     <attribute type="unit.Server.Attributes.NodeRelativePath" />
#     <attribute type="unit.Server.Attributes.IsObject" value="false" />
#     <ct:object name="MOPS_02_01" base-type="Types.DIAG.FB_MPS_S.FB_MPS_S_PLC" access-level="public" access-scope="global" aspect="Aspects.PLC" uuid="85d83706-6ea0-4e09-afd7-eabb5ded6f6e">
#       <attribute type="unit.System.Attributes.Description" value="КСПА 001 УСО1. 2MOPS1" />
#       <attribute type="Attributes.GeneralPlan" value="ГП001" />
#     </ct:object>
from core.validators import value_is_not_none_or_empty
from core.fields import Field, SeverityField
from .sensor import Sensor

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!НОВЫЙ ДАТЧИК! ОБЯЗАТЕЛЬНО ВСЁ ПРОВЕРИТЬ!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
class FB_MPS_S(Sensor):
    """
    Класс для работы с датчиками типа FB_MPS_S. Поле Severity отсутствует в таблице, его значение
    рассчитывается на основе значения в поле SOUND_ON.
    """
    BASE_TYPE = 'Types.FB_MPS_S.FB_MPS_S_PLC'
    CLASS_NAME = 'MPS_STB'
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
