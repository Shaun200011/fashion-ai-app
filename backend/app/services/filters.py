from collections import Counter

from sqlmodel import Session, select

from app.db.models import AiMetadata
from app.schemas.filter import FilterGroup, FilterOption


FILTER_FIELDS = [
    ("garment_type", "Garment"),
    ("material", "Material"),
    ("season", "Season"),
    ("occasion", "Occasion"),
]


def list_filter_groups(session: Session) -> list[FilterGroup]:
    metadata_rows = session.exec(select(AiMetadata)).all()
    groups: list[FilterGroup] = []

    for field_name, label in FILTER_FIELDS:
        counts = Counter(
            getattr(row, field_name)
            for row in metadata_rows
            if getattr(row, field_name, None)
        )
        options = [
            FilterOption(label=value, value=value, count=count)
            for value, count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))
        ]
        groups.append(FilterGroup(key=field_name, label=label, options=options))

    return groups
