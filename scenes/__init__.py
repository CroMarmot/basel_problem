from .convergence import BaselConvergence
from .euler import BaselEuler
from .fourier import BaselFourier
from .geometry import BaselGeometry
from .history import BaselHistory
from .intro import BaselIntro

SCENES = [
    ("intro", BaselIntro),
    ("history", BaselHistory),
    ("convergence", BaselConvergence),
    ("euler", BaselEuler),
    ("fourier", BaselFourier),
    ("geometry", BaselGeometry),
]

CHAPTER_NUMBERS = {
    "intro": 1,
    "history": 2,
    "convergence": 3,
    "euler": 5,
    "fourier": 6,
    "geometry": 7,
}

__all__ = ["SCENES", "CHAPTER_NUMBERS"]
