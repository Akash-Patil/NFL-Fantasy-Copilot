# Python Syntax Quick Reference
**Your FastAPI/Pydantic Syntax Cheat Sheet**

---

## 1. Chaining Dictionary and List Access

### What does this mean?
```python
response.json()["choices"][0]["message"]["content"]
```

**Answer:** Navigate through nested dictionaries and lists to extract data.

### Step-by-step breakdown:
```python
# OpenAI API returns this structure:
{
  "choices": [                    # ← List
    {
      "message": {                # ← Dict
        "content": "Hello!"       # ← String (what we want)
      }
    }
  ]
}

# Step 1: Convert response to dict
response.json()
# Returns: {...}

# Step 2: Get "choices" key (returns a list)
response.json()["choices"]
# Returns: [{...}]

# Step 3: Get first item from list
response.json()["choices"][0]
# Returns: {"message": {...}}

# Step 4: Get "message" key
response.json()["choices"][0]["message"]
# Returns: {"content": "Hello!"}

# Step 5: Get "content" key
response.json()["choices"][0]["message"]["content"]
# Returns: "Hello!"
```

### Alternative (step by step):
```python
data = response.json()
choices = data["choices"]
first_choice = choices[0]
message = first_choice["message"]
text = message["content"]
# text = "Hello!"
```

### Common pattern in APIs:
```python
# GitHub API
username = response.json()["user"]["login"]

# Weather API
temperature = response.json()["main"]["temp"]

# Your router
model = response.json()["model_used"]
```

---

## 2. The Three Dots `...` (Ellipsis)

### What does this mean?
```python
content: str = Field(..., min_length=1, max_length=100000)
```

**Answer:** The `...` means **"REQUIRED field"** (no default value).

### Required vs Optional:
```python
from pydantic import BaseModel, Field

class Example(BaseModel):
    # REQUIRED - must provide
    required1: str                              # Simple way
    required2: str = Field(...)                 # With validation
    required3: str = Field(..., min_length=1)   # With constraints
    
    # OPTIONAL - has default
    optional1: str = "default"
    optional2: str = Field(default="default")
    optional3: str | None = None

# Usage:
Example(required1="a", required2="b", required3="c")  # ✅ Works
Example(required1="a")  # ❌ Fails - missing required2, required3
```

### When to use `...`:
```python
# No validation needed - simple way
message: str

# With validation - use Field(...)
message: str = Field(..., min_length=1, max_length=1000)
```

### Quick reference:
| Code | Meaning |
|------|---------|
| `field: str` | Required (simplest) |
| `field: str = Field(...)` | Required with validation |
| `field: str = "default"` | Optional with default |
| `field: str \| None = None` | Optional, can be None |

---

## 3. The Pipe `|` Operator (Union Types)

### What does this mean?
```python
preferred_provider: ModelProvider | None = None
```

**Answer:** The `|` means **"OR"** - field can be one type OR another.

### Basic usage:
```python
# Can be string OR None
name: str | None = None

# Can be int OR float
number: int | float = 42

# Can be one of three types
data: str | int | list = "hello"
```

### Three ways to write the same thing:
```python
# Modern (Python 3.10+) - recommended
field: str | None = None

# Older with typing.Optional
from typing import Optional
field: Optional[str] = None

# Older with typing.Union
from typing import Union
field: Union[str, None] = None
```

### In your router:
```python
class ChatRequest(BaseModel):
    message: str                    # Must be string
    conversation_id: str | None = None  # Can be string OR None
    force_model: str | None = None      # Can be string OR None

# Valid requests:
ChatRequest(message="hi")  # conversation_id defaults to None
ChatRequest(message="hi", conversation_id="123")
ChatRequest(message="hi", conversation_id=None)
```

### Complex unions:
```python
# List can contain strings OR integers
mixed: list[str | int] = ["hello", 42, "world"]

# Field can be Message object OR None
message: Message | None = None
```

---

## 4. BaseModel (Pydantic)

### What is BaseModel?
```python
from pydantic import BaseModel

class Person(BaseModel):
    name: str
    age: int
```

**Answer:** BaseModel is Pydantic's parent class that gives your class automatic:
- ✅ Type validation
- ✅ Type conversion
- ✅ JSON serialization
- ✅ Error messages
- ✅ FastAPI integration

### Without BaseModel (manual work):
```python
class Person:
    def __init__(self, name, age):
        # Manual validation
        if not isinstance(name, str):
            raise ValueError("name must be string")
        if not isinstance(age, int):
            raise ValueError("age must be int")
        self.name = name
        self.age = age

person = Person("Akash", "25")  # ❌ age is string but no error!
```

### With BaseModel (automatic):
```python
from pydantic import BaseModel

class Person(BaseModel):
    name: str
    age: int

person = Person(name="Akash", age="25")  # ✅ Auto-converts "25" to 25
print(person.age)  # 25 (integer)

person = Person(name="Akash", age="invalid")  # ❌ Clear error message
```

### What you get for free:
```python
class User(BaseModel):
    username: str
    age: int

user = User(username="akash", age=25)

# 1. Dot notation access
user.username  # "akash"
user.age       # 25

# 2. Convert to dictionary
user.model_dump()
# {'username': 'akash', 'age': 25}

# 3. Convert to JSON
user.model_dump_json()
# '{"username":"akash","age":25}'

# 4. Create from dictionary
User.model_validate({"username": "john", "age": 30})

# 5. Automatic validation
User(username="test", age="not a number")  # ❌ Detailed error
```

### In FastAPI:
```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(request: ChatRequest):
    # FastAPI automatically:
    # 1. Reads JSON from request
    # 2. Creates ChatRequest object
    # 3. Validates types
    # 4. Gives you validated 'request'
    
    print(request.message)  # Access with dot notation
    return {"response": "..."}
```

---

## 5. The `@` Symbol (Decorators)

### What does `@` mean?
```python
@something
def my_function():
    pass
```

**Answer:** The `@` is a **decorator** - it modifies or wraps the function below it.

### Basic decorator example:
```python
def log_function(func):
    def wrapper():
        print("Starting...")
        func()
        print("Done!")
    return wrapper

@log_function
def say_hello():
    print("Hello!")

say_hello()
# Output:
# Starting...
# Hello!
# Done!
```

### Common decorators you'll see:

#### FastAPI route decorators:
```python
from fastapi import FastAPI

app = FastAPI()

@app.post("/chat")  # ← Makes this an API endpoint
async def chat(request: ChatRequest):
    return {"response": "..."}

@app.get("/stats")  # ← GET endpoint
async def stats():
    return {"total": 100}
```

#### Pydantic field validators:
```python
from pydantic import BaseModel, field_validator

class ChatRequest(BaseModel):
    message: str
    
    @field_validator("message")  # ← Validates the "message" field
    @classmethod
    def check_not_empty(cls, v):
        if not v:
            raise ValueError("Message cannot be empty")
        return v
```

#### Class method decorator:
```python
class MyClass:
    name = "Example"
    
    # Regular method - needs instance
    def regular(self):
        print(self)
    
    # Class method - works on class itself
    @classmethod
    def class_method(cls):
        print(cls.name)

MyClass.class_method()  # Works without creating instance!
```

#### Property decorator:
```python
class Person:
    def __init__(self, first, last):
        self.first = first
        self.last = last
    
    @property  # ← Access like an attribute
    def full_name(self):
        return f"{self.first} {self.last}"

person = Person("Akash", "Patel")
print(person.full_name)  # No () needed!
```

### Stacked decorators (multiple `@`):
```python
@field_validator("messages")  # Applied second
@classmethod                  # Applied first
def validate_messages(cls, v):
    if not v:
        raise ValueError("Required")
    return v

# Read bottom to top:
# 1. @classmethod makes it a class method
# 2. @field_validator tells Pydantic to use it for validation
```

---

## 6. Is It Calling Itself? (Recursion)

### The question:
```python
@app.get("/conversations/{conv_id}")
async def get_conversation(conv_id: str):
    return await db.get_conversation(conv_id)
```

**Answer:** **NO!** Two different functions with similar names.

### The two functions:
```python
# Function #1: Your API endpoint
async def get_conversation(conv_id: str):
    return await db.get_conversation(conv_id)
                    ↑
                    # Function #2: Database method (different!)

# Complete picture:
class Database:
    async def get_conversation(self, conv_id: str):  # ← Function #2
        return self.data.get(conv_id)

db = Database()

@app.get("/conversations/{conv_id}")
async def get_conversation(conv_id: str):  # ← Function #1
    return await db.get_conversation(conv_id)  # Calls Function #2
```

### Why it's NOT recursion:
```python
# Different objects = different functions
get_conversation(id)      # Standalone function
db.get_conversation(id)   # Method on 'db' object
api.get_conversation(id)  # Method on 'api' object

# Like saying:
akash.say_hello()  # Akash's method
john.say_hello()   # John's method (different!)
```

### If it WAS recursion (infinite loop):
```python
async def get_conversation(conv_id: str):
    return await get_conversation(conv_id)  # ❌ Calls itself! No 'db.'
    # This would loop forever and crash
```

### Common pattern (same name, different layers):
```python
# API Layer
@app.get("/users/{id}")
async def get_user(id: str):
    return await service.get_user(id)  # ← Service layer

# Service Layer
class UserService:
    async def get_user(self, id: str):
        return await repo.get_user(id)  # ← Database layer

# Database Layer
class UserRepository:
    async def get_user(self, id: str):
        return await db.query(...)  # ← Actual query
```

All named `get_user`, but three different functions!

---

## Running Python Programs (Bonus)

### Basic commands:
```bash
# Run a Python file
python filename.py
python main.py

# Run with uvicorn (FastAPI)
uvicorn main:app --reload
#       ↑    ↑    ↑
#       file:variable --auto-reload

# Run with options
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Run tests
pytest test_router.py -v

# Run module
python -m pytest tests/
```

### Virtual environment:
```bash
# Create
python -m venv router-venv

# Activate (Windows PowerShell)
router-venv\Scripts\activate

# Activate (Windows CMD)
router-venv\Scripts\activate.bat

# You'll see:
(router-venv) D:\smart-router>

# Deactivate
deactivate
```

### FastAPI workflow:
```bash
# 1. Navigate to project
D:
cd D:\smart-router

# 2. Activate virtual environment
router-venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run server
uvicorn main:app --reload

# 5. Visit in browser
# http://localhost:8000/docs
```

---

## Quick Reference Card

| Syntax | Meaning | Example |
|--------|---------|---------|
| `dict["key"]` | Access dictionary | `data["choices"]` |
| `list[0]` | Access first item in list | `choices[0]` |
| `...` | Required field (Pydantic) | `Field(..., min_length=1)` |
| `\|` | Union type (OR) | `str \| None` |
| `BaseModel` | Pydantic parent class | `class User(BaseModel):` |
| `@decorator` | Function modifier | `@app.post("/chat")` |
| `db.method()` | Call method on object | `db.get_conversation(id)` |
| `async def` | Async function | `async def chat():` |
| `await` | Wait for async result | `await get_data()` |

---

## Common Mistakes to Avoid

### 1. Confusing required vs optional:
```python
# ❌ Wrong - looks required but has default
field: str = None  # This is actually optional!

# ✅ Correct
field: str           # Required
field: str | None = None  # Optional
```

### 2. Forgetting `await` with async:
```python
# ❌ Wrong
result = get_data()  # Returns coroutine object, not data!

# ✅ Correct
result = await get_data()
```

### 3. Wrong order in chaining:
```python
# ❌ Wrong - can't get [0] from a dict
data["choices"]["message"][0]

# ✅ Correct
data["choices"][0]["message"]
```

### 4. Mixing up `self` vs `cls`:
```python
# Regular method
def method(self):  # Use for instance methods
    pass

# Class method
@classmethod
def method(cls):   # Use for class methods
    pass
```

---

**Keep this as your reference while building the smart router!**
