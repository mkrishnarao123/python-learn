from fastapi import APIRouter, Depends
import database_models
from database import get_db
from sqlalchemy.orm import Session
# from auth_token import get_current_user

router = APIRouter()

@router.get("/ChecklistDay")
def get_all_checlist(db: Session = Depends(get_db)):
    db_checklist = db.query(database_models.ChecklistDay).all()
    # db_sub_checklist = db.query(database_models.ChecklistTask).all()
    db_final_checklist = []
    for i in db_checklist:
        db_sub_checklist = db.query(database_models.ChecklistTask).filter(database_models.ChecklistTask.day_id == i.id).all()
        db_obj = i
        db_obj.tasks = db_sub_checklist
        db_final_checklist.append(db_obj)
    return db_final_checklist

@router.get("/menu-list")
def get_menu_list(db: Session = Depends(get_db)):
    db_sidebar_config = db.query(database_models.SidebarConfig).all()
    db_sidebar_menu = db.query(database_models.SidebarMenuItem).all()
    db_sidebar = db_sidebar_config[0]
    db_sidebar.menuItems = db_sidebar_menu
    return db_sidebar

@router.get("/interview-qa")
def get_interview_qa(db: Session = Depends(get_db)):
    db_interview_topics = db.query(database_models.InterviewTopicMap).all()
    db_interview_starter_commands = db.query(database_models.InterviewStarterCommand).all()
    topicMap = {}
    for i in db_interview_topics:
        key = i.topic_title
        topicMap[key] = i

    interview_qa = {"topicMap": topicMap, "starterCommands": db_interview_starter_commands}
    return interview_qa

@router.get("/practice-topics")
def get_practice_topics(db: Session = Depends(get_db)):
    db_practice_topic = db.query(database_models.PracticeTopic).all()
    topicMap = {}
    for i in db_practice_topic:
        db_practice_topic_command = db.query(database_models.PracticeTopicCommand).filter(database_models.PracticeTopicCommand.practice_topic_id == i.id).all()
        db_practice_topic_commands = [cmd.command for cmd in db_practice_topic_command]
        key = i.topic_title
        topicMap[key] = {
            "id": i.id,
            "topic_title": i.topic_title,
            "details": i.details,
            "code": i.code,
            "commands": db_practice_topic_commands,
        }
    # practice_topic_id
    interview_qa = {"topicMap": topicMap}
    return interview_qa

@router.get("/quiz-bank")
def get_quiz_bank(db: Session = Depends(get_db)):
    db_quiz_topic = db.query(database_models.QuizTopic).all()

    db_final_quiz_tpoics = []
    for i in db_quiz_topic:

        db_quiz_topic_keyword = db.query(database_models.QuizTopicKeyword).filter(database_models.QuizTopicKeyword.topic_id == i.id).all()
        db_quiz_topic_keywords = [cmd.keyword for cmd in db_quiz_topic_keyword]

        db_quiz_subtopics = db.query(database_models.QuizSubtopic).filter(database_models.QuizSubtopic.topic_id == i.id).all()
        quiz_subtopics_arr = []
        for j in db_quiz_subtopics:

            db_quiz_subtopic_matcher = db.query(database_models.QuizSubtopicMatcher).filter(database_models.QuizSubtopicMatcher.subtopic_id == j.id).all()
            db_quiz_subtopic_matchers = [cmd.matcher for cmd in db_quiz_subtopic_matcher]

            dn_quiz_question = db.query(database_models.QuizQuestion).all()
            dn_quiz_question_arr = []
            for g in dn_quiz_question:

                db_quiz_question_accepted_phrase = db.query(database_models.QuizQuestionAcceptedPhrase).filter(database_models.QuizQuestionAcceptedPhrase.question_id == g.id).all()
                db_quiz_question_accepted_phrases = [cmd.phrase for cmd in db_quiz_question_accepted_phrase]

                dn_quiz_question_obj = {
                    "id": g.question_key,
                    "prompt": g.prompt,
                    "answer": g.answer,
                    "acceptedPhrases": db_quiz_question_accepted_phrases,
                }
                dn_quiz_question_arr.append(dn_quiz_question_obj)

            subtopic_obj = {
                "id": j.subtopic_key,
                "title": j.title,
                "googleQuery": j.google_query,
                "matchers": db_quiz_subtopic_matchers,
                "questions": dn_quiz_question_arr,
            }

            quiz_subtopics_arr.append(subtopic_obj)

        topicObj = {
            "id": i.topic_key,
            "title": i.title,
            "keywords": db_quiz_topic_keywords,
            "subtopics": quiz_subtopics_arr
        }


        db_final_quiz_tpoics.append(topicObj)

    return {"topics": db_final_quiz_tpoics}