from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncpg
import httpx
import logging
import openai
from fastapi import HTTPException
import logging
from openai import api_key


# Your existing FastAPI setup
app = FastAPI()
logger = logging.getLogger(__name__)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Model for ChatGPT prompt request
class ChatGPTRequest(BaseModel):
    prompt: str


class ChatBoxData(BaseModel):
    maxtokens: int
    openaiapibase: str
    openaiapikeys: str
    agentname: str
    role: str
    goal: str
    backstory: str
    capability: str
    task: str

class RoleGoalTemperatureInput(BaseModel):
    role: str
    goal: str
    temperature: float 
    backstory: str


class Data(BaseModel):
    maxtokens: int
    openaiapibase: str
    openaiapikeys: str
    agentname: str  # Change the field name here
    role: str
    goal: str
    backstory: str
    capability: str
    task: str


    
class AgentData(BaseModel):
    agentName: str
    role: str
    goal: str
    backstory: str
    capability: str
    task: str


class LLMData(BaseModel):
    maxtokens: str
    openaiapibase: str
    openaiapikeys: str
    temperature: str

class AgentInfo(BaseModel):
    agentName: str
    role: str
    goal: str
    backstory: str
    capability: str
    task: str

class ResponseModel(BaseModel):
    response: str
    
# PostgreSQL connection settings
POSTGRES_DSN = "postgresql://parishiieb:@ep-shy-resonance-a59aitl2.us-east-2.aws.neon.tech/calendly?sslmode=require"


# Helper function to create a database connection pool
async def create_pool():
    return await asyncpg.create_pool(dsn=POSTGRES_DSN)


pool = None


@app.on_event("startup")
async def startup_event():
    global pool
    pool = await create_pool()

# Event handler to close the database connection pool when the application stops
@app.on_event("shutdown")
async def shutdown_event():
    await pool.close()

# Model for ChatBox
class ChatBox(BaseModel):
    chatName: str
    chatDesc: str
    LLM: str

class RoleGoalTemperatureInput(BaseModel):
    role: str
    goal: str
    temperature: str  # Change type to str (string)
    backstory: str

class OpenAIInput(BaseModel):
    openaiapibase: str
    openaiapikeys: str
    llm: str
    agentname: str

class TaskInput(BaseModel):
    task: str
    backstory: str
    capability: str 

class PromptRequest(BaseModel):
    prompt: str

class ResponseModel(BaseModel):
    response: str

class ChatboxInfo(BaseModel):
    id: int
    chatname: str
    chatdesc: str
    llm: str
    agentname: str
    role: str
    goal: str
    backstory: str
    capability: str
    task: str
    maxtokens: int
    openaiapibase: str
    openaiapikeys: str
    temperature: float

class ChatData(BaseModel):
    agentname: str
    role: str
    goal: str
    backstory: str
    capability: str
    task: str
    temperature: float
    maxtokens: int
    prompt: str
    openaiapikeys: str

@app.post("/insert_role_goal_temperature/{id}")
async def insert_role_goal_temperature(id: int, data: RoleGoalTemperatureInput):
    try:
        async with pool.acquire() as connection:
            # Construct the SQL query
            query = """
                INSERT INTO chat_boxes (id, role, goal, temperature, backstory, maxtokens)
                VALUES ($1, $2, $3, $4, $5, $6)
                ON CONFLICT (id) DO UPDATE
                SET role = EXCLUDED.role,
                    goal = EXCLUDED.goal,
                    temperature = COALESCE(EXCLUDED.temperature, 0.7),  
                    backstory = EXCLUDED.backstory,
                    maxtokens = EXCLUDED.maxtokens;  
            """

            # Execute the SQL query with the provided parameters
            await connection.execute(query, id, data.role, data.goal, data.temperature, data.backstory, data.maxtokens)

        return {"message": f"Role, Goal, backstory, and Temperature for ID {id} inserted/updated successfully"}

    except asyncpg.exceptions.PostgresError as e:
        print(f"PostgreSQL Error: {e}")  # Print the PostgreSQL error message
        raise HTTPException(status_code=500, detail="Database error: Unable to insert/update role, goal, and temperature")


@app.post("/insert_task/{id}")
async def insert_task(id: int, data: TaskInput):
    try:
        async with pool.acquire() as connection:
            query = """
                INSERT INTO chat_boxes (id, task, backstory, capability) VALUES ($1, $2, $3, $4)
                ON CONFLICT (id) DO UPDATE SET task = EXCLUDED.task, backstory = EXCLUDED.backstory, capability = EXCLUDED.capability;
            """
            await connection.execute(query, id, data.task, data.backstory, data.capability)
        
        return {"message": f"Task, backstory, and capability for ID {id} inserted/updated successfully"}

    except asyncpg.exceptions.PostgresError as e:
        print(f"PostgreSQL Error: {e}")
        raise HTTPException(status_code=500, detail="Database error: Unable to insert/update task, backstory, and capability")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

@app.post("/insert_openai_keys/{id}")
async def insert_openai_keys(id: int, data: OpenAIInput):
    try:
        async with pool.acquire() as connection:
            query = """
                INSERT INTO chat_boxes (id, openaiapibase, openaiapikeys, llm, agentname) 
                VALUES ($1, $2, $3, $4, $5)
                ON CONFLICT (id) DO UPDATE 
                SET openaiapibase = EXCLUDED.openaiapibase, 
                    openaiapikeys = EXCLUDED.openaiapikeys,
                    llm = EXCLUDED.llm,
                    agentname = EXCLUDED.agentname;
            """
            await connection.execute(query, id, data.openaiapibase, data.openaiapikeys, data.llm, data.agentname)
        
        return {"message": f"OpenAI keys, LLM, and Agent Name for ID {id} inserted/updated successfully"}

    except asyncpg.exceptions.PostgresError as e:
        print(f"PostgreSQL Error: {e}")
        raise HTTPException(status_code=500, detail="Database error: Unable to insert/update OpenAI keys, LLM, and Agent Name")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

@app.put('/insertdata/{id}')
async def insert_data(id: int, data: Data):
    try:
        async with pool.acquire() as connection:
            query = """
                INSERT INTO chat_boxes (id, maxtokens, openaiapibase, openaiapikeys, temperature, agentname, role, goal, backstory, capability, task)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
                ON CONFLICT (id) DO UPDATE 
                SET maxtokens = $2, openaiapibase = $3, openaiapikeys = $4, temperature = $5, agentname = $6, role = $7, goal = $8, backstory = $9, capability = $10, task = $11;
            """

            await connection.execute(
                query,
                id,
                data.maxtokens,
                data.openaiapibase,
                data.openaiapikeys,
                data.temperature,
                data.agentname,
                data.role,
                data.goal,
                data.backstory,
                data.capability,
                data.task
            )

        return {"message": "Data inserted/updated successfully"}

    except asyncpg.exceptions.PostgresError as postgres_error:
        raise HTTPException(status_code=400, detail="Database error: Check your data and try again")

    except asyncpg.exceptions.DataError as data_error:
        raise HTTPException(status_code=400, detail="Data error: Verify your input data")

    except HTTPException as http_exception:
        raise http_exception

    except Exception as generic_exception:
        raise HTTPException(status_code=500, detail="An unexpected error occurred while processing the request")

@app.post("/createChatBox")
async def create_chat_box(chat_box: ChatBox, background_tasks: BackgroundTasks):
    try:
        # Access the form data from the user object
        chatName = chat_box.chatName
        chatDesc = chat_box.chatDesc
        llm = chat_box.LLM

        # Generate text using ChatGPT
        prompt = f"Chat Name: {chatName}\nChat Description: {chatDesc}\nLLM: {llm}\n"
        background_tasks.add_task(generate_text, prompt)

        # Return a response
        return {"message": "Chat box creation initiated"}
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while processing the request")

@app.post("/openChatGPT")
async def open_chatgpt_prompt(chatgpt_request: ChatGPTRequest):
    try:
        # Access the prompt from the request body
        prompt = chatgpt_request.prompt

        # Call ChatGPT to generate a response
        response = await generate_chatgpt_response(prompt)

        # Return the response from ChatGPT
        return {"response": response}
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while processing the request")

async def generate_chatgp00t_response(prompt: str):
    try:
        headers = {
            "Authorization": "Bearer openaiapikeys",  # Replace with your OpenAI API key
            "Content-Type": "application/json"
        }
        data = {
            "model": "gpt-3.5-turbo",  # Specify the ChatGPT model here
            "prompt": prompt,
            "max_tokens": 50  # Set the maximum number of tokens for the response
        }

        async with httpx.AsyncClient() as client:
            response = await client.post("https://api.openai.com/v1/completions", headers=headers, json=data)
            if response.status_code == 200:
                result = response.json()
                generated_text = result["choices"][0]["text"]
                return generated_text
            else:
                print("OpenAI API Error:", response.status_code, response.text)
                return "Error: Unable to generate response"
    except Exception as e:
        print("An error occurred while generating text:", str(e))
        return "Error: An error occurred while generating response"

@app.get("/allInfo")
async def get_all_info():
    try:
        async with pool.acquire() as connection:
            # Execute a SQL query to fetch all chatbox information
            query = "SELECT * FROM chat_boxes;"
            rows = await connection.fetch(query)

            # If there are no rows returned, return an empty list
            if not rows:
                return []

            # Convert rows to dictionaries for JSON serialization
            chat_boxes = [dict(row) for row in rows]

            # Return the fetched chatbox information
            return chat_boxes
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while processing the request")

@app.get('/getInfo/{index}')
async def get_info(index: int):
    try:
        async with pool.acquire() as connection:
            # Execute a SQL query to fetch the chat box information based on the provided index
            query = "SELECT * FROM chat_boxes WHERE id = $1;"
            row = await connection.fetchrow(query, index)

            # If no row is returned, the chat box with the given index does not exist
            if row is None:
                raise HTTPException(status_code=404, detail="Chat box not found")

            # Convert the row to a dictionary for JSON serialization
            chat_box = dict(row)

            # Return the fetched chat box information
            return chat_box
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while processing the request")

@app.post("/generateResponse/{id}", response_model=ResponseModel)
async def generate_response(chatgpt_request: ChatGPTRequest, id: int):
    try:
        # Fetch values from the database using the provided id
        async with pool.acquire() as connection:
            query = "SELECT agentname, role, goal, backstory, capability, task FROM chat_boxes WHERE id = $1"
            fetched_data = await connection.fetchrow(query, id)

        if fetched_data is None:
            raise HTTPException(status_code=404, detail="Data not found")

        # Assign fetched values to variables
        agent_name = fetched_data['agentname']
        role = fetched_data['role']
        goal = fetched_data['goal']
        backstory = fetched_data['backstory']
        capability = fetched_data['capability']
        task = fetched_data['task']
        llm = fetched_data['llm']

        # Access the prompt from the request body
        prompt = chatgpt_request.prompt


        # Construct a prompt incorporating agent information
        full_prompt = f"{prompt}\n\nAgent Name: {agent_name}\nRole: {role}\nGoal: {goal}\nBackstory: {backstory}\nCapability: {capability}\nTask: {task}"

        # Call a function to generate a response using the combined prompt
        response = await generate_chatgpt_response(full_prompt)

        # Return the generated response
        return {"response": response}
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while processing the request")

async def generate_chatgpt_response(prompt: str):
    try:
        # Specify model parameters
        model = "gpt-3.5-turbo"  # Specify the ChatGPT model here
        max_tokens = 100  # Set the maximum number of tokens for the response
        temperature = 0.5  # Adjust temperature for diversity in responses

        # Set up HTTP headers
        headers = {
            "Authorization": "Bearer openaiapikeys",  # Replace with your OpenAI API key
            "Content-Type": "application/json"
        }

        # Set up request data including 'messages' parameter
        data = {
            "model": model,
            "messages": [{"role": "system", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": temperature
        }

        # Make a POST request to the OpenAI API
        async with httpx.AsyncClient() as client:
            response = await client.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)

            # Check if the request was successful
            if response.status_code == 200:
                result = response.json()
                generated_text = result["choices"][0]["message"]["content"]
                return generated_text
            else:
                print("OpenAI API Error:", response.status_code, response.text)
                return "Error: Unable to generate response"
    except Exception as e:
        print("An error occurred while generating text:", str(e))
        return "Error: An error occurred while generating response"
    
def is_button_disabled(chat_box_data):
    # Check if any column, except the 'prompt' column, is empty
    for key, value in chat_box_data.items():
        if key != 'prompt' and not value:
            return True  # Disable the button if any non-prompt column is empty
    return False  # Enable the button if all non-prompt columns are non-empty

@app.get("/isButtonDisabled/{chat_box_id}")
async def check_button_disabled(chat_box_id: int):
    try:
        async with pool.acquire() as connection:
            # Execute a SQL query to fetch the chat box data based on the provided ID
            query = "SELECT * FROM chat_boxes WHERE id = $1;"
            row = await connection.fetchrow(query, chat_box_id)

            # If no row is returned, the chat box with the given ID does not exist
            if row is None:
                raise HTTPException(status_code=404, detail="Chat box not found")

            # Convert the row to a dictionary
            chat_box_data = dict(row)

            # Check if the button should be disabled for this chat box
            disabled = is_button_disabled(chat_box_data)

            # Return the result
            return {"disabled": disabled}
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while processing the request")


@app.get("/chatboxes/{chatbox_id}/all_data")
async def get_chatbox_all_data(chatbox_id: int):
    try:
        async with pool.acquire() as connection:
            # Execute a SQL query to fetch all data for the chatbox with the provided ID
            query = "SELECT * FROM chat_boxes WHERE id = $1;"
            row = await connection.fetchrow(query, chatbox_id)

            # If no row is returned, the chatbox with the given ID does not exist
            if row is None:
                raise HTTPException(status_code=404, detail="Chatbox not found")

            # Convert the row to a dictionary for JSON serialization
            chatbox_data = dict(row)

            # Return the fetched chatbox data
            return chatbox_data
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while processing the request")



@app.get("/chatboxes/{chatbox_id}/all_data")
async def get_chatbox_all_data(chatbox_id: int):
    try:
        # Make a GET request to fetch chatbox data
        response = requests.get(f"http://localhost:8000/chatboxes/{chatbox_id}/all_data")
        # Check if the request was successful
        response.raise_for_status()
        # Parse the JSON response
        chatbox_data = response.json()

        return chatbox_data
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while processing the request")


logging.basicConfig(level=logging.ERROR)

# Custom exception classes
class IncompleteDataError(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Incomplete chat data provided")

class APIError(HTTPException):
    def __init__(self, message):
        super().__init__(status_code=500, detail=message)

# Function to generate prompt
def generate_prompt(chat_data):
    return f"Agent Name: {chat_data.agentname}\nRole: {chat_data.role}\nGoal: {chat_data.goal}\nBackstory: {chat_data.backstory}\nCapability: {chat_data.capability}\nTask: {chat_data.task}\nPrompt: {chat_data.prompt}"

