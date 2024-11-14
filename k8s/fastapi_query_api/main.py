from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI
import subprocess
import time
import json
import os

######################
# HELPER FUNCTIONS
######################

# Load environment variables from the .env file
load_dotenv()

# Retrieve the API key from the environment
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable not set.")

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

class Commands_(BaseModel):
    terminal_commands: list[str]


def get_k8s_command(query):
  completion = client.chat.completions.create(
    model="gpt-4o",
  #   response_format= Commands_,
    response_format={"type": "json_object"},
    messages=[
      {"role": "system", "content": "You are a helpfull assistant who analysis the user query and gernates specific kuberneties commands to run to gether relavent information to answer user query. remember you can run 'minikube', 'kubectl' and topics may cover status, info, or logs from Minikube. Do not gernate commands for deleting/editing/chaning. You are only allowed to gernate read commands only. Output in JSON like {\"terminal_commands\": [\"<list of commands>\"]}"},
      {"role": "user", "content": query}
    ]
  )
  reasoning = completion.choices[0].message
  print(reasoning.content)

  return reasoning

def run_kubectl_command(command):
    """
    Run a kubectl command and return the output.
    Args:
        command (str): Command to run as a string.
    Returns:
        str: The command's output or error message.
    """
    try:
        # Run the command
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        # Check for errors
        if result.returncode != 0:
            return f"Error: {result.stderr.strip()}"
        
        # Return the command's output
        return result.stdout.strip()
    
    except Exception as e:
        return f"Exception occurred: {str(e)}"
    
def run_loop_on_command(reasoning):
    result_dict = {}
    # If the model refuses to respond, you will get a refusal message
    if (reasoning.refusal):
        print(reasoning.refusal)
    else:
        # print(reasoning.content)
        # parse into JSON/disctionary
        print('^^ Parsing commands ^^')
        commands = json.loads(reasoning.content)

        # run commands
        print('^^ Running commands ^^')
        for i, command in enumerate(commands["terminal_commands"]):
            print('{})'.format(i+1),command)
            result = run_kubectl_command(command)
            result_dict[command] = result
            time.sleep(1)

    return result_dict

def get_query_response(query, result_dict):
  completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
      {"role": "system", "content": """You are a helpfull assistant who answer queries about K8s deployed applications while using information from kuberneties commands run results attached below.
      Query Scope:
       -Only read actions are required.
       -Topics may cover status, info, or logs from Minikube.
       - Respond with just the answer, omitting identifiers (e.g., "mongodb" instead of "mongodb-56c598c8fc")."""},
      {"role": "user", "content": """user query:{}.
       k8s commands results:{}""".format(query, json.dumps(result_dict))}
    ]
  )
  reasoning = completion.choices[0].message
  return reasoning


#############
# FAST API
#############
# Create an instance of FastAPI
app = FastAPI()

# Define the request payload format
class QueryRequest(BaseModel):
    query: str

# Define the response format using Pydantic
class QueryResponse(BaseModel):
    query: str
    answer: str

# Mock function to simulate answering a query (for illustration)
def process_query(query: str) -> str:
    if query :
        command_list = get_k8s_command(query)
        command_result_dict = run_loop_on_command(command_list)
        text_result = get_query_response(query, command_result_dict)
        if (text_result.content):
            return text_result.content
        else:
            return text_result.refusal
    return "Query not recognized."

# Define the POST endpoint for query submission
@app.post("/query", response_model=QueryResponse)
async def query_submission(request: QueryRequest):
    answer = process_query(request.query)
    if not answer:
        raise HTTPException(status_code=404, detail="Answer not found for the query")
    return QueryResponse(query=request.query, answer=answer)
