from sqlalchemy import Column, Integer, String,Table, ForeignKey
from robots.datasource.models import Base

author_course_association = Table(
    'author_course',
    Base.metadata,
    Column('courseId', Integer, ForeignKey('course.id')),
    Column('authorId', Integer, ForeignKey('author.id'))
)