from core.validators import value_is_not_none_or_empty
from core.fields import Field
from .sensor import Sensor


class FB_QSA_S(Sensor):
    """
    Класс для работы с датчиками типа FB_QSA_S. Поле Severity отсутствует в таблице, его значение
    рассчитывается на основе значения в поле SOUND_ON.
    """
    BASE_TYPE = 'Types.FB_QSA_S.FB_QSA_S_PLC'
    CLASS_NAME = 'QSA'
    Name = Field(name='name', column='D', validators=[value_is_not_none_or_empty])
    EUnit = Field(name='EUnit', column='L', validators=[value_is_not_none_or_empty])
    SensorType = Field(name='Sensor_Type', column='O', validators=[value_is_not_none_or_empty])
    SensorPosition = Field(name='Sensor_Position', column='N')
    GP = Field(name='GeneralPlan', column='J', validators=[value_is_not_none_or_empty])
    Description = Field(name='Description', column='E', validators=[value_is_not_none_or_empty])
    IvxxTp = Field(name='IVXX_TP', column='Y')
    Substance = Field(name='Substance', column='N', validators=[value_is_not_none_or_empty])
    IfexTp = Field(name='IFEX_TP', column='AD')
    It1xTp = Field(name='IT1X_TP', column='Z')
    It2xTp = Field(name='IT2X_TP', column='AA')

    def to_omx(self) -> str:
        omx_block = (
            f'    <ct:object {self.Name.name}="{getattr(self, self.Name.key)}" base-type="{self.BASE_TYPE}" aspect="Aspects.PLC" access-level="public" uuid="{self.pk}">\n'
            f'      <attribute type="Attributes.{self.EUnit.name}" value="{getattr(self, self.EUnit.key)}"/>\n'
            f'      <attribute type="Attributes.FracDigits" value="2" />\n'
            f'      <attribute type="Attributes.{self.SensorPosition.name}" value="{getattr(self, self.SensorPosition.key)}"/>\n'
            f'      <attribute type="Attributes.{self.SensorType.name}" value="{getattr(self, self.SensorType.key)}"/>\n'
            f'      <attribute type="unit.System.Attributes.{self.Description.name}" value="{getattr(self, self.Description.key)}"/>\n'
            f'      <attribute type="Attributes.{self.IvxxTp.name}" value="{getattr(self, self.IvxxTp.key)}"/>\n'
            f'      <attribute type="Attributes.{self.Substance.name}" value="{getattr(self, self.Substance.key)}"/>\n'
            f'      <attribute type="Attributes.{self.GP.name}" value="{getattr(self, self.GP.key)}"/>\n'
            f'      <attribute type="Attributes.{self.IfexTp.name}" value="{getattr(self, self.IfexTp.key)}"/>\n'
            f'      <attribute type="Attributes.{self.It1xTp.name}" value="{getattr(self, self.It1xTp.key)}"/>\n'
            f'      <attribute type="Attributes.{self.It2xTp.name}" value="{getattr(self, self.It2xTp.key)}"/>\n'
            f'    </ct:object>\n'
        )
        return omx_block
