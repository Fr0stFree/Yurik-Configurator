from core.validators import value_is_not_none_or_empty
from core.fields import Field, SeverityField
from .sensor import Sensor


class FB_AI_S(Sensor):
    """
    Класс для работы с датчиками типа FB_AI_S. Поле Severity отсутствует в таблице, его значение
    рассчитывается на основе значения в поле SOUND_ON.
    """
    BASE_TYPE = 'Types.FB_AI_S.FB_AI_S_PLC'
    CLASS_NAME = 'AI  '
    Name = Field(name='name', column='D', validators=[value_is_not_none_or_empty])
    EUnit = Field(name='EUnit', column='L', validators=[value_is_not_none_or_empty])
    ParName = Field(name='ParName', column='K', validators=[value_is_not_none_or_empty])
    SensorType = Field(name='Sensor_Type', column='O', validators=[value_is_not_none_or_empty])
    SensorPosition = Field(name='Sensor_Position', column='N')
    GP = Field(name='GeneralPlan', column='J', validators=[value_is_not_none_or_empty])
    Description = Field(name='Description', column='E', validators=[value_is_not_none_or_empty])
    IvxxTp = Field(name='IVXX_TP', column='Y')

    def to_omx(self) -> str:
        omx_block = (
            f'    <ct:object {self.Name.name}="{getattr(self, self.Name.key)}" base-type="{self.BASE_TYPE}" aspect="Aspects.PLC" access-level="public" uuid="{self.pk}">\n'
            f'      <attribute type="Attributes.{self.EUnit.name}" value="{getattr(self, self.EUnit.key)}"/>\n'
            f'      <attribute type="Attributes.FracDigits" value="2" />\n'
            f'      <attribute type="Attributes.{self.ParName.name}" value="{getattr(self, self.ParName.key)}"/>\n'
            f'      <attribute type="Attributes.{self.SensorPosition.name}" value="{getattr(self, self.SensorPosition.key)}"/>\n'
            f'      <attribute type="Attributes.{self.SensorType.name}" value="{getattr(self, self.SensorType.key)}"/>\n'
            f'      <attribute type="unit.System.Attributes.{self.Description.name}" value="{getattr(self, self.Description.key)}"/>\n'
            f'      <attribute type="Attributes.{self.IvxxTp.name}" value="{getattr(self, self.IvxxTp.key)}"/>\n'
            f'      <attribute type="Attributes.{self.GP.name}" value="{getattr(self, self.GP.key)}"/>\n'
            f'    </ct:object>\n'
        )
        return omx_block
