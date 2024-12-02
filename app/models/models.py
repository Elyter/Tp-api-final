from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

# Tables d'association
todo_tags = Table(
    'todo_tags',
    Base.metadata,
    Column('todo_id', Integer, ForeignKey('todos.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

recurring_todo_tags = Table(
    'recurring_todo_tags',
    Base.metadata,
    Column('recurring_todo_id', Integer, ForeignKey('recurring_todos.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    todos = relationship("Todo", back_populates="owner")
    recurring_todos = relationship("RecurringTodo", back_populates="owner")

class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime, nullable=True)
    priority = Column(Integer, default=1)
    owner_id = Column(Integer, ForeignKey("users.id"))
    recurring_todo_id = Column(Integer, ForeignKey("recurring_todos.id"), nullable=True)
    
    owner = relationship("User", back_populates="todos")
    recurring_parent = relationship("RecurringTodo", back_populates="todo_instances")
    tags = relationship("Tag", secondary=todo_tags, back_populates="todos")

class RecurringTodo(Base):
    __tablename__ = "recurring_todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    frequency = Column(String)  # 'daily', 'weekly', 'monthly'
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    owner = relationship("User", back_populates="recurring_todos")
    todo_instances = relationship("Todo", back_populates="recurring_parent")
    tags = relationship("Tag", secondary=recurring_todo_tags, back_populates="recurring_todos")

class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    color = Column(String)
    
    todos = relationship("Todo", secondary=todo_tags, back_populates="tags")
    recurring_todos = relationship("RecurringTodo", secondary=recurring_todo_tags, back_populates="tags")