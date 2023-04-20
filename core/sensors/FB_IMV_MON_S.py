# <ct:object name="IMv_MON" access-level="public" access-scope="global" uuid="881e5461-2fc0-453e-92c5-b64ce7e9efce">
#     <attribute type="unit.Server.Attributes.NodeRelativePath" />
#     <attribute type="unit.Server.Attributes.IsObject" value="false" />
#     <ct:object name="GP001_BP_01" base-type="Types.FB_IMv_MON_S.FB_IMv_MON_S_PLC" access-level="public" access-scope="global" aspect="Aspects.PLC" uuid="7b5874b0-8ef7-42e5-b2fc-ae91aba72242">
#       <attribute type="unit.System.Attributes.Description" value="ГП 1. Клапан дренчерный К1" />
#       <attribute type="Attributes.IFXX_TP" value="-" />
#       <attribute type="Attributes.IOFX_TP" value="-" />
#       <attribute type="Attributes.IONX_TP" value="-" />
#       <attribute type="Attributes.GeneralPlan" value="ГП001" />
#     </ct:object>

from core.validators import value_is_not_none_or_empty
from core.fields import Field, SeverityField
from .sensor import Sensor
##!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!НОВЫЙ ДАТЧИК! ОБЯЗАТЕЛЬНО ВСЁ ПРОВЕРИТЬ!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
class FB_IMv_MON_S(Sensor):
    """
    Класс для работы с датчиками типа FB_IMv_S. Поле Severity отсутствует в таблице, его значение
    рассчитывается на основе значения в поле SOUND_ON.
    """
    BASE_TYPE = 'Types.FB_IMv_MON_S.FB_IMv_MON_S_PLC'
    CLASS_NAME = 'FB_IMv_MON_S'
    Name = Field(name='name', column='D', validators=[value_is_not_none_or_empty])
    Description = Field(name='Description', column='E', validators=[value_is_not_none_or_empty])
    IfxxTp = Field(name='IFXX_TP', column='AD')
    IofxTp = Field(name='IOFX_TP', column='AA')
    IonxTp = Field(name='IONX_TP', column='Z')
    GP = Field(name='GeneralPlan', column='J', validators=[value_is_not_none_or_empty])


    def to_omx(self) -> str:
        omx_block = (
            f'    <ct:object {self.Name.name}="{getattr(self, self.Name.key)}" base-type="{self.BASE_TYPE}" aspect="Aspects.PLC" access-level="public" uuid="{self.pk}">\n'
            f'      <attribute type="unit.System.Attributes.{self.Description.name}" value="{getattr(self, self.Description.key)}"/>\n'
            f'      <attribute type="Attributes.{self.IfxxTp.name}" value="{getattr(self, self.IfxxTp.key)}"/>\n'
            f'      <attribute type="Attributes.{self.IofxTp.name}" value="{getattr(self, self.IofxTp.key)}"/>\n'
            f'      <attribute type="Attributes.{self.IonxTp.name}" value="{getattr(self, self.IonxTp.key)}"/>\n'
            f'      <attribute type="Attributes.{self.GP.name}" value="{getattr(self, self.GP.key)}"/>\n'
            f'    </ct:object>\n'
        )
        return omx_block
