from fastapi import APIRouter, Depends, HTTPException
from models import AnswerMatch
import database_models
from database import get_db
from sqlalchemy.orm import Session
# from auth_token import get_current_user

router = APIRouter()


@router.get("/ChecklistDay/{userId}")
def get_all_checlist(userId: int, db: Session = Depends(get_db)):
    db_checklist = db.query(database_models.ChecklistDay).all()
    # db_sub_checklist = db.query(database_models.ChecklistTask).all()
    db_final_checklist = []
    for i in db_checklist:
        db_sub_checklist = db.query(database_models.ChecklistTask).filter(
            database_models.ChecklistTask.day_id == i.id
        ).order_by(database_models.ChecklistTask.sort_order.asc()).all()
        sub_task_list = []
        for subTask in db_sub_checklist:
            user_task_status = db.query(database_models.UserBasedTaskCompleted).filter(
                database_models.UserBasedTaskCompleted.user_id == userId,
                database_models.UserBasedTaskCompleted.sub_topic_id == subTask.id,
                database_models.UserBasedTaskCompleted.topic_id == subTask.day_id,
            ).first()
            task_obj = subTask
            task_obj.done_default = user_task_status.task_completed
            sub_task_list.append(task_obj)
        db_obj = i
        db_obj.tasks = sub_task_list
        db_obj.userId = userId
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

            dn_quiz_question = db.query(database_models.QuizQuestion).filter(database_models.QuizQuestion.subtopic_id == j.id).all()
            dn_quiz_question_arr = []
            for g in dn_quiz_question:

                db_quiz_question_accepted_phrase = db.query(database_models.QuizQuestionAcceptedPhrase).filter(database_models.QuizQuestionAcceptedPhrase.question_id == g.id).all()
                db_quiz_question_accepted_phrases = [cmd.phrase for cmd in db_quiz_question_accepted_phrase]

                dn_quiz_question_obj = {
                    "id": g.id,
                    "prompt": g.prompt,
                    "answer": g.answer,
                    "acceptedPhrases": db_quiz_question_accepted_phrases,
                }
                dn_quiz_question_arr.append(dn_quiz_question_obj)
            subtopic_obj = {
                "id": j.id,
                "title": j.title,
                "googleQuery": j.google_query,
                "matchers": db_quiz_subtopic_matchers,
                "questions": dn_quiz_question_arr,
                "completed": j.completed
            }
            dn_quiz_question_arr = []

            quiz_subtopics_arr.append(subtopic_obj)

        topicObj = {
            "id": i.id,
            "title": i.title,
            "keywords": db_quiz_topic_keywords,
            "subtopics": quiz_subtopics_arr
        }


        db_final_quiz_tpoics.append(topicObj)

    return {"topics": db_final_quiz_tpoics}

@router.get("/subtopic-questions/{subtopicId}")
def sub_topic_questions( subtopicId: int, db: Session = Depends(get_db)):
    dn_quiz_question = db.query(database_models.QuizQuestion).filter(database_models.QuizQuestion.subtopic_id == subtopicId).all()
    dn_quiz_question_arr = []
    for g in dn_quiz_question:

        db_quiz_question_accepted_phrase = db.query(database_models.QuizQuestionAcceptedPhrase).filter(database_models.QuizQuestionAcceptedPhrase.question_id == g.id).all()
        db_quiz_question_accepted_phrases = [cmd.phrase for cmd in db_quiz_question_accepted_phrase]

        dn_quiz_question_obj = {
            "id": g.id,
            "prompt": g.prompt,
            "answer": g.answer,
            "acceptedPhrases": db_quiz_question_accepted_phrases,
        }
        dn_quiz_question_arr.append(dn_quiz_question_obj)

    return dn_quiz_question_arr

@router.post("/check-answer")
def check_answer(answerMatches: list[AnswerMatch], db: Session = Depends(get_db)):

    try:
        updated = 0
        for match in answerMatches:
            user_based_task_completed = db.query(database_models.UserBasedTaskCompleted).filter(
                database_models.UserBasedTaskCompleted.user_id == match.user_id,
                database_models.UserBasedTaskCompleted.topic_id == match.topicId,
                database_models.UserBasedTaskCompleted.sub_topic_id == match.subtopicId
            ).first()
            if user_based_task_completed:
                dn_quiz_question = db.query(database_models.QuizQuestion).filter(
                    database_models.QuizQuestion.subtopic_id == match.subtopicId, 
                    database_models.QuizQuestion.id == match.id, 
                    ).first()
                if match.answer != dn_quiz_question.answer:
                    user_based_task_completed.task_completed = False
                    db.commit()
                    return {"success": False}
                user_based_task_completed.task_completed = True if match.answer == dn_quiz_question.answer else False
                updated += 1

        # commit once after processing all items
        db.commit()

        return {"success": True, "updated": updated}
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(exc)}")

@router.put("/restart/{user_id}")
def restart_quiz(user_id: int, db: Session = Depends(get_db)):
    try:
        user_task_completed = db.query(database_models.UserBasedTaskCompleted).filter(
            database_models.UserBasedTaskCompleted.user_id == user_id
        ).all()
        for user_task in user_task_completed:
            user_task.task_completed = False
        db.commit()
        return {"success": True, "updated": len(user_task_completed), "message": "All quiz progress reset"}
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(exc)}")
   

def create_user_tasks( db: Session) -> dict:
    """
    Helper function to create user task records.
    Can be called from other modules like auth_api.
    """
    try:
        # Check if user already has task records
        
        db_sub_checklist = db.query(database_models.ChecklistTask).all()
        db_users = db.query(database_models.User).all()
        # If no records exist, create them for all tasks
        for user in db_users:
            for task in db_sub_checklist:
                existing_records = db.query(database_models.UserBasedTaskCompleted).filter(
                    database_models.UserBasedTaskCompleted.user_id == user.id,
                    database_models.UserBasedTaskCompleted.topic_id == task.day_id,
                    database_models.UserBasedTaskCompleted.sub_topic_id == task.id,
                    ).first()
                if not existing_records:
                    new_record = database_models.UserBasedTaskCompleted(
                        user_id=user.id,
                        topic_id=task.day_id,
                        sub_topic_id=task.id,
                        task_completed=False
                    )
                    db.add(new_record)
        db.commit()
        return {"success": True, "created": len(db_sub_checklist)}
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating user tasks: {str(exc)}")
