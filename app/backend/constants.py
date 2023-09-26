from app.base import ProcessTypes

GROUP_OMX_START_STRING = (
    '  <ct:object name="{0}" access-level="public" uuid="{1}">\n'
    '    <attribute type="unit.Server.Attributes.NodeRelativePath" />\n'
    '    <attribute type="unit.Server.Attributes.IsObject" value="false" />\n'
)
GROUP_OMX_END_STRING = "  </ct:object>\n"
GROUP_HMI_START_STRING = ""
GROUP_HMI_END_STRING = ""
CLUSTER_OMX_END_STRING = "</omx>\n"
CLUSTER_HMI_END_STRING = "</type>\n"
CLUSTER_OMX_START_STRING = '<omx xmlns="system" xmlns:ct="automation.control">\n'
CLUSTER_HMI_START_STRING = (
    '<type access-modifier="private" name="ParcerHMI" display-name="ParcerHMI" uuid="9a110b5c-0c05-4f31-b7ec-58eb4abcc96e" base-type="Form" base-type-id="ffaf5544-6200-45f4-87ec-9dd24558a9d5" ver="4">\n'
    '    <designed target="X" value="0" ver="4"/>\n'
    '    <designed target="Y" value="0" ver="4"/>\n'
    '    <designed target="ZValue" value="0" ver="4"/>\n'
    '    <designed target="Rotation" value="0" ver="4"/>\n'
    '    <designed target="Scale" value="1" ver="4"/>\n'
    '    <designed target="Visible" value="true" ver="4"/>\n'
    '    <designed target="Opacity" value="1" ver="4"/>\n'
    '    <designed target="Enabled" value="true" ver="4"/>\n'
    '    <designed target="Tooltip" value="" ver="4"/>\n'
    '    <designed target="Width" value="3000" ver="4"/>\n'
    '    <designed target="Height" value="3000" ver="4"/>\n'
    '    <designed target="PenColor" value="0xff000000" ver="4"/>\n'
    '    <designed target="PenStyle" value="0" ver="4"/>\n'
    '    <designed target="PenWidth" value="1" ver="4"/>\n'
    '    <designed target="BrushColor" value="0xffc0c0c0" ver="4"/>\n'
    '    <designed target="BrushStyle" value="1" ver="4"/>\n'
    '    <designed target="WindowX" value="0" ver="4"/>\n'
    '    <designed target="WindowY" value="0" ver="4"/>\n'
    '    <designed target="WindowWidth" value="1920" ver="4"/>\n'
    '    <designed target="WindowHeight" value="1080" ver="4"/>\n'
    '    <designed target="WindowCaption" value="" ver="4"/>\n'
    '    <designed target="ShowWindowCaption" value="true" ver="4"/>\n'
    '    <designed target="ShowWindowMinimize" value="true" ver="4"/>\n'
    '    <designed target="ShowWindowMaximize" value="true" ver="4"/>\n'
    '    <designed target="ShowWindowClose" value="true" ver="4"/>\n'
    '    <designed target="AlwaysOnTop" value="false" ver="4"/>\n'
    '    <designed target="WindowSizeMode" value="0" ver="4"/>\n'
    '    <designed target="WindowBorderStyle" value="1" ver="4"/>\n'
    '    <designed target="WindowState" value="0" ver="4"/>\n'
    '    <designed target="WindowScalingMode" value="0" ver="4"/>\n'
    '    <designed target="MonitorNumber" value="0" ver="4"/>\n'
    '    <designed target="WindowPosition" value="0" ver="4"/>\n'
    '    <designed target="WindowCloseMode" value="0" ver="4"/>\n'
)

START_STRING = {
    ProcessTypes.OMX: CLUSTER_OMX_START_STRING,
    ProcessTypes.HMI: CLUSTER_HMI_START_STRING,
}
END_STRING = {
    ProcessTypes.OMX: CLUSTER_OMX_END_STRING,
    ProcessTypes.HMI: CLUSTER_HMI_END_STRING,
}
