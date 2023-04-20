# <ct:object name="BTF" access-level="public" access-scope="global" uuid="316fd334-7992-483b-9660-cce7126cf8a0">
#     <attribute type="unit.Server.Attributes.NodeRelativePath" />
#     <attribute type="unit.Server.Attributes.IsObject" value="false" />
#     <ct:object name="GP001_BTF_11_01" base-type="Types.FB_BTF_S.FB_BTF_S_PLC" access-level="public" access-scope="global" aspect="Aspects.PLC" uuid="095471d8-5ccc-472d-96d7-de94e0a2662f">
#       <attribute type="Attributes.SensorType" value="6" />
#       <attribute type="Attributes.SoundOn" value="Тревога" />
#       <attribute type="Attributes.MessageOn" value=". Внимание" />
#       <attribute type="unit.System.Attributes.Description" value="ГП 1. ИП пламени BTF11/1" />
#       <attribute type="Attributes.SeverityOn" value="5" />
#       <attribute type="Attributes.GeneralPlan" value="ГП001" />
#       <attribute type="Attributes.IFEX_TP" value="-" />
#       <attribute type="Attributes.IVXX_TP" value="-" />
#     </ct:object>
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!НОВЫЙ ДАТЧИК! ОБЯЗАТЕЛЬНО ВСЁ ПРОВЕРИТЬ!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
from core.validators import value_is_not_none_or_empty
from core.fields import Field, SeverityField
from core.sensors import Sensor

class FB_BTF_S(Sensor):
    """
    Класс для работы с датчиками типа FB_BTF_S. Поле Severity отсутствует в таблице, его значение
    рассчитывается на основе значения в поле SOUND_ON.
    """
    BASE_TYPE = 'Types.FB_BTF_S.FB_BTF_S_PLC'
    CLASS_NAME = 'BTF'
    Name = Field(name='name', column='D', validators=[value_is_not_none_or_empty])
    SensorType = Field(name='Sensor_Type', column='O', validators=[value_is_not_none_or_empty])
    SoundOn = Field(name='SoundOn', column='P', validators=[value_is_not_none_or_empty])
    MessageOn = Field(name='MessageOn', column='O', validators=[value_is_not_none_or_empty])
    Description = Field(name='Description', column='E', validators=[value_is_not_none_or_empty])
    Severity = SeverityField(name='SeverityOn', column='P')
    GP = Field(name='GeneralPlan', column='J', validators=[value_is_not_none_or_empty])
    IfexTp = Field(name='IFEX_TP', column='AD')
    IvxxTp = Field(name='IVXX_TP', column='Y')

    def to_omx(self) -> str:
        omx_block = (
            f'    <ct:object {self.Name.name}="{getattr(self, self.Name.key)}" base-type="{self.BASE_TYPE}" aspect="Aspects.PLC" access-level="public" uuid="{self.pk}">\n'
            f'      <attribute type="Attributes.{self.SensorType.name}" value="{getattr(self, self.SensorType.key)}"/>\n'
            f'      <attribute type="Attributes.{self.SoundOn.name}" value="{getattr(self, self.SoundOn.key)}"/>\n'
            f'      <attribute type="Attributes.{self.MessageOn.name}" value="{getattr(self, self.MessageOn.key)}"/>\n'
            f'      <attribute type="unit.System.Attributes.{self.Description.name}" value="{getattr(self, self.Description.key)}"/>\n'
            f'      <attribute type="Attributes.{self.Severity.name}" value="{getattr(self, self.Severity.key)}"/>\n'
            f'      <attribute type="Attributes.{self.GP.name}" value="{getattr(self, self.GP.key)}"/>\n'
            f'      <attribute type="Attributes.{self.IfexTp.name}" value="{getattr(self, self.IfexTp.key)}"/>\n'
            f'      <attribute type="Attributes.{self.IvxxTp.name}" value="{getattr(self, self.IvxxTp.key)}"/>\n'
            f'    </ct:object>\n'
        )
        return omx_block