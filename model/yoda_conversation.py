"""Yoda-specific conversation class with Star Wars themed system prompt."""

from dataclasses import dataclass, field

from model.base_conversation import BaseConversation


@dataclass(frozen=True)
class YodaConversation(BaseConversation):
    """Conversation class specifically configured for Yoda chatbot interactions.

    This class extends BaseConversation with a Yoda-themed system prompt
    that instructs the AI to respond in the style of Yoda from Star Wars.

    Attributes:
        _system_prompt: The Yoda-themed system prompt for the AI model.
    """

    _system_prompt: str = field(
        default="You are a Yoda chatbot. You will answer questions in the style of Yoda from Star Wars matching the tone, language, grammar, and style of Yoda.",
        init=False,
        repr=False,
    )
