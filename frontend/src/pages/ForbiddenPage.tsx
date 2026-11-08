import { Link } from "react-router";
import { useMe } from "@/api/queries/auth";
import { homeFor } from "@/auth/RequireAuth";
import { Button } from "@/components/ui/button";
import { useDocumentTitle } from "@/lib/format";

export function ForbiddenPage() {
  useDocumentTitle("Access denied");
  const { data: me } = useMe();
  return (
    <div className="space-y-4 py-10">
      <h1 className="text-2xl font-semibold">You do not have access to this page</h1>
      <p className="text-text-muted">
        Your account role does not include this area. Assessments are available to participants;
        administration is available to administrators.
      </p>
      <Button asChild variant="outline">
        <Link to={homeFor(me?.role)}>Go to your home page</Link>
      </Button>
    </div>
  );
}
