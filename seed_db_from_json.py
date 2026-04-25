from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable, Type

from sqlalchemy.orm import Session

import database_models
from database import engine, session


JSON_DIR = Path(__file__).resolve().parent / "DBTablesJSON"

TABLE_MODEL_MAP: dict[str, type] = {
    "checklist_days": database_models.ChecklistDay,
    "checklist_tasks": database_models.ChecklistTask,
    "checklist_extra_topics": database_models.ChecklistExtraTopic,
    "quiz_topics": database_models.QuizTopic,
    "quiz_topic_keywords": database_models.QuizTopicKeyword,
    "quiz_subtopics": database_models.QuizSubtopic,
    "quiz_subtopic_matchers": database_models.QuizSubtopicMatcher,
    "quiz_questions": database_models.QuizQuestion,
    "quiz_question_accepted_phrases": database_models.QuizQuestionAcceptedPhrase,
    "dashboard_hero": database_models.DashboardHero,
    "dashboard_focus_items": database_models.DashboardFocusItem,
    "sidebar_config": database_models.SidebarConfig,
    "sidebar_menu_items": database_models.SidebarMenuItem,
    "practice_topics": database_models.PracticeTopic,
    "practice_topic_commands": database_models.PracticeTopicCommand,
    "interview_topic_map": database_models.InterviewTopicMap,
    "interview_starter_commands": database_models.InterviewStarterCommand,
    "header_defaults": database_models.HeaderDefault,
}

LOAD_ORDER: list[str] = [
    "checklist_days",
    "checklist_tasks",
    "checklist_extra_topics",
    "quiz_topics",
    "quiz_topic_keywords",
    "quiz_subtopics",
    "quiz_subtopic_matchers",
    "quiz_questions",
    "quiz_question_accepted_phrases",
    "dashboard_hero",
    "dashboard_focus_items",
    "sidebar_config",
    "sidebar_menu_items",
    "practice_topics",
    "practice_topic_commands",
    "interview_topic_map",
    "interview_starter_commands",
    "header_defaults",
]


def read_json_records(file_path: Path) -> list[dict[str, Any]]:
    with file_path.open("r", encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, list):
        raise ValueError(f"{file_path.name} must contain a JSON array of objects")
    return data


def seed_table(session: Session, table_name: str) -> int:
    model = TABLE_MODEL_MAP[table_name]
    json_path = JSON_DIR / f"{table_name}.json"
    if not json_path.exists():
        return 0

    records = read_json_records(json_path)
    count = 0
    for record in records:
        if not isinstance(record, dict):
            continue
        session.merge(model(**record))
        count += 1
    session.commit()
    return count


def seed_all() -> None:
    database_models.Base.metadata.create_all(bind=engine)
    db_session = session()
    try:
        for table_name in LOAD_ORDER:
            loaded = seed_table(db_session, table_name)
            print(f"Loaded {loaded} records into {table_name}")
    finally:
        db_session.close()


if __name__ == "__main__":
    seed_all()
