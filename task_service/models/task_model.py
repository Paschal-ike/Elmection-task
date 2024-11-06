# models/task_model.py

class Task:
    tasks = []
    id_counter = 1

    @classmethod
    def get_all_tasks(cls):
        return cls.tasks

    @classmethod
    def get_task_by_id(cls, task_id):
        return next((task for task in cls.tasks if task['id'] == task_id), None)

    @classmethod
    def create_task(cls, title, description):
        task = {
            "id": cls.id_counter,
            "title": title,
            "description": description,
            "completed": False
        }
        cls.tasks.append(task)
        cls.id_counter += 1
        return task

    @classmethod
    def update_task(cls, task_id, data):
        task = cls.get_task_by_id(task_id)
        if task:
            task.update({key: value for key, value in data.items() if key in task})
        return task
