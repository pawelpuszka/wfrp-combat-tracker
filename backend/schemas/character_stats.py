from pydantic import BaseModel, Field

class CharacterStats(BaseModel):
    WS: int = Field(ge=0)   # WW
    BS: int = Field(ge=0)   # US
    S: int = Field(ge=0)    # S
    T: int = Field(ge=0)    # Wt
    I: int = Field(ge=0)    # I
    Ag: int = Field(ge=0)   # Zw
    Dex: int = Field(ge=0)  # Zr
    Int: int = Field(ge=0)  # Int
    WP: int = Field(ge=0)   # SW
    Fel: int = Field(ge=0)  # Ogd

    fate: int = Field(ge=0)
    fortune: int = Field(ge=0)
    resilience: int = Field(ge=0)
    determination: int = Field(ge=0)

    
