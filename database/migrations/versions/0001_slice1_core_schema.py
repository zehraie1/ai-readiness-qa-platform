"""Slice 1 core schema (reviewed autogenerate; adapted from docs/database/SCHEMA_PROPOSAL.sql).

Revision ID: 0001
Revises: 
Create Date: 2026-11-08 19:49:26.662090
"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = '0001'
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table('assessment_tracks',
    sa.Column('id', sa.Text(), nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('sort_order', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_assessment_tracks')),
    sa.UniqueConstraint('name', name=op.f('uq_assessment_tracks_name'))
    )
    op.create_table('competencies',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('code', sa.Text(), nullable=False),
    sa.Column('label', sa.Text(), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_competencies')),
    sa.UniqueConstraint('code', name=op.f('uq_competencies_code'))
    )
    op.create_table('question_bank_versions',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('version_label', sa.Text(), nullable=False),
    sa.Column('status', sa.Text(), nullable=False),
    sa.Column('content_provenance', sa.Text(), nullable=False),
    sa.Column('published_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.CheckConstraint("content_provenance IN ('placeholder_unverified','approved_research')", name=op.f('ck_question_bank_versions_content_provenance')),
    sa.CheckConstraint("status IN ('draft','review','published','retired')", name=op.f('ck_question_bank_versions_status')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_question_bank_versions')),
    sa.UniqueConstraint('version_label', name=op.f('uq_question_bank_versions_version_label'))
    )
    op.create_index('uq_question_bank_versions_one_published', 'question_bank_versions', ['status'], unique=True, postgresql_where=sa.text("status = 'published'"))
    op.create_table('scoring_policies',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('version_label', sa.Text(), nullable=False),
    sa.Column('status', sa.Text(), nullable=False),
    sa.Column('rules_json', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.CheckConstraint("status IN ('draft','approved','retired')", name=op.f('ck_scoring_policies_status')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_scoring_policies')),
    sa.UniqueConstraint('version_label', name=op.f('uq_scoring_policies_version_label'))
    )
    op.create_table('users',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('email', sa.Text(), nullable=False),
    sa.Column('password_hash', sa.Text(), nullable=False),
    sa.Column('display_name', sa.Text(), nullable=False),
    sa.Column('system_role', sa.Text(), nullable=False),
    sa.Column('is_active', sa.Boolean(), server_default=sa.text('true'), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.CheckConstraint("system_role IN ('participant','administrator')", name=op.f('ck_users_system_role')),
    sa.CheckConstraint('email = lower(email)', name=op.f('ck_users_email_lowercase')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_users')),
    sa.UniqueConstraint('email', name=op.f('uq_users_email'))
    )
    op.create_table('assessment_templates',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('bank_version_id', sa.Uuid(), nullable=False),
    sa.Column('track_id', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['bank_version_id'], ['question_bank_versions.id'], name=op.f('fk_assessment_templates_bank_version_id_question_bank_versions')),
    sa.ForeignKeyConstraint(['track_id'], ['assessment_tracks.id'], name=op.f('fk_assessment_templates_track_id_assessment_tracks')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_assessment_templates')),
    sa.UniqueConstraint('bank_version_id', 'track_id', name=op.f('uq_assessment_templates_bank_version_id_track_id'))
    )
    op.create_table('questions',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('code', sa.Text(), nullable=False),
    sa.Column('scope', sa.Text(), nullable=False),
    sa.Column('track_id', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.CheckConstraint("(scope = 'common' AND track_id IS NULL) OR (scope = 'role_specific' AND track_id IS NOT NULL)", name=op.f('ck_questions_scope_track')),
    sa.CheckConstraint("scope IN ('common','role_specific')", name=op.f('ck_questions_scope')),
    sa.ForeignKeyConstraint(['track_id'], ['assessment_tracks.id'], name=op.f('fk_questions_track_id_assessment_tracks')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_questions')),
    sa.UniqueConstraint('code', name=op.f('uq_questions_code'))
    )
    op.create_table('recommendation_rules',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('version_label', sa.Text(), nullable=False),
    sa.Column('competency_id', sa.Uuid(), nullable=False),
    sa.Column('title', sa.Text(), nullable=False),
    sa.Column('body', sa.Text(), nullable=False),
    sa.Column('status', sa.Text(), nullable=False),
    sa.Column('content_provenance', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.CheckConstraint("content_provenance IN ('placeholder_unverified','approved_research')", name=op.f('ck_recommendation_rules_content_provenance')),
    sa.CheckConstraint("status IN ('draft','active','retired')", name=op.f('ck_recommendation_rules_status')),
    sa.ForeignKeyConstraint(['competency_id'], ['competencies.id'], name=op.f('fk_recommendation_rules_competency_id_competencies')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_recommendation_rules')),
    sa.UniqueConstraint('version_label', 'competency_id', name=op.f('uq_recommendation_rules_version_label_competency_id'))
    )
    op.create_table('user_sessions',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('user_id', sa.Uuid(), nullable=False),
    sa.Column('token_hash', sa.LargeBinary(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('revoked_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_user_sessions_user_id_users'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_user_sessions')),
    sa.UniqueConstraint('token_hash', name=op.f('uq_user_sessions_token_hash'))
    )
    op.create_index('ix_user_sessions_user_id', 'user_sessions', ['user_id'], unique=False)
    op.create_table('assessment_attempts',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('participant_id', sa.Uuid(), nullable=False),
    sa.Column('track_id', sa.Text(), nullable=False),
    sa.Column('template_id', sa.Uuid(), nullable=False),
    sa.Column('bank_version_id', sa.Uuid(), nullable=False),
    sa.Column('scoring_policy_id', sa.Uuid(), nullable=False),
    sa.Column('recommendation_rule_version', sa.Text(), nullable=True),
    sa.Column('status', sa.Text(), nullable=False),
    sa.Column('started_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('submitted_at', sa.DateTime(timezone=True), nullable=True),
    sa.CheckConstraint("(status = 'submitted') = (submitted_at IS NOT NULL)", name=op.f('ck_assessment_attempts_submitted_at_matches')),
    sa.CheckConstraint("status IN ('in_progress','submitted')", name=op.f('ck_assessment_attempts_status')),
    sa.ForeignKeyConstraint(['bank_version_id'], ['question_bank_versions.id'], name=op.f('fk_assessment_attempts_bank_version_id_question_bank_versions')),
    sa.ForeignKeyConstraint(['participant_id'], ['users.id'], name=op.f('fk_assessment_attempts_participant_id_users')),
    sa.ForeignKeyConstraint(['scoring_policy_id'], ['scoring_policies.id'], name=op.f('fk_assessment_attempts_scoring_policy_id_scoring_policies')),
    sa.ForeignKeyConstraint(['template_id'], ['assessment_templates.id'], name=op.f('fk_assessment_attempts_template_id_assessment_templates')),
    sa.ForeignKeyConstraint(['track_id'], ['assessment_tracks.id'], name=op.f('fk_assessment_attempts_track_id_assessment_tracks')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_assessment_attempts'))
    )
    op.create_index('ix_assessment_attempts_owner_status', 'assessment_attempts', ['participant_id', 'status'], unique=False)
    op.create_index('uq_assessment_attempts_one_in_progress', 'assessment_attempts', ['participant_id', 'track_id'], unique=True, postgresql_where=sa.text("status = 'in_progress'"))
    op.create_table('question_revisions',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('question_id', sa.Uuid(), nullable=False),
    sa.Column('revision_no', sa.Integer(), nullable=False),
    sa.Column('status', sa.Text(), nullable=False),
    sa.Column('competency_id', sa.Uuid(), nullable=False),
    sa.Column('prompt', sa.Text(), nullable=False),
    sa.Column('options_json', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
    sa.Column('correct_option_id', sa.Text(), nullable=False),
    sa.Column('explanation', sa.Text(), nullable=False),
    sa.Column('evidence_reference', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.CheckConstraint("correct_option_id IN ('A','B','C','D')", name=op.f('ck_question_revisions_correct_option')),
    sa.CheckConstraint("jsonb_typeof(options_json) = 'array' AND jsonb_array_length(options_json) = 4", name=op.f('ck_question_revisions_four_options')),
    sa.CheckConstraint("status IN ('draft','review','published','retired')", name=op.f('ck_question_revisions_status')),
    sa.ForeignKeyConstraint(['competency_id'], ['competencies.id'], name=op.f('fk_question_revisions_competency_id_competencies')),
    sa.ForeignKeyConstraint(['question_id'], ['questions.id'], name=op.f('fk_question_revisions_question_id_questions')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_question_revisions')),
    sa.UniqueConstraint('question_id', 'revision_no', name=op.f('uq_question_revisions_question_id_revision_no'))
    )
    op.create_table('attempt_questions',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('attempt_id', sa.Uuid(), nullable=False),
    sa.Column('position', sa.Integer(), nullable=False),
    sa.Column('question_id', sa.Uuid(), nullable=False),
    sa.Column('question_revision_id', sa.Uuid(), nullable=False),
    sa.Column('category', sa.Text(), nullable=False),
    sa.CheckConstraint("category IN ('common','role_specific')", name=op.f('ck_attempt_questions_category')),
    sa.CheckConstraint('position BETWEEN 1 AND 20', name=op.f('ck_attempt_questions_position_range')),
    sa.ForeignKeyConstraint(['attempt_id'], ['assessment_attempts.id'], name=op.f('fk_attempt_questions_attempt_id_assessment_attempts'), ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['question_id'], ['questions.id'], name=op.f('fk_attempt_questions_question_id_questions')),
    sa.ForeignKeyConstraint(['question_revision_id'], ['question_revisions.id'], name=op.f('fk_attempt_questions_question_revision_id_question_revisions')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_attempt_questions')),
    sa.UniqueConstraint('attempt_id', 'position', name=op.f('uq_attempt_questions_attempt_id_position')),
    sa.UniqueConstraint('attempt_id', 'question_id', name=op.f('uq_attempt_questions_attempt_id_question_id'))
    )
    op.create_table('score_results',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('attempt_id', sa.Uuid(), nullable=False),
    sa.Column('scoring_policy_id', sa.Uuid(), nullable=False),
    sa.Column('overall_score', sa.SmallInteger(), nullable=False),
    sa.Column('correct_count', sa.SmallInteger(), nullable=False),
    sa.Column('common_score', sa.SmallInteger(), nullable=False),
    sa.Column('role_specific_score', sa.SmallInteger(), nullable=False),
    sa.Column('readiness_band', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.CheckConstraint("readiness_band IN ('foundation','developing','proficient','advanced')", name=op.f('ck_score_results_readiness_band')),
    sa.CheckConstraint('common_score BETWEEN 0 AND 50', name=op.f('ck_score_results_common_range')),
    sa.CheckConstraint('overall_score BETWEEN 0 AND 100', name=op.f('ck_score_results_overall_range')),
    sa.CheckConstraint('role_specific_score BETWEEN 0 AND 50', name=op.f('ck_score_results_role_range')),
    sa.ForeignKeyConstraint(['attempt_id'], ['assessment_attempts.id'], name=op.f('fk_score_results_attempt_id_assessment_attempts')),
    sa.ForeignKeyConstraint(['scoring_policy_id'], ['scoring_policies.id'], name=op.f('fk_score_results_scoring_policy_id_scoring_policies')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_score_results')),
    sa.UniqueConstraint('attempt_id', name=op.f('uq_score_results_attempt_id'))
    )
    op.create_table('template_questions',
    sa.Column('template_id', sa.Uuid(), nullable=False),
    sa.Column('position', sa.Integer(), nullable=False),
    sa.Column('question_revision_id', sa.Uuid(), nullable=False),
    sa.Column('category', sa.Text(), nullable=False),
    sa.CheckConstraint("category IN ('common','role_specific')", name=op.f('ck_template_questions_category')),
    sa.CheckConstraint('position BETWEEN 1 AND 20', name=op.f('ck_template_questions_position_range')),
    sa.ForeignKeyConstraint(['question_revision_id'], ['question_revisions.id'], name=op.f('fk_template_questions_question_revision_id_question_revisions')),
    sa.ForeignKeyConstraint(['template_id'], ['assessment_templates.id'], name=op.f('fk_template_questions_template_id_assessment_templates'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('template_id', 'position', name=op.f('pk_template_questions')),
    sa.UniqueConstraint('template_id', 'question_revision_id', name=op.f('uq_template_questions_template_id_question_revision_id'))
    )
    op.create_table('attempt_answers',
    sa.Column('attempt_question_id', sa.Uuid(), nullable=False),
    sa.Column('attempt_id', sa.Uuid(), nullable=False),
    sa.Column('selected_option_id', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.CheckConstraint("selected_option_id IN ('A','B','C','D')", name=op.f('ck_attempt_answers_selected_option')),
    sa.ForeignKeyConstraint(['attempt_id'], ['assessment_attempts.id'], name=op.f('fk_attempt_answers_attempt_id_assessment_attempts'), ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['attempt_question_id'], ['attempt_questions.id'], name=op.f('fk_attempt_answers_attempt_question_id_attempt_questions'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('attempt_question_id', name=op.f('pk_attempt_answers'))
    )
    op.create_index('ix_attempt_answers_attempt_id', 'attempt_answers', ['attempt_id'], unique=False)
    op.create_table('competency_scores',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('score_result_id', sa.Uuid(), nullable=False),
    sa.Column('competency_id', sa.Uuid(), nullable=False),
    sa.Column('correct_count', sa.Integer(), nullable=False),
    sa.Column('total_count', sa.Integer(), nullable=False),
    sa.Column('percentage', sa.SmallInteger(), nullable=True),
    sa.CheckConstraint('percentage IS NULL OR percentage BETWEEN 0 AND 100', name=op.f('ck_competency_scores_percentage_range')),
    sa.ForeignKeyConstraint(['competency_id'], ['competencies.id'], name=op.f('fk_competency_scores_competency_id_competencies')),
    sa.ForeignKeyConstraint(['score_result_id'], ['score_results.id'], name=op.f('fk_competency_scores_score_result_id_score_results'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_competency_scores')),
    sa.UniqueConstraint('score_result_id', 'competency_id', name=op.f('uq_competency_scores_score_result_id_competency_id'))
    )
    op.create_table('result_recommendations',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('score_result_id', sa.Uuid(), nullable=False),
    sa.Column('competency_id', sa.Uuid(), nullable=False),
    sa.Column('recommendation_rule_id', sa.Uuid(), nullable=False),
    sa.Column('position', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['competency_id'], ['competencies.id'], name=op.f('fk_result_recommendations_competency_id_competencies')),
    sa.ForeignKeyConstraint(['recommendation_rule_id'], ['recommendation_rules.id'], name=op.f('fk_result_recommendations_recommendation_rule_id_recommendation_rules')),
    sa.ForeignKeyConstraint(['score_result_id'], ['score_results.id'], name=op.f('fk_result_recommendations_score_result_id_score_results'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_result_recommendations')),
    sa.UniqueConstraint('score_result_id', 'competency_id', name=op.f('uq_result_recommendations_score_result_id_competency_id'))
    )


def downgrade() -> None:
    op.drop_table('result_recommendations')
    op.drop_table('competency_scores')
    op.drop_index('ix_attempt_answers_attempt_id', table_name='attempt_answers')
    op.drop_table('attempt_answers')
    op.drop_table('template_questions')
    op.drop_table('score_results')
    op.drop_table('attempt_questions')
    op.drop_table('question_revisions')
    op.drop_index('uq_assessment_attempts_one_in_progress', table_name='assessment_attempts', postgresql_where=sa.text("status = 'in_progress'"))
    op.drop_index('ix_assessment_attempts_owner_status', table_name='assessment_attempts')
    op.drop_table('assessment_attempts')
    op.drop_index('ix_user_sessions_user_id', table_name='user_sessions')
    op.drop_table('user_sessions')
    op.drop_table('recommendation_rules')
    op.drop_table('questions')
    op.drop_table('assessment_templates')
    op.drop_table('users')
    op.drop_table('scoring_policies')
    op.drop_index('uq_question_bank_versions_one_published', table_name='question_bank_versions', postgresql_where=sa.text("status = 'published'"))
    op.drop_table('question_bank_versions')
    op.drop_table('competencies')
    op.drop_table('assessment_tracks')
