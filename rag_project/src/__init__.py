from clearml import Task

_task = None

def get_task():
    global _task
    if _task is None:
        try:
            Task.close()
        except:
            pass
        _task = Task.init(project_name='RAG_System', task_name='RAG_Pipeline')
    return _task