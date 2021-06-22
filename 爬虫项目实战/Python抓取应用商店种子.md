### Spider_seed 代码设计

1、每个站点的 URL 规则设计。

```json
{
  "3dmgame.com": {
    "seed_url": {
      "https://shouyou.3dmgame.com/android/1_1_1/": {
        "type": "category_multi_page",
        "app_type": "game",
        "xpath_str_get_category": "is_full_category_url",
        "xpath_str_get_next_page": "//li[@class='next']/a/@href",
        "xpath_str_get_page_seed": "//div[@class='downl_item']/div[@class='item']/div/a[1]/@href"
      }
    }
  }
}

{
  "99danji.com": {
    "seed_url": {
      "https://www.99danji.com/az/shejiao/": {
        "type": "category_multi_page",
        "app_type": "soft",
        "xpath_str_get_category": "/html/body/section[2]/nav/p/a/@href",
        "xpath_str_get_next_page": "/html/body/section[2]/section[3]/div/div/a[position()>1 and @class='a1' and contains(text(),'下一页')]/@href",
        "xpath_str_get_page_seed": "/html/body/section[2]/section[3]/ul/li/a/@href"
      },
      "https://www.99danji.com/az/saiche/": {
        "type": "category_multi_page",
        "app_type": "game",
        "xpath_str_get_category": "/html/body/section[2]/nav/p/a/@href",
        "xpath_str_get_next_page": "/html/body/section[2]/section[3]/div/div/a[position()>1 and @class='a1' and contains(text(),'下一页')]/@href",
        "xpath_str_get_page_seed": "/html/body/section[2]/section[3]/ul/li/a/@href"
      }
    }
  }
}
```

xpath_str_get_category 表示该站点是一次性拿到所有分类的种子还是需要遍历每个分类的种子。

