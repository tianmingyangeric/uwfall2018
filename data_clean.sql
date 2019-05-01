# data cleaning

delete from user_elite where year < 2004 || year > 2018;

delete from review where date < '2004-09-30' || date > '2018-04-30';

delete from tip where date < '2004-09-30' || date > '2018-04-30';

delete from user where yelping_since < '2004-09-30' || yelping_since > '2018-04-30';
	
delete review from review inner join 
     (select review.business_id 
     from review left join business on review.business_id = business.id where business.id is null) as new_table
on review.business_id = new_table.business_id;

delete review from review inner join 
     (select review.user_id 
     from review left join user on review.user_id = user.id where user.id is null) as new_table
on review.user_id = new_table.user_id;

delete elite_years from elite_years inner join
    (select elite_years.user_id
    from elite_years left join user on e.user_id = user.id where user.id is null) as new_table
on elite_years.user_id = new_table.user_id;
    
delete user from user inner join 
    (select new.user_id from user inner join
       (select user_id, count(*) total from review group by user_id) as new
on user.id = new.user_id where new.total > user.review_count) as new_table
on user.id = new_table.user_id;


