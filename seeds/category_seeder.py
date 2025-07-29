
import random
from flask_seeder import Seeder, Faker, generator
from api.models import MsCategory

class CategorySeeder(Seeder):

  # run() will be called by Flask-Seeder
  def run(self):
    categories = ['INCOME', 'EXPENSE']
    for idx, category_name in enumerate(categories, start=1):
        category_id = idx
        print(f"Adding category: {category_name} with ID: {category_id}")
        category = MsCategory(id=category_id, name=category_name)
        self.db.session.add(category)
    self.db.session.commit()