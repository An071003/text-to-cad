"""Watch Exterior Components Package for Classical 42 mm Dress Wristwatch.

Contains parametric CAD models for:
- Caseband (vỏ giữa, 4 lugs, spring-bar holes, crown tube)
- Bezel & Front Sapphire Crystal (vành bezel vát bóng, chapter-ring/rehaut, kính sapphire)
- Dial (mặt số sector dial cổ điển Ø35 mm, applied batons, small-seconds subdial tại 9h)
- Hands (bộ kim feuille/dauphine thép nung xanh, kim giây tại trục fourth wheel)
- Crown (núm vặn khía rãnh Ø6.5 mm, ống crown tube, gioăng, hỗ trợ 2 tư thế)
- Exhibition Caseback (nắp đáy ren thép lộ máy, kính sapphire sau, vòng đệm movement holder)
"""

from .bezel import bezel
from .caseback import caseback
from .caseband import caseband
from .crown import crown
from .dial import dial
from .hands import hands

__all__ = [
    "caseband",
    "bezel",
    "dial",
    "hands",
    "crown",
    "caseback",
]
