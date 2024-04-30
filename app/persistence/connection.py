from mysql.connector.pooling import MySQLConnectionPool
from typing import Self, Any


class MySQLConnectionPoolBuilder:
    def __init__(self):
        self._pool_config = {
            'pool_name': 'my_pool',
            'pool_size': 5,
            'host': 'localhost',
            'database': 'db_1',
            'user': 'user',
            'password': 'user1234',
            'port': 3306
        }

    def pool_size(self, new_pool_size: int) -> Self:
        self._pool_config['pool_size'] = new_pool_size
        return self

    def host(self, new_host: str) -> Self:
        self._pool_config['host'] = new_host
        return self

    def database(self, new_database: str) -> Self:
        self._pool_config['database'] = new_database
        return self

    def user(self, new_user: str) -> Self:
        self._pool_config['user'] = new_user
        return self

    def password(self, new_password: str) -> Self:
        self._pool_config['password'] = new_password
        return self

    def port(self, new_port: int) -> Self:
        self._pool_config['port'] = new_port
        return self

    def build(self) -> MySQLConnectionPool:
        return MySQLConnectionPool(**self._pool_config)

    @classmethod
    def builder(cls) -> Self:
        return cls()


conn_pool = MySQLConnectionPoolBuilder.builder().port(3308).build()


# test_connection_pool = MySQLConnectionPoolBuilder.builder().port(3308).build()
def create_tables(connection_pool: MySQLConnectionPool):
    with connection_pool.get_connection() as conn:
        cursor = conn.cursor()

        teams_table_sql = '''
        create table if not exists teams (
        id_ integer primary  key auto_increment,
        name varchar(50) not null,
        points integer default 0
        )
    '''
    #
    #     players_table_sql = '''
    #     create table if not exists players (
    #     id_ integer primary key auto_increment,
    #     name varchar(50) not null,
    #     goals integer default 0,
    #     team_id integer,
    #     foreign key (team_id) references teams(id_) on delete cascade on update cascade
    #     )
    # '''
    #     cursor.execute(teams_table_sql)
        cursor.execute(teams_table_sql)
