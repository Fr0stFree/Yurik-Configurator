from ..validators import value_is_not_none_or_empty
from ..field import Field
from ..sensor import Sensor


class M957D(Sensor):
    BASE_TYPE = "Types.DIAG.M957D.M957D_PLC"
    CLASS_NAME = "M957D"
    Name = Field(name="name", column="D", validators=[value_is_not_none_or_empty])
    Description = Field(name="Description", column="E", validators=[value_is_not_none_or_empty])
    GP = Field(name="GeneralPlan", column="J", validators=[value_is_not_none_or_empty])

    def to_omx(self) -> str:
        omx_block = (
            f'    <ct:object {self.Name.name}="{getattr(self, self.Name.key)}" base-type="{self.BASE_TYPE}" aspect="Aspects.PLC" access-level="public" uuid="{self.pk}">\n'
            f'      <attribute type="unit.System.Attributes.{self.Description.name}" value="{getattr(self, self.Description.key)}"/>\n'
            f'      <attribute type="Attributes.{self.GP.name}" value="{getattr(self, self.GP.key)}"/>\n'
            f"    </ct:object>\n"
        )
        return omx_block
