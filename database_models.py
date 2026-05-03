from __future__ import annotations

from sqlalchemy import Boolean, ForeignKey, Column, Float, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class User(Base):

    __tablename__ = "auth"

    id = Column(Integer, primary_key=True, index=True)
    fullName = Column(String)
    mobileNumber = Column(String)
    password = Column(String)
    username = Column(String)
    restart = Column(Boolean)

class Base(DeclarativeBase):
    pass


class ChecklistDay(Base):
    __tablename__ = "checklist_days"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    day_number: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)

    tasks: Mapped[list["ChecklistTask"]] = relationship(
        back_populates="day", cascade="all, delete-orphan"
    )
    extra_topics: Mapped[list["ChecklistExtraTopic"]] = relationship(
        back_populates="day", cascade="all, delete-orphan"
    )


class ChecklistTask(Base):
    __tablename__ = "checklist_tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    day_id: Mapped[int] = mapped_column(
        ForeignKey("checklist_days.id", ondelete="CASCADE"), nullable=False, index=True
    )
    task_text: Mapped[str] = mapped_column(Text, nullable=False)
    done_default: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    day: Mapped["ChecklistDay"] = relationship(back_populates="tasks")


class ChecklistExtraTopic(Base):
    __tablename__ = "checklist_extra_topics"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    day_id: Mapped[int] = mapped_column(
        ForeignKey("checklist_days.id", ondelete="CASCADE"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    details: Mapped[str] = mapped_column(Text, nullable=False)
    question: Mapped[str] = mapped_column(Text, nullable=False)
    answer: Mapped[str] = mapped_column(Text, nullable=False)
    code: Mapped[str] = mapped_column(Text, nullable=False)
    command: Mapped[str] = mapped_column(Text, nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    day: Mapped["ChecklistDay"] = relationship(back_populates="extra_topics")


class QuizTopic(Base):
    __tablename__ = "quiz_topics"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    topic_key: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)

    keywords: Mapped[list["QuizTopicKeyword"]] = relationship(
        back_populates="topic", cascade="all, delete-orphan"
    )
    subtopics: Mapped[list["QuizSubtopic"]] = relationship(
        back_populates="topic", cascade="all, delete-orphan"
    )


class QuizTopicKeyword(Base):
    __tablename__ = "quiz_topic_keywords"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    topic_id: Mapped[int] = mapped_column(
        ForeignKey("quiz_topics.id", ondelete="CASCADE"), nullable=False, index=True
    )
    keyword: Mapped[str] = mapped_column(String(255), nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    topic: Mapped["QuizTopic"] = relationship(back_populates="keywords")


class QuizSubtopic(Base):
    __tablename__ = "quiz_subtopics"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    completed: Mapped[bool] = mapped_column(Boolean)
    topic_id: Mapped[int] = mapped_column(
        ForeignKey("quiz_topics.id", ondelete="CASCADE"), nullable=False, index=True
    )
    subtopic_key: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    google_query: Mapped[str] = mapped_column(Text, nullable=False)

    __table_args__ = (
        UniqueConstraint("topic_id", "subtopic_key", name="uq_quiz_subtopics_topic_key"),
    )

    topic: Mapped["QuizTopic"] = relationship(back_populates="subtopics")
    matchers: Mapped[list["QuizSubtopicMatcher"]] = relationship(
        back_populates="subtopic", cascade="all, delete-orphan"
    )
    questions: Mapped[list["QuizQuestion"]] = relationship(
        back_populates="subtopic", cascade="all, delete-orphan"
    )


class QuizSubtopicMatcher(Base):
    __tablename__ = "quiz_subtopic_matchers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    subtopic_id: Mapped[int] = mapped_column(
        ForeignKey("quiz_subtopics.id", ondelete="CASCADE"), nullable=False, index=True
    )
    matcher: Mapped[str] = mapped_column(String(255), nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    subtopic: Mapped["QuizSubtopic"] = relationship(back_populates="matchers")


class QuizQuestion(Base):
    __tablename__ = "quiz_questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    subtopic_id: Mapped[int] = mapped_column(
        ForeignKey("quiz_subtopics.id", ondelete="CASCADE"), nullable=False, index=True
    )
    question_key: Mapped[str] = mapped_column(String(100), nullable=False)
    prompt: Mapped[str] = mapped_column(Text, nullable=False)
    answer: Mapped[str] = mapped_column(Text, nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    __table_args__ = (
        UniqueConstraint("subtopic_id", "question_key", name="uq_quiz_questions_subtopic_key"),
    )

    subtopic: Mapped["QuizSubtopic"] = relationship(back_populates="questions")
    accepted_phrases: Mapped[list["QuizQuestionAcceptedPhrase"]] = relationship(
        back_populates="question", cascade="all, delete-orphan"
    )


class QuizQuestionAcceptedPhrase(Base):
    __tablename__ = "quiz_question_accepted_phrases"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    question_id: Mapped[int] = mapped_column(
        ForeignKey("quiz_questions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    phrase: Mapped[str] = mapped_column(Text, nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    question: Mapped["QuizQuestion"] = relationship(back_populates="accepted_phrases")


class DashboardHero(Base):
    __tablename__ = "dashboard_hero"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    kicker: Mapped[str] = mapped_column(String(255), nullable=False)
    title_template: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    focus_items: Mapped[list["DashboardFocusItem"]] = relationship(
        back_populates="hero", cascade="all, delete-orphan"
    )


class DashboardFocusItem(Base):
    __tablename__ = "dashboard_focus_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    hero_id: Mapped[int] = mapped_column(
        ForeignKey("dashboard_hero.id", ondelete="CASCADE"), nullable=False, index=True
    )
    item_text: Mapped[str] = mapped_column(Text, nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    hero: Mapped["DashboardHero"] = relationship(back_populates="focus_items")


class SidebarConfig(Base):
    __tablename__ = "sidebar_config"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    brand: Mapped[str] = mapped_column(String(255), nullable=False)
    footer: Mapped[str] = mapped_column(Text, nullable=False)

    menu_items: Mapped[list["SidebarMenuItem"]] = relationship(
        back_populates="sidebar_config", cascade="all, delete-orphan"
    )


class SidebarMenuItem(Base):
    __tablename__ = "sidebar_menu_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sidebar_config_id: Mapped[int] = mapped_column(
        ForeignKey("sidebar_config.id", ondelete="CASCADE"), nullable=False, index=True
    )
    label: Mapped[str] = mapped_column(String(255), nullable=False)
    path: Mapped[str] = mapped_column(String(255), nullable=False)
    icon_key: Mapped[str] = mapped_column(String(120), nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    sidebar_config: Mapped["SidebarConfig"] = relationship(back_populates="menu_items")


class PracticeTopic(Base):
    __tablename__ = "practice_topics"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    topic_title: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    details: Mapped[str] = mapped_column(Text, nullable=False)
    code: Mapped[str] = mapped_column(Text, nullable=False)

    commands: Mapped[list["PracticeTopicCommand"]] = relationship(
        back_populates="practice_topic", cascade="all, delete-orphan"
    )


class PracticeTopicCommand(Base):
    __tablename__ = "practice_topic_commands"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    practice_topic_id: Mapped[int] = mapped_column(
        ForeignKey("practice_topics.id", ondelete="CASCADE"), nullable=False, index=True
    )
    command: Mapped[str] = mapped_column(Text, nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    practice_topic: Mapped["PracticeTopic"] = relationship(back_populates="commands")


class InterviewTopicMap(Base):
    __tablename__ = "interview_topic_map"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    topic_title: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    question: Mapped[str] = mapped_column(Text, nullable=False)
    answer: Mapped[str] = mapped_column(Text, nullable=False)
    code: Mapped[str] = mapped_column(Text, nullable=False)


class HeaderDefault(Base):
    __tablename__ = "header_defaults"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)


class InterviewStarterCommand(Base):
    __tablename__ = "interview_starter_commands"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    label: Mapped[str] = mapped_column(String(255), nullable=False)
    command: Mapped[str] = mapped_column(Text, nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
