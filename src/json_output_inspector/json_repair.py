import json
from typing import Tuple

from json_output_inspector.llm import ModelHandler
from json_output_inspector.llm import REPAIR_SYSTEM_MESSAGE


def check_json(json_str: str) -> Tuple[str, bool]:
    """checks if JSON is valid
    :param json_str: JSON string
    :type json_str: str
    :return: JSON string and whether it is broken
    :rtype: Tuple[str, bool]
    """
    try:
        json.loads(json_str)
        return json_str, False
    except:
        return json_str, True


def repair_json(json_str: str, model_name: str, endpoint_url: str, num_tries: int = 5) -> str:
    """repairs the input JSON string

    :param json_input: input JSON string
    :type json_input: str
    :param model_name: model name for OpenAI API call (e.g. "llama3.2", "tgi", or mounted path for vLLM)
    :type model_name: str
    :param endpoint_url: model endpoint URL
    :type endpoint_url: str
    :param num_tries: maximum number of tries to repair the JSON, defaults to 5
    :type num_tries: int, optional
    :return: repaired JSON string
    :rtype: str
    """
    # initialize model handler
    model = ModelHandler(
        model_name=model_name,
        endpoint_url=endpoint_url,
        system_message=REPAIR_SYSTEM_MESSAGE,
        temperature=0.0,
    )
    # check if json is already valid
    json_str, broken = check_json(json_str)
    for _ in range(num_tries):
        if not broken:
            break
        json_str = model.invoke(f"INPUT: {json_str}\nOUTPUT: ")
        json_str, broken = check_json(json_str)
    return json_str
