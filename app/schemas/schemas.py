from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum

class TagBase(BaseModel):
    name: str
    color: str

class TagCreate(TagBase):
    pass

class Tag(TagBase):
    id: int

    class Config:
        from_attributes = True

class TodoPriority(int, Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

class RecurringFrequency(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"

class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    due_date: Optional[datetime] = None
    priority: TodoPriority = TodoPriority.LOW
    tag_ids: Optional[List[int]] = None

class TodoCreate(TodoBase):
    pass

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    due_date: Optional[datetime] = None
    priority: Optional[TodoPriority] = None
    tag_ids: Optional[List[int]] = None

class Todo(TodoBase):
    id: int
    created_at: datetime
    owner_id: int
    tags: List[Tag]
    recurring_todo_id: Optional[int] = None

    class Config:
        from_attributes = True

class RecurringTodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    frequency: str
    active: bool = True
    tag_ids: Optional[List[int]] = None

class RecurringTodoCreate(RecurringTodoBase):
    pass

class RecurringTodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    frequency: Optional[RecurringFrequency] = None
    active: Optional[bool] = None
    tag_ids: Optional[List[int]] = None

class RecurringTodo(RecurringTodoBase):
    id: int
    created_at: datetime
    owner_id: int
    tags: List[Tag]

    class Config:
        from_attributes = True

class TodoFilter(BaseModel):
    completed: Optional[bool] = None
    tag_id: Optional[int] = None
    priority: Optional[TodoPriority] = None
    due_before: Optional[datetime] = None
    due_after: Optional[datetime] = None
    search_term: Optional[str] = None

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None