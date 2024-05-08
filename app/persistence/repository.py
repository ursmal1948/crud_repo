from abc import ABC
from dataclasses import dataclass
from typing import Any
import logging
from mysql.connector.pooling import MySQLConnectionPool
import inflection
from datetime import date, datetime
from app.persistence.model import Player, Team, Stadium

logging.basicConfig(level=logging.INFO)


class CrudRepository(ABC):
    def __init__(self, connection_pool: MySQLConnectionPool, entity: Any):
        self._connection_pool = connection_pool
        self._entity = entity
        self._entity_type = type(entity)

    def insert(self, item: Any) -> int:
        with self._connection_pool.get_connection() as conn:
            cursor = conn.cursor()

            sql = (f'insert into {self._table_name()} ({self._column_names_for_insert()})'
                   f' values ({self._column_values_for_insert(item)})')
            cursor.execute(sql)
            conn.commit()
            return cursor.lastrowid

    # inserto into teams (points, name) values ()
    def insert_many(self, items: list[Any]) -> int:
        with self._connection_pool.get_connection() as conn:
            cursor = conn.cursor()
            print(self._table_name())
            values = ", ".join([f'({CrudRepository._column_values_for_insert(item)})' for item in items])
            sql = (f'insert into {self._table_name()} ({self._column_names_for_insert()})'
                   f' values {values}')
            cursor.execute(sql)
            conn.commit()
            return cursor.lastrowid

    # 'update teams set column1 = value1, column2 = value2 where condition '

    def update(self, id_: int, item: Any) -> int:
        with self._connection_pool.get_connection() as conn:
            cursor = conn.cursor()
            sql = (f'update {self._table_name()} set {CrudRepository._column_names_and_values_for_update(item)}'
                   f' where id_={id_}')
            logging.info("****")
            logging.info(sql)
            logging.info("****")
            cursor.execute(sql)
            conn.commit()
            return id_

    def count(self) -> int:
        with self._connection_pool.get_connection() as conn:
            cursor = conn.cursor()
            sql = f'select count(*) from {self._table_name()}'
            cursor.execute(sql)
            # logging.info("EXECUTED")
            return cursor.fetchone()

    def find_all(self) -> list[Any]:
        with self._connection_pool.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f'select * from {self._table_name()}')
            # logging.info("SQL EXECUTED")
            return [self._entity(*row) for row in cursor.fetchall()]

    def find_by_id(self, id_: int) -> Any:
        with self._connection_pool.get_connection() as conn:
            cursor = conn.cursor()
            sql = f'select * from {self._table_name()} where id_={id_}'
            cursor.execute(sql)
            # logging.info("SQL EXECUTED")
            return cursor.fetchone()

    def delete(self, id_: int) -> int:
        with self._connection_pool.get_connection() as conn:
            cursor = conn.cursor()
            sql = f'delete from {self._table_name()} where id_={id_}'
            cursor.execute(sql)
            conn.commit()
            return id_

    def delete_all(self) -> None:
        with self._connection_pool.get_connection() as conn:
            cursor = conn.cursor()
            sql = f'delete from {self._table_name()} where id_>0'
            cursor.execute(sql)
            # logging.info('exeec')
            conn.commit()

    def _table_name(self) -> str:
        # print("HERE")
        # print(inflection.tableize(self._entity.__name__))
        return inflection.tableize(self._entity.__name__)

    def _field_names(self) -> list[str]:
        return self._entity().__dict__.keys()

    def _column_names_for_insert(self) -> str:
        fields = [name for name in self._field_names() if name.lower() != 'id_']
        return ', '.join(fields)

    @staticmethod
    def _to_str(value: Any) -> str:
        return f"'{value}'" if isinstance(value, (str, datetime, date)) else str(value)

    # insert into teams (name, points) values ('A', 20)
    @staticmethod
    def _column_values_for_insert(item: Any) -> str:
        values = [CrudRepository._to_str(value) for field, value in item.__dict__.items() if field != 'id_']
        return ', '.join(values)

    # 'update teams set column1 = value1, column2 = value2 where condition '
    @staticmethod
    def _column_names_and_values_for_update(item: Any) -> str:
        return ', '.join([f'{field}={CrudRepository._to_str(value)}' for field, value in item.__dict__.items() if
                          field.lower() != 'id_' and value is not None])


class PlayerRepository(CrudRepository):
    def __init__(self, connection_pool: MySQLConnectionPool):
        super().__init__(connection_pool, Player)

    def find_all_with_goals_higher_than(self, goals_limit: int) -> list[Player]:
        with self._connection_pool.get_connection() as conn:
            cursor = conn.cursor()
            sql = f'select * from players p where p.goals > {goals_limit}'
            cursor.execute(sql)
            return [Player(*player) for player in cursor.fetchall()]

    def find_all_meeting_regex(self, regex: str) -> list[Player]:
        with self._connection_pool.get_connection() as conn:
            cursor = conn.cursor()
            sql = f"select * from players p where p.name REGEXP '{regex}'"
            cursor.execute(sql)
            return [Player(*player) for player in cursor.fetchall()]


class TeamRepository(CrudRepository):
    def __init__(self, connection_pool: MySQLConnectionPool):
        super().__init__(connection_pool, Team)

    def find_all_by_points_between(self, points_from: int, points_to: int) -> list[Team]:
        with self._connection_pool.get_connection() as conn:
            cursor = conn.cursor()
            sql = f'select * from teams t where t.points between {points_from} and {points_to}'
            cursor.execute(sql)
            return [self._entity(*row) for row in cursor.fetchall()]

    def find_by_name(self, name: str) -> Team:
        with self._connection_pool.get_connection() as conn:
            cursor = conn.cursor()
            sql = f"select * from teams t where t.name = '{name}'"
            cursor.execute(sql)
            res = cursor.fetchone()
            # logging.info("***")
            # logging.info(res)
            # logging.info("***")
            return Team(*res) if res else res
    #
    # def update_team(self, new_team: Team):
    #     with self._connection_pool.get_connection() as conn:
    #         cursor = conn.cursor()
    #         sql =


@dataclass
class PlayerWithTeamRepository:
    connection_pool: MySQLConnectionPool

    def find_all_players_with_teams(self, points_from: int, points_to: int):
        with self.connection_pool.get_connection() as conn:
            cursor = conn.cursor()
            sql = (f'select p.* from players p join teams t on p.team_id=t.id_ '
                   f'where t.points between {points_from} and {points_to}')
            cursor.execute(sql)
            return [Player(*pl) for pl in cursor.fetchall()]


# def find_all(self):
#     with self._connection_pool.get_connection() as conn:
#         cursor = conn.cursor()
#         sql = f'select * from teams'
#         cursor.execute(sql)
#         logging.info("SQL EXECUTED")
#         return [Team(*row) for row in cursor.fetchall()]


# class w
class StadiumRepository(CrudRepository):
    def __init__(self, connection_pool: MySQLConnectionPool):
        super().__init__(connection_pool, Stadium)
