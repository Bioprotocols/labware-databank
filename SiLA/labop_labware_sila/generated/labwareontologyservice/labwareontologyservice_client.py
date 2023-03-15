# Generated by sila2.code_generator; sila2.__version__: 0.10.2
# -----
# This class does not do anything useful at runtime. Its only purpose is to provide type annotations.
# Since sphinx does not support .pyi files (yet?), so this is a .py file.
# -----

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Iterable, Optional

    from labwareontologyservice_types import CreateLabware_Responses
    from sila2.client import ClientMetadataInstance


class LabwareOntologyServiceClient:
    """
    CRUD operations on the labware ontology.
    """

    def CreateLabware(
        self, Name: str, *, metadata: Optional[Iterable[ClientMetadataInstance]] = None
    ) -> CreateLabware_Responses:
        """
        Creates Labware individual in Labware ontology.
        """
        ...
