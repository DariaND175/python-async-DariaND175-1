import numpy as np
import pandas as pd
import time

class Clinic:
    """Класс для работы с медицинским оборудованием"""

    def __init__(self,file:list):
        """Инициализатор класса.

            Args:
                file: файл с данными

        """

        self.__file = file
        self.__data = None

        self.read_excel()

    def read_excel(self):
        """Чтение файлов.

        Returns:
            self.__data: данные из файлов.
        """
        data = []

        for file in self.__file:
            df =pd.read_excel(file,sheet_name = 'Sheet1')
            data.append(df)

        self.__data = pd.concat(data, ignore_index=True)
        return self.__data


    def filter_data_warranty(self):
        """Фильтрация данных по гарантии.

        Returns:
                result: Отфильтрованные данные.
        """

        self.__data['warranty_until'] = pd.to_datetime(self.__data['warranty_until'],format = 'mixed', dayfirst = True, errors='coerce').dt.normalize()

        conditions = [(self.__data['warranty_until'] >= pd.Timestamp.today())]
        choice = ['Активна']

        self.__data['warranty_status'] = np.select(conditions,choice,default ='Истекла')

        result = self.__data.sort_values(['warranty_status','warranty_until'] ,ascending = [True, True],na_position='last')

        return result

    def clinics_most_problems(self):
        """Агрегация клиник с наибольшим количеством проблем.

        Returns:
                result: Отфильтрованные данные.
        """

        clinics = self.__data.groupby('clinic_name').agg({
            'clinic_id': 'first',
            'city': 'first',
            'issues_reported_12mo':'sum',
            'failure_count_12mo': 'sum'
        }).reset_index()

        clinics['all_problems'] = clinics['issues_reported_12mo']+clinics['failure_count_12mo']
        max_errors = clinics['all_problems'].max()

        result = clinics.sort_values('all_problems', ascending=False).head(5)

        return result

    def calibration_report(self):
        """ Отчёт по срокам калибровки.

         Returns:
                result: Отфильтрованные данные.
        """

        self.__data['install_date'] = pd.to_datetime(self.__data['install_date'],format = 'mixed', dayfirst = True, errors='coerce').dt.normalize()
        self.__data['last_calibration_date'] = pd.to_datetime(self.__data['last_calibration_date'], format = 'mixed', dayfirst = True, errors='coerce').dt.normalize()

        valid_dates = self.__data[
            (self.__data['install_date'] <= self.__data['last_calibration_date']) &
            (self.__data['install_date'].notna()) & (self.__data['last_calibration_date'].notna())
        ].copy()

        valid_dates['time_after_calibration'] = (pd.Timestamp.now().normalize() - valid_dates['last_calibration_date']).dt.days

        valid_dates.loc[valid_dates['time_after_calibration'] < 0, 'time_after_calibration'] = 0

        result = valid_dates.groupby('clinic_name').agg(
            clinics = ('clinic_id','first'),
            devices = ('device_id', 'count'),
            new_calibration_date = ('last_calibration_date','max'),
            old_calibration_date = ('last_calibration_date','min'),
            average_days_since_calibration = ('time_after_calibration','mean'),
            days_since_new_calibration =  ('time_after_calibration', 'min'),
            days_since_old_calibration=('time_after_calibration', 'max')

        ).reset_index()

        round_meaning = ['average_days_since_calibration', 'days_since_new_calibration', 'days_since_old_calibration']

        for meaning in round_meaning:
            if meaning in result.columns:
                result[meaning] = result[meaning].round(0).astype(int)

        conditions = [
            (result['days_since_new_calibration'] >= 180) & (result['days_since_new_calibration']<365),
            result['days_since_new_calibration'] >=365
        ]

        choices = ['Внимание', 'Критично']

        result['status'] = np.select(conditions, choices, default = 'В порядке')

        rank_dangerous = {'Критично' : 1, 'Внимание': 2, 'В порядке': 3 }

        result['rank_dangerous'] = result['status'].map(rank_dangerous)
        result = result.sort_values(['rank_dangerous', 'days_since_old_calibration'], ascending=[True, False])
        result = result.drop('rank_dangerous', axis=1)

        return result

    def unification_information(self):
        """Объединение данные по клиникам и оборудованию.

        Returns:
                result: Отфильтрованные данные.
        """

        status_device = {
            'planned_installation': 'planned_installation',
            'op': 'operational',
            'OK': 'operational',
            'operational': 'operational',
            'maintenance_scheduled': 'maintenance_scheduled',
            'broken': 'faulty',
            'faulty': 'faulty'
        }

        self.__data['status'] = self.__data['status'].map(status_device)

        self.__data['last_calibration_date'] = pd.to_datetime(self.__data['last_calibration_date'], format='mixed', dayfirst=True, errors='coerce').dt.normalize()
        self.__data['last_service_date'] = pd.to_datetime(self.__data['last_service_date'], format='mixed', dayfirst=True, errors='coerce').dt.normalize()
        self.__data['warranty_until'] = pd.to_datetime(self.__data['warranty_until'], format='mixed', dayfirst=True, errors='coerce').dt.normalize()
        self.__data['install_date'] = pd.to_datetime(self.__data['install_date'],format = 'mixed', dayfirst = True, errors='coerce').dt.normalize()

        self.__data['warranty_active'] = np.where(
            self.__data['warranty_until'] >= pd.Timestamp.now().normalize(),
            1, 0
        )

        self.__data['problems'] = self.__data['failure_count_12mo'] + self.__data['issues_reported_12mo']

        valid_dates = self.__data[
            (self.__data['install_date'] <= self.__data['last_calibration_date']) &
            (self.__data['install_date'].notna()) & (self.__data['last_calibration_date'].notna())
            ].copy()

        self.__data.loc[valid_dates.index,'time_after_calibration'] = (pd.Timestamp.now().normalize() - valid_dates['last_calibration_date']).dt.days

        result = self.__data.groupby(['clinic_name', 'clinic_id', 'serial_number']).agg(
            status = ('status','first'),
            devices = ('device_id','count'),
            city = ('city', 'first'),
            department = ('department', 'first'),
            model = ('model','first'),
            install_date = ('install_date','min'),
            problems = ('problems','sum'),
            warranty_active = ('warranty_active', 'max'),
            uptime_pct = ('uptime_pct','mean'),
            last_calibration_date = ('time_after_calibration','max'),
            last_service_date = ('last_service_date', 'max')
        ).reset_index()

        return result

    def write_excel(self):
        """Сохранение файла в формате xlsx."""

        try:
            with pd.ExcelWriter("med_clinics.xlsx", datetime_format='DD-MM-YYYY') as writer:
                self.filter_data_warranty().to_excel(writer, sheet_name="Sorted_data_warranty", index=False)
                self.clinics_most_problems().to_excel(writer, sheet_name="Problems", index=False)
                self.calibration_report().to_excel(writer, sheet_name = 'Calibration', index=False)
                self.unification_information().to_excel(writer,sheet_name = 'All information', index=False)

            print("Файл успешно сохранен: med_clinics.xlsx")
        except Exception as e:
            print(f"Ошибка при сохранении файла: {e}")

if __name__ == "__main__":
    start_time = time.time()

    clinic = Clinic(['medical_diagnostic_devices_1.xlsx',
                     'medical_diagnostic_devices_2.xlsx',
                     'medical_diagnostic_devices_3.xlsx',
                     'medical_diagnostic_devices_4.xlsx',
                     'medical_diagnostic_devices_5.xlsx',
                     'medical_diagnostic_devices_6.xlsx',
                     'medical_diagnostic_devices_7.xlsx',
                     'medical_diagnostic_devices_9.xlsx',
                     'medical_diagnostic_devices_9.xlsx',
                     'medical_diagnostic_devices_10.xlsx'
                     ])

    clinic.write_excel()

    end_time = time.time()
    all_time = end_time - start_time

    print(f'Время выполнения синхронного кода: {all_time}')