import logging
from contextlib import asynccontextmanager

import project.refine_prompt_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="uiuukm",
    lifespan=lifespan,
    description="To create a single API endpoint for refining LLM prompts using GPT-4, we'll leverage the FastAPI framework, considering its asynchronous support and its ease in building APIs. Here's a comprehensive project plan including the steps, technologies used, and key considerations:\n\n1. **Setup FastAPI**: Establish a new FastAPI project. This includes setting up a virtual environment, installing FastAPI along with Uvicorn for serving the application.\n\n2. **Install OpenAI's Python package**: Ensure the OpenAI package is installed to interact with GPT-4. This package will be used within the API endpoint to send prompts to GPT-4 and receive refined prompts.\n\n3. **API Endpoint Implementation**: Create a POST endpoint `/refine-prompt` which accepts a JSON payload with the key 'prompt'. This endpoint will use the OpenAI Python package to send the user's prompt to the GPT-4 model and return a refined prompt in the response.\n\n4. **Prompt Refinement Logic**: Incorporate the system message 'You are a prompt refiner. Use advanced prompt engineering techniques to refine the user's prompt.' as part of the API logic. This means structuring the prompt sent to GPT-4 in a way that it understands it's supposed to refine the input prompt. It might involve surrounding the user's prompt with additional context or instructions to ensure the intended refinement is achieved.\n\n5. **Error Handling and Validation**: Implement error handling to manage potential issues with the API request or with interacting with OpenAI's service. This should include validating the input to ensure a prompt is provided and handling any errors returned from the OpenAI API gracefully, providing useful feedback to the user.\n\n6. **Testing and Documentation**: Develop tests to verify that the endpoint behaves as expected, particularly focusing on the prompt refinement functionality and error handling. Document the endpoint, including the expected request format and the structure of the response.\n\n7. **Deployment**: Prepare the application for deployment. This could involve containerizing the application with Docker and deploying it to a cloud service provider. Ensure environment variables are used for sensitive information such as the OpenAI API key.\n\nKey Notes:\n- Ensure your OpenAI API key is securely stored and not hard-coded into your application.\n- Consider rate limits and potential costs associated with the OpenAI API usage.\n- Monitor the performance of the GPT-4 model in refining prompts, adjusting the surrounding instructions if necessary to improve outcomes.\n- Provide clear API documentation to help users understand how to use the endpoint effectively.",
)


@app.post(
    "/refine-prompt", response_model=project.refine_prompt_service.RefinePromptResponse
)
async def api_post_refine_prompt(
    user_prompt: str,
) -> project.refine_prompt_service.RefinePromptResponse | Response:
    """
    Takes a string LLM prompt from user and returns a refined version improved by GPT-4.
    """
    try:
        res = project.refine_prompt_service.refine_prompt(user_prompt)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
