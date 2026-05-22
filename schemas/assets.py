from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class AssetCategory(str, Enum):
    characters = "Characters"
    props = "Props"
    environments = "Environments"
    vehicles = "Vehicles"
    weapons = "Weapons"
    ui_icons = "UI/Icons"

class LicenseType(str, Enum):
    cc0 = "cc0"
    free = "free"
    paid = "paid"

class Asset(BaseModel):
    id: str
    name: str
    category: AssetCategory
    source: str
    license: LicenseType
    url: str
    thumbnail_url: Optional[str] = None
    fit_rationale: str


class RecommendationResult(BaseModel):
    assets: List[Asset]