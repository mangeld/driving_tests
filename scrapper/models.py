from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey

Base = declarative_base()

class Questionary(Base):

    __tablename__ = "questionary"

    id   = Column(Integer, primary_key=True, unique=True)
    type = Column(String(length=8)) # A2, A1, B, etc
    todotest_link = Column(String(length=2048))

class Question(Base):

    __tablename__ = "question"

    id             = Column(Integer, primary_key=True, unique=True)
    text           = Column(String(length=1024))
    questionary_id = Column(ForeignKey("questionary.id"))
    valid_answer   = Column(ForeignKey("answer.id"))
    image          = Column(String(length=1024))

class QuestionAnswers(Base):

    __tablename__ = "question_answers"

    id          = Column(Integer, primary_key=True, unique=True)
    question_id = Column(ForeignKey("question.id"), unique=False)
    answer_id   = Column(ForeignKey("answer.id"), unique=False)

class Answer(Base):

    __tablename__ = "answer"

    id   = Column(Integer,  primary_key=True, unique=True)
    text = Column(String(length=2048), primary_key=True)
