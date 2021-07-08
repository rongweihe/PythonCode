# 获取应用商店网站的 APP 链接

比如像下面这些网站：https://sj.qq.com/myapp/category.htm?orgame=1&categoryId=122

现在需要抓取网站所有分类的所有APP的详情页。

##### 观察发现有的站点有很多分类那么我们就可以用 xpath 提取这个网站的所有 分类，拿到分类之后，遍历所有的分类在用 xpath 去提取所有页面的种子。

### 1、这里会碰到几种情况

1、有些网站某个分类，网页内容需要鼠标滚动加载才能显式全的问题，这个时候如果要模拟翻页的时候就必须加载出全部的内容，不然定位元素会找不到，出现报错。

**这里提供两种方法供大家参考**

- 一，通过 selenium 模拟浏览器，然后设置浏览器高度足够长，最后延时使之能够将页面的内容都能够加载出来：

  ```python
  1. import time
  2. from selenium import webdriver
  3. driver = webdriver.Firefox()
  4. driver.set_window_size(1000,30000)
  5. driver.get(url)
  6. time.sleep(5)
  ```

- 二，通过selenium模拟浏览器下拉操作

  ```python
  1. from selenium import webdriver
  2. import time
  3. browser.execute_script("window.scrollBy(0,3000)")
  4. time.sleep(1)
  5. browser.execute_script("window.scrollBy(0,5000)")
  6. time.sleep(1)
  7. browser.execute_script("window.scrollBy(0,8000)")
  8. time.sleep(1)
  ```

**补充知识：针对懒加载如何实现 selenium 滑动至页面底部 page_source一次性包含全部网页内容**

2、比如像这种网站：https://www.99danji.com/az/shejiao/  网页主页分好几个分类，而且每个分类下面都有底部栏，第几页，上一页，下一页这种。那么针对这种的，我们该怎么提取所有的 APP 链接呢？其实这种相对第一种更好提取，还是一样，利用 xpath 来提取：当我们处理到每一个分类的页面的时候，利用 xpath 提取当前页面所有的 APP 详情页，并同时提取下一页的链接，在当前页面所有APP详情页获取完毕之后用下一页的链接替换当前分类的链接，继续处理，这样一直处理到所有的页面。这里也有一些小细节：

- 当前分类页面有反爬措施，需要考虑是否上代理。
- 当前页面种子一次性提取不完整，需要考虑引入重试机制。
- 所有的 xpath 可以考虑配置成模板，在代码中逻辑中具体分类具体处理。

3、有些网站，全网只有一个分类，这样的就不需要处理其它的分类页面。 

### 2、spider_seed 代码设计

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

`xpath_str_get_category`  表示该站点是一次性拿到所有分类的种子还是需要遍历每个分类的种子。

`do_get_all_category_urls` 逻辑分三种情况：

- `xpath_str_get_category == is_full_category_url` 表示当前页面就是全部种子的准备。
- `is_fix_category_url` 表示当前子分类，且需要提取当前页面所有其它分类链接。
- 其它的就代表 `get_html` 获取当前页面信息，然后提取 `xpath_str_get_category` 提取当前页面的分类链接。

`fetch_worker` 逻辑主要是所有的 `APP`  种子链接来提取：

- 即遍历当前大分类下所有小分类类级，通过消费队列来实时消费数据。
- 对于每一个 `next_url`  引入重试机制，并且用 `set` 去重。
- 如果拿到了 `seed url` 并 `get_html` 获取当前种子链接，即退出不重试了。
- 拿到种子之后写入文件。

