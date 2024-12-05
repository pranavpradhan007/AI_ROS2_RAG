from clearml import Task, Logger

_task = None

def get_task():
    global _task
    if _task is None:
        try:
            current_task = Task.current_task()
            if current_task:
                return current_task
        except:
            pass
        _task = Task.create(project_name='RAG_System', task_name='RAG_Pipeline')
    return _task

def init_clearml():
    return get_task()

