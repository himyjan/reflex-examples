from __future__ import annotations

from .style import Style as QuestionStyle

QUESTION_STYLE: QuestionStyle = QuestionStyle()
QUESTION_STYLE.default.update(
    {
        "justify": "flex-start",
        "align_self": "flex-start",
    },
)