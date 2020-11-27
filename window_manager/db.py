import psycopg2
from .config import DB_HOST, DB_USER, DB_NAME, DB_PASSWORD

db_conn = psycopg2.connect(
    host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD
)


def get_acc_indices():
    cur = db_conn.cursor()
    cur.execute(
        """SELECT account FROM team WHERE active = TRUE
        ORDER BY account ASC"""
    )

    return [x[0] for x in cur.fetchall()]


if __name__ == "__main__":
    print(get_acc_indices())
