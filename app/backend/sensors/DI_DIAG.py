from ..validators import value_is_not_none_or_empty
from ..field import Field
from ..sensor import Sensor


class DI_DIAG(Sensor):
    BASE_TYPE = "Types.DIAG.DI_DIAG.DI_DIAG_PLC"
    CLASS_NAME = "DI_DIAG"
    Name = Field(name="name", column="D", validators=[value_is_not_none_or_empty])
    MessageOn = Field(name="MessageOn", column="O", validators=[value_is_not_none_or_empty])
    Description = Field(name="Description", column="E", validators=[value_is_not_none_or_empty])
    GP = Field(name="GeneralPlan", column="J", validators=[value_is_not_none_or_empty])
    SoundOn = Field(name="SoundOn", column="P", validators=[value_is_not_none_or_empty])
    ColorOn = Field(name="ColorOn", column="Q", validators=[value_is_not_none_or_empty])

    def to_omx(self) -> str:
        omx_block = (
            f'    <ct:object {self.Name.name}="{getattr(self, self.Name.key)}" base-type="{self.BASE_TYPE}" aspect="Aspects.PLC" access-level="public" uuid="{self.pk}">\n'
            f'      <attribute type="Attributes.{self.MessageOn.name}" value="{getattr(self, self.MessageOn.key)}"/>\n'
            f'      <attribute type="unit.System.Attributes.{self.Description.name}" value="{getattr(self, self.Description.key)}"/>\n'
            f'      <attribute type="Attributes.{self.GP.name}" value="{getattr(self, self.GP.key)}"/>\n'
            f'      <attribute type="Attributes.{self.SoundOn.name}" value="{getattr(self, self.SoundOn.key)}"/>\n'
            f'      <attribute type="Attributes.{self.ColorOn.name}" value="{getattr(self, self.ColorOn.key)}"/>\n'
            f"    </ct:object>\n"
        )
        return omx_block
