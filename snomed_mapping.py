"""Utilities for mapping symptom text to SNOMED CT codes.

This module centralises the SNOMED CT dictionaries and helper functions so
that they can be reused without bloating the main Flask application module.
"""
from __future__ import annotations

import re
from typing import Dict, Iterable, Optional

SNOMED_CT_CODES: Dict[str, str] = {
    "fever": "386661006",
    "common cold": "82272006",
    "cold": "82272006",
    "runny nose": "126660000",
    "sneezing": "230014001",
    "rash": "271807003",
    "dizziness": "404640003",
    "weakness": "13791008",
    "loss of appetite": "79890006",
    "cough": "49727002",
    "constipation": "14760008",
    "diarrhea": "62315008",
    "flu": "6142004",
    "shortness of breath": "267036007",
    "breathlessness": "267036007",
    "rapid breathing": "271823003",
    "tachypnea": "271823003",
    "migraine": "37796009",
    "headache": "25064002",
    "itching": "418290006",
    "pruritus": "418290006",
    "swelling": "271789005",
    "vomiting": "422400008",
    "nausea": "422587007",
    "infection": "40733004",
    "inflammation": "409774005",
    "cramp": "56018004",
    "bleeding": "131148009",
    "irritation": "418363000",
    "anxiety": "48694002",
    "depression": "35489007",
    "congestion": "68235000",
    "nasal congestion": "68235000",
    "insomnia": "193462001",
    "diabetes": "73211009",
    "allergy": "419076005",
    "weight loss": "267064002",
    "weight gain": "8943002",
    "hair loss": "84387000",
    "blurred vision": "44021004",
    "numbness": "44077006",
    "dry mouth": "162397003",
    "frequent urination": "162116003",
    "acne": "11381005",
    "confusion": "40917007",
    "memory loss": "386807006",
    "difficulty swallowing": "40739000",
    "restlessness": "55525008",
    "bloating": "116289008",
    "flatulence": "271832001",
    "gas": "271832001",
    "indigestion": "162076009",
    "heartburn": "1121000119100",
    "acidity": "1121000119100",
    "nosebleed": "232280008",
    "blood in stool": "405729008",
    "high blood pressure": "38341003",
    "low blood pressure": "45007003",
    "excessive thirst": "267388004",
    "dehydration": "34095006",
    "skin burning": "62564004",
    "sweating": "415690000",
    "jaundice": "18165001",
    "hernia": "52515009",
    "appendicitis": "74400008",
    "gallstones": "26650008",
    "hearing loss": "418363000",
    "balance problem": "271780003",
    "irregular heartbeat": "698247007",
    "palpitations": "80313002",
    "fainting": "271594007",
    "tremor": "26079004",
    "nervousness": "162214009",
    "panic attack": "25569003",
    "mood swing": "162214003",
    "difficulty concentrating": "263102004",
    "hallucination": "7011001",
    "lack of motivation": "36692007",
    "exhaustion": "267038008",
    "fatigue": "84229001",
    "sprain": "44465007",
    "strain": "20929002",
    "gout": "90560007",
    "injury": "417746004",
    "chills": "43724002",
    "stress": "73595000",
    "cholesterol": "267396005",
    "high cholesterol": "267396005",
    "heart problem": "56265001",
    "heart pain": "29857009",
    "heart attack": "22298006",
    "asthma": "195967001",
    "pneumonia": "233604007",
    "tingling": "279007007",
    "difficulty speaking": "80164001",
    "fatty liver": "197321007",
    "brittle nails": "24548002",
    "obesity": "414916001",
    "seizures": "91175000",
    "hiccups": "62721007",
    "ulcers": "429040005",
    "malaria": "61462000",
    "dengue": "16541001",
    "covid": "840539006",
    "covid-19": "840539006",
    "typhoid": "4834000",
    "chickenpox": "38907003",
    "kidney issue": "90708001",
    "kidney problem": "90708001",
    "kidney pain": "162049009",
    "blood in urine": "34436003",
    "wound": "416462003",
    "cold intolerance": "267064003",
    "goiter": "387517004",
    "arthritis": "201819000",
    "joint pain": "57676002",
    "joint swelling": "298349001",
    "back pain": "161891005",
    "low back pain": "279039007",
    "upper back pain": "279038004",
    "neck pain": "81680005",
    "neck stiffness": "16356006",
    "shoulder pain": "23924001",
    "shoulder stiffness": "272040008",
    "knee pain": "30989003",
    "ankle pain": "290002008",
    "foot pain": "47933007",
    "leg pain": "287047008",
    "arm pain": "44335007",
    "hand pain": "444899003",
    "ear pain": "160903007",
    "eye pain": "162424001",
    "throat pain": "162397003",
    "sore throat": "162397003",
    "toothache": "4266003",
    "chest pain": "29857009",
    "chest tightness": "29857009",
    "abdominal pain": "21522001",
    "stomach pain": "21522001",
    "pelvic pain": "162149003",
    "hip pain": "299060003",
    "period pain": "266599000",
    "period cramps": "266599000",
    "pregnancy": "77386006",
    "menopause": "56386008",
    "thyroid": "40930008",
    "piles": "70153002",
    "liver issue": "235856003",
    "liver pain": "162034007",
}

SNOMED_CT_STOPWORDS: set[str] = {
    "left",
    "right",
    "upper",
    "lower",
    "mild",
    "severe",
    "chronic",
    "acute",
    "ongoing",
    "persistent",
    "recurrent",
}

SNOMED_CT_ALIASES: Dict[str, str] = {
    "cold": "common cold",
    "runny nose": "runny nose",
    "sneezing": "sneezing",
    "breathlessness": "shortness of breath",
    "rapid breathing": "tachypnea",
    "gas": "flatulence",
    "bloating": "bloating",
    "stomach ache": "stomach pain",
    "belly pain": "stomach pain",
    "abdomen pain": "abdominal pain",
    "tummy pain": "stomach pain",
    "gastric pain": "stomach pain",
    "lower stomach pain": "stomach pain",
    "upper stomach pain": "stomach pain",
    "epigastric pain": "abdominal pain",
    "back ache": "back pain",
    "lower back pain": "low back pain",
    "upper back pain": "upper back pain",
    "head pain": "headache",
    "eye ache": "eye pain",
    "ear ache": "ear pain",
    "tooth pain": "toothache",
    "throat issue": "sore throat",
    "throat pain": "sore throat",
    "throat ache": "sore throat",
    "chest issue": "chest pain",
    "chest discomfort": "chest pain",
    "chest tightness": "chest pain",
    "knee issue": "knee pain",
    "shoulder issue": "shoulder pain",
    "neck issue": "neck pain",
    "hip issue": "hip pain",
    "pelvic issue": "pelvic pain",
    "leg issue": "leg pain",
    "arm issue": "arm pain",
    "hand issue": "hand pain",
    "foot issue": "foot pain",
    "period issue": "period pain",
    "female issue": "period pain",
    "kidney issue": "kidney problem",
    "heart issue": "chest pain",
    "heart problem": "heart problem",
}


def _normalise_snomed_key(symptom: str) -> str:
    """Normalise raw symptom text to improve SNOMED lookups."""
    cleaned = re.sub(r"[^a-z0-9\s]", " ", symptom.lower())
    tokens = [tok for tok in cleaned.split() if tok and tok not in SNOMED_CT_STOPWORDS]
    normalised = " ".join(tokens).strip()
    if not normalised:
        return ""
    return SNOMED_CT_ALIASES.get(normalised, normalised)


def map_symptoms_to_snomed(symptom_names: Iterable[str]) -> Dict[str, Optional[str]]:
    """Return a mapping of the provided symptom names to SNOMED CT codes."""
    mapping: Dict[str, Optional[str]] = {}
    for raw_name in symptom_names:
        if not raw_name:
            continue
        normalised = _normalise_snomed_key(raw_name)
        code = SNOMED_CT_CODES.get(normalised)

        if code is None and normalised.endswith(" issue"):
            base = normalised[:-6].strip()
            if base:
                candidate = SNOMED_CT_ALIASES.get(base, base)
                code = SNOMED_CT_CODES.get(candidate)
                if code is None:
                    alt = f"{base} pain"
                    alt = SNOMED_CT_ALIASES.get(alt, alt)
                    code = SNOMED_CT_CODES.get(alt)

        mapping[raw_name] = code
    return mapping


__all__ = [
    "map_symptoms_to_snomed",
    "SNOMED_CT_CODES",
    "SNOMED_CT_ALIASES",
    "SNOMED_CT_STOPWORDS",
]
