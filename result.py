import asyncio
from asin_pandas import ClinicA
from sync_pandas import Clinic
import time

class ResultAsync:
    """Класс для работы с асинхронным кодом"""

    @staticmethod
    async def time_work():
        """Замер времени работы асинхронного кода.

        Returns:
            result: время выполнения каждой программы.

        """

        clinic = ClinicA([
            "medical_diagnostic_devices_1.xlsx",
            "medical_diagnostic_devices_2.xlsx",
            "medical_diagnostic_devices_3.xlsx",
            "medical_diagnostic_devices_4.xlsx",
            "medical_diagnostic_devices_5.xlsx",
            "medical_diagnostic_devices_6.xlsx",
            "medical_diagnostic_devices_7.xlsx",
            "medical_diagnostic_devices_8.xlsx",
            "medical_diagnostic_devices_9.xlsx",
            "medical_diagnostic_devices_10.xlsx"
        ])

        result = {}

        start_first_function = time.time()

        await clinic.read_excel_files()

        finish_first_function = time.time()
        time_first_function = finish_first_function - start_first_function
        result['read_excel_files'] = time_first_function

        start_second_function = time.time()

        await clinic.filter_data_warranty()

        finish_second_function = time.time()
        time_second_function = finish_second_function - start_second_function
        result['filter_data_warranty'] = time_second_function

        start_three_function = time.time()

        await clinic.clinics_most_problems()

        finish_three_function = time.time()
        time_three_function = finish_three_function - start_three_function
        result['clinics_most_problems'] = time_three_function

        start_four_function = time.time()

        await clinic.calibration_report()

        finish_four_function = time.time()
        time_four_function = finish_four_function - start_four_function
        result['calibration_report'] = time_four_function

        start_five_function = time.time()

        await clinic.unification_information()

        finish_five_function = time.time()
        time_five_function = finish_five_function - start_five_function
        result['unification_information'] = time_five_function

        start_six_function = time.time()

        await clinic.write_excel("result_target.xlsx")

        finish_six_function = time.time()
        time_six_function = finish_six_function - start_six_function
        result['write_excel'] = time_six_function

        for key, values in result.items():
            print(f'Время работы {key}: {values} c.')

        return result

class ResultSync:
    """Класс для работы с синхронным кодом"""

    @staticmethod
    def time_work():
        """Замер времени работы синхронного кода.

        Returns:
            result: время выполнения каждой программы.

        """

        clinic = Clinic([
            "medical_diagnostic_devices_1.xlsx",
            "medical_diagnostic_devices_2.xlsx",
            "medical_diagnostic_devices_3.xlsx",
            "medical_diagnostic_devices_4.xlsx",
            "medical_diagnostic_devices_5.xlsx",
            "medical_diagnostic_devices_6.xlsx",
            "medical_diagnostic_devices_7.xlsx",
            "medical_diagnostic_devices_8.xlsx",
            "medical_diagnostic_devices_9.xlsx",
            "medical_diagnostic_devices_10.xlsx"
        ])

        result = {}

        start_first_function = time.time()

        clinic.read_excel()

        finish_first_function = time.time()
        time_first_function = finish_first_function - start_first_function
        result['read_excel_files'] = time_first_function

        start_second_function = time.time()

        clinic.filter_data_warranty()

        finish_second_function = time.time()
        time_second_function = finish_second_function - start_second_function
        result['filter_data_warranty'] = time_second_function

        start_three_function = time.time()

        clinic.clinics_most_problems()

        finish_three_function = time.time()
        time_three_function = finish_three_function - start_three_function
        result['clinics_most_problems'] = time_three_function

        start_four_function = time.time()

        clinic.calibration_report()

        finish_four_function = time.time()
        time_four_function = finish_four_function - start_four_function
        result['calibration_report'] = time_four_function

        start_five_function = time.time()

        clinic.unification_information()

        finish_five_function = time.time()
        time_five_function = finish_five_function - start_five_function
        result['unification_information'] = time_five_function

        start_six_function = time.time()

        clinic.write_excel()

        finish_six_function = time.time()
        time_six_function = finish_six_function - start_six_function
        result['write_excel'] = time_six_function

        for key, values in result.items():
            print(f'Время работы {key}: {values} c.')

        return result

if __name__ == "__main__":
    print('Время асинхронного выполнения')

    asyncio.run(ResultAsync.time_work())

    print('__________________________________')
    print('Время синхронного выполнения')

    ResultSync.time_work()

