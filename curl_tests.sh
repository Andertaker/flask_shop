#!/bin/bash

site_url="http://127.0.0.1:5000"
echo "host: $site_url"


#поиск
#http://flask-restless.readthedocs.org/en/latest/searchformat.html

#Возвращает корневые категории
curl \
  -G \
  -H "Content-type: application/json" \
  -d "q={\"filters\":[{\"name\":\"parent_id\",\"op\":\"is_null\"}]}" \
  $site_url/api/category




#curl -X GET "$site_url/api/category" -H "Content-Type: application/json"

#curl -X POST "$site_url/api/category" -d '{"name": "abc", "parent_id": "1"}' -H "Content-Type: application/json"
echo
curl -X PUT "$site_url/api/category/3" -d '{"name": "sddfs", "parent_id": "2"}' -H "Content-Type: application/json"  

echo
echo "Try to delete category 5:"
curl -X DELETE "$site_url/api/category/5" -H "Content-Type: application/json" -I -s | grep HTTP


