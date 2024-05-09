import os
import json

docs_index = [
  {
    "path": "vuejs/src/guide",
    "base_url": "https://vuejs.org/guide"
  },
  {
    "path": "pinia/packages/docs/core-concepts",
    "base_url": "https://pinia.vuejs.org/core-concepts"
  }
]

json_file_content = []
for doc_index in docs_index:
  for dirpath, dirs, files in os.walk(doc_index["path"]):
    for file in files:
      if ".md" in file:
        file_path = dirpath + '/' + file
        output_file_path = './output/' + file
        relative_file_path = dirpath.replace(doc_index["path"], '')
        
        os.makedirs('./output', exist_ok=True)
        os.system(f'cp {file_path} {output_file_path}')

        json_file_content.append({
          "filename": file,
          "url": doc_index["base_url"] + relative_file_path + '/' + file.replace('.md', '.html')
        })

json_file_path = './output/index.json'
json_file = open(json_file_path, 'w')
json_file.write(json.dumps(json_file_content, indent=2))
json_file.close()