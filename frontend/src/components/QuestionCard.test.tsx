import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";
import { question } from "@/test/fixtures";
import { QuestionCard } from "./QuestionCard";

describe("QuestionCard", () => {
  it("labels the radio group with the prompt and each option with its text", () => {
    render(<QuestionCard question={question} total={20} onSelect={() => {}} />);
    const group = screen.getByRole("radiogroup", { name: question.prompt });
    expect(group).toBeInTheDocument();
    expect(screen.getAllByRole("radio")).toHaveLength(4);
    expect(screen.getByRole("radio", { name: /Metamorphic testing/ })).not.toBeChecked();
    expect(screen.getByText(/Question 3 of 20/)).toBeInTheDocument();
  });

  // Arrow-key selection relies on real browser focus behaviour: covered in tests/e2e/keyboard.spec.ts.
  it("selects an option by clicking its label", async () => {
    const onSelect = vi.fn();
    const user = userEvent.setup();
    render(<QuestionCard question={question} total={20} onSelect={onSelect} />);
    await user.click(screen.getByText("Load testing"));
    expect(onSelect).toHaveBeenLastCalledWith("C");
  });

  it("shows the persisted selection", () => {
    render(<QuestionCard question={{ ...question, selected_option_id: "D" }} total={20} onSelect={() => {}} />);
    expect(screen.getByRole("radio", { name: /Static analysis/ })).toBeChecked();
  });
});
