import os
import json
import datetime
from dotenv import load_dotenv, dotenv_values
from openai import OpenAI

load_dotenv()

def build_index():
  docs_index = [
    {
      "path": "vuejs/src/guide",
      "base_url": "https://vuejs.org/guide"
    },
    {
      "path": "vuejs/src/api",
      "base_url": "https://vuejs.org/api"
    },
    {
      "path": "pinia/packages/docs/core-concepts",
      "base_url": "https://pinia.vuejs.org/core-concepts"
    },
    {
      "path": "pinia/packages/docs/api",
      "base_url": "https://pinia.vuejs.org/api"
    },
    {
      "path": "pinia/packages/docs/cookbook",
      "base_url": "https://pinia.vuejs.org/cookbook"
    },
    {
      "path": "router/packages/docs/guide",
      "base_url": "https://router.vuejs.org/guide"
    },
    {
      "path": "router/packages/docs/api",
      "base_url": "https://router.vuejs.org/api"
    }
  ]

  json_file_content = []
  for doc_index in docs_index:
    for dirpath, dirs, files in os.walk(doc_index["path"]):
      for file in files:
        if ".md" in file:
          file_path = dirpath + '/' + file
          output_file_path = './output/files/' + file
          relative_file_path = dirpath.replace(doc_index["path"], '')
          
          os.makedirs('./output/files', exist_ok=True)
          os.system(f'cp {file_path} {output_file_path}')

          json_file_content.append({
            "filename": file,
            "url": doc_index["base_url"] + relative_file_path + '/' + file.replace('.md', '.html')
          })

  json_file_path = './output/index.json'
  json_file = open(json_file_path, 'w')
  json_file.write(json.dumps(json_file_content, indent=2))
  json_file.close()

def create_file_vector():
  client = OpenAI(
    organization=os.getenv("OPENAI_ORG"),
    api_key=os.getenv("OPENAI_API_KEY")
  )

  current_time = datetime.datetime.now().strftime("%H:%M:%S")
  vector_store = client.beta.vector_stores.create(name="VueJS Docs " + current_time)
  file_paths = [f"./output/files/{file}" for file in os.listdir("./output/files")]
  file_streams = [open(path, "rb") for path in file_paths]
 
  file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
    vector_store_id=vector_store.id, files=file_streams
  )

build_index()
create_file_vector()