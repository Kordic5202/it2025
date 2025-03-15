SELECT *
from students;

select * from ranks;

select * from students where rank_id=6;

select full_name, rank_id, birth_date 
from students 
where rank_id=6
order by birth_date
limit 2;

# Вибрати кількість днів народження кожного місяця
SELECT extract(month from birth_date) as Birth, 
count(*) as count
from students
group by birth
having count(*) > 3
order by count desc;

SELECT TO_CHAR(birth_date, 'Month') AS Birth_Month, 
       COUNT(*) AS count
FROM students
GROUP BY Birth_Month
HAVING COUNT(*) > 3
ORDER BY count DESC;

SELECT g.group_name, r.rank_name, s.full_name 
from students s
join "groups" g  on s.group_id=g.id
join ranks r on r.id=s.rank_id
order by g.group_name, s.rank_id desc, s.full_name;
