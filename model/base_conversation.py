"""Base conversation class for managing chat interactions."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class BaseConversation:
    """Base class for managing conversation history and formatting.

    This class provides functionality to store and format conversation
    history between users and AI models. It maintains immutable state
    using dataclass with frozen=True.

    Attributes:
        _questions: Tuple of user questions in the conversation.
        _answers: Tuple of AI responses in the conversation.
        _system_prompt: System prompt for the AI model.
    """

    _questions: tuple[str, ...] = field(default_factory=tuple, init=False, repr=False)
    _answers: tuple[str, ...] = field(default_factory=tuple, init=False, repr=False)
    _system_prompt: str = field(default="", init=False, repr=False)

    # Mutation methods
    def add_question(self, q: str) -> None:
        """Add a user question to the conversation history.

        Args:
            q: The question text to add to the conversation.
        """
        object.__setattr__(self, "_questions", (*self._questions, q))

    def add_answer(self, a: str) -> None:
        """Add an AI answer to the conversation history.

        Args:
            a: The answer text to add to the conversation.
        """
        object.__setattr__(self, "_answers", (*self._answers, a))

    def get_questions(self) -> list[str]:
        """Get all user questions from the conversation.

        Returns:
            A list of all user questions in the conversation.
        """
        return list(self._questions)

    def get_answers(self) -> list[str]:
        """Get all AI answers from the conversation.

        Returns:
            A list of all AI answers in the conversation.
        """
        return list(self._answers)

    def __str__(self) -> str:
        """Convert the conversation to a formatted string for model input.

        Returns:
            A formatted string containing the system prompt and conversation
            history in the format expected by the language model.
        """
        if not self._system_prompt and not self._questions and not self._answers:
            return ""

        output = []
        if self._system_prompt:
            output.append(self._system_prompt.strip())

        q_len = len(self._questions)
        a_len = len(self._answers)
        max_len = max(q_len, a_len)

        for i in range(max_len):
            if i < q_len:
                output.append(f"<start_of_turn>user\n{self._questions[i]}<end_of_turn>")
            if i < a_len:
                output.append(f"<start_of_turn>model\n{self._answers[i]}<end_of_turn>")
            elif q_len > a_len and i == a_len:  # Extra user question
                output.append("<start_of_turn>model")

        return "\n".join(output)
