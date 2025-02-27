# from sqlmodel import SQLModel, Field

from enum import Enum


class TaskRangeParams(Enum):
    today = 'today'
    week = 'week'
    month = 'month'