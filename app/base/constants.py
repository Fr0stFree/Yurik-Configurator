from enum import Enum


class ProcessTypes(Enum):
    OMX = "to OMX"
    HMI = "to HMI"

    @property
    def extension(self) -> str:
        options = {
            ProcessTypes.OMX: ".omx-export",
            ProcessTypes.HMI: ".omobj",
        }
        return options[self]

    @classmethod
    def default(cls) -> "ProcessTypes":
        return cls.OMX
