from abc import ABC, abstractmethod
import sqlalchemy as sa
import random
from datetime import date, datetime

from .accessor import DBAccessor
from . import model


class DbManager(ABC):
    @abstractmethod
    def create_data_from_sheet(self, df):
        pass


class ReportManager(DbManager):
    """
    Managing table operations
    """
    def __init__(self, db_accessor: DBAccessor):
        self._engine = db_accessor.engine

    def create_data_from_sheet(self, sheet):
        """
        Creating data from excel sheet
        """
        with self._engine.begin() as conn:
            for row in sheet:
                company_id = self._get_or_create_company(conn, company_name=row[1].value)

                fact_qliq_id = self._create_data_frame(conn, data={"data1": row[2].value, "data2": row[3].value})
                fact_qoil_id = self._create_data_frame(conn, data={"data1": row[4].value, "data2": row[5].value})
                fact_id = self._create_data_stamp(conn, data={"qliq": fact_qliq_id, "qoil": fact_qoil_id})

                forecast_qliq_id = self._create_data_frame(conn, data={"data1": row[6].value, "data2": row[7].value})
                forecast_qoil_id = self._create_data_frame(conn, data={"data1": row[8].value, "data2": row[9].value})
                forecast_id = self._create_data_stamp(conn, data={"qliq": forecast_qliq_id, "qoil": forecast_qoil_id})

                self._create_report(
                    conn, data={"id": row[0].value, "company": company_id, "fact": fact_id, "forecast": forecast_id}
                )

    def _get_or_create_company(self, conn, company_name):
        company_id = conn.scalar(
            sa.select(model.company.c.id).where(model.company.c.name == company_name)
        )
        if company_id is None:
            company_id = conn.scalar(
                model.company.insert().values(name=company_name).returning(model.company.c.id)
            )
        return company_id

    def _create_data_frame(self, conn, data):
        return conn.scalar(
            model.data_frame.insert().values(data).returning(model.data_frame.c.id)
        )

    def _create_data_stamp(self, conn, data):
        return conn.scalar(
            model.data_stamp.insert().values(data).returning(model.data_stamp.c.id)
        )

    def _create_report(self, conn, data):
        conn.execute(
            model.report.insert().values(data)
        )

    def update_random_date(self):
        """
        Adding a random date to all rows of the main table
        """
        with self._engine.begin() as conn:
            ret = conn.execute(
                sa.select(model.report.c.id)
            )
            for row in ret:
                report_id = row[0]
                conn.execute(
                    model.report.update().values(date=random_date()).where(model.report.c.id == report_id)
                )

    def get_total_by_date(self):
        """
        Getting of the settlement total by grouped date
        """
        with self._engine.connect() as conn:
            # aliases for separating datas tables
            fact = model.data_stamp.alias("fact")
            forecast = model.data_stamp.alias("forecast")

            fact_qliq = model.data_frame.alias("fact_qliq")
            fact_qoil = model.data_frame.alias("fact_qoil")
            forecast_qliq = model.data_frame.alias("forecast_qliq")
            forecast_qoil = model.data_frame.alias("forecast_qoil")

            ret = conn.execute(
                sa.select(
                    sa.func.sum(fact_qliq.c.data1),
                    sa.func.sum(fact_qliq.c.data2),
                    sa.func.sum(fact_qoil.c.data1),
                    sa.func.sum(fact_qoil.c.data2),
                    sa.func.sum(forecast_qliq.c.data1),
                    sa.func.sum(forecast_qliq.c.data2),
                    sa.func.sum(forecast_qoil.c.data1),
                    sa.func.sum(forecast_qoil.c.data2),
                    model.report.c.date,
                )
                .join(fact, model.report.c.fact == fact.c.id)
                .join(forecast, model.report.c.forecast == forecast.c.id)

                .join(fact_qliq, fact.c.qliq == fact_qliq.c.id)
                .join(fact_qoil, fact.c.qoil == fact_qoil.c.id)
                .join(forecast_qliq, forecast.c.qliq == forecast_qliq.c.id)
                .join(forecast_qoil, forecast.c.qoil == forecast_qoil.c.id)

                .group_by(model.report.c.date)
            )
        return [tuple(row) for row in ret]


def random_date():
    now = datetime.now()
    random_day = random.randint(1, 10)
    return date(now.year, now.month, random_day)
