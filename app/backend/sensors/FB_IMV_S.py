from ..validators import value_is_not_none_or_empty
from ..field import Field
from ..sensor import Sensor


class FB_IMv_S(Sensor):
    """
    Класс для работы с датчиками типа FB_DO_STB_S. Поле Severity отсутствует в таблице, его значение
    рассчитывается на основе значения в поле SOUND_ON.
    """

    BASE_TYPE = "Types.FB_IMv_S.FB_IMv_S_PLC"
    CLASS_NAME = "IMv"
    Name = Field(name="name", column="D", validators=[value_is_not_none_or_empty])
    Description = Field(name="Description", column="E", validators=[value_is_not_none_or_empty])
    IfxxTp = Field(name="IFXX_TP", column="AD")
    IofxTp = Field(name="IOFX_TP", column="AA")
    IonxTp = Field(name="IONX_TP", column="Z")
    OrcxTp = Field(name="IRCX_TP", column="AC")
    OxofTp = Field(name="OXOF_TP", column="AF")
    OxonTp = Field(name="OXON_TP", column="AE")
    IlcxTp = Field(name="ILCX_TP", column="AB")
    OxspTp = Field(name="OXSP_TP", column="AG")
    GP = Field(name="GeneralPlan", column="J", validators=[value_is_not_none_or_empty])
    OsofTp = Field(name="ISOF_TP", column="AJ")
    IsonTp = Field(name="ISON_TP", column="AI")

    def to_omx(self) -> str:
        omx_block = (
            f'    <ct:object {self.Name.name}="{getattr(self, self.Name.key)}" base-type="{self.BASE_TYPE}" aspect="Aspects.PLC" access-level="public" uuid="{self.pk}">\n'
            f'      <attribute type="unit.System.Attributes.{self.Description.name}" value="{getattr(self, self.Description.key)}"/>\n'
            f'      <attribute type="Attributes.{self.IfxxTp.name}" value="{getattr(self, self.IfxxTp.key)}"/>\n'
            f'      <attribute type="Attributes.{self.IofxTp.name}" value="{getattr(self, self.IofxTp.key)}"/>\n'
            f'      <attribute type="Attributes.{self.IonxTp.name}" value="{getattr(self, self.IonxTp.key)}"/>\n'
            f'      <attribute type="Attributes.{self.OrcxTp.name}" value="{getattr(self, self.OrcxTp.key)}"/>\n'
            f'      <attribute type="Attributes.{self.OxofTp.name}" value="{getattr(self, self.OxofTp.key)}"/>\n'
            f'      <attribute type="Attributes.{self.OxonTp.name}" value="{getattr(self, self.OxonTp.key)}"/>\n'
            f'      <attribute type="Attributes.{self.IlcxTp.name}" value="{getattr(self, self.IlcxTp.key)}"/>\n'
            f'      <attribute type="Attributes.{self.OxspTp.name}" value="{getattr(self, self.OxspTp.key)}"/>\n'
            f'      <attribute type="Attributes.{self.GP.name}" value="{getattr(self, self.GP.key)}"/>\n'
            f'      <attribute type="Attributes.{self.OsofTp.name}" value="{getattr(self, self.OsofTp.key)}"/>\n'
            f'      <attribute type="Attributes.ISON_TP" value="-" />\n'
            f"    </ct:object>\n"
        )
        return omx_block
