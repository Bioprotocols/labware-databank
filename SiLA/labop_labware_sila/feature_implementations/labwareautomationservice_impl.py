# Generated by sila2.code_generator; sila2.__version__: 0.10.1
from __future__ import annotations

from typing import TYPE_CHECKING

from sila2.server import MetadataDict

from ..generated.labwareautomationservice import GetLabwareDimensions_Responses, LabwareAutomationServiceBase

if TYPE_CHECKING:
    from ..server import Server


class LabwareAutomationServiceImpl(LabwareAutomationServiceBase):
    def __init__(self, parent_server: Server) -> None:
        super().__init__(parent_server=parent_server)

    def GetLabwareDimensions(
        self, Vendor: str, ProductNumber: str, *, metadata: MetadataDict
    ) -> GetLabwareDimensions_Responses:
        raise NotImplementedError  # TODO
