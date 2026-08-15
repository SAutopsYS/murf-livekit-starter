# 42 — Education Experience Platform

Teacher / student / parent layer. No new score store.

Wraps `LearningService`, `TeacherConsoleService`, `ParentDashboardService`, tenant classrooms.

`ExperienceProvider` projects `buildLearningIntelligence`. Do not mount on the hall.

Events: StudentJoined, LessonCompleted, AssignmentSubmitted, ProgressUpdated, ParentNotified.

Attendance/assignments are engines, not UIs.
