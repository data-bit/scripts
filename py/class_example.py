# ==============================================================
# AUTHOR:   MITCH ALVES
# DATE:     2021-01-15
# DESC:     Example of PY Class
# ==============================================================


# ==============================================================
#   CLASS: List_URL
# ==============================================================

class List_URL:
  def __init__(self, request_id, keyword, url):
    self.request_id = request_id
    self.keyword = keyword
    self.url = url

  def get_id(self):
    print("Request ID: " + self.request_id)

  def get_keyword(self):
    print("Keyword: " + self.keyword)

  def get_url(self):
    print("URL: " + self.url + self.keyword)

  def output(self):
    self.get_id() 
    self.get_keyword() 
    self.get_url()
    

# ==============================================================
#   MAIN
# ==============================================================

list_url = []

list_keyword = [
  'apple'
  ,'banana'
  ,'kiwi'
  ,'orange'
  ,'papaya'
]

for x in range(0, len(list_keyword)):
    item_url = List_URL(str(x), list_keyword[x], 'google.com/search?q=')
    list_url.append(item_url)


for u in (list_url):
    if u.output() is not None:
        print(u.output())
