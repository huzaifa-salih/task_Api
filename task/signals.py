from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from task.models import COMPLETED, NOT_COMPLETED, Task


@receiver(post_save, sender=Task)
def update_house_points(sender, instance, created, **kwargs):
    house = instance.task_list.house
    if instance.status == COMPLETED:
        house.points += 10
    elif instance.status == NOT_COMPLETED:
        if house.points > 10:
            house.points -= 10
    house.save()


@receiver(post_save, sender=Task)
def update_tasklist_status(sender, instance, created, **kwargs):
    task_list = instance.task_list
    is_complete = True
    for task in task_list.tasks.all():
        if task.status != "COMPLETED":
            is_complete = False
            break
    task_list.status = COMPLETED if is_complete else NOT_COMPLETED
    task_list.save()
