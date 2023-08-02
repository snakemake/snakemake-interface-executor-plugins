from dataclasses import dataclass
from enum import Enum
from typing import Type


class AttributeMode(Enum):
    OPTIONAL = 1
    REQUIRED = 2


class AttributeKind(Enum):
    OBJECT = 1
    CLASS = 2


@dataclass
class AttributeType:
    cls: Type
    mode: AttributeMode = AttributeMode.REQUIRED
    kind: AttributeKind = AttributeKind.OBJECT

    @property
    def is_optional(self):
        return self.mode == AttributeMode.OPTIONAL

    @property
    def is_class(self):
        return self.kind == AttributeKind.CLASS

    def into_required(self):
        return AttributeType(cls=self.cls, mode=AttributeMode.REQUIRED, kind=self.kind)
