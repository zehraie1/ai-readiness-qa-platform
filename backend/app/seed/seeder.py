"""Idempotent seeding: deterministic uuid5 IDs + merge (insert-or-update). Never for production
content unless provenance is approved research (ADR-010)."""

import uuid
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.content.models import (
    AssessmentTemplate,
    Competency,
    Question,
    QuestionBankVersion,
    QuestionRevision,
    RecommendationRule,
    TemplateQuestion,
)
from app.modules.scoring.models import ScoringPolicy
from app.modules.tracks.models import AssessmentTrack
from app.seed.bank_schema import Bank

NAMESPACE = uuid.UUID("5b0f5f3e-8a4c-4f37-9c2e-0d6f3c1a7b21")


def sid(kind: str, key: str) -> uuid.UUID:
    return uuid.uuid5(NAMESPACE, f"{kind}:{key}")


class SeedRefused(RuntimeError):
    pass


def seed_content(db: Session, bank: Bank, app_env: str) -> None:
    m = bank.manifest
    if app_env == "production" and (m.content_provenance != "approved_research" or m.not_for_production):
        raise SeedRefused("Refusing to seed placeholder/unverified content in production.")

    for t in bank.tracks:
        db.merge(AssessmentTrack(id=t.id, name=t.name, description=t.description, sort_order=t.sort_order))

    comp_ids: dict[str, uuid.UUID] = {}
    for c in bank.competencies:
        comp_ids[c.code] = sid("competency", c.code)
        db.merge(Competency(id=comp_ids[c.code], code=c.code, label=c.label, description=c.description))

    sp = bank.scoring_policy
    db.merge(
        ScoringPolicy(
            id=sid("scoring_policy", sp.version_label),
            version_label=sp.version_label,
            status=sp.status,
            rules_json=sp.rules.model_dump(),
        )
    )

    rec = bank.recommendations
    for r in rec.rules:
        db.merge(
            RecommendationRule(
                id=sid("recommendation", f"{rec.version_label}:{r.competency}"),
                version_label=rec.version_label,
                competency_id=comp_ids[r.competency],
                title=r.title,
                body=r.body,
                status="active",
                content_provenance=rec.content_provenance,
            )
        )

    other_published = db.scalar(
        select(QuestionBankVersion).where(
            QuestionBankVersion.status == "published",
            QuestionBankVersion.version_label != m.version_label,
        )
    )
    if other_published is not None:
        raise SeedRefused(f"Another bank is already published: {other_published.version_label}")
    bank_id = sid("bank", m.version_label)
    existing_bank = db.get(QuestionBankVersion, bank_id)
    db.merge(
        QuestionBankVersion(
            id=bank_id,
            version_label=m.version_label,
            status="published",
            content_provenance=m.content_provenance,
            published_at=(existing_bank.published_at if existing_bank else None) or datetime.now(UTC),
        )
    )
    db.flush()

    files = [bank.common, *bank.role_files.values()]
    revision_ids: dict[str, uuid.UUID] = {}
    for f in files:
        for q in f.questions:
            qid = sid("question", q.code)
            db.merge(Question(id=qid, code=q.code, scope=f.scope, track_id=f.track_id))
            revision_ids[q.code] = sid("revision", f"{q.code}:1")
            db.merge(
                QuestionRevision(
                    id=revision_ids[q.code],
                    question_id=qid,
                    revision_no=1,
                    status="published",
                    competency_id=comp_ids[q.competency],
                    prompt=q.prompt,
                    options_json=[o.model_dump() for o in q.options],
                    correct_option_id=q.correct_option_id,
                    explanation=q.explanation,
                    evidence_reference=q.evidence_reference,
                )
            )
    db.flush()

    for t in bank.tracks:
        template_id = sid("template", f"{m.version_label}:{t.id}")
        db.merge(AssessmentTemplate(id=template_id, bank_version_id=bank_id, track_id=t.id))
        db.flush()
        for position, q, category in bank.template_order(t.id):
            db.merge(
                TemplateQuestion(
                    template_id=template_id,
                    position=position,
                    question_revision_id=revision_ids[q.code],
                    category=category,
                )
            )
    db.flush()
