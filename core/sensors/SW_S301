from core.validators import value_is_not_none_or_empty
from core.fields import Field, SeverityField
from core.sensors import Sensor

class SW_S301(Sensor):
    BASE_TYPE = 'Types.SW_S301.SW_S301_PLC'
    CLASS_NAME = 'S301'
    Name = Field(name='name', column='D', validators=[value_is_not_none_or_empty])
    Description = Field(name='Description', column='E', validators=[value_is_not_none_or_empty])
    GP = Field(name='GeneralPlan', column='J', validators=[value_is_not_none_or_empty])
    IvxxTp = Field(name='IVXX_TP', column='Y')
    IffxTp = Field(name='IFEX_TP', column='AD')
    OxonTp = Field(name='OXON_TP', column='AE')
    IofxTp = Field(name='IOFX_TP', column='AA')
    IonxTp = Field(name='IONX_TP', column='Z')
    OrcxTp = Field(name='IRCX_TP', column='AC')
    OxofTp = Field(name='OXOF_TP', column='AF')
    IlcxTp = Field(name='ILCX_TP', column='AB')
    OxspTp = Field(name='OXSP_TP', column='AG')
    OsofTp = Field(name='ISOF_TP', column='AJ')
    IsonTp = Field(name='ISON_TP', column='AI')
    ItonTp = Field(name='ITON_TP', column='AH')

    def to_omx(self) -> str:
        omx_block = (
            f'    <ct:object {self.Name.name}="{getattr(self, self.Name.key)}" base-type="{self.BASE_TYPE}" aspect="Aspects.PLC" access-level="public" uuid="{self.pk}">\n'
            f'      <attribute type="unit.System.Attributes.{self.Description.name}" value="{getattr(self, self.Description.key)}"/>\n'
            f'      <attribute type="Attributes.{self.IffxTp.name}" value="{getattr(self, self.IffxTp.key)}"/>\n'
            f'      <attribute type="Attributes.{self.IofxTp.name}" value="{getattr(self, self.IofxTp.key)}"/>\n'
            f'      <attribute type="Attributes.{self.IonxTp.name}" value="{getattr(self, self.IonxTp.key)}"/>\n'
            f'      <attribute type="Attributes.{self.OrcxTp.name}" value="{getattr(self, self.OrcxTp.key)}"/>\n'
            f'      <attribute type="Attributes.{self.OxofTp.name}" value="{getattr(self, self.OxofTp.key)}"/>\n'
            f'      <attribute type="Attributes.{self.OxonTp.name}" value="{getattr(self, self.OxonTp.key)}"/>\n'
            f'      <attribute type="Attributes.{self.IlcxTp.name}" value="{getattr(self, self.IlcxTp.key)}"/>\n'
            f'      <attribute type="Attributes.{self.OxspTp.name}" value="{getattr(self, self.OxspTp.key)}"/>\n'
            f'      <attribute type="Attributes.{self.GP.name}" value="{getattr(self, self.GP.key)}"/>\n'
            f'      <attribute type="Attributes.{self.IsonTp.name}" value="{getattr(self, self.IsonTp.key)}"/>\n'
            f'      <attribute type="Attributes.{self.ItonTp.name}" value="{getattr(self, self.ItonTp.key)}"/>\n'
            f'    </ct:object>\n'
        )
        return omx_block
