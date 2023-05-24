from core.validators import value_is_not_none_or_empty
from core.fields import Field, SeverityField
from .sensor import Sensor


class FB_DO_STB_S(Sensor):
    """
    Класс для работы с датчиками типа FB_DO_STB_S. Поле Severity отсутствует в таблице, его значение
    рассчитывается на основе значения в поле SOUND_ON.
    """
    BASE_TYPE = 'Types.FB_DO_STB_S.FB_DO_STB_S_PLC'
    CLASS_NAME = 'DO'
    Name = Field(name='name', column='D', validators=[value_is_not_none_or_empty])
    ColorOn = Field(name='ColorOn', column='Q', validators=[value_is_not_none_or_empty])
    GP = Field(name='GeneralPlan', column='J', validators=[value_is_not_none_or_empty])
    Description = Field(name='Description', column='E', validators=[value_is_not_none_or_empty])
    SirenType = Field(name='SirenType', column='N', validators=[value_is_not_none_or_empty])
    OxonTp = Field(name='OXON_TP', column='AE')

    def to_omx(self) -> str:
        omx_block = (
            f'    <ct:object {self.Name.name}="{getattr(self, self.Name.key)}" base-type="{self.BASE_TYPE}" aspect="Aspects.PLC" access-level="public" uuid="{self.pk}">\n'
            f'      <attribute type="Attributes.{self.GP.name}" value="{getattr(self, self.GP.key)}"/>\n'
            f'      <attribute type="Attributes.{self.ColorOn.name}" value="{getattr(self, self.ColorOn.key)}"/>\n'
            f'      <attribute type="unit.System.Attributes.{self.Description.name}" value="{getattr(self, self.Description.key)}"/>\n'
            f'      <attribute type="Attributes.{self.SirenType.name}" value="{getattr(self, self.SirenType.key)}"/>\n'
            f'      <attribute type="Attributes.{self.OxonTp.name}" value="{getattr(self, self.OxonTp.key)}"/>\n'
            f'    </ct:object>\n'
        )
        return omx_block


