import psycopg2
import pandas as pd


def send_dataset(with_columns: bool) -> bool:

    conn = psycopg2.connect(
        "host=localhost dbname=postgres user=postgres password=postgres"
    )
    cur = conn.cursor()
    data = pd.read_csv("./data/dataset.csv")

    columns = data.columns.values

    if with_columns:

        columns_with_types = []
        string_types = ["weatherDesc", "region", "soil", "winddir16Point"]
        date_types = ["date"]
        sql = "create table dataset("
        for i in columns:
            if i not in string_types and i not in date_types:
                columns_with_types.append(f" {i} numeric,")
            elif i in date_types:
                columns_with_types.append(f" {i} date,")
            else:
                columns_with_types.append(f" {i} varchar(255),")

        columns_with_types[-1] = columns_with_types[-1].replace(",", "")
        sql = f"{sql} {''.join(columns_with_types)});"
        cur.execute(sql)
        conn.commit()
    with open("./data/dataset.csv", "r", encoding="utf-8") as f:
        # Notice that we don't need the `csv` module.
        # next(f)
        # print(pd.read_csv(f, sep=","))
        # print(f.read().replace('"', "'"))
        copy_sql = """
            COPY public.dataset FROM stdin WITH CSV HEADER
            DELIMITER as ',' ENCODING 'UTF-8'
           """
        cur.copy_expert(sql=copy_sql, file=f)
        # cur.copy_from(f, 'public.dataset', columns=tuple(columns), sep=',')
    conn.commit()
    conn.close()

    return True


def send_dataset_test(with_columns: bool) -> bool:
    conn = psycopg2.connect(
        "host=localhost dbname=postgres user=postgres password=postgres"
    )
    cur = conn.cursor()
    data = pd.read_csv("./data/dataset_test.csv")

    columns = data.columns.values

    if with_columns:

        columns_with_types = []
        string_types = ["weatherDesc", "region", "soil", "winddir16Point"]
        date_types = ["date"]
        sql = "create table dataset_test("
        for i in columns:
            if i not in string_types and i not in date_types:
                columns_with_types.append(f" {i} numeric,")
            elif i in date_types:
                columns_with_types.append(f" {i} date,")
            else:
                columns_with_types.append(f" {i} varchar(255),")

        columns_with_types[-1] = columns_with_types[-1].replace(",", "")
        sql = f"{sql} {''.join(columns_with_types)});"
        cur.execute(sql)
        conn.commit()

    cur.execute("TRUNCATE TABLE public.dataset_test")

    with open("./data/dataset_test.csv", "r", encoding="utf-8") as f:
        # Notice that we don't need the `csv` module.
        # next(f)
        # print(pd.read_csv(f, sep=","))
        # print(f.read().replace('"', "'"))
        copy_sql = """
            COPY public.dataset_test FROM stdin WITH CSV HEADER
            DELIMITER as ',' ENCODING 'UTF-8'
           """
        cur.copy_expert(sql=copy_sql, file=f)
        # cur.copy_from(f, 'public.dataset', columns=tuple(columns), sep=',')
    conn.commit()

    conn.close()

    return True


def send_dataset_train_test(with_columns: bool) -> bool:
    conn = psycopg2.connect(
        "host=localhost dbname=postgres user=postgres password=postgres"
    )
    cur = conn.cursor()
    data = pd.read_csv("./data/dataset_train_test.csv")

    columns = data.columns.values

    if with_columns:

        columns_with_types = []
        string_types = ["weatherDesc", "region", "soil", "winddir16Point"]
        date_types = ["date"]
        sql = "create table dataset_train_test("
        for i in columns:
            if i not in string_types and i not in date_types:
                columns_with_types.append(f" {i} numeric,")
            elif i in date_types:
                columns_with_types.append(f" {i} date,")
            else:
                columns_with_types.append(f" {i} varchar(255),")

        columns_with_types[-1] = columns_with_types[-1].replace(",", "")
        sql = f"{sql} {''.join(columns_with_types)});"
        print(sql)
        cur.execute(sql)
        conn.commit()

    cur.execute("TRUNCATE TABLE public.dataset_train_test")

    with open("./data/dataset_train_test.csv", "r", encoding="utf-8") as f:
        # Notice that we don't need the `csv` module.
        # next(f)
        # print(pd.read_csv(f, sep=","))
        # print(f.read().replace('"', "'"))
        copy_sql = """
            COPY public.dataset_train_test FROM stdin WITH CSV HEADER
            DELIMITER as ',' ENCODING 'UTF-8'
           """
        cur.copy_expert(sql=copy_sql, file=f)
        # cur.copy_from(f, 'public.dataset', columns=tuple(columns), sep=',')
    conn.commit()

    conn.close()

    return True


def send_dataset_new_test(with_columns: bool) -> bool:
    conn = psycopg2.connect(
        "host=localhost dbname=postgres user=postgres password=postgres"
    )
    cur = conn.cursor()
    data = pd.read_csv("./data/dataset_new_test.csv")

    columns = data.columns.values

    if with_columns:

        columns_with_types = []
        string_types = ["weatherDesc", "region", "soil", "winddir16Point"]
        date_types = ["date"]
        sql = "create table dataset_new_test("
        for i in columns:
            if i not in string_types and i not in date_types:
                columns_with_types.append(f" {i} numeric,")
            elif i in date_types:
                columns_with_types.append(f" {i} date,")
            else:
                columns_with_types.append(f" {i} varchar(255),")

        columns_with_types[-1] = columns_with_types[-1].replace(",", "")
        sql = f"{sql} {''.join(columns_with_types)});"

        cur.execute(sql)
        conn.commit()

    cur.execute("TRUNCATE TABLE public.dataset_new_test")

    with open("./data/dataset_new_test.csv", "r", encoding="utf-8") as f:
        # Notice that we don't need the `csv` module.
        # next(f)
        # print(pd.read_csv(f, sep=","))
        # print(f.read().replace('"', "'"))
        copy_sql = """
            COPY public.dataset_new_test FROM stdin WITH CSV HEADER
            DELIMITER as ',' ENCODING 'UTF-8'
            """
        cur.copy_expert(sql=copy_sql, file=f)
        # cur.copy_from(f, 'public.dataset', columns=tuple(columns), sep=',')
    conn.commit()

    conn.close()

    return True


if __name__ == "__main__":
    send_dataset(False)
#     # send_dataset_test(False)
#     # send_dataset_train_test(False)
#     #send_dataset_new_test(True)
