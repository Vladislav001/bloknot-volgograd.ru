import sys

sys.path.append('../')
from database import Database

# Подключение к бд
db = Database()

# Сохранение текста статей по отдельным файлам, где имя файлов - ид статьи в бд
print("Saving articles...")

saving_folder_name = "input_articles"
articles = db.getAllNews()
for article in articles:
    output_file_name = saving_folder_name + "/" + str(article["_id"]) + ".txt"
    f = open(output_file_name, 'w')
    f.write(article["text"]);

print("Articles have been saved.")

