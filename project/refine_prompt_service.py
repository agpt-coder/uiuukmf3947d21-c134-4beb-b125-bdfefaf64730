from typing import Optional

import openai
from pydantic import BaseModel


class RefinePromptResponse(BaseModel):
    """
    Model for the response returned after refining a user's LLM prompt through GPT-4.
    """

    original_prompt: str
    refined_prompt: str
    refinement_successful: bool
    error_message: Optional[str] = None


def refine_prompt(user_prompt: str) -> RefinePromptResponse:
    """
    Takes a string LLM prompt from user and returns a refined version improved by GPT-4.

    This function processes the user's LLM prompt by sending it to the GPT-4 API with a specific
    instruction to refine the prompt. It captures the API response and returns the refined prompt,
    including additional information about the success of the operation and any error encountered.

    Args:
        user_prompt (str): The original LLM prompt provided by the user for refinement.

    Returns:
        RefinePromptResponse: Model for the response returned after refining a user's LLM prompt through GPT-4.
    """
    openai.api_key = "your_openai_api_key"
    instruction = "You are a prompt refiner. Use advanced prompt engineering techniques to refine the user's prompt: "
    input_prompt = instruction + user_prompt
    try:
        response = openai.Completion.create(
            engine="text-davinci-004",
            prompt=input_prompt,
            temperature=0.7,
            max_tokens=150,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
        )
        refined_prompt_text = (
            response["choices"][0]["text"].strip() if response["choices"] else ""
        )  # TODO(autogpt): "__getitem__" method not defined on type "Generator[Unknown | list[Unknown] | dict[Unknown, Unknown], None, None]". reportIndexIssue
        error_message = None
        refinement_successful = bool(refined_prompt_text)
    except Exception as e:
        refined_prompt_text = ""
        error_message = f"Failed to refine prompt due to an error: {str(e)}"
        refinement_successful = False
    return RefinePromptResponse(
        original_prompt=user_prompt,
        refined_prompt=refined_prompt_text,
        refinement_successful=refinement_successful,
        error_message=error_message,
    )
