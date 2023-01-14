import uuid

from openpyxl.worksheet.worksheet import Worksheet

from core.validators import non_empty_value
from .base import Field, Sensor


class FB_SHPS_S(Sensor):
    """Класс для работы с датчиками типа FB_SHPS_S."""
    NAME = Field(name='name', column='D', key='name', validators=[non_empty_value])
    SENSOR_TYPE = Field(name='SensorType', column='N', key='sensor_type', validators=[non_empty_value])
    COLOR_ON = Field(name='ColorOn', column='Q', key='color_on')
    GP = Field(name='GeneralPlan', column='J', key='gp', validators=[non_empty_value])
    SOUND_ON = Field(name='SoundOn', column='P', key='sound_on', validators=[non_empty_value])
    MESSAGE_ON = Field(name='MessageOn', column='O', key='message_on', validators=[non_empty_value])
    DESCRIPTION = Field(name='Description', column='E', key='description', validators=[non_empty_value])
    SEVERITY = Field(name='Severity', column=None, key='severity',)
    IVXX_TP = Field(name='IVXX_TP', column='Y', key='ivxx_tp')


    def _to_omx(self) -> str:
        omx_block = (
            f'  <ct:object {self.NAME.name}="{getattr(self, self.NAME.key)}" base-type="Types.FB_SHPS_S.FB_SHPS_S_PLC" aspect="Aspects.PLC" access-level="public" uuid="{self.pk}">\n'
            f'    <attribute type="Attributes.{self.SENSOR_TYPE.name}" value="{getattr(self, self.SENSOR_TYPE.key)}"/>\n'
            f'    <attribute type="Attributes.ColorOff" value="Серый" />\n'
            f'    <attribute type="Attributes.{self.COLOR_ON.name}" value="{getattr(self, self.COLOR_ON.key)}"/>\n'
            f'    <attribute type="Attributes.{self.GP.name}" value="{getattr(self, self.GP.key)}"/>\n'
            f'    <attribute type="Attributes.{self.SOUND_ON.name}" value="{getattr(self, self.SOUND_ON.key)}"/>\n'
            f'    <attribute type="Attributes.{self.MESSAGE_ON.name}" value="{getattr(self, self.MESSAGE_ON.key)}"/>\n'
            f'    <attribute type="unit.System.Attributes.{self.DESCRIPTION.name}" value="{getattr(self, self.DESCRIPTION.key)}"/>\n'
            f'    <attribute type="Attributes.{self.SEVERITY.name}" value="{getattr(self, self.SEVERITY.key)}"/>\n'
            f'    <attribute type="Attributes.{self.IVXX_TP.name}" value="{getattr(self, self.IVXX_TP.key)}"/>\n'
            f'  </ct:object>\n'
        )
        return omx_block
