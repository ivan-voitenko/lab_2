from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table, DateTime, insert, update, delete
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import random
import string
from datetime import datetime, timedelta
import psycopg2

Base = declarative_base()


class Students(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    birthday = Column(DateTime, nullable=False)
    faculty = Column(String(50), nullable=False)
    age = Column(Integer, nullable=False)

    grant_applications = relationship('GrantApplication', back_populates='student')
    scholarship_applications = relationship('ScholarshipApplication', back_populates='student')

    def __repr__(self):
        return (f"<Students(id={self.id}, name='{self.name}', birthday='{self.birthday}', "
                f"faculty='{self.faculty}', age={self.age})>")


class Grants(Base):
    __tablename__ = 'grants'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    total = Column(Integer, nullable=False)
    organisation = Column(String(50), nullable=False)

    applications = relationship('GrantApplication', back_populates='grant')
    selection_criteria = relationship('SelectionCriteria', back_populates='grant')

    def __repr__(self):
        return (f"<Grants(id={self.id}, name='{self.name}', total={self.total}, "
                f"organisation='{self.organisation}')>")


class Scholarships(Base):
    __tablename__ = 'scholarships'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    total = Column(Integer, nullable=False)
    type = Column(String(50), nullable=False)

    applications = relationship('ScholarshipApplication', back_populates='scholarship')
    selection_criteria = relationship('SelectionCriteria', back_populates='scholarship')

    def __repr__(self):
        return (f"<Scholarships(id={self.id}, name='{self.name}', total={self.total}, "
                f"type='{self.type}')>")


class GrantApplication(Base):
    __tablename__ = 'grant_application'

    id = Column(Integer, primary_key=True)
    status = Column(Integer, nullable=False)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    grant_id = Column(Integer, ForeignKey('grants.id'), nullable=False)

    student = relationship('Students', back_populates='grant_applications')
    grant = relationship('Grants', back_populates='applications')

    def __repr__(self):
        return (f"<GrantApplication(id={self.id}, status={self.status}, "
                f"student_id={self.student_id}, grant_id={self.grant_id})>")


class ScholarshipApplication(Base):
    __tablename__ = 'scholarship_application'

    id = Column(Integer, primary_key=True)
    status = Column(Integer, nullable=False)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    scholarship_id = Column(Integer, ForeignKey('scholarships.id'), nullable=False)

    student = relationship('Students', back_populates='scholarship_applications')
    scholarship = relationship('Scholarships', back_populates='applications')

    def __repr__(self):
        return (f"<ScholarshipApplication(id={self.id}, status={self.status}, "
                f"student_id={self.student_id}, scholarship_id={self.scholarship_id})>")


class SelectionCriteria(Base):
    __tablename__ = 'selection_criteria'

    id = Column(Integer, primary_key=True)
    description = Column(String(50), nullable=False)
    type = Column(String(50), nullable=False)
    grant_id = Column(Integer, ForeignKey('grants.id'), nullable=False)
    scholarship_id = Column(Integer, ForeignKey('scholarships.id'), nullable=False)

    grant = relationship('Grants', back_populates='selection_criteria')
    scholarship = relationship('Scholarships', back_populates='selection_criteria')

    def __repr__(self):
        return (f"<SelectionCriteria(id={self.id}, description='{self.description}', "
                f"type='{self.type}', grant_id={self.grant_id}, scholarship_id={self.scholarship_id})>")


class Model:
    def __init__(self):
        self.engine = create_engine('postgresql://postgres:1111@127.0.0.1:8080/postgres')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

        self.conn = psycopg2.connect(
            host="127.0.0.1",
            database="postgres",
            user="postgres",
            password="1111",
            port=8080
        )

    def get_all_tables(self):
        return Base.metadata.tables.keys()

    def add_data(self, table_name, columns, val):
        session = self.Session()
        try:
            table_class = globals()[table_name]
            record = table_class(**dict(zip(columns, val)))
            session.add(record)
            session.commit()
            return 1
        except Exception as e:
            print(e)
            session.rollback()
            return 0
        finally:
            session.close()

    def update_data(self, table_name, column, id, new_value):
        session = self.Session()
        try:
            table_class = globals()[table_name]
            record = session.query(table_class).get(id)
            if record:
                setattr(record, column, new_value)
                session.commit()
                return 1
            else:
                return 0
        except Exception as e:
            print(e)
            session.rollback()
            return 0
        finally:
            session.close()

    def get_table(self, table_name):
        session = self.Session()
        try:
            table_class = globals()[table_name]
            records = session.query(table_class).all()
            return records
        except Exception as e:
            print(f"Error: {e}")
            session.rollback()
            return []
        finally:
            session.close()

    def delete_data(self, table_name, id):
        session = self.Session()
        try:
            table_class = globals()[table_name]
            record = session.query(table_class).get(id)
            if record:
                session.delete(record)
                session.commit()
                return 1
            else:
                return 0
        except Exception as e:
            print(e)
            session.rollback()
            return 0
        finally:
            session.close()

    def random_string(self, length=10):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    def random_date(self, start_year=2000, end_year=2023):
        start_date = datetime(start_year, 1, 1)
        end_date = datetime(end_year, 12, 31)
        return (start_date + timedelta(days=random.randint(0, (end_date - start_date).days))).strftime('%Y-%m-%d')

    def generate_data(self, table_name, count):
        c = self.conn.cursor()

        c.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_name = %s", (table_name,))
        if c.fetchone()[0] == 0:
            return

        c.execute(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = %s", (table_name,))
        columns_info = c.fetchall()
        if not columns_info:
            return

        id_column = 'id'

        for i in range(count):
            columns = []
            values = []

            for column_info in columns_info:
                column_name = column_info[0]
                column_type = column_info[1]

                if column_name == id_column:
                    continue

                if column_type in ('integer', 'bigint') or column_name == 'age':
                    columns.append(f'"{column_name}"')
                    values.append(str(random.randint(18, 30)))
                elif column_type in ('integer', 'bigint'):
                    columns.append(f'"{column_name}"')
                    values.append(str(random.randint(1, 1000)))
                elif column_type.startswith('character varying'):
                    columns.append(f'"{column_name}"')
                    values.append(f"'{self.random_string(10)}'")
                elif column_type in ('date', 'timestamp without time zone'):
                    columns.append(f'"{column_name}"')
                    values.append(f"'{self.random_date()}'")
                elif column_type == 'timestamp with time zone':
                    columns.append(f'"{column_name}"')
                    values.append(f"'{self.random_date()} 08:30:00+03'")
                elif column_name.endswith('_id'):
                    columns.append(f'"{column_name}"')
                    values.append(str(random.randint(1, 100)))

            if not columns or not values:
                continue

            insert_query = f'INSERT INTO "{table_name}" ({", ".join(columns)}) VALUES ({", ".join(values)})'
            try:
                c.execute(insert_query)
            except Exception as e:
                self.conn.rollback()
                continue

        try:
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
