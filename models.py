from pydantic import BaseModel, ConfigDict


class User(BaseModel):
    id: int | None = None
    fullName: str
    mobileNumber: str
    username: str
    password: str
    role: str

    model_config = ConfigDict(populate_by_name=True, extra="ignore")


class LoginRequest(BaseModel):
    username: str
    password: str


class ChecklistDay(BaseModel):
    id: int | None = None
    day_number: int
    title: str

    model_config = ConfigDict(populate_by_name=True, extra="ignore")


class ChecklistTask(BaseModel):
    id: int | None = None
    day_id: int
    task_text: str
    done_default: bool = False
    sort_order: int = 0

    model_config = ConfigDict(populate_by_name=True, extra="ignore")


class ChecklistExtraTopic(BaseModel):
    id: int | None = None
    day_id: int
    title: str
    details: str
    question: str
    answer: str
    code: str
    command: str
    sort_order: int = 0

    model_config = ConfigDict(populate_by_name=True, extra="ignore")


class QuizTopic(BaseModel):
    id: int | None = None
    topic_key: str
    title: str

    model_config = ConfigDict(populate_by_name=True, extra="ignore")


class QuizTopicKeyword(BaseModel):
    id: int | None = None
    topic_id: int
    keyword: str
    sort_order: int = 0

    model_config = ConfigDict(populate_by_name=True, extra="ignore")


class QuizSubtopic(BaseModel):
    id: int | None = None
    topic_id: int
    subtopic_key: str
    title: str
    google_query: str

    model_config = ConfigDict(populate_by_name=True, extra="ignore")


class QuizSubtopicMatcher(BaseModel):
    id: int | None = None
    subtopic_id: int
    matcher: str
    sort_order: int = 0

    model_config = ConfigDict(populate_by_name=True, extra="ignore")


class QuizQuestion(BaseModel):
    id: int | None = None
    subtopic_id: int
    question_key: str
    prompt: str
    answer: str
    sort_order: int = 0

    model_config = ConfigDict(populate_by_name=True, extra="ignore")


class QuizQuestionAcceptedPhrase(BaseModel):
    id: int | None = None
    question_id: int
    phrase: str
    sort_order: int = 0

    model_config = ConfigDict(populate_by_name=True, extra="ignore")


class DashboardHero(BaseModel):
    id: int | None = None
    kicker: str
    title_template: str
    description: str

    model_config = ConfigDict(populate_by_name=True, extra="ignore")


class DashboardFocusItem(BaseModel):
    id: int | None = None
    hero_id: int
    item_text: str
    sort_order: int = 0

    model_config = ConfigDict(populate_by_name=True, extra="ignore")


class SidebarConfig(BaseModel):
    id: int | None = None
    brand: str
    footer: str

    model_config = ConfigDict(populate_by_name=True, extra="ignore")


class SidebarMenuItem(BaseModel):
    id: int | None = None
    sidebar_config_id: int
    label: str
    path: str
    icon_key: str
    sort_order: int = 0

    model_config = ConfigDict(populate_by_name=True, extra="ignore")


class PracticeTopic(BaseModel):
    id: int | None = None
    topic_title: str
    details: str
    code: str

    model_config = ConfigDict(populate_by_name=True, extra="ignore")


class PracticeTopicCommand(BaseModel):
    id: int | None = None
    practice_topic_id: int
    command: str
    sort_order: int = 0

    model_config = ConfigDict(populate_by_name=True, extra="ignore")


class InterviewTopicMap(BaseModel):
    id: int | None = None
    topic_title: str
    question: str
    answer: str
    code: str

    model_config = ConfigDict(populate_by_name=True, extra="ignore")


class InterviewStarterCommand(BaseModel):
    id: int | None = None
    label: str
    command: str
    sort_order: int = 0

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

