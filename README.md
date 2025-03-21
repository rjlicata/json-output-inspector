# json-output-inspector

Use an LLM to repair broken JSON outputs. This is a common issue when trying to generate a JSON with an LLM that is already performing a task. It is even more prevalent when using a small LLM (< 8B parameters). This package is intended to be used as an alternative to Langchain parsers. Some people have certain feelings about them...

## Usage

Right now, this is an initial implementation. It is not on PyPI, so follow these instructions.

```
git clone https://github.com/rjlicata/json-output-inspector.git
cd json-output-parser
pip install .
```

## Dependencies

This would require that you have a locally hosted LLM using either Ollama, HuggingFace TGI, or vLLM. Once that is up, you can feed the information (endpoint url and model name) to this tool, and it will leverage that model. The only dependency is `openai` which is used for a local API call to the model endpoint.

## How it works

This is very simple, because this is a case where a simple fix works well for most use cases. The use case is you are using an LLM for a certain task (e.g. structure data from text). Often times with a smaller LLM, trying to perform tasks and output in JSON format results in very minor errors that will fail parsing checks. I have found that having a secondary LLM call (with the right prompt) can often fix this mistake - even if it takes a few tries.

This tool will prompt a model with a task to fix faulty JSON strings with a single example for formatting purposes. It will inject your string into the prompt and have it return its attempt at a correct JSON. If it fails, it tries again with its own output. There is a configurable "max_attempts" which defaults to 5.

## Python Implementation

In this hypothetical, you have an LLM hosted using HuggingFace TGI at port 8080. You have a JSON that you want fixed that we will call `json_output` (as if it came from an LLM output from elsewhere). Here is the code required.

```python
from json_output_inspector import repair_json

endpoint_url = "http://localhost:8080/v1" # endpoint for Ollama, TGI, or vLLM model
model_name = "tgi" # name for local OpenAI API call

json_output = <your_json_goes_here>
json_output = repair_json(json_output, model_name, endpoint_url)
```

### Example

See [this file](initial_test.py) for a working sample code. The broken input mimics a bad LLM output:

```
Sure, here is the JSON you requested:
{
    "name": "John
    age: 30
    "city": "New York",
    "state": "NY",
    "zip": 10001,
    "is_active": true
    "is_admin": false,
    roles: [
        "admin",
        "user"
    ],
    "address": {
        "street": "123 Main St",
        "unit": 1
    
}
```

and the model was able to produce a correctly formatted JSON:

```
{
    "name": "John",
    "age": 30,
    "city": "New York",
    "state": "NY",
    "zip": 10001,
    "is_active": true,
    "is_admin": false,
    "roles": [
        "admin",
        "user"
    ],
    "address": {
        "street": "123 Main St",
        "unit": 1
    }
}
```