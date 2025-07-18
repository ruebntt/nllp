# Обработка объяснения алгоритма Insertion Sort в виде таблицы (пример):
import pandas as pd

# Начальные данные
initial_array = [3, 2, 1, 5]
# Размер массива
n = len(initial_array)

# Таблица для хранения шагов
steps = []

# Создаем копию массива, чтобы не менять исходный
A = initial_array.copy()

for j in range(1, n):
    key = A[j]
    i = j - 1
    # Запоминаем состояние массива на этой итерации
    step_snapshot = {
        'j': j + 1,  # нумерация с 1 для удобства
        'A': A.copy()
    }
    # Внутренний цикл вставки
    while i >= 0 and A[i] > key:
        A[i + 1] = A[i]
        i -= 1
    A[i + 1] = key
    # Запоминаем состояние после вставки
    step_snapshot['A_after'] = A.copy()
    steps.append(step_snapshot)

# Вывод таблицы
df = pd.DataFrame(steps)
print(df)










 Общий код для выполнения этого анализа:

CopyRun
import pandas as pd

def insertion_sort_steps(array):
    n = len(array)
    A = array.copy()
    steps = []

    for j in range(1, n):
        key = A[j]
        i = j - 1
        # Запоминаем состояние перед вставкой
        step_snapshot = {
            'j': j + 1,
            'A_before': A.copy()
        }
        while i >= 0 and A[i] > key:
            A[i + 1] = A[i]
            i -= 1
        A[i + 1] = key
        # Запоминаем состояние после вставки
        step_snapshot['A_after'] = A.copy()
        steps.append(step_snapshot)
    return steps

# Пример
initial_array = [3, 2, 1, 5]
steps = insertion_sort_steps(initial_array)

# Форматирование вывода
for step in steps:
    print(f"j={step['j']}, Before: {step['A_before']}, After: {step['A_after']}")



requirements.txt:

CopyRun
Flask==2.2.3
SQLAlchemy==2.0.19
psycopg2-binary==2.9.5
pytest==7.3.1
gunicorn==20.1.0



Основной код приложения (app.py):
CopyRun
from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import os

# Конфигурация соединения
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost:5432/mydb')

engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20, pool_timeout=30, pool_recycle=1800)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

app = Flask(__name__)

# Модель пользователя с правами
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    permissions = Column(String)  # например, 'read', 'write', 'admin'

# Создаем таблицы
def init_db():
    Base.metadata.create_all(bind=engine)

@app.before_first_request
def setup():
    init_db()

# Простая маршрутизация с проверкой прав
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    username = data.get('username')
    permissions = data.get('permissions', 'read')
    session = SessionLocal()
    try:
        user = User(username=username, permissions=permissions)
        session.add(user)
        session.commit()
        return jsonify({'id': user.id, 'username': user.username, 'permissions': user.permissions})
    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    session = SessionLocal()
    try:
        user = session.query(User).filter(User.id == user_id).first()
        if user:
            return jsonify({'id': user.id, 'username': user.username, 'permissions': user.permissions})
        else:
            return jsonify({'error': 'User not found'}), 404
    finally:
        session.close()

# Обработка ошибок для отказоустойчивости
@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Для запуска с Gunicorn или напрямую
    app.run(host='0.0.0.0', port=5000, debug=False)
























