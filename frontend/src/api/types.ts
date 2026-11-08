import type { components } from "./schema";

type S = components["schemas"];
export type Me = S["MeOut"];
export type Track = S["TrackOut"];
export type Attempt = S["AttemptOut"];
export type AttemptQuestion = S["AttemptQuestionOut"];
export type AttemptSummary = S["AttemptSummaryOut"];
export type AttemptList = S["AttemptListOut"];
export type Review = S["ReviewOut"];
export type Result = S["ResultOut"];
export type CompetencyResult = S["CompetencyResultOut"];
export type Recommendation = S["RecommendationOut"];
export type AdminCompetency = S["CompetencyOut"];
export type ParticipantSummary = S["ParticipantSummaryOut"];
export type TrackStatus = S["TrackStatusOut"];
export type AdminSummary = S["AdminSummaryOut"];
