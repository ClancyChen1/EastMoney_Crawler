only_popular_posts = False

select_posts_by = 'date'  # 'date' or 'page'


start_date = '2026-01-01'
end_date = '2026-01-15'

start_page = 1
end_page = 3

db_name = 'post_info'



if select_posts_by == 'date':
    Args = ('select by date', start_date, end_date)
else:
    Args = ('select by page', start_page, end_page)
