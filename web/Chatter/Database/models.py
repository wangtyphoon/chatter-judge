import time
import uuid

from sqlalchemy import Column, ForeignKey, String, select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship

from .connection import engine, get_db

__all__ = ["Base", "User", "init_models"]

CONNECT_TIMEOUT = 20

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True, nullable=False
    )
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)


class Scope(Base):
    __tablename__ = "scopes"
    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True, nullable=False
    )
    name = Column(String, unique=True, index=True, nullable=False)

    questions = relationship("Question", back_populates="scope", lazy="selectin")


class Question(Base):
    __tablename__ = "questions"

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True, nullable=False
    )
    scope_id = Column(UUID(as_uuid=True), ForeignKey("scopes.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)

    scope = relationship("Scope", back_populates="questions", lazy="selectin")
    input_and_outputs = relationship("InputAndOutput", back_populates="question", lazy="selectin")


class InputAndOutput(Base):
    __tablename__ = "input_and_outputs"

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True, nullable=False
    )
    input = Column(String, nullable=False)
    output = Column(String, nullable=False)
    question_id = Column(UUID(as_uuid=True), ForeignKey("questions.id"), nullable=False)

    question = relationship("Question", back_populates="input_and_outputs", lazy="selectin")


async def init_models() -> None:
    for _ in range(CONNECT_TIMEOUT):
        try:
            async with engine.begin() as connection:
                await connection.run_sync(Base.metadata.create_all)
            return
        except OSError:
            time.sleep(1)


async def init_default_data() -> None:
    async for session in get_db():
        # TODO: Adjust the default data in the future

        # create default users if users table is empty
        if not (await session.execute(select(User))).scalars().first():
            from Chatter.Utils.Auth import get_password_hash

            admin = User(username="admin", password=get_password_hash("admin"))
            session.add(admin)
            await session.commit()
            user = User(username="user", password=get_password_hash("user"))
            session.add(user)

        # create default question if questions table is empty
        if not (await session.execute(select(Question))).scalars().first():
            scope = Scope(name="HW01")
            session.add(scope)
            await session.commit()

            question = Question(name="Q1", description="# Echo", scope_id=scope.id)
            session.add(question)
            await session.commit()

            input_and_output = InputAndOutput(
                input="Hello World!", output="Hello World!", question_id=question.id
            )
            session.add(input_and_output)
            await session.commit()

            question = Question(name="Q2", description="# Echo * 2", scope_id=scope.id)
            session.add(question)
            await session.commit()

            input_and_output = InputAndOutput(
                input="Hello World!", output="Hello World!Hello World!", question_id=question.id
            )
            session.add(input_and_output)
            await session.commit()


async def add_question(name, description, scope_name, input, output):
    async for session in get_db():
        existing_scope = await session.execute(select(Scope).where(Scope.name == scope_name))
        scope = existing_scope.scalars().first()

        if not scope:
            scope = Scope(name=scope_name)
            session.add(scope)
            await session.commit()

            question = Question(name=name, description=description, scope_id=scope.id)
            session.add(question)
            await session.commit()

            input_and_output = InputAndOutput(input=input, output=output, question_id=question.id)
            session.add(input_and_output)
            await session.commit()

            return "題目新增成功!"
        else:
            existing_question = await session.execute(
                select(Question).where(Question.name == name and Question.scope_id == scope.id)
            )
            question = existing_question.scalars().first()
            question.description = description
            # 檢查 InputAndOutput 是否存在，不存在則新增
            existing_input_and_output = await session.execute(
                select(InputAndOutput).where(InputAndOutput.question_id == question.id)
            )
            input_and_output_obj = existing_input_and_output.scalars().first()
            if not input_and_output_obj:
                input_and_output_obj = InputAndOutput(
                    input=input, output=output, question_id=question.id
                )
                session.add(input_and_output_obj)
            else:
                # 更新 InputAndOutput
                input_and_output_obj.input = input
                input_and_output_obj.output = output
            await session.commit()
            return "題目更新成功!"
