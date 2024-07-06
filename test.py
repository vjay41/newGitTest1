import psycopg2
from psycopg2 import pool
from psycopg2 import OperationalError

class ProgresDBConnection:
    def __init__(self, min_conn=1, max_conn=10, **kwargs):
        self.min_conn = min_conn
        self.max_conn = max_conn
        self.connection_pool = None
        try:
            self.connection_pool = psycopg2.pool.SimpleConnectionPool(
                self.min_conn,
                self.max_conn,
                **kwargs
            )
        except OperationalError as e:
            print(f"Error: {e}")

    def get_connection(self):
        if self.connection_pool:
            return self.connection_pool.getconn()
        else:
            raise OperationalError("Connection pool is not initialized.")

    def put_connection(self, conn):
        if self.connection_pool and conn is not None:
            self.connection_pool.putconn(conn)
        else:
            raise OperationalError("Connection pool is not initialized or connection is None.")

    def close_all_connections(self):
        if self.connection_pool:
            self.connection_pool.closeall()

    def execute_select(self, sql_query):
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(sql_query)
            columns = [desc[0] for desc in cursor.description]
            data = cursor.fetchall()
            cursor.close()
            return pd.DataFrame(data, columns=columns)
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error: {error}")
            return pd.DataFrame()
        finally:
            if conn:
                self.put_connection(conn)
    
    def execute_query(self, query):
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            affected_rows = cursor.rowcount
            cursor.close()
            return affected_rows
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error: {error}")
            return 0
        finally:
            if conn:
                self.put_connection(conn)

    def execute_insert(self, sql_query):
        affected_rows = self.execute_query(sql_query)
        print(f"{affected_rows} row(s) inserted.")

    def execute_update(self, sql_query):
        affected_rows = self.execute_query(sql_query)
        print(f"{affected_rows} row(s) updated.")

    def execute_delete(self, sql_query):
        affected_rows = self.execute_query(sql_query)
        print(f"{affected_rows} row(s) deleted.")

# Example usage:
if __name__ == "__main__":
    # Construct connection string
    db_connection_string = "dbname='your_database' user='your_username' password='your_password' host='your_host' port='your_port'"

    connection_pool = ProgresDBConnection(dsn=db_connection_string)

    try:
        # Insert example
        insert_query = "INSERT INTO users (name, age) VALUES ('John Doe', 30)"
        connection_pool.execute_insert(insert_query)

        # Update example
        update_query = "UPDATE users SET age = 31 WHERE name = 'John Doe'"
        connection_pool.execute_update(update_query)

        # Delete example
        delete_query = "DELETE FROM users WHERE name = 'John Doe'"
        connection_pool.execute_delete(delete_query)

    except OperationalError as e:
        print(f"Error: {e}")
    finally:
        connection_pool.close_all_connections()
