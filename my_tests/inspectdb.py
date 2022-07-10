import io
import sys
from sqlalchemy import create_engine, MetaData
from sqlacodegen.codegen import CodeGenerator

from config.conf import PROJECT_CONF


def generate_model(outfile=None):
    engine = create_engine(PROJECT_CONF.DB_URL)
    metadata = MetaData(bind=engine)
    metadata.reflect()
    outfile = io.open(outfile, 'w', encoding='utf-8') if outfile else sys.stdout
    generator = CodeGenerator(metadata)
    generator.render(outfile)


if __name__ == '__main__':
    generate_model('db_models.py')
