import json

story = """ {
    "model": "whats_fresh_api.Image",
    "pk": "{0}",
    "fields": {
      "name": "{0}",
      "caption": "{0}",
      "image": "{0}",
      "created": "2014-08-08 23:27:05.568395+00:00",
      "modified": "2014-08-08 23:27:05.568395+00:00"
    }
  }
"""

obj = json.loads(story)

final_str= ""

for i in range(33):
    for key in ['name', 'image', 'caption']:
      obj['fields'][key] = str(i)
    obj['pk'] = str(i)
    final_str = final_str + "," + json.dumps(obj, indent=4)

print final_str