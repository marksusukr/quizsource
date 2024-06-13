import sqlite3
from random import randint

db_name = 'quiz.sqlite'
conn = None
cursor = None

def open():
    global conn, cursor
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

def close():
    cursor.close()
    conn.close()

def do(query):
    cursor.execute(query)
    conn.commit()

def clear_db():
    open()
    query = '''DROP TABLE IF EXISTS quiz_content'''
    do(query)
    query = '''DROP TABLE IF EXISTS question'''
    do(query)
    query = '''DROP TABLE IF EXISTS quiz'''
    do(query)
    close()

def create():
    open()
    cursor.execute('''PRAGMA foreign_keys=on''')
    
    do('''CREATE TABLE IF NOT EXISTS quiz (
            id INTEGER PRIMARY KEY, 
            name VARCHAR,
            image_url VARCHAR)''' 
    )
    do('''CREATE TABLE IF NOT EXISTS question (
                id INTEGER PRIMARY KEY, 
                question VARCHAR, 
                answer VARCHAR, 
                wrong1 VARCHAR, 
                wrong2 VARCHAR, 
                wrong3 VARCHAR)'''
    )
    do('''CREATE TABLE IF NOT EXISTS quiz_content (
                id INTEGER PRIMARY KEY,
                quiz_id INTEGER,
                question_id INTEGER,
                FOREIGN KEY (quiz_id) REFERENCES quiz (id),
                FOREIGN KEY (question_id) REFERENCES question (id) )'''
    )
    close()

def show(table):
    query = 'SELECT * FROM ' + table
    open()
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    close()

def show_tables():
    show('question')
    show('quiz')
    show('quiz_content')

def add_questions():
    questions = [
        ('2+2=', '4', '5', '3', '22'),
        ('√100=', '10', '25', '50', '1'),
        ('5^2=', '25', '10', '50', '15'),
        ('Що таке Пайтон?', 'Мова програмування', 'Мова розмітки', 'Змія', 'Ігровий рушій'),
        ('Що таке HTML?', 'Мова розмітки гіпертексту', 'Мова програмування', 'Букви ', 'Щось на омериканському'),
        ('Як запустити комп\'ютер?', 'Натиснути кнопку живлення', 'Вдарити кулаком по столу', 'Викинути його у вікно', 'Увімкнути його в розетку'),
        ('Що таке підмет?', 'Це головний член двоскладного речення', 'Рисочка знизу слова', 'Я внє палітікі', 'Палка'),
        ('Хто така Леся Українка?', 'Письменниця', 'Тьотка З України', 'Леся', 'Хз'),
        ('Що таке дієслово?', 'Самостійна частина мови', 'Слово', 'Дія', 'Я незнаю')
    ]
    open()
    cursor.executemany('''INSERT INTO question (question, answer, wrong1, wrong2, wrong3) VALUES (?,?,?,?,?)''', questions)
    conn.commit()
    close()

def add_quiz():
    quizes = [
        ('Математика', 'https://www.englishdom.com/dynamicus/blog-post/000/002/256/1621948173_content_700x455.jpg'),
        ('Інформатика', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSVjKCMAwF4Z0MIcT2DFWv1NT7c5Jw_7Lf-wA&usqp=CAU'),
        ('Укр. Мова', 'https://glavcom.ua/img/article/8880/87_main-v1668012343.jpg')
    ]
    open()
    cursor.executemany('''INSERT INTO quiz (name, image_url) VALUES (?,?)''', quizes)
    conn.commit()
    close()

def add_links():
    open()
    cursor.execute('''PRAGMA foreign_keys=on''')
    query = "INSERT INTO quiz_content (quiz_id, question_id) VALUES (?,?)"
    answer = input("Додати зв'язок (y / n)?")
    while answer != 'n':
        quiz_id = int(input("id вікторини: "))
        question_id = int(input("id питання: "))
        cursor.execute(query, [quiz_id, question_id])
        conn.commit()
        answer = input("Додати зв'язок (y / n)?")
    close()


def get_question_after(last_id=0, vict_id=1):
    open()
    query = '''
    SELECT quiz_content.id, question.question, question.answer, question.wrong1, question.wrong2, question.wrong3
    FROM question, quiz_content 
    WHERE quiz_content.question_id == question.id
    AND quiz_content.id > ? AND quiz_content.quiz_id == ? 
    ORDER BY quiz_content.id '''
    cursor.execute(query, [last_id, vict_id] )
    result = cursor.fetchone()
    close()
    return result 

def get_quizes():
    query = 'SELECT * FROM quiz ORDER BY id'
    open()
    cursor.execute(query)
    result = cursor.fetchall()
    close()
    return result 

def check_answer(q_id, ans_text):
    query = '''
            SELECT question.answer 
            FROM quiz_content, question 
            WHERE quiz_content.id = ? 
            AND quiz_content.question_id = question.id
        '''
    open()
    cursor.execute(query, str(q_id))
    result = cursor.fetchone()
    close()    
    if result is None:
        return False 
    else:
        if result[0] == ans_text:
            return True 
        else:
            return False 

def get_quiz_count():
    query = 'SELECT MAX(quiz_id) FROM quiz_content'
    open()
    cursor.execute(query)
    result = cursor.fetchone()
    close()
    return result 

def get_random_quiz_id():
    query = 'SELECT quiz_id FROM quiz_content'
    open()
    cursor.execute(query)
    ids = cursor.fetchall()
    rand_num = randint(0, len(ids) - 1)
    rand_id = ids[rand_num][0]
    close()
    return rand_id

def main():
    clear_db()
    create()
    add_questions()
    add_quiz()
    show_tables()
    add_links()
    show_tables()
    pass
    
if __name__ == "__main__":
    main()
