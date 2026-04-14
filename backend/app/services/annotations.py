from sqlmodel import Session, select

from app.db.models import Annotation, Image
from app.schemas.annotation import AnnotationCreate, AnnotationResponse


def create_annotation(
    session: Session,
    image_id: int,
    payload: AnnotationCreate,
) -> AnnotationResponse:
    image = session.get(Image, image_id)
    if image is None:
        raise ValueError("Image not found")

    annotation = Annotation(
        image_id=image_id,
        kind=payload.kind,
        content=payload.content,
        author=payload.author,
    )
    session.add(annotation)
    session.commit()
    session.refresh(annotation)

    return AnnotationResponse(
        id=annotation.id or 0,
        image_id=annotation.image_id,
        kind=annotation.kind,
        content=annotation.content,
        author=annotation.author,
        created_at=annotation.created_at,
    )


def list_annotations_for_images(session: Session) -> dict[int, list[AnnotationResponse]]:
    rows = session.exec(select(Annotation).order_by(Annotation.created_at.desc())).all()
    annotations_by_image_id: dict[int, list[AnnotationResponse]] = {}

    for row in rows:
        annotations_by_image_id.setdefault(row.image_id, []).append(
            AnnotationResponse(
                id=row.id or 0,
                image_id=row.image_id,
                kind=row.kind,
                content=row.content,
                author=row.author,
                created_at=row.created_at,
            )
        )

    return annotations_by_image_id
