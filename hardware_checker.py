import random

class HardwareChecker:
    def __init__(self, simulation_mode=True):
        self.simulation_mode = simulation_mode

    def read_power(self):
        if self.simulation_mode:
            voltage = round(random.uniform(4.9, 5.1), 2)
            sample_currents = [0.0, 0.15, 0.48, 0.95, 1.20]
            current = random.choice(sample_currents)
            
            return {
                "voltage_v": voltage,
                "current_a": current,
                "status": "simulation"
            }
        else:
            return {"current_a": 0.0, "voltage_v": 0.0}

    def analyze_hardware(self, current_a):
        if current_a == 0.0:
            return "عدم وجود سحب تيار (0mA). احتمال قطع في مسار VBUS، فلاتة الشحن، أو آيسي الشحن."
        elif 0.01 <= current_a <= 0.20:
            return "سحب ضعيف/تسريب خفيف. احتمال مشكلة في آيسي الباور أو كريستالة التوقيت."
        elif 0.21 <= current_a <= 0.80:
            return "سحب تيار طبيعي لعملية الإقلاع أو الشحن."
        elif current_a > 1.0:
            return "سحب تيار مرتفع (شحن سريع أو وجود شورت/قصر صريح في البوردة)."
        else:
            return "حالة غير محددة، تتطلب فحص المكونات بالأفوميتر."