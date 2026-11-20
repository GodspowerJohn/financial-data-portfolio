# Data dictionary
- `transaction_id`: synthetic primary key; never a real customer ID
- `event_time`: simulated event timestamp
- `amount_ngn`: simulated transaction amount (NGN)
- `prior_24h_transactions`: assumed count available at event time
- `new_device`: 1 if a transaction originates from a newly-seen device
- `cross_border`: 1 if flagged as cross-border for simulation
- `hour_of_day`: hour of event
- `is_fraud`: synthetic retrospective label; **excluded from model features**
