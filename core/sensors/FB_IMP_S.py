# <ct:object name="IMp" access-level="public" access-scope="global" uuid="a10470aa-cbdc-49c1-ae60-665208b5c7e1">
#     <attribute type="unit.Server.Attributes.NodeRelativePath" />
#     <attribute type="unit.Server.Attributes.IsObject" value="false" />
#     <ct:object name="GP001_V_01" base-type="Types.FB_IMp_S.FB_IMp_S_PLC" access-level="public" access-scope="global" aspect="Aspects.PLC" uuid="31c4bb26-0f8e-4897-80cd-2490a135e395">
#       <attribute type="unit.System.Attributes.Description" value="ГП 1. Вентилятор В1" />
#       <attribute type="Attributes.IFXX_TP" value="-" />
#       <attribute type="Attributes.IOFX_TP" value="-" />
#       <attribute type="Attributes.IONX_TP" value="-" />
#       <attribute type="Attributes.IRCX_TP" value="-" />
#       <attribute type="Attributes.OXOF_TP" value="-" />
#       <attribute type="Attributes.OXON_TP" value="-" />
#       <attribute type="Attributes.ILCX_TP" value="-" />
#       <attribute type="Attributes.OXSP_TP" value="-" />
#       <attribute type="Attributes.GeneralPlan" value="ГП001" />
#       <attribute type="Attributes.ISOF_TP" value="-" />
#       <attribute type="Attributes.ISON_TP" value="-" />
#     </ct:object>

from core.validators import value_is_not_none_or_empty
from core.fields import Field, SeverityField
from .sensor import Sensor

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!НОВЫЙ ДАТЧИК! ОБЯЗАТЕЛЬНО ВСЁ ПРОВЕРИТЬ!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
class FB_IMp_S(Sensor):
    """
    Класс для работы с датчиками типа FB_IMP_S. Поле Severity отсутствует в таблице, его значение
    рассчитывается на основе значения в поле SOUND_ON.
    """
    BASE_TYPE = 'Types.FB_IMP_S.FB_IMP_S_PLC'
    CLASS_NAME = 'FB_IMp_S'
    Name = Field(name='name', column='D', validators=[value_is_not_none_or_empty])
   


    ColorOn = Field(name='ColorOn', column='Q')
        SoundOn = Field(name='SoundOn', column='P', validators=[value_is_not_none_or_empty])
    Description = Field(name='Description', column='E', validators=[value_is_not_none_or_empty])
    IfxxTp = Field(name='IFXX_TP', column='AD')
    IofxTp = Field(name='IOFX_TP', column='AA')
    IonxTp = Field(name='IONX_TP', column='Z')
    OrcxTp = Field(name='IRCX_TP', column='AC')
    OxofTp = Field(name='OXOF_TP', column='AF')
    OxonTp = Field(name='OXON_TP', column='AE')
    IlcxTp = Field(name='ILCX_TP', column='AB')
    OxspTp = Field(name='OXSP_TP', column='AG')
    GP = Field(name='GeneralPlan', column='J', validators=[value_is_not_none_or_empty])
    OsofTp = Field(name='ISOF_TP', column='AJ')
    #IsonTp = Field(name='ISON_TP', column='AE') НЕ НАШЕЛ В ТАБЛИЦЕ


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
            f'    </ct:object>\n'
        )
        return omx_block
