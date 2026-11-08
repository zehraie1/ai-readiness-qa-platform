import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";

interface Props {
  unanswered: number;
  submitting: boolean;
  onConfirm: () => void;
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export function ConfirmSubmitDialog({ unanswered, submitting, onConfirm, open, onOpenChange }: Props) {
  const blocked = unanswered > 0;
  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <div className="space-y-2">
        <DialogTrigger asChild>
          <Button size="lg" disabled={blocked} aria-describedby="submit-help">
            Submit assessment
          </Button>
        </DialogTrigger>
        <p id="submit-help" className="text-sm text-text-muted">
          {blocked
            ? `Answer all questions to submit. ${unanswered} ${unanswered === 1 ? "question remains" : "questions remain"} unanswered.`
            : "All questions are answered. You can submit when ready."}
        </p>
      </div>
      <DialogContent>
        <DialogTitle>Submit your assessment?</DialogTitle>
        <DialogDescription>
          Once submitted, your answers are final and cannot be changed. Your score will be calculated
          immediately.
        </DialogDescription>
        <DialogFooter>
          <DialogClose asChild>
            <Button variant="outline">Keep reviewing</Button>
          </DialogClose>
          <Button onClick={onConfirm} disabled={submitting}>
            {submitting ? "Submitting…" : "Confirm submission"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
