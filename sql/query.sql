select
    c.customer_id,
    sum(a.balance)
from (
    select *
    from customer
    where country = "Vatican City"
) as c
left join account as a on c.customer_id = a.customer_id
group by c.customer_id

-- we want to know the total amount of money per person living in vatican city.

