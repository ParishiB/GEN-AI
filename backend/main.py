from multiprocessing import pool
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import asyncpg
import httpx
import redis
from openai import api_key

# python3 -m uvicorn main:app --reload  

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

POSTGRES_DSN = "postgresql://parishiieb@ep-shy-resonance-a59aitl2.us-east-2.aws.neon.tech/calendly?sslmode=require"

async def create_pool():
    try:
        return await asyncpg.create_pool(dsn=POSTGRES_DSN, timeout=300)  
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database connection error")

@app.on_event("startup")
async def startup_event():
    app.pool = await create_pool()

@app.on_event("shutdown")
async def shutdown_event():
    await app.pool.close()


class ChatBox(BaseModel):
    chatName: str
    chatDesc: str

class ResponseModel(BaseModel):
    response: str

class ChatGPTRequest(BaseModel):
    prompt: str
class OpenAIInput(BaseModel):
    openaiapibase: str
    openaiapikeys: str
    llm: str
    agentname: str

class TaskInput(BaseModel):
    task: str
    backstory: str
    capability: str 



class RoleGoalTemperatureInput(BaseModel):
    role: str
    goal: str
    temperature: float 
    backstory: str
    maxtokens: str

    
class AgentData(BaseModel):
    agentName: str
    role: str
    goal: str
    backstory: str
    capability: str
    task: str 



@app.get("/allInfo")
async def get_all_info():
    try:
        async with app.pool.acquire() as connection:
            query = "SELECT * FROM chat_boxes;"
            rows = await connection.fetch(query)

            if not rows:
                return []

            chat_boxes = [dict(row) for row in rows]

            return chat_boxes
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while processing the request")
    

@app.post("/createChatBox")
async def create_chat_box(chat_box: ChatBox):
    try:
        async with app.pool.acquire() as connection:
        
            chatname = chat_box.chatName
            chatdesc = chat_box.chatDesc

            query = "INSERT INTO chat_boxes (chatname, chatdesc) VALUES ($1, $2)"
            await connection.execute(query, chatname, chatdesc)

      
            return {"message": "Chat box created successfully"}
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while processing the request")

@app.get('/getInfo/{index}')
async def get_info(index: int):
    try:
        async with app.pool.acquire() as connection:  
            query = "SELECT * FROM chat_boxes WHERE id = $1;"
            row = await connection.fetchrow(query, index)

            if row is None:
                raise HTTPException(status_code=404, detail="Chat box not found")

            chat_box = dict(row)

            return chat_box
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while processing the request")
      
def is_button_disabled(chat_box_data):
 
    for key, value in chat_box_data.items():
        if key != 'prompt' and not value:
            return True 
    return False  


@app.get("/isButtonDisabled/{chat_box_id}")
async def check_button_disabled(chat_box_id: int):
    try:
        async with pool.acquire() as connection:
         
            query = "SELECT * FROM chat_boxes WHERE id = $1;"
            row = await connection.fetchrow(query, chat_box_id)

            if row is None:
                raise HTTPException(status_code=404, detail="Chat box not found")
     
            chat_box_data = dict(row)

          
            disabled = is_button_disabled(chat_box_data)
            return {"disabled": disabled}
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while processing the request")


@app.post("/insert_role_goal_temperature/{id}")
async def insert_role_goal_temperature(id: int, data: RoleGoalTemperatureInput):
    try:
        async with pool.acquire() as connection:
         
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

            #
            await connection.execute(query, id, data.role, data.goal, data.temperature, data.backstory, data.maxtokens)

        return {"message": f"Role, Goal, backstory, and Temperature for ID {id} inserted/updated successfully"}

    except asyncpg.exceptions.PostgresError as e:
        print(f"PostgreSQL Error: {e}")  
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

@app.post("/generateResponse/{id}", response_model=ResponseModel)
async def generate_response(chatgpt_request: ChatGPTRequest, id: int):
    try:
      
        async with pool.acquire() as connection:
            query = "SELECT agentname, role, goal, backstory, capability, task FROM chat_boxes WHERE id = $1"
            fetched_data = await connection.fetchrow(query, id)

        if fetched_data is None:
            raise HTTPException(status_code=404, detail="Data not found")

       
        agent_name = fetched_data['agentname']
        role = fetched_data['role']
        goal = fetched_data['goal']
        backstory = fetched_data['backstory']
        capability = fetched_data['capability']
        task = fetched_data['task']
        llm = fetched_data['llm']
        openaiapikeys = fetched_data['openaiapikeys']

   
        prompt = chatgpt_request.prompt
 
        full_prompt = f"{prompt}\n\nAgent Name: {agent_name}\nRole: {role}\nGoal: {goal}\nBackstory: {backstory}\nCapability: {capability}\nTask: {task}"

        response = await generate_chatgpt_response(full_prompt,openaiapikeys)

        return {"response": response}
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while processing the request")



# Additiional function added it the model is openai then the below fucntion if not then different function created according to llm chosen

async def generate_chatgpt_response(prompt: str , openaiapikeys : str):
    try:
        model = "gpt-3.5-turbo" 
        max_tokens = 100 
        temperature = 0.5  

        # Set up HTTP headers
        headers = {
            "Authorization": f"Bearer {openaiapikeys}",
            "Content-Type": "application/json"
        }

        data = {
            "model": model,
            "messages": [{"role": "system", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": temperature
        }

   
        async with httpx.AsyncClient() as client:
            response = await client.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)

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
    

async def generate_azure_openai_response():
    try:
        print('If the llm chosen is this then the this function would be called isntead of above')
    except Exception as e:
        print("An error occurred while generating text:", str(e))
        return "Error: An error occurred while generating response"
#   redis_client = redis.Redis(host='localhost', port=6379, db=0)  
# async def generate_chatgpt_response(prompt: str, openaiapikeys: str):
#     try:
#         # Check if prompt exists in Redis cache
#         cached_key = f"chatgpt:{prompt}"
#         cached_response = redis_client.get(cached_key)
#         if cached_response:
#             # If cached response exists, check if it's still valid
#             cached_data = cached_response.decode('utf-8').split("\n\n")
#             if len(cached_data) == 2:
#                 cached_timestamp, cached_text = cached_data
#                 cached_timestamp = float(cached_timestamp)
#                 # Check if the cached response is still valid (within 10 minutes)
#                 if time.time() - cached_timestamp <= 600:
#                     # If valid, return new prompt + cached response
#                     return f"{prompt}\n{cached_text}"

#         # Cache has expired or no cached response exists, generate new response
#         model = "gpt-3.5-turbo" 
#         max_tokens = 100 
#         temperature = 0.5  

#         # Set up HTTP headers
#         headers = {
#             "Authorization": f"Bearer {openaiapikeys}",
#             "Content-Type": "application/json"
#         }

#         data = {
#             "model": model,
#             "messages": [{"role": "system", "content": prompt}],
#             "max_tokens": max_tokens,
#             "temperature": temperature
#         }

#         async with httpx.AsyncClient() as client:
#             response = await client.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)

#             if response.status_code == 200:
#                 result = response.json()
#                 generated_text = result["choices"][0]["message"]["content"]
                
#                 # Cache the new response along with current timestamp
#                 cached_value = f"{time.time()}\n\n{generated_text}"
#                 redis_client.setex(cached_key, 600, cached_value)  # Cache for 10 minutes
#                 # Return new prompt + generated response
#                 return f"{prompt}\n{generated_text}"
#             else:
#                 print("OpenAI API Error:", response.status_code, response.text)
#                 return "Error: Unable to generate response"
#     except Exception as e:
#         print("An error occurred while generating text:", str(e))
#         return "Error: An error occurred while generating response"
    
def redis_connect() -> redis.client.Redis:
    try:
        client = redis.Redis(
            host="localhost",
            port=6379,
            db=0,
        )
        ping = client.ping()
        if ping is True:
            return client
    except redis.ConnectionError:
        print("Connection Error!")
       


client = redis_connect()

async def redis_gpt_response(prompt: str, openaiapikeys: str):
    try:     
        cached_prompt = client.get("cached_prompt")
        if cached_prompt:
            cached_prompt = cached_prompt.decode('utf-8')
            return {"new_prompt": prompt, "cached_prompt": cached_prompt}

        client.setex("cached_prompt", 600, prompt)
        return {"new_prompt": prompt, "cached_prompt": None}

    except Exception as e:
        print("An error occurred while generating text:", str(e))
        return "Error: An error occurred while generating response"
