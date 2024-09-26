import asyncio
from typing import Any

import gradio as gr
import jinja2
import typer
from pydantic import BaseModel

from ragbits.core.llms import LiteLLM
from ragbits.core.llms.clients import LiteLLMOptions
from ragbits.core.prompt import Prompt
from ragbits.dev_kit.prompt_lab.discovery.prompt_discovery import DEFAULT_FILE_PATTERN, PromptDiscovery


class PromptState:
    """
    Class to store the current state of the application.

    This class holds various data structures used throughout the application's lifecycle.

    Attributes:
        prompts (list): A list containing discovered prompts.
        variable_values (dict): A dictionary to store values entered by the user for prompt input fields.
        dynamic_tb (dict): A dictionary containing dynamically created textboxes based on prompt input fields.
        current_prompt (Prompt): The currently processed Prompt object. This is created upon clicking the
                                 "Render Prompt" button and reflects in the "Rendered Prompt" field.
                                 It is used for communication with the LLM.
        llm_model_name (str): The name of the selected LLM model.
        llm_api_key (str | None): The API key for the chosen LLM model.
        temp_field_name (str): Temporary field name used internally.
    """

    prompts: list = []
    variable_values: dict = {}
    dynamic_tb: dict = {}
    current_prompt: Prompt | None = None
    llm_model_name: str | None = None
    llm_api_key: str | None = None
    temp_field_name: str = ""


def load_prompts_list(pattern: str, state: gr.State) -> gr.State:
    """
    Fetches a list of prompts based on provided paths and updates the application state.

    This function takes a path-pattern for discovering prompt definition files and uses the
    PromptDiscovery class to discover prompts within those files. The discovered prompts are then
    stored in the application state object.

    Args:
        pattern (str): A pattern for looking up prompt files.
        state (gr.State): The Gradio state object to update with discovered prompts.

    Returns:
        gr.State: The updated Gradio state object containing the list of discovered prompts.
    """
    obj = PromptDiscovery(file_pattern=pattern)
    discovered_prompts = list(obj.discover())
    state.value.prompts = discovered_prompts

    return state


def render_prompt(
    index: int, system_prompt: str, user_prompt: str, state: gr.State, *args: Any
) -> tuple[str, str, gr.State]:
    """
    Renders a prompt based on the provided key, system prompt, user prompt, and input variables.

    This function constructs a Prompt object using the prompt constructor and input constructor
    associated with the given key. It then updates the current prompt in the application state.

    Args:
        index (int): The index of the prompt to render in the prompts state.
        system_prompt (str): The system prompt template for the prompt.
        user_prompt (str): The user prompt template for the prompt.
        state (PromptState): The application state object.
        args (tuple): A tuple of input values for the prompt.

    Returns:
        tuple[str, str, PromptState]: A tuple containing the rendered system prompt, rendered user prompt,
                                        and the updated application state.
    """
    variables = dict(zip(state.dynamic_tb.keys(), args))

    prompt_class = state.prompts[index]
    prompt_class.system_prompt_template = jinja2.Template(system_prompt)
    prompt_class.user_prompt_template = jinja2.Template(user_prompt)

    input_type = prompt_class.input_type
    input_data = input_type(**variables) if input_type is not None else None
    prompt_object = prompt_class(input_data=input_data)
    state.current_prompt = prompt_object

    chat_dict = {entry["role"]: entry["content"] for entry in prompt_object.chat}

    return chat_dict["system"], chat_dict["user"], state


def list_prompt_choices(state: gr.State) -> list[tuple[str, int]]:
    """
    Returns a list of prompt choices based on the discovered prompts.

    This function generates a list of tuples containing the names of discovered prompts and their
    corresponding indices.

    Args:
        state (gr.State): The application state object.

    Returns:
        list[tuple[str, int]]: A list of tuples containing prompt names and their indices.
    """
    return [(prompt.__name__, idx) for idx, prompt in enumerate(state.value.prompts)]


def send_prompt_to_llm(state: gr.State) -> str:
    """
    Sends the current prompt to the LLM and returns the response.

    This function creates a LiteLLM client using the LLM model name and API key stored in the
    application state. It then calls the LLM client to generate a response based on the current prompt.

    Args:
        state (gr.State): The application state object.

    Returns:
        str: The response generated by the LLM.
    """
    current_prompt = state.current_prompt

    llm_client = LiteLLM(model_name=state.llm_model_name, api_key=state.llm_api_key)

    try:
        response = asyncio.run(llm_client.client.call(conversation=current_prompt.chat, options=LiteLLMOptions()))
    except Exception as e:  # pylint: disable=broad-except
        response = str(e)

    return response


def get_input_type_fields(obj: BaseModel | None) -> list[dict]:
    """
    Retrieves the field names and default values from the input type of a prompt.

    This function inspects the input type object associated with a prompt and extracts information
    about its fields, including their names and default values.

    Args:
        obj (BaseModel): The input type object of the prompt.

    Returns:
        list[dict]: A list of dictionaries, each containing a field name and its default value.
    """
    if obj is None:
        return []
    return [
        {"field_name": k, "field_default_value": v["schema"].get("default", None)}
        for (k, v) in obj.__pydantic_core_schema__["schema"]["fields"].items()
    ]


typer_app = typer.Typer(no_args_is_help=True)


@typer_app.command()
def run_app(
    file_pattern: str = DEFAULT_FILE_PATTERN, llm_model: str | None = None, llm_api_key: str | None = None
) -> None:
    """
    Launches the interactive application for working with Large Language Models (LLMs).

    This function serves as the entry point for the application. It performs several key tasks:

    1. Initializes the application state using the PromptState class.
    2. Sets the LLM model name and API key based on user-provided arguments.
    3. Fetches a list of prompts from the specified paths using the load_prompts_list function.
    4. Creates a Gradio interface with various UI elements:
        - A dropdown menu for selecting prompts.
        - Textboxes for displaying and potentially modifying system and user prompts.
        - Textboxes for entering input values based on the selected prompt.
        - Buttons for rendering prompts, sending prompts to the LLM, and displaying the response.

    Args:
        file_pattern (str): A pattern for looking up prompt files.
        llm_model (str): The name of the LLM model to use.
        llm_api_key (str): The API key for the chosen LLM model.
    """
    with gr.Blocks() as gr_app:
        prompt_state_obj = PromptState()
        prompt_state_obj.llm_model_name = llm_model
        prompt_state_obj.llm_api_key = llm_api_key

        prompts_state = gr.State(value=prompt_state_obj)
        prompts_state = load_prompts_list(pattern=file_pattern, state=prompts_state)
        prompt_selection_dropdown = gr.Dropdown(
            choices=list_prompt_choices(prompts_state), value=0, label="Select Prompt"
        )

        @gr.render(inputs=[prompt_selection_dropdown, prompts_state])
        def show_split(index: int, state: gr.State) -> None:
            prompt = state.prompts[index]
            list_of_vars = []
            with gr.Row():
                with gr.Column(scale=1):
                    with gr.Tab("Inputs"):
                        input_fields: list = get_input_type_fields(prompt.input_type)
                        tb_dict = {}
                        for entry in input_fields:
                            with gr.Row():
                                var = gr.Textbox(
                                    label=entry["field_name"],
                                    value=entry["field_default_value"],
                                    interactive=True,
                                )
                                list_of_vars.append(var)

                                tb_dict[entry["field_name"]] = var

                        state.dynamic_tb = tb_dict

                        render_prompt_button = gr.Button(value="Render prompts")

                with gr.Column(scale=4):
                    with gr.Tab("Prompt"):
                        with gr.Row():
                            with gr.Column():
                                prompt_details_system_prompt = gr.Textbox(
                                    label="System Prompt", value=prompt.system_prompt, interactive=True
                                )

                            with gr.Column():
                                prompt_details_system_prompt_rendered = gr.Textbox(
                                    label="Rendered System Prompt", value="", interactive=False
                                )

                        with gr.Row():
                            with gr.Column():
                                prompt_details_user_prompt = gr.Textbox(
                                    label="User Prompt", value=prompt.user_prompt, interactive=True
                                )

                            with gr.Column():
                                prompt_details_user_prompt_rendered = gr.Textbox(
                                    label="Rendered User Prompt", value="", interactive=False
                                )

            # TODO: Gray out the "Send to LLM" button if LLM has not been configured
            llm_request_button = gr.Button(value="Send to LLM")
            llm_prompt_response = gr.Textbox(lines=10, label="LLM response")

            render_prompt_button.click(
                render_prompt,
                [
                    prompt_selection_dropdown,
                    prompt_details_system_prompt,
                    prompt_details_user_prompt,
                    prompts_state,
                    *list_of_vars,
                ],
                [prompt_details_system_prompt_rendered, prompt_details_user_prompt_rendered, prompts_state],
            )
            llm_request_button.click(send_prompt_to_llm, prompts_state, llm_prompt_response)

    gr_app.launch()


if __name__ == "__main__":
    typer_app()
