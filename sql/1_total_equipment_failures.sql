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
select
    count(equipment_id) tot_errors
from t1
