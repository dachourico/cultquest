#how skills work, xp rates etc go here


# skills.py
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Dict, Callable, Optional


def xp_to_level_osrs(level: int) -> int:
    """
    Simple OSRS-ish growth curve (not exact OSRS table, but similar feel).
    XP required to go from this level -> next level.
    """
    # You can tune this. This ramps up fast enough to feel grindy later.
    return int(50 * (level ** 1.35) + 50)


@dataclass
class SkillDef:
    key: str
    display_name: str
    category: str  # "cultivation" | "business" | "combat"
    # Optional function that returns a dict of derived effects for the current level.
    effect_fn: Optional[Callable[[int], Dict[str, float]]] = None


class Skill:
    def __init__(self, definition: SkillDef, level: int = 1, xp: int = 0):
        self.defn = definition
        self.level = level
        self.xp = xp

    @property
    def xp_to_next(self) -> int:
        return xp_to_level_osrs(self.level)

    def add_xp(self, amount: int) -> bool:
        """Returns True if at least one level-up happened."""
        if amount <= 0:
            return False

        leveled = False
        self.xp += amount
        while self.xp >= self.xp_to_next:
            self.xp -= self.xp_to_next
            self.level += 1
            leveled = True
        return leveled

    def effects(self) -> Dict[str, float]:
        """Derived stats based on level (success rate, speed multipliers, etc.)."""
        if self.defn.effect_fn is None:
            return {}
        return self.defn.effect_fn(self.level)

    def to_dict(self) -> Dict:
        return {"key": self.defn.key, "level": self.level, "xp": self.xp}

    @staticmethod
    def from_dict(skill_def: SkillDef, data: Dict) -> "Skill":
        return Skill(skill_def, level=int(data.get("level", 1)), xp=int(data.get("xp", 0)))


# ---------- Effects (your diagram translated into formulas) ----------

def pct(cap: float, start: float, per_level: float, level: int) -> float:
    """Helper: grows linearly and caps."""
    return min(cap, start + per_level * (level - 1))


def breeding_effect(level: int) -> Dict[str, float]:
    return {
        # success rate for breeding
        "success_rate": pct(0.95, 0.55, 0.01, level),
        # stability could reduce chance of negative outcomes
        "stability": pct(0.90, 0.20, 0.012, level),
    }


def cloning_effect(level: int) -> Dict[str, float]:
    return {
        "success_rate": pct(0.98, 0.50, 0.012, level),
        # bonus viable clones at higher levels (e.g., 0,1,2...)
        "extra_clones_chance": pct(0.35, 0.00, 0.005, level),
    }


def watering_effect(level: int) -> Dict[str, float]:
    return {
        # higher level = faster growth (multiplier)
        "growth_multiplier": 1.0 + min(0.50, 0.01 * (level - 1)),
        # automation efficiency boost
        "automation_bonus": min(0.40, 0.008 * (level - 1)),
    }


def transplanting_effect(level: int) -> Dict[str, float]:
    return {
        "success_rate": pct(0.99, 0.60, 0.01, level),
        # lower is faster (seconds per transplant), cap at some min
        "seconds_per_transplant": max(1.0, 6.0 - 0.06 * (level - 1)),
    }


def pruning_effect(level: int) -> Dict[str, float]:
    return {
        "speed_multiplier": 1.0 + min(0.60, 0.012 * (level - 1)),
        # small chance of harming plant early, drops with level
        "damage_chance": max(0.0, 0.08 - 0.0015 * (level - 1)),
    }


def harvesting_effect(level: int) -> Dict[str, float]:
    return {
        "speed_multiplier": 1.0 + min(0.75, 0.015 * (level - 1)),
        # unlock harvesting multiple plants at once
        "multi_harvest": 1 + (1 if level >= 15 else 0) + (1 if level >= 30 else 0),
    }


def trimming_effect(level: int) -> Dict[str, float]:
    return {
        "speed_multiplier": 1.0 + min(0.70, 0.014 * (level - 1)),
        "quality_bonus": min(0.35, 0.008 * (level - 1)),
    }


def extraction_effect(level: int) -> Dict[str, float]:
    # unlock tiers of extract types
    types_unlocked = 1
    if level >= 10:
        types_unlocked = 2
    if level >= 20:
        types_unlocked = 3
    if level >= 35:
        types_unlocked = 4

    return {
        "types_unlocked": float(types_unlocked),
        "yield_bonus": min(0.40, 0.01 * (level - 1)),
        "quality_bonus": min(0.45, 0.012 * (level - 1)),
    }


def construction_effect(level: int) -> Dict[str, float]:
    return {
        # chance of breaking pieces while building, drops with level
        "break_chance": max(0.01, 0.18 - 0.004 * (level - 1)),
        "build_speed_multiplier": 1.0 + min(0.60, 0.012 * (level - 1)),
    }


def sales_effect(level: int) -> Dict[str, float]:
    return {
        "sale_chance_bonus": min(0.50, 0.01 * (level - 1)),
        "price_bonus": min(0.25, 0.006 * (level - 1)),
    }


def marketing_effect(level: int) -> Dict[str, float]:
    return {
        "demand_multiplier": 1.0 + min(0.80, 0.02 * (level - 1)),
        "ad_efficiency": min(0.60, 0.015 * (level - 1)),
    }


def networking_effect(level: int) -> Dict[str, float]:
    return {
        "vendor_unlock_chance": min(0.35, 0.007 * (level - 1)),
        "wholesale_discount": min(0.20, 0.004 * (level - 1)),
    }


def managing_effect(level: int) -> Dict[str, float]:
    return {
        "team_efficiency": 1.0 + min(0.60, 0.015 * (level - 1)),
        "passive_xp_bonus": min(0.30, 0.01 * (level - 1)),
    }


def attack_effect(level: int) -> Dict[str, float]:
    return {
        "hit_chance_bonus": min(0.35, 0.008 * (level - 1)),
        "damage_bonus": min(0.40, 0.01 * (level - 1)),
    }


def defense_effect(level: int) -> Dict[str, float]:
    return {
        "damage_reduction": min(0.40, 0.01 * (level - 1)),
        "dodge_chance": min(0.20, 0.005 * (level - 1)),
    }


SKILL_DEFS: Dict[str, SkillDef] = {
    # Cultivation
    "breeding": SkillDef("breeding", "Breeding", "cultivation", breeding_effect),
    "cloning": SkillDef("cloning", "Cloning", "cultivation", cloning_effect),
    "watering": SkillDef("watering", "Watering", "cultivation", watering_effect),
    "transplanting": SkillDef("transplanting", "Transplanting", "cultivation", transplanting_effect),
    "pruning": SkillDef("pruning", "Pruning", "cultivation", pruning_effect),
    "harvesting": SkillDef("harvesting", "Harvesting", "cultivation", harvesting_effect),
    "trimming": SkillDef("trimming", "Trimming", "cultivation", trimming_effect),
    "extraction": SkillDef("extraction", "Extraction", "cultivation", extraction_effect),
    "construction": SkillDef("construction", "Construction", "cultivation", construction_effect),

    # Business
    "sales": SkillDef("sales", "Sales", "business", sales_effect),
    "marketing": SkillDef("marketing", "Marketing", "business", marketing_effect),
    "networking": SkillDef("networking", "Networking", "business", networking_effect),
    "managing": SkillDef("managing", "Managing", "business", managing_effect),

    # Combat
    "attack": SkillDef("attack", "Attack", "combat", attack_effect),
    "defense": SkillDef("defense", "Defense", "combat", defense_effect),
}

    #breeding
        # % success rate stability
    #cloning
        # % success rate cloning
    #watering
        # increase with each watering event, automation included
    #transplanting
        # % success transplant/speed per transplant
    #pruning
        # determines speed
    #harvesting
        # determines speed, ability to harvest more than 1 plant at a time
    #trimming
        # speed and quality
    #extraction
        # types of extract, 
        # % yield, 
        # quality
    #construction
        #% chance of stuff breaking while building
    #business
        #increase % chance of sales, 
        #increases with buying ads
        #increases with buying buildings
    #attack
        #undecided
    #defense
        #undecided
        