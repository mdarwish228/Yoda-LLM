"""Model layer for the Yoda Chat Bot UI application."""

import threading
from collections.abc import Callable

from transformers import AutoModelForCausalLM, AutoTokenizer

from model.yoda_conversation import YodaConversation
from util.prompt_util import prompt


class YodaModel:
    """Model layer for managing Yoda chatbot operations.

    This class handles the LLM model initialization, conversation management,
    and asynchronous response generation for the UI application.
    """

    def __init__(self) -> None:
        """Initialize the Yoda model with conversation and LLM components."""
        self.conversation = YodaConversation()
        self.model: AutoModelForCausalLM | None = None
        self.tokenizer: AutoTokenizer | None = None
        self.model_id = "unsloth/gemma-2-2b-it"
        self._is_initialized = False
        self._is_generating = False

    def initialize_model(
        self, progress_callback: Callable[[str], None] | None = None
    ) -> None:
        """Initialize the model and tokenizer asynchronously.

        Args:
            progress_callback: Optional callback function to report progress updates.
        """

        def _initialize() -> None:
            try:
                if progress_callback:
                    progress_callback("Loading tokenizer...")

                self.tokenizer = AutoTokenizer.from_pretrained(self.model_id)

                if progress_callback:
                    progress_callback("Loading model...")

                self.model = AutoModelForCausalLM.from_pretrained(
                    self.model_id, device_map="auto"
                )

                self._is_initialized = True

                if progress_callback:
                    progress_callback("Model ready!")

            except Exception as e:
                if progress_callback:
                    progress_callback(f"Error: {e!s}")

        # Run initialization in a separate thread
        thread = threading.Thread(target=_initialize, daemon=True)
        thread.start()

    def is_ready(self) -> bool:
        """Check if the model is ready for inference.

        Returns:
            True if the model is initialized and ready, False otherwise.
        """
        return (
            self._is_initialized
            and self.model is not None
            and self.tokenizer is not None
        )

    def is_generating(self) -> bool:
        """Check if the model is currently generating a response.

        Returns:
            True if generating, False otherwise.
        """
        return self._is_generating

    def generate_response(
        self,
        question: str,
        response_callback: Callable[[str], None],
        error_callback: Callable[[str], None] | None = None,
    ) -> None:
        """Generate a response for the given question asynchronously.

        Args:
            question: The user's question.
            response_callback: Callback function to receive the generated response.
            error_callback: Optional callback function to receive error messages.
        """
        if not self.is_ready():
            if error_callback:
                error_callback(
                    "Model is not ready yet. Please wait for initialization."
                )
            return

        if self._is_generating:
            if error_callback:
                error_callback("Already generating a response. Please wait.")
            return

        def _generate() -> None:
            try:
                self._is_generating = True

                # Add question to conversation
                self.conversation.add_question(question)

                # Generate response
                answer = prompt(self.model, self.tokenizer, str(self.conversation))

                # Add answer to conversation
                self.conversation.add_answer(answer)

                # Send response back to UI
                response_callback(answer.strip())

            except Exception as e:
                if error_callback:
                    error_callback(f"Error generating response: {e!s}")
            finally:
                self._is_generating = False

        # Run generation in a separate thread
        thread = threading.Thread(target=_generate, daemon=True)
        thread.start()

    def get_conversation_history(self) -> list[tuple[str, str]]:
        """Get the conversation history as a list of (question, answer) tuples.

        Returns:
            List of conversation exchanges.
        """
        questions = self.conversation.get_questions()
        answers = self.conversation.get_answers()

        # Ensure we have matching pairs
        history = []
        for i in range(len(questions)):
            question = questions[i]
            answer = answers[i] if i < len(answers) else ""
            history.append((question, answer))

        return history

    def clear_conversation(self) -> None:
        """Clear the conversation history."""
        self.conversation = YodaConversation()
