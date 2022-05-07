from asyncpraw.models.reddit.comment import Comment, CommentModeration
from asyncpraw.models.reddit.submission import Submission, SubmissionModeration

content_type = Submission | Comment
mod_type = SubmissionModeration | CommentModeration
