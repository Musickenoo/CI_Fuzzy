import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# กำหนด universe (universe of discourse) ของ temperature, fuel, และ power
temperature = ctrl.Antecedent(np.linspace(10, 100, 101), 'temperature')
fuel = ctrl.Antecedent(np.linspace(0, 100, 101), 'fuel')
power = ctrl.Consequent(np.linspace(0, 100, 101), 'power')

# กำหนด membership functions ของ temperature
temperature['low'] = fuzz.trimf(temperature.universe, [10, 20, 40])
temperature['medium'] = fuzz.trimf(temperature.universe, [20, 50, 80])
temperature['high'] = fuzz.trimf(temperature.universe, [60, 80, 100])

# กำหนด membership functions ของ fuel
fuel['low'] = fuzz.trimf(fuel.universe, [0, 20, 40])
fuel['medium'] = fuzz.trimf(fuel.universe, [30, 50, 70])
fuel['high'] = fuzz.trimf(fuel.universe, [60, 80, 100])

# กำหนด membership functions ของ power
power['low'] = fuzz.trimf(power.universe, [0, 20, 40])
power['medium'] = fuzz.trimf(power.universe, [30, 50, 70])
power['high'] = fuzz.trimf(power.universe, [60, 80, 100])

# กำหนดความสัมพันธ์ระหว่าง temperature และ fuel กับ power โดยใช้กฎ fuzzy
rule1 = ctrl.Rule(temperature['low'] & fuel['low'], power['low'])
rule2 = ctrl.Rule(temperature['low'] & fuel['medium'], power['low'])
rule3 = ctrl.Rule(temperature['low'] & fuel['high'], power['medium'])
rule4 = ctrl.Rule(temperature['medium'] & fuel['low'], power['low'])
rule5 = ctrl.Rule(temperature['medium'] & fuel['medium'], power['medium'])
rule6 = ctrl.Rule(temperature['medium'] & fuel['high'], power['high'])
rule7 = ctrl.Rule(temperature['high'] & fuel['low'], power['medium'])
rule8 = ctrl.Rule(temperature['high'] & fuel['medium'], power['high'])
rule9 = ctrl.Rule(temperature['high'] & fuel['high'], power['high'])

# เพิ่มกฎ fuzzy ลงในระบบ
fuzzy_system = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])

# สร้างระบบ Fuzzy Logic โดยใช้กฎที่กำหนดไว้
fuzzy_system = ctrl.ControlSystemSimulation(fuzzy_system)

# กำหนดอินพุทเป็นค่า temperature และ fuel ที่ต้องการ
targetTemp = float(input('Enter Target Temperature (10-100): '))
targetfuel = float(input('Enter Target Fuel Level (0-100): '))

# กำหนดอินพุทในระบบ Fuzzy Logic
fuzzy_system.input['temperature'] = targetTemp
fuzzy_system.input['fuel'] = targetfuel

# ประมวลผลระบบ Fuzzy
fuzzy_system.compute()

# แสดงผลลัพธ์ (power)
print("Centroid power: ",fuzzy_system.output['power'])

# แสดงกราฟของ temperature และ fuel ที่ใช้
temperature.view(sim=fuzzy_system, canvas_color='white')
fuel.view(sim=fuzzy_system)
power.view(sim=fuzzy_system)

# เพิ่มเส้นแนวตั้งที่ temperature และ fuel ที่ใช้
plt.axvline(x=targetTemp, color='red', linestyle='--', label='temperature')
plt.axvline(x=targetfuel, color='blue', linestyle='--', label='fuel')
plt.legend()
plt.show()
