#consumables info goes here


# consumables.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Literal, Optional

MediumType = Literal["soil", "organic_soil", "no_till", "peat_coco", "coco_rockwool"]
GeneticType = Literal["autoflower", "rando_cuts", "breeder_cuts"]
NutrientType = Literal["worms", "cover_crop", "synthetics", "secret_sauce",
                       "salts", "pro_blend", "cloning_gel"]


@dataclass(frozen=True)
class Medium:
    key: MediumType
    display_name: str
    # Gameplay knobs
    growth_speed_mult: float          # e.g. 1.00 = baseline soil
    fail_chance: float                # 0.20 = 20%
    runs_before_replace: int          # how many cycles before it’s “spent”
    yield_mult: float                 # 1.00 = baseline yield
    quality_base: int                 # 0-10 base quality contribution
    water_need_mult: float = 1.0      # 1.0 normal, >1 needs more
    irrigation_required: bool = False # coco/rockwool etc.


@dataclass(frozen=True)
class Nutrient:
    key: NutrientType
    display_name: str
    target: Literal["soil", "hydro", "cloning"]
    growth_speed_bonus: float = 0.0   # additive bonus (0.05 = +5%)
    yield_bonus: float = 0.0
    quality_bonus: float = 0.0
    clone_success_bonus: float = 0.0  # for cloning gels etc.


@dataclass(frozen=True)
class Genetics:
    key: GeneticType
    display_name: str
    quality_mult: float               # multiplier on quality outcome
    fail_chance_mult: float           # multiplier on failure chance
    yield_mult: float                 # multiplier on yield outcome


# --------- Definitions (your notes -> real numbers) ---------

MEDIUMS: dict[MediumType, Medium] = {
    "soil": Medium(
        key="soil",
        display_name="Soil",
        growth_speed_mult=0.90,     # "slow growing"
        fail_chance=0.20,
        runs_before_replace=1,
        yield_mult=0.10,
        quality_base=5,
    ),
    "organic_soil": Medium(
        key="organic_soil",
        display_name="Organic Soil",
        growth_speed_mult=1.00,     # 10% faster than soil (soil=0.90 => ~1.0)
        fail_chance=0.10,
        runs_before_replace=2,
        yield_mult=0.25,
        quality_base=6,
    ),
    "no_till": Medium(
        key="no_till",
        display_name="No-Till",
        growth_speed_mult=1.10,     # 20% faster than soil (0.90*1.2=1.08-ish)
        fail_chance=0.00,
        runs_before_replace=4,
        yield_mult=0.50,
        quality_base=7,
    ),
    "peat_coco": Medium(
        key="peat_coco",
        display_name="Peat/Coco Blend",
        growth_speed_mult=1.125,    # 25% faster than soil (0.90*1.25=1.125)
        fail_chance=0.10,
        runs_before_replace=1,
        yield_mult=0.75,
        quality_base=6,
        water_need_mult=1.25,
    ),
    "coco_rockwool": Medium(
        key="coco_rockwool",
        display_name="Coco/Rockwool",
        growth_speed_mult=1.17,     # 30% faster than soil (0.90*1.3=1.17)
        fail_chance=0.10,
        runs_before_replace=1,
        yield_mult=1.00,
        quality_base=6,
        irrigation_required=True,
        water_need_mult=1.35,
    ),
}

NUTRIENTS: dict[NutrientType, Nutrient] = {
    # Soil additives
    "worms": Nutrient("worms", "Worm Castings", target="soil", growth_speed_bonus=0.05),
    "cover_crop": Nutrient("cover_crop", "Cover Crop", target="soil", yield_bonus=0.05),
    "synthetics": Nutrient("synthetics", "Synthetics", target="soil", growth_speed_bonus=0.10),
    "secret_sauce": Nutrient("secret_sauce", "Secret Sauce", target="soil", quality_bonus=0.10),

    # Hydro nutrients
    "salts": Nutrient("salts", "Ya Boy's Salts", target="hydro", growth_speed_bonus=0.08, yield_bonus=0.08),
    "pro_blend": Nutrient("pro_blend", "Pro Blend", target="hydro", growth_speed_bonus=0.06, quality_bonus=0.06),

    # Cloning
    "cloning_gel": Nutrient("cloning_gel", "Cloning Gel", target="cloning", clone_success_bonus=0.15),
}

GENETICS: dict[GeneticType, Genetics] = {
    "autoflower": Genetics(
        key="autoflower",
        display_name="Autoflower",
        quality_mult=0.85,
        fail_chance_mult=1.25,
        yield_mult=0.80,
    ),
    "rando_cuts": Genetics(
        key="rando_cuts",
        display_name="Random Cuts",
        quality_mult=1.00,
        fail_chance_mult=1.00,
        yield_mult=1.00,
    ),
    "breeder_cuts": Genetics(
        key="breeder_cuts",
        display_name="Breeder Cuts",
        quality_mult=1.15,
        fail_chance_mult=0.70,
        yield_mult=1.20,
    ),
}


# --------- Simple calculator helpers (so you can test balance) ---------

@dataclass
class GrowSetup:
    medium: Medium
    genetics: Genetics
    nutrient: Optional[Nutrient] = None


def compute_outcomes(setup: GrowSetup):
    # growth speed
    growth_mult = setup.medium.growth_speed_mult
    if setup.nutrient:
        growth_mult *= (1.0 + setup.nutrient.growth_speed_bonus)

    # yield
    yield_mult = setup.medium.yield_mult * setup.genetics.yield_mult
    if setup.nutrient:
        yield_mult *= (1.0 + setup.nutrient.yield_bonus)

    # quality (very simple starter formula)
    quality = setup.medium.quality_base
    quality *= setup.genetics.quality_mult
    if setup.nutrient:
        quality *= (1.0 + setup.nutrient.quality_bonus)
    quality = max(0.0, min(10.0, quality))

    # failure chance
    fail_chance = setup.medium.fail_chance * setup.genetics.fail_chance_mult

    return {
        "growth_multiplier": round(growth_mult, 3),
        "yield_multiplier": round(yield_mult, 3),
        "quality_out_of_10": round(quality, 2),
        "fail_chance": round(min(0.99, max(0.0, fail_chance)), 3),
        "runs_before_replace": setup.medium.runs_before_replace,
        "water_need_mult": setup.medium.water_need_mult,
        "irrigation_required": setup.medium.irrigation_required,
    }

#Medium
    #soil - 
        # slow growing
        # 20% risk of failed crop
        # 1 run
        # .1x yield multiplier
        # 5/10 quality

    #organic soil - 
        # 10% faster than soil, 
        # 10% risk of failed crop, 
        # 2 runs
        # .25x yield multiplier
        # 6/10 quality

    #no-till - 
        #20% faster than soil, 
        # no failed crops, 
        # lasts 4 runs before needing amendments
        # .5x yield multiplier


    #peat/coco blend 
        # 25% faster than soil,
        #  more water needs,
        #  10% failed crops,
        #  lasts 1 run
        #  .75 yield multiplier

    #coco/rockwool
        # 30% faster than soil,
        # irrigation needed
        # 10% failed crops
        # 1 x yield multiplier

#Nutrients:
    #soil -
        # worms (boost growth speed by 5%)
        # cover crop (boost yield by 5%)
        # synthetics (boost speed by 10%)
        # some guy's secret sauce (they say it's mostly pee)(boost quality by 10%)

    #hydro - 
        # ya boy's salts
        # pro blend

    #cloning gels
        # +% success of clones


# Genetics:
    #autoflower
        # worst quality
        # highest chance of failure
        # lowest yield

    #rando cuts
        # mid
        # med chance of failure
        # med yield

    # breeder cuts
        #top shelf
        # little/no chance of failure
        # high yield





