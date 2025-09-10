"""Controller layer for the Yoda Chat Bot UI application."""

from typing import TYPE_CHECKING

from model.ui import YodaModel

if TYPE_CHECKING:
    from view import YodaView


class YodaController:
    """Controller layer for coordinating between Model and View.

    This class handles the business logic and coordinates communication
    between the YodaModel and YodaView components.
    """

    def __init__(self, model: YodaModel, view: "YodaView") -> None:
        """Initialize the controller.

        Args:
            model: The YodaModel instance.
            view: The YodaView instance.
        """
        self.model = model
        self.view = view

        # Set up the view's controller callback
        self.view.set_controller(self.handle_user_message)

        # Initialize the model
        self._initialize_model()

    def _initialize_model(self) -> None:
        """Initialize the model with progress updates."""
        self.view.disable_input()  # Disable input during initialization
        self.view.update_status("Loading Yoda...")
        self.view.add_system_message(
            "Initializing Yoda model. This may take a moment..."
        )

        def progress_callback(message: str) -> None:
            """Handle progress updates from model initialization."""
            # Convert technical messages to user-friendly ones
            if "tokenizer" in message.lower():
                self.view.update_status("Loading tokenizer...")
            elif "model" in message.lower() and "ready" not in message.lower():
                self.view.update_status("Loading model...")
            elif "ready" in message.lower():
                self.view.update_status("")
                self.view.add_system_message(
                    "Yoda model is ready! You can now start chatting."
                )
                self.view.enable_input()  # Enable input when model is ready
            elif "error" in message.lower():
                self.view.update_status("")
                self.view.enable_input()  # Enable input even on error

        self.model.initialize_model(progress_callback)

    def handle_user_message(self, message: str) -> None:
        """Handle a user message.

        Args:
            message: The user's message.
        """
        # Check if model is ready
        if not self.model.is_ready():
            self.view.show_error(
                "Model is not ready yet. Please wait for initialization to complete."
            )
            return

        # Check if model is already generating
        if self.model.is_generating():
            self.view.show_error(
                "Yoda is already thinking. Please wait for the current response."
            )
            return

        # Add user message to view
        self.view.add_message("You", message)

        # Show loading state
        self.view.show_loading()

        # Generate response
        self.model.generate_response(
            question=message,
            response_callback=self._on_response_received,
            error_callback=self._on_error_occurred,
        )

    def _on_response_received(self, response: str) -> None:
        """Handle a response received from the model.

        Args:
            response: The generated response from Yoda.
        """
        # Hide loading state
        self.view.hide_loading()

        # Add Yoda's response to view
        self.view.add_message("Yoda", response)

    def _on_error_occurred(self, error_message: str) -> None:
        """Handle an error that occurred during response generation.

        Args:
            error_message: The error message.
        """
        # Hide loading state
        self.view.hide_loading()

        # Show error to user
        self.view.show_error(error_message)

        # Add error message to chat
        self.view.add_system_message(f"Error: {error_message}")

    def clear_conversation(self) -> None:
        """Clear the conversation history."""
        self.model.clear_conversation()
        self.view.add_system_message("Conversation cleared.")

    def get_conversation_history(self) -> list[tuple[str, str]]:
        """Get the conversation history.

        Returns:
            List of (question, answer) tuples.
        """
        return self.model.get_conversation_history()

    def is_model_ready(self) -> bool:
        """Check if the model is ready.

        Returns:
            True if model is ready, False otherwise.
        """
        return self.model.is_ready()

    def is_model_generating(self) -> bool:
        """Check if the model is currently generating.

        Returns:
            True if generating, False otherwise.
        """
        return self.model.is_generating()
