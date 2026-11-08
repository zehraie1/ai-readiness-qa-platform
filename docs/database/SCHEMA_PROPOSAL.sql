-- DESIGN REFERENCE ONLY: NOT AN EXECUTABLE MIGRATION. PostgreSQL syntax proposed.
-- Decisions pending: auth identifiers, question option schema, scoring policy, retention.
CREATE TABLE users (
 id uuid PRIMARY KEY, auth_subject text UNIQUE NOT NULL,
 system_role text NOT NULL CHECK (system_role IN ('participant','administrator')),
 created_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE assessment_tracks (
 id text PRIMARY KEY, display_name text NOT NULL UNIQUE
);
CREATE TABLE competencies (
 id uuid PRIMARY KEY, code text UNIQUE NOT NULL, label text NOT NULL
);
CREATE TABLE question_bank_versions (
 id uuid PRIMARY KEY, version_label text UNIQUE NOT NULL,
 status text NOT NULL CHECK (status IN ('draft','review','published','retired')),
 published_at timestamptz
);
CREATE TABLE questions (id uuid PRIMARY KEY, logical_code text UNIQUE NOT NULL);
CREATE TABLE question_revisions (
 id uuid PRIMARY KEY, question_id uuid NOT NULL REFERENCES questions(id),
 revision_number integer NOT NULL CHECK (revision_number > 0),
 competency_id uuid NOT NULL REFERENCES competencies(id),
 prompt text NOT NULL, options_json jsonb NOT NULL, correct_option_id text NOT NULL,
 explanation text NOT NULL, evidence_reference text NOT NULL,
 UNIQUE(question_id, revision_number)
);
CREATE TABLE assessment_templates (
 id uuid PRIMARY KEY, bank_version_id uuid NOT NULL REFERENCES question_bank_versions(id),
 track_id text NOT NULL REFERENCES assessment_tracks(id),
 UNIQUE(bank_version_id,track_id)
);
CREATE TABLE template_questions (
 template_id uuid NOT NULL REFERENCES assessment_templates(id),
 question_revision_id uuid NOT NULL REFERENCES question_revisions(id),
 category text NOT NULL CHECK(category IN ('common','role_specific')),
 position integer NOT NULL CHECK(position BETWEEN 1 AND 20),
 PRIMARY KEY(template_id,question_revision_id), UNIQUE(template_id,position)
);
CREATE TABLE assessment_attempts (
 id uuid PRIMARY KEY, participant_id uuid NOT NULL REFERENCES users(id),
 template_id uuid NOT NULL REFERENCES assessment_templates(id),
 status text NOT NULL CHECK(status IN ('in_progress','submitted')),
 started_at timestamptz NOT NULL DEFAULT now(), submitted_at timestamptz
);
CREATE INDEX ix_attempt_owner_status ON assessment_attempts(participant_id,status,started_at DESC);
CREATE TABLE attempt_questions (
 id uuid PRIMARY KEY, attempt_id uuid NOT NULL REFERENCES assessment_attempts(id),
 question_revision_id uuid NOT NULL REFERENCES question_revisions(id),
 position integer NOT NULL CHECK(position BETWEEN 1 AND 20),
 UNIQUE(attempt_id,question_revision_id), UNIQUE(attempt_id,position),
 UNIQUE(id,attempt_id)
);
CREATE TABLE attempt_answers (
 attempt_question_id uuid PRIMARY KEY REFERENCES attempt_questions(id),
 selected_option_id text NOT NULL, updated_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE scoring_policies (
 id uuid PRIMARY KEY, version_label text UNIQUE NOT NULL, rules_json jsonb NOT NULL,
 status text NOT NULL CHECK(status IN ('draft','approved','retired'))
);
CREATE TABLE score_results (
 id uuid PRIMARY KEY, attempt_id uuid NOT NULL UNIQUE REFERENCES assessment_attempts(id),
 scoring_policy_id uuid NOT NULL REFERENCES scoring_policies(id),
 overall_score numeric(6,2) NOT NULL CHECK(overall_score BETWEEN 0 AND 100),
 breakdown_json jsonb NOT NULL, created_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE competency_scores (
 score_result_id uuid NOT NULL REFERENCES score_results(id),
 competency_id uuid NOT NULL REFERENCES competencies(id),
 score numeric(6,2) NOT NULL CHECK(score BETWEEN 0 AND 100),
 PRIMARY KEY(score_result_id,competency_id)
);
CREATE TABLE recommendation_rules (
 id uuid PRIMARY KEY, version_label text NOT NULL, competency_id uuid REFERENCES competencies(id),
 rule_json jsonb NOT NULL, status text NOT NULL
);
CREATE TABLE result_recommendations (
 score_result_id uuid NOT NULL REFERENCES score_results(id),
 recommendation_rule_id uuid NOT NULL REFERENCES recommendation_rules(id),
 PRIMARY KEY(score_result_id,recommendation_rule_id)
);
CREATE TABLE content_audit_events (
 id uuid PRIMARY KEY, actor_id uuid NOT NULL REFERENCES users(id),
 entity_type text NOT NULL, entity_id uuid NOT NULL, action text NOT NULL,
 occurred_at timestamptz NOT NULL DEFAULT now(), details_json jsonb NOT NULL
);
CREATE INDEX ix_audit_entity ON content_audit_events(entity_type,entity_id,occurred_at DESC);
-- REQUIRED BEFORE IMPLEMENTATION: enforce published revision immutability,
-- template 10+10 cardinality, option membership, bank publication and role mapping
-- transactionally; verify actual PostgreSQL syntax and migrations with Alembic.
