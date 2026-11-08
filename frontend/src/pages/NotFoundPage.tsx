import { Link } from "react-router";
import { Button } from "@/components/ui/button";

export function NotFoundPage() {
  return (
    <div className="space-y-4 py-10">
      <h1 className="text-2xl font-semibold">Page not found</h1>
      <p className="text-text-muted">The page you requested does not exist or is not available to you.</p>
      <Button asChild variant="outline">
        <Link to="/">Go to dashboard</Link>
      </Button>
    </div>
  );
}
