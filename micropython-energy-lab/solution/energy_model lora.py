import numpy as np

#### Duty cycle
active_time = 30    ### seconds
sleep_time = 30    ### seconds
duty_cycle = active_time / (active_time + sleep_time)
print('Duty cycle:', duty_cycle)
print(active_time-1)


### sensor
t_sr = 1/3600
i_sr = 2.8e-6
t_si = (active_time-1)/3600
i_si = 0.1e-6

### communication
t_tx = 185e-3/3600
i_tx = 26e-3
t_rx = 29.815/3600
# t_rx = 7*t_tx    ### assuming that it receives 7 pkts on an average, and rx is only active during reception of these packets
i_rx = 10.3e-3
t_cs = sleep_time/3600
i_cs = 0.2e-6

### CPU
t_proc = active_time/3600
i_proc = 54.6e-3
t_ss = sleep_time/3600
i_ss = 240e-6
t_id = sleep_time/3600
i_id = 42.3e-3

### led
t1_led = (active_time+sleep_time)/3600
t2_led = (active_time)/3600
i_led = 6e-3

p_sense = t_sr*i_sr + t_si*i_si
p_comm = t_tx*i_tx + t_rx*i_rx + t_cs*i_cs 
p_cpu = t_proc*i_proc + t_ss*i_ss
p_led = t1_led*i_led + t2_led*i_led
p_cpu2 = t_proc*i_proc + t_id*i_id    ### if we use time.sleep


p_total = p_sense + p_comm + p_cpu + p_led
p_total = p_total*10**3

p_total2 = p_sense + p_comm + p_cpu2 + p_led
p_total2 = p_total2*10**3

print('LoRa:\n')
print('Current consumption for sensing:', p_sense, 'Ah')
print('Current consumption for communication:', p_comm, 'Ah')
print('Current consumption for CPU (Light Sleep):', p_cpu, 'Ah')
print('Current consumption for CPU2 (IDLE):', p_cpu2, 'Ah')

print('Theoretical charge consumption for one cycle:', p_total, 'mAh')
print('Theoretical charge consumption for five cycles:', p_total*5, 'mAh')

# print('Theoretical charge consumption for one cycle (IDLE):', p_total2, 'mAh')
# print('Total charge consumption for five cycles (IDLE):', p_total2*5, 'mAh')

# print('')

runtime_light = np.floor(20e3/(p_total))
print('Theoretical Runtime (Light Sleep):', runtime_light, 'cycles')
print('Theoretical Runtime (Light Sleep):', runtime_light/60, 'hours')
print('Theoretical Runtime (Light Sleep):', runtime_light/(60*24), 'days')

print('')


# Constants
power_mWh = 18      # Power consumption in mWh over 5 minutes
voltage = 5.15        # Supply voltage in Volts
battery_capacity_mAh = 20000

# Step 1: Convert power to energy in Wh
energy_Wh = power_mWh / 1000

# Step 2: Energy to charge (Ah)
charge_Ah = energy_Wh / voltage
charge_mAh = charge_Ah * 1000

# Step 3: Hourly current consumption
current_mA = (charge_mAh / 5) * 60

# Step 3: Hourly current consumption
current_mA_min = (charge_mAh / 5)

# Step 4: Runtime in hours
runtime_hours = battery_capacity_mAh / current_mA

# Print results
print(f"Charge Consumption (5 minutes): {charge_mAh} mAh")
print(f"Current Consumption (per minute): {current_mA_min} mA")
print(f"Estimated Runtime: {runtime_hours:.2f} hours (~{runtime_hours / 24:.2f} days)")


