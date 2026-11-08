import { FlaskConical } from "lucide-react";
import { Alert } from "@/components/ui/alert";

/** Permanent notice while the question bank is a DRAFT placeholder (ADR-010). */
export function DraftContentBanner({ provenance }: { provenance?: string | null }) {
  if (provenance !== "placeholder_unverified") return null;
  return (
    <Alert tone="warning" role="note" aria-label="Draft content notice">
      <FlaskConical aria-hidden="true" />
      <p>
        <strong>Draft content.</strong> Questions, competencies and recommendations are unverified
        placeholders for development and testing. They are not research-backed.
      </p>
    </Alert>
  );
}
