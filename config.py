only_popular_posts = False

select_posts_by = 'date'  # 'date' or 'page'

start_date = '2026-01-15'
end_date = '2026-01-30'

start_page = 1
end_page = 3

post_db_name = 'post_info'
comment_db_name = 'comment_info'

stock_list = ['000333', '002027']  # 可在此处添加更多股票代码

cookies_path = 'cookies.txt'  # cookies 文件路径


if select_posts_by == 'date':
    Args = ('select by date', start_date, end_date)
else:
    Args = ('select by page', start_page, end_page)



