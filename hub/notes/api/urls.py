from django.urls import path
from .views import (
    NoteRepositoryList,
    NoteRepositoryDetail,
    NoteFileList,
    NoteContentDetail,
    SyncNotesView,
    QuickSyncView,
    FileTreeView,
    NoteDetailView,
    UploadNoteView,
    DeleteNoteView,
    InitializeLocalRepoView
)

urlpatterns = [
    path('repositories/', NoteRepositoryList.as_view(), name='note-repository-list'),
    path('repositories/<int:pk>/', NoteRepositoryDetail.as_view(), name='note-repository-detail'),
    path('repositories/<int:repository_id>/notes/', NoteFileList.as_view(), name='note-file-list'),
    path('repositories/<int:repository_id>/notes/<path:file_path>/', NoteContentDetail.as_view(), name='note-content-detail'),
    path('repositories/<int:repository_id>/sync/', SyncNotesView.as_view(), name='sync-notes'),
    path('sync/', QuickSyncView.as_view(), name='quick-sync'),
    path('repositories/<int:repository_id>/file-tree/', FileTreeView.as_view(), name='file-tree'),
    path('repositories/<int:repository_id>/note/<path:file_path>/', NoteDetailView.as_view(), name='note-detail'),
    path('repositories/<int:repository_id>/upload/', UploadNoteView.as_view(), name='upload-note'),
    path('repositories/<int:repository_id>/delete/', DeleteNoteView.as_view(), name='delete-note'),
    path('init-local-repo/', InitializeLocalRepoView.as_view(), name='init-local-repo'),
]
