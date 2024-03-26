import psycopg2
import configparser


# Функция для чтения password (пароль к postgresSQL),
# name_bd (название базы данных) из файла 'password.ini'
def get_password():
    data = configparser.ConfigParser()
    data.read('password.ini')
    password = data["password"]["password"]
    name_bd = data["password"]["name_bd"]
    user = data["password"]["user"]
    return [password, name_bd, user]


# 1.Функция DROP удаления (если есть) и создания (без данных) таблиц VK_Partners, VK_Photos, VK_Settings
def drop_create_table():
    with psycopg2.connect(database=get_password()[1], user=get_password()[2], password=get_password()[0]) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                DROP TABLE IF EXISTS VK_Partners CASCADE;

                """)
            conn.commit()

            cur.execute("""
                CREATE TABLE IF NOT EXISTS VK_Partners (
                    id SERIAL PRIMARY KEY,
                    first_name VARCHAR(100) NOT NULL,
                    last_name VARCHAR(100),
                    partner_id VARCHAR(20) UNIQUE NOT NULL,
                    partner_link VARCHAR(100) NOT NULL,
                    favorite BOOLEAN NOT NULL DEFAULT False,
                    ban BOOLEAN NOT NULL DEFAULT False);
                 """)
            conn.commit()

            cur.execute("""
                CREATE TABLE IF NOT EXISTS VK_Photos (
                    id SERIAL PRIMARY KEY,
                    partner_id VARCHAR(20) NOT NULL REFERENCES VK_Partners(partner_id),
                    photo_link VARCHAR(100) NOT NULL);
                """)
            conn.commit()

            cur.execute("""
                CREATE TABLE IF NOT EXISTS VK_Settings (
                    id SERIAL PRIMARY KEY,
                    conf_name VARCHAR(20) NOT NULL,
                    conf_value VARCHAR(250) NOT NULL);
                 """)
            conn.commit()


# 2.Функция добавления партнеров в таблицу VK_Partners
# Запись данных по каждому партнеру first_name, last_name, partner_id, partner_link
def add_partner(first_name, last_name, partner_id, partner_link):
    with psycopg2.connect(database=get_password()[1], user=get_password()[2], password=get_password()[0]) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO vk_partners(first_name, last_name, partner_id, partner_link) 
                VALUES(%s, %s, %s, %s)
                RETURNING first_name, last_name, partner_id, favorite, ban
                """, (first_name, last_name, partner_id, partner_link))
            new_VK_Partners = cur.fetchone()
            print(f'Добавлен партнер {new_VK_Partners}')
            conn.commit()
    conn.close()


# 3.Функция добавления фото в таблицу VK_Partners
def add_photo(partner_id, photo_link):
    with psycopg2.connect(database=get_password()[1], user=get_password()[2], password=get_password()[0]) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO VK_Photos(partner_id, photo_link) 
                VALUES(%s, %s)
                RETURNING partner_id, photo_link
                """, (partner_id, photo_link))
            new_VK_Photos = cur.fetchone()
            print(f'Добавлено фото партнера id({new_VK_Photos[0]}) link({new_VK_Photos[1]})')
            conn.commit()
    conn.close()


# 4.Функция получения количества партнеров
def select_count_partners():
    with psycopg2.connect(database=get_password()[1], user=get_password()[2], password=get_password()[0]) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT COUNT(*)
                FROM VK_Partners
                """)
            count = cur.fetchone()
            return count[0]
            conn.commit()
    conn.close()


# 5.Функция проверки, что партнер (partner_id) в бане (ban = True или False)
def check_ban_partner(partner_id):
    with psycopg2.connect(database=get_password()[1], user=get_password()[2], password=get_password()[0]) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT ban
                FROM VK_Partners
                WHERE partner_id = %s;
                """, (partner_id,))
            check_ban = cur.fetchone()
            return check_ban
            conn.commit()
    conn.close()


# 6.Функция добавления партнера (partner_id) в бан (ban = True)
def add_ban_partner(partner_id):
    with psycopg2.connect(database=get_password()[1], user=get_password()[2], password=get_password()[0]) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE VK_Partners
                SET ban = True
                WHERE partner_id = %s;
                """, (partner_id,))
            conn.commit()
    conn.close()


# 7.Функция проверки, что партнер (partner_id) в избранном (favorite = True или False)
def check_favorite_partner(partner_id):
    with psycopg2.connect(database=get_password()[1], user=get_password()[2], password=get_password()[0]) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT favorite
                FROM VK_Partners
                WHERE partner_id = %s;
                """, (partner_id,))
            check_favorite = cur.fetchone()
            return check_favorite
            conn.commit()
    conn.close()


# 8.Функция добавления партнера (partner_id) в избранное (favorite = True)
def add_favorite_partner(partner_id):
    with psycopg2.connect(database=get_password()[1], user=get_password()[2], password=get_password()[0]) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE VK_Partners
                SET favorite = True
                WHERE partner_id = %s;
                """, (partner_id,))
            conn.commit()
    conn.close()


# 9.Функция получения всех данных о партнере (имя, фамилия, partner_id, фото)
def select_partner(partner_id):
    with psycopg2.connect(database=get_password()[1], user=get_password()[2], password=get_password()[0]) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT first_name, last_name, VK_Partners.partner_id, photo_link
                FROM VK_Partners JOIN VK_Photos ON VK_Partners.partner_id = VK_Photos.partner_id
                WHERE VK_Partners.partner_id = %s;
                """, (partner_id,))
            partner = cur.fetchall()
            return partner
            conn.commit()
    conn.close()


# 10.Функция получения данных о партнере (имя, фамилия, линк) по id из таблицы VK_Partners
def select_partner_fn_ln_link(partner_id):
    with psycopg2.connect(database=get_password()[1], user=get_password()[2], password=get_password()[0]) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT first_name, last_name, partner_link
                FROM VK_Partners 
                WHERE partner_id = %s;
                """, (partner_id,))
            partner = cur.fetchone()
            partner_str = f'{partner[0]} {partner[1]}, {partner[2]}'
            return partner_str
            conn.commit()
    conn.close()


# 11.Функция получения данных о партнере (partner_id) по id из таблицы VK_Partners
def select_partner_id(id):
    with psycopg2.connect(database=get_password()[1], user=get_password()[2], password=get_password()[0]) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                 SELECT partner_id
                 FROM VK_Partners 
                 WHERE id = %s;
                 """, (id,))
            partner = cur.fetchone()
            return partner
            conn.commit()
    conn.close()


# 11.1 Функция получения id записи по значени partner_id из таблицы VK_Partners
def select_id(partner_id):
    with psycopg2.connect(database=get_password()[1], user=get_password()[2], password=get_password()[0]) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                 SELECT id
                 FROM VK_Partners 
                 WHERE partner_id = %s;
                 """, (partner_id,))
            partner = cur.fetchone()
            return id[0]
            conn.commit()
    conn.close()


# 12.Функция получаем фото из таблицы VK_Photos по partner_id (id партнера)
def get_photo(partner_id):
    with psycopg2.connect(database=get_password()[1], user=get_password()[2], password=get_password()[0]) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT photo_link
                FROM VK_Photos
                WHERE partner_id = %s;
                """, (partner_id,))
            # photo = cur.fetchall()
            photo = [r[0] for r in cur.fetchall()]
            return photo
            conn.commit()
    conn.close()

    # 13.Функция добавления conf_name, conf_value в таблицу VK_Settings


def add_conf(conf_name, conf_value):
    with psycopg2.connect(database=get_password()[1], user=get_password()[2], password=get_password()[0]) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO VK_Settings(conf_name, conf_value) 
                VALUES(%s, %s)
                RETURNING conf_name, conf_value
                """, (conf_name, conf_value))
            new_VK_Settings = cur.fetchone()
            print(f'Добавлены данные {new_VK_Settings}')
            conn.commit()
    conn.close()


# 14.Функция получения conf_value из таблицы VK_Settings по значению conf_name
def get_VK_Settings_conf_value(conf_name):
    with psycopg2.connect(database=get_password()[1], user=get_password()[2], password=get_password()[0]) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT conf_value
                FROM VK_Settings
                WHERE conf_name = %s;
                """, (conf_name,))
            conf_name = cur.fetchall()
            return conf_name[0][0]
            conn.commit()
    conn.close()


# 15.Функция удаления записи conf_value из таблицы VK_Settings по значению conf_name
def del_VK_Settings_conf_value(conf_name):
    with psycopg2.connect(database=get_password()[1], user=get_password()[2], password=get_password()[0]) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                DELETE FROM VK_Settings
                WHERE conf_name = %s
                RETURNING conf_name;
                """, (conf_name,))
            conf_name = cur.fetchall()
            conf_name_list = [i[0] for i in conf_name]
            print(f'запись {conf_name_list} удалена')
            conn.commit()
    conn.close()