from core.validators import value_is_not_none_or_empty
from core.fields import Field, SeverityField
from .sensor import Sensor


class FB_DI_S(Sensor):
    """
    Класс для работы с датчиками типа FB_DI_S. Поле Severity отсутствует в таблице, его значение
    рассчитывается на основе значения в поле SOUND_ON.
    """
    BASE_TYPE = 'Types.FB_DI_S.FB_DI_S_PLC'
    CLASS_NAME = 'DI'
    Name = Field(name='name', column='D', validators=[value_is_not_none_or_empty])
    SensorType = Field(name='SensorType', column='O', validators=[value_is_not_none_or_empty])
    ColorOn = Field(name='ColorOn', column='Q')
    GP = Field(name='GeneralPlan', column='J', validators=[value_is_not_none_or_empty])
    SoundOn = Field(name='SoundOn', column='P', validators=[value_is_not_none_or_empty])
    MessageOn = Field(name='MessageOn', column='O', validators=[value_is_not_none_or_empty])
    Description = Field(name='Description', column='E', validators=[value_is_not_none_or_empty])
    Severity = SeverityField(name='SeverityOn', column='P')
    IvxxTp = Field(name='IVXX_TP', column='Y')

    def to_omx(self) -> str:
        omx_block = (
            f'    <ct:object {self.Name.name}="{getattr(self, self.Name.key)}" base-type="{self.BASE_TYPE}" aspect="Aspects.PLC" access-level="public" uuid="{self.pk}">\n'
            f'      <attribute type="Attributes.ColorOff" value="Серый" />\n'
            f'      <attribute type="Attributes.{self.ColorOn.name}" value="{getattr(self, self.ColorOn.key)}"/>\n'
            f'      <attribute type="Attributes.{self.MessageOn.name}" value="{getattr(self, self.MessageOn.key)}"/>\n'
            f'      <attribute type="Attributes.{self.Severity.name}" value="{getattr(self, self.Severity.key)}"/>\n'
            f'      <attribute type="Attributes.{self.SoundOn.name}" value="{getattr(self, self.SoundOn.key)}"/>\n'
            f'      <attribute type="unit.System.Attributes.{self.Description.name}" value="{getattr(self, self.Description.key)}"/>\n'
            f'      <attribute type="Attributes.{self.GP.name}" value="{getattr(self, self.GP.key)}"/>\n'
            f'      <attribute type="Attributes.{self.SensorType.name}" value="{getattr(self, self.SensorType.key)}"/>\n'
            f'      <attribute type="Attributes.{self.IvxxTp.name}" value="{getattr(self, self.IvxxTp.key)}"/>\n'
            f'    </ct:object>\n'
        )
        return omx_block
