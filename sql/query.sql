select
    c.customer_id,
    c.first_name,
    c.surname,
    sum(a.balance) as sum_balance
from (
    select *
    from customer
    where country = "Vatican City"
) as c
left join account as a on c.customer_id = a.customer_id
group by c.customer_id