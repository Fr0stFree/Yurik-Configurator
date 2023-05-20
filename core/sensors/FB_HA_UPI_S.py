from core.validators import value_is_not_none_or_empty
from core.fields import Field, SeverityField
from .sensor import Sensor

class FB_HA_UPI_S(Sensor):
    """
    Класс для работы с датчиками типа FB_UPI_S. Поле Severity отсутствует в таблице, его значение
    рассчитывается на основе значения в поле SOUND_ON.
    """
    BASE_TYPE = 'Types.FB_HA_UPI_S.FB_HA_UPI_S_PLC'
    CLASS_NAME = 'HA_UPI'
    Name = Field(name='name', column='D', validators=[value_is_not_none_or_empty])
    Description = Field(name='Description', column='E', validators=[value_is_not_none_or_empty])
    GP = Field(name='GeneralPlan', column='J', validators=[value_is_not_none_or_empty])


    def to_omx(self) -> str:
        omx_block = (
            f'    <ct:object {self.Name.name}="{getattr(self, self.Name.key)}" base-type="{self.BASE_TYPE}" aspect="Aspects.PLC" access-level="public" uuid="{self.pk}">\n'
            f'      <attribute type="unit.System.Attributes.{self.Description.name}" value="{getattr(self, self.Description.key)}"/>\n'
            f'      <attribute type="Attributes.GeneralPlan" value="ДИАГ КСПА.000.УПИ" />\n'
            f'    </ct:object>\n'
        )
        return omx_block

        #     f'      <attribute type="Attributes.{self.GP.name}" value="{getattr(self, self.GP.key)}"/>\n'
        #     f'      <attribute type="Attributes.{self.ColorOn.name}" value="{getattr(self, self.ColorOn.key)}"/>\n'
        #     f'      <attribute type="Attributes.{self.SoundOn.name}" value="{getattr(self, self.SoundOn.key)}"/>\n'
        #     f'      <attribute type="unit.System.Attributes.{self.Description.name}" value="{getattr(self, self.Description.key)}"/>\n'
        #     f'      <attribute type="Attributes.{self.Severity.name}" value="{getattr(self, self.Severity.key)}"/>\n'
        #     f'      <attribute type="Attributes.{self.OxonTp.name}" value="{getattr(self, self.OxonTp.key)}"/>\n'
        #     f'      <ct:object name="HA_UPI" access-level="public" access-scope="global" uuid="52f98c31-e644-4d88-9d76-fb8d9170d665">\n'
        #     f'      <ct:object name="UPI" base-type="Types.FB_HA_UPI_S.FB_HA_UPI_S_PLC" access-level="public" access-scope="global" aspect="Aspects.PLC" uuid="6d44e0c5-2760-4fb2-b309-7cb642d790bf">\n'
        #     f'      <attribute type="unit.System.Attributes.{self.Description.name}" value="{getattr(self, self.Description.key)}" />\n'
        #     f'      <attribute type="Attributes.GeneralPlan" value="ДИАГ КСПА.000.УПИ" />\n'
        #
        #
        #
        #
        #
        #     f'    </ct:object>\n'
        # )
        # return omx_block
