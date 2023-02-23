# Generated by sila2.code_generator; sila2.__version__: 0.10.2
from __future__ import annotations

import logging

from typing import TYPE_CHECKING

from sila2.server import MetadataDict

from ..generated.labwarequeryservice import LabwareQueryServiceBase, SPARQLQuery_Responses

if TYPE_CHECKING:
    from ..server import Server


class LabwareQueryServiceImpl(LabwareQueryServiceBase):
    def __init__(self, parent_server: Server) -> None:
        super().__init__(parent_server=parent_server)

    def SPARQLQuery(self, Query: str, *, metadata: MetadataDict) -> SPARQLQuery_Responses:
        #raise NotImplementedError  # TODO

        logging.info(f"SPARQLQuery called with Query: {Query}")

        res = F"{Query} -> dummy result "

        return SPARQLQuery_Responses(Result=res)
