import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { useState } from "react";
import { describe, expect, it, vi } from "vitest";
import { ConfirmSubmitDialog } from "./ConfirmSubmitDialog";

function Harness({ unanswered, onConfirm }: { unanswered: number; onConfirm: () => void }) {
  const [open, setOpen] = useState(false);
  return <ConfirmSubmitDialog unanswered={unanswered} submitting={false} onConfirm={onConfirm} open={open} onOpenChange={setOpen} />;
}

describe("ConfirmSubmitDialog", () => {
  it("blocks submission while questions are unanswered and explains why", () => {
    render(<Harness unanswered={2} onConfirm={() => {}} />);
    const button = screen.getByRole("button", { name: "Submit assessment" });
    expect(button).toBeDisabled();
    expect(button).toHaveAccessibleDescription(/2 questions remain unanswered/);
  });

  it("confirms via dialog and returns focus to the trigger on cancel", async () => {
    const user = userEvent.setup();
    const onConfirm = vi.fn();
    render(<Harness unanswered={0} onConfirm={onConfirm} />);
    const trigger = screen.getByRole("button", { name: "Submit assessment" });
    await user.click(trigger);
    expect(screen.getByRole("dialog", { name: "Submit your assessment?" })).toBeInTheDocument();
    await user.click(screen.getByRole("button", { name: "Keep reviewing" }));
    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
    expect(trigger).toHaveFocus();
    await user.click(trigger);
    await user.click(screen.getByRole("button", { name: "Confirm submission" }));
    expect(onConfirm).toHaveBeenCalledOnce();
  });
});
