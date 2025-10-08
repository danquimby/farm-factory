"""insert_resources

Revision ID: 6652f2259ef1
Revises: 1ff13ab8554c
Create Date: 2025-09-26 21:01:57.905146

"""
import json
from typing import Sequence, Union
from pathlib import Path

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6652f2259ef1'
down_revision: Union[str, Sequence[str], None] = '1ff13ab8554c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    connection = op.get_bind()
    data_file = Path(__file__).parent.parent  / 'data' / 'resources.json'

    if not data_file.exists():
        print(f"Data file {data_file} not found. Skipping data seeding.")
        return

    with open(data_file, 'r', encoding='utf-8') as f:
        resources_data = json.load(f)

    insert_query = sa.text("""
        INSERT INTO resources (type, name, icon)
        VALUES (:type, :name, :icon)
        """)

    data_to_insert = []
    for item in resources_data:
        data_to_insert.append({
            'type': item['type'],
            'name': item['name'],
            'icon': item['icon'],
        })

    if data_to_insert:
        connection.execute(insert_query, data_to_insert)


def downgrade() -> None:
    op.execute("TRUNCATE TABLE resources RESTART IDENTITY CASCADE")
    print("All data removed from resources table")
