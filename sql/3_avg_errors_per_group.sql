with t1 as (
    select
        es.equipment_id
        , sl.event_date
        , array_agg(
            sl.sensor_id
        ) sensors
    from sensors_log sl
    left join equipment_sensors es
    on sl.sensor_id = es.sensor_id
    where
        True
        and sl.status = "ERROR"
        and extract(month from sl.event_date) = 1
        and extract(year from sl.event_date) = 2020
    group by 1, 2
)
, t2 as (
    select
        eg.group_name
        , eg.code
        , count(t1.equipment_id) tot
    from t1 t1
    left join equipment_group eg
    on t1.equipment_id = eg.equipment_id
    group by eg.group_name, eg.code
)
select
    distinct
    group_name
    , avg(tot) over(partition by group_name) error_avg
from t2
order by error_avg
