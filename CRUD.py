from fastapi import FastAPI,HTTPException,Depends,Header
from pydantic import BaseModel

app = FastAPI()

tasks=[]
next_id=1

class TaskCreate(BaseModel):
    title:str
    description:str
    completed:bool=False
    priority:int=5

class TaskResponse(BaseModel):
    id:int
    title:str
    description:str
    completed:bool
    priority:int

def verify_token(x_token : str = Header()):
    if x_token!="secret-token":
        raise HTTPException(status_code=401,detail="Invalid Token")
    return x_token

@app.post("/tasks",response_model=TaskResponse)
def create_task(task:TaskCreate,token:str=Depends(verify_token)):
    global next_id
    new_task={
        "id" : next_id,
        "title" : task.title,
        "description" : task.description,
        "completed" : task.completed,
        "priority" : task.priority
    }
    next_id+=1
    tasks.append(new_task)
    return new_task

@app.get("/tasks",response_model=list[TaskResponse])
def get_tasks(completed:bool|None=None,token:str=Depends(verify_token)):
    if completed==None:
        return tasks
    
    returning_tasks=[]
    for task in tasks:
        if task["completed"] is completed:
            returning_tasks.append(task)
    return returning_tasks

@app.get("/tasks/{task_id}",response_model=TaskResponse)
def get_task(task_id : int,token:str=Depends(verify_token)):
    for task in tasks:
        if task["id"]==task_id:
            return task

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )

@app.delete("/tasks/{task_id}")
def delete_taskId(task_id:int,token:str=Depends(verify_token)):
    for task in tasks:
        if task["id"]==task_id:
            tasks.remove(task)
            return{
                "message" : "Task deleted succesfully"
            }

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )

@app.put("/tasks/{task_id}",response_model=TaskResponse)
def update_task(task_id:int,updated_task:TaskCreate,token:str=Depends(verify_token)):
    for task in tasks:
        if task["id"]==task_id:
            task["title"]=updated_task.title
            task["description"]=updated_task.description
            task["completed"]=updated_task.completed
            task["priority"]=updated_task.priority
            return task
    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )