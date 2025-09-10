"""Utility functions for generating prompts with language models."""

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


def prompt(model: AutoModelForCausalLM, tokenizer: AutoTokenizer, prompt: str) -> str:
    """Generate a response from the language model using the given prompt.

    Args:
        model: The pre-trained language model for text generation.
        tokenizer: The tokenizer associated with the model.
        prompt: The input text prompt to generate a response for.

    Returns:
        The generated text response from the model.
    """

    input_ids = tokenizer(prompt, return_tensors="pt").to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            **input_ids,
            do_sample=True,
            max_new_tokens=100,
            temperature=0.7,
        )

    output_tokens = outputs[0]
    output_tokens = output_tokens[input_ids["input_ids"].shape[1] :]

    return tokenizer.decode(output_tokens, skip_special_tokens=True)
