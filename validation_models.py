from ipaddress import IPv4Address
from typing import List, Optional
from pydantic import BaseModel, Field


class Peers(BaseModel):
    """Class for BGP Peer Configuration.
       This class is a subclass of the BGPConfig class.

    Types:
        neighbor: BGP peer neighbor address. This field requires a valid IPv4 address.
        peer_asn: BGP peer autonomous system number. This value should be an integer within the range of 1 to 65535.
    """

    neighbor: IPv4Address
    peer_asn: int = Field(gt=0, le=65535)


class BGPConfig(BaseModel):
    """Class for BGP Configuration.

    Types:
        asn: The local autonomous system number. The value must be a whole number within the range of 1 to 65535.
        peers: Remote BGP peer configurations. The types must conform to the Peers definitions.
    """

    asn: int = Field(gt=0, le=65535)
    peers: Optional[List[Peers]]
