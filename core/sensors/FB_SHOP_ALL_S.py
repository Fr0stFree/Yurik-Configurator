# <ct:object name="SHOP_ALL" access-level="public" access-scope="global" uuid="fcc0348b-9bbe-4817-bfc0-d57e8442eb81">
#     <attribute type="unit.Server.Attributes.NodeRelativePath" />
#     <attribute type="unit.Server.Attributes.IsObject" value="false" />
#     <ct:object name="GP001_OP" base-type="Types.FB_SHOP_ALL.FB_SHOP_ALL_PLC" access-level="public" access-scope="global" aspect="Aspects.PLC" uuid="8a1180bd-5ff7-43f2-a7db-128b59a22377">
#       <attribute type="unit.System.Attributes.Description" value="ГП 1. Здание входных ниток и пробкоуловителей. Оповещение" />
#       <attribute type="Attributes.GeneralPlan" value="ГП001" />
#     </ct:object>
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!НОВЫЙ ДАТЧИК! ОБЯЗАТЕЛЬНО ВСЁ ПРОВЕРИТЬ!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

class FB_SHOP_ALL(Sensor):
    """
    Класс для работы с датчиками типа FB_DO_STB_S. Поле Severity отсутствует в таблице, его значение
    рассчитывается на основе значения в поле SOUND_ON.
    """
    BASE_TYPE = 'Types.FB_SHOP_ALL.FB_SHOP_ALL_PLC'
    CLASS_NAME = 'FB_SHOP_ALL'
    Name = Field(name='name', column='D', validators=[value_is_not_none_or_empty])
    Description = Field(name='Description', column='E', validators=[value_is_not_none_or_empty])
    GP = Field(name='GeneralPlan', column='J', validators=[value_is_not_none_or_empty])


    def to_omx(self) -> str:
        omx_block = (
            f'    <ct:object {self.Name.name}="{getattr(self, self.Name.key)}" base-type="{self.BASE_TYPE}" aspect="Aspects.PLC" access-level="public" uuid="{self.pk}">\n'
            f'      <attribute type="unit.System.Attributes.{self.Description.name}" value="{getattr(self, self.Description.key)}"/>\n'
            f'      <attribute type="Attributes.{self.GP.name}" value="{getattr(self, self.GP.key)}"/>\n'
            f'    </ct:object>\n'
        )
        return omx_block