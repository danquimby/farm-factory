"""insert_structures

Revision ID: d1d32689b8a1
Revises: fd1c8fb011e7
Create Date: 2025-09-15 11:07:49.685806

"""
import json
from pathlib import Path
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd1d32689b8a1'
down_revision: Union[str, Sequence[str], None] = 'fd1c8fb011e7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    connection = op.get_bind()
    data_file = Path(__file__).parent.parent  / 'data' / 'structures.json'

    if not data_file.exists():
        print(f"Data file {data_file} not found. Skipping data seeding.")
        return

    with open(data_file, 'r', encoding='utf-8') as f:
        structures_data = json.load(f)


    insert_query = sa.text("""
        INSERT INTO structures (w, h, max_level, icon, name, image)
        VALUES (:w, :h, :max_level, :icon, :name, :image)
        """)

    data_to_insert = []
    for item in structures_data:
        data_to_insert.append({
            'w': item['w'],
            'h': item['h'],
            'max_level': item['max_level'],
            'icon': item['icon'],
            'name': item['name'],
            'image': item['image']
        })

    if data_to_insert:
        connection.execute(insert_query, data_to_insert)


def downgrade() -> None:
    op.execute("TRUNCATE TABLE structures RESTART IDENTITY CASCADE")
    print("All data removed from structures table")
