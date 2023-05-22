from datetime import date, datetime, timedelta
from random import randint, choice
import faker
from sqlalchemy import select

from database.models import Teacher, Student, Discipline, Grade, Group
from database.db import session



def date_range(start: date, end: date) -> list:
    result = []
    current_date = start
    while current_date <= end:
        if current_date.isoweekday() < 6:
            result.append(current_date)
        current_date += timedelta(1)
    return result



def fill_data():
    disciplines = [
    "Математичний аналіз",
    "Дискретна математика",
    "Геометрія",
    "Програмування",
    "Теорія імовірності",
    "Англійська",
    "Основи баз даних"
]

    groups = ['ДК-21', 'ДК-22', 'ДК-23']

    fake = faker.Faker('uk-UA')
    number_of_teachers = 7
    number_of_students = 50

    def seed_teachers():
        for _ in range(number_of_teachers):
            teacher = Teacher(fullname=fake.name())
            session.add(teacher)
        session.commit()

    def seed_disciplines():
        teacher_ids = session.scalars(select(Teacher.id)).all()
        for discipline in disciplines:
            session.add(Discipline(name=discipline, teacher_id=choice(teacher_ids)))
        session.commit()

    def seed_groups():
        for group in groups:
            session.add(Group(name=group))
        session.commit()

    def seed_students():
        group_ids = session.scalars(select(Group.id)).all()
        for _ in range(number_of_students):
            student = Student(fullname=fake.name(), group_id=choice(group_ids))
            session.add(student)
        session.commit()

    def seed_grades():
        start_date = datetime.strptime("2022-09-01", "%Y-%m-%d")
        end_date = datetime.strptime("2023-06-15", "%Y-%m-%d")

        def get_list_date(start: date, end: date) -> list[date]:
            result = []
            current_date = start
            while current_date <= end:
                if current_date.isoweekday() < 6:
                    result.append(current_date)
                current_date += timedelta(1)
            return result

        list_dates = get_list_date(start_date, end_date)

        for day in list_dates:
            random_subject = randint(1, len(disciplines))
            random_students = [randint(1, number_of_students) for _ in range(5)]
            for student in random_students:
                grade = Grade(grade=randint(10, 100), date_of=day.date(), student_id=student,
                              discipline_id=random_subject)
                session.add(grade)
        session.commit()

    seed_teachers()
    seed_disciplines()
    seed_groups()
    seed_students()
    seed_grades()


if __name__ == '__main__':
    fill_data()
