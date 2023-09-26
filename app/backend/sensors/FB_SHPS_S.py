from ..validators import value_is_not_none_or_empty
from ..field import Field, SeverityField
from ..sensor import Sensor


class FB_SHPS_S(Sensor):
    """
    Класс для работы с датчиками типа FB_SHPS_S. Поле Severity отсутствует в таблице, его значение
    рассчитывается на основе значения в поле SOUND_ON.
    """

    BASE_TYPE = "Types.FB_SHPS_S.FB_SHPS_S_PLC"
    CLASS_NAME = "SHPS"
    Name = Field(name="name", column="D", validators=[value_is_not_none_or_empty])
    SensorType = Field(name="SensorType", column="N", validators=[value_is_not_none_or_empty])
    ColorOn = Field(name="ColorOn", column="Q", validators=[value_is_not_none_or_empty])
    GP = Field(name="GeneralPlan", column="J", validators=[value_is_not_none_or_empty])
    SoundOn = Field(name="SoundOn", column="P", validators=[value_is_not_none_or_empty])
    MessageOn = Field(name="MessageOn", column="O", validators=[value_is_not_none_or_empty])
    Description = Field(name="Description", column="E", validators=[value_is_not_none_or_empty])
    Severity = SeverityField(name="SeverityOn", column="P")
    IvxxTp = Field(name="IVXX_TP", column="Y")

    def to_omx(self) -> str:
        omx_block = (
            f'    <ct:object {self.Name.name}="{getattr(self, self.Name.key)}" base-type="{self.BASE_TYPE}" aspect="Aspects.PLC" access-level="public" uuid="{self.pk}">\n'
            f'      <attribute type="Attributes.{self.SensorType.name}" value="{getattr(self, self.SensorType.key)}"/>\n'
            f'      <attribute type="Attributes.ColorOff" value="Серый" />\n'
            f'      <attribute type="Attributes.{self.ColorOn.name}" value="{getattr(self, self.ColorOn.key)}"/>\n'
            f'      <attribute type="Attributes.{self.GP.name}" value="{getattr(self, self.GP.key)}"/>\n'
            f'      <attribute type="Attributes.{self.SoundOn.name}" value="{getattr(self, self.SoundOn.key)}"/>\n'
            f'      <attribute type="Attributes.{self.MessageOn.name}" value="{getattr(self, self.MessageOn.key)}"/>\n'
            f'      <attribute type="unit.System.Attributes.{self.Description.name}" value="{getattr(self, self.Description.key)}"/>\n'
            f'      <attribute type="Attributes.{self.Severity.name}" value="{getattr(self, self.Severity.key)}"/>\n'
            f'      <attribute type="Attributes.{self.IvxxTp.name}" value="{getattr(self, self.IvxxTp.key)}"/>\n'
            f"    </ct:object>\n"
        )
        return omx_block

    def to_hmi(self, index: int) -> str:
        hmi_block = (
            f'    <object access-modifier="private" name="{getattr(self, self.Name.key)}" display-name="{getattr(self, self.Name.key)}" uuid="{self.pk}" base-type="{self.BASE_TYPE}" base-type-id="486dd59f-52d3-4c14-a25d-e54fb8eb80f6" ver="5">\n'
            f'        <designed target="X" value="-138.75" ver="5"/>\n'
            f'        <designed target="Y" value="81" ver="5"/>\n'
            f'        <designed target="Rotation" value="0" ver="5"/>\n'
            f'        <init target="_init_APSource" ver="5" ref="unit.Global.ApMain"/>\n'
            f'        <init target="_init_Object" ver="5" value="KSPA001_SHU.GP001_BTH_01"/>\n'
            f"    </object>\n"
            f'    <object access-modifier="private" name="Text_393" display-name="Text_393" uuid="{self.pk}" base-type="Text" base-type-id="21d59f8d-2ca4-4592-92ca-b4dc48992a0f" ver="4">\n'
            f'        <designed target="X" value="9.16665" ver="4"/>\n'
            f'        <designed target="Y" value="43" ver="4"/>\n'
            f'        <designed target="ZValue" value="0" ver="4"/>\n'
            f'        <designed target="Rotation" value="0" ver="4"/>\n'
            f'        <designed target="Scale" value="1" ver="4"/>\n'
            f'        <designed target="Visible" value="true" ver="4"/>\n'
            f'        <designed target="Opacity" value="1" ver="4"/>\n'
            f'        <designed target="Enabled" value="true" ver="4"/>\n'
            f'        <designed target="Tooltip" value="" ver="4"/>\n'
            f'        <designed target="Width" value="45.6667" ver="4"/>\n'
            f'        <designed target="Height" value="13.7143" ver="4"/>\n'
            f'        <designed target="Text" value="3BTH2" ver="4"/>\n'
            f'        <designed target="Font" value="Liberation Sans,10,-1,5,75,0,0,0,0,0,Bold" ver="4"/>\n'
            f'        <designed target="FontColor" value="0xff000000" ver="4"/>\n'
            f'        <designed target="TextAlignment" value="132" ver="4"/>\n'
            f"    </object>\n"
        )
        return hmi_block
