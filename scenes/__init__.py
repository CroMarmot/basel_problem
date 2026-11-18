from .convergence import BaselConvergence
from .euler import BaselEuler
from .fourier import (
    BaselFourierParseval,
    BaselFourierResult,
    BaselFourierSeries,
)
from .geometry import (
    BaselGeometryCircle,
    BaselGeometryDoubling,
    BaselGeometryLight,
    BaselGeometryLimit,
    BaselGeometryPythagoras,
    BaselGeometryResult,
)
from .history import BaselHistory
from .intro import BaselIntro
from .summary import BaselGeometryQuestion, BaselGeometrySummary

SCENES = [
    ("intro", BaselIntro),
    ("history", BaselHistory),
    ("convergence", BaselConvergence),
    ("euler", BaselEuler),
    ("fourier_series", BaselFourierSeries),
    ("fourier_parseval", BaselFourierParseval),
    ("fourier_result", BaselFourierResult),
    ("geometry_light", BaselGeometryLight),
    ("geometry_pythagoras", BaselGeometryPythagoras),
    ("geometry_circle", BaselGeometryCircle),
    ("geometry_doubling", BaselGeometryDoubling),
    ("geometry_limit", BaselGeometryLimit),
    ("geometry_result", BaselGeometryResult),
    ("geometry_summary", BaselGeometrySummary),
    ("geometry_question", BaselGeometryQuestion),
]

CHAPTERS = [
    ("intro", 1, ["intro"]),
    ("history", 2, ["history"]),
    ("convergence", 3, ["convergence"]),
    ("euler", 4, ["euler"]),
    ("fourier", 5, ["fourier_series", "fourier_parseval", "fourier_result"]),
    ("geometry", 6, [
        "geometry_light",
        "geometry_pythagoras",
        "geometry_circle",
        "geometry_doubling",
        "geometry_limit",
        "geometry_result",
    ]),
    ("summary", 7, ["geometry_summary", "geometry_question"]),
]

CHAPTER_NUMBERS = {key: number for key, number, _ in CHAPTERS}
CHAPTER_SEGMENTS = {key: segments for key, _, segments in CHAPTERS}

__all__ = ["SCENES", "CHAPTERS", "CHAPTER_NUMBERS", "CHAPTER_SEGMENTS"]
