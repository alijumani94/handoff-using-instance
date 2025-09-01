from agents import Agent, Runner, Handoff
from dotenv import load_dotenv

load_dotenv()

python_agent= Agent(
    name= "python assistant",
    instructions= "You are python assistant which provide information regarding python programming language"
)

js_agent= Agent(
    name= "Java script assistant",
    instructions= "You are a help java script assistant which provides information regarding java script programming language"
)

python_handoff= Handoff(
    agent_name= python_agent,
    tool_name="python_handoff",
    tool_description="Handoff to the Python assistant",
    input_json_schema={
        "type": "object",
        "properties": {
            "query": {"type": "string"}
        },
        "required": ["query"]
    },
    on_invoke_handoff=lambda args: Runner.run_sync(
        starting_agent=python_agent,
        input=args["query"]
    )
    )

js_handoff= Handoff(
    agent_name= js_agent,
    tool_name="javascript_handoff",
    tool_description="Handoff to the JavaScript assistant",
    input_json_schema={
        "type": "object",
        "properties": {
            "query": {"type": "string"}
        },
        "required": ["query"]
    },
    on_invoke_handoff=lambda args: Runner.run_sync(
        starting_agent=js_agent,
        input=args["query"]
    )
)

triage_agent= Agent(
    name= "Triage agent",
    instructions= "You are a helpful triage agent, Do not answer regarding python or javascript, instead handoff to js_agent or python_agent",
    handoffs= [python_agent, js_agent]
)

result= Runner.run_sync(
    starting_agent= triage_agent,
    input= "explain me array in javascript"
)

print("Output: ", result.final_output)
print("\nLast agent: ", result.last_agent)