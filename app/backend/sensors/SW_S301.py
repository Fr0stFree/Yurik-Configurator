from ..validators import value_is_not_none_or_empty
from ..field import Field
from ..sensor import Sensor


class SW_S301(Sensor):
    BASE_TYPE = "Types.DIAG.SW_S301.SW_S301_PLC"
    CLASS_NAME = "S301"
    Name = Field(name="name", column="D", validators=[value_is_not_none_or_empty])
    Description = Field(name="Description", column="E", validators=[value_is_not_none_or_empty])
    GP = Field(name="GeneralPlan", column="J", validators=[value_is_not_none_or_empty])
    AbonentPort1 = Field(name="AbonentPort1", column="Y")
    AbonentPort2 = Field(name="AbonentPort2", column="AD")
    AbonentPort3 = Field(name="AbonentPort3", column="AE")
    AbonentPort4 = Field(name="AbonentPort4", column="AA")
    AbonentPort5 = Field(name="AbonentPort5", column="Z")
    AbonentPort6 = Field(name="AbonentPort6", column="AC")
    AbonentPort7 = Field(name="AbonentPort7", column="AF")
    AbonentPort8 = Field(name="AbonentPort8", column="AB")
    AbonentPort9 = Field(name="AbonentPort9", column="AG")
    AbonentPort10 = Field(name="AbonentPort10", column="AJ")

    def to_omx(self) -> str:
        omx_block = (
            f'    <ct:object {self.Name.name}="{getattr(self, self.Name.key)}" base-type="{self.BASE_TYPE}" aspect="Aspects.PLC" access-level="public" uuid="{self.pk}">\n'
            f'      <attribute type="unit.System.Attributes.{self.Description.name}" value="{getattr(self, self.Description.key)}"/>\n'
            f'      <attribute type="Attributes.{self.AbonentPort1.name}" value="{getattr(self, self.AbonentPort1.key)}"/>\n'
            f'      <attribute type="Attributes.{self.AbonentPort2.name}" value="{getattr(self, self.AbonentPort2.key)}"/>\n'
            f'      <attribute type="Attributes.{self.AbonentPort3.name}" value="{getattr(self, self.AbonentPort3.key)}"/>\n'
            f'      <attribute type="Attributes.{self.AbonentPort4.name}" value="{getattr(self, self.AbonentPort4.key)}"/>\n'
            f'      <attribute type="Attributes.{self.AbonentPort5.name}" value="{getattr(self, self.AbonentPort5.key)}"/>\n'
            f'      <attribute type="Attributes.{self.AbonentPort6.name}" value="{getattr(self, self.AbonentPort6.key)}"/>\n'
            f'      <attribute type="Attributes.{self.AbonentPort7.name}" value="{getattr(self, self.AbonentPort7.key)}"/>\n'
            f'      <attribute type="Attributes.{self.AbonentPort8.name}" value="{getattr(self, self.AbonentPort8.key)}"/>\n'
            f'      <attribute type="Attributes.{self.GP.name}" value="{getattr(self, self.GP.key)}"/>\n'
            f'      <attribute type="Attributes.{self.AbonentPort9.name}" value="{getattr(self, self.AbonentPort9.key)}"/>\n'
            f'      <attribute type="Attributes.{self.AbonentPort10.name}" value="{getattr(self, self.AbonentPort10.key)}"/>\n'
            f"    </ct:object>\n"
        )
        return omx_block
