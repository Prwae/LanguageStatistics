import requests
import math
from terminaltables import SingleTable
import os
from dotenv import load_dotenv

languages = ["JavaScript", "Java", "Python", "Ruby", "PHP", "C++", "CSS", "C#", "C"]


def predict_rub_salary(salary_from, salary_to):
    if salary_from and salary_to:
        return salary_from + salary_to / 2
    elif salary_from:
        return salary_from * 1.2
    elif salary_to:
        return salary_to * 0.8


def process_language_statistics_hh():
    languages_statistics = {}
    for programming_language in languages:
        languages_statistics[programming_language] = {}

        json_response = {}

        all_salaries = []
        page = 0
        pages_number = 1
        place_id = "1"
        while page < pages_number:
            payload = {
                "text": f"Программист {programming_language}",
                "area": place_id,
                "page": page
            }

            response = requests.get("https://api.hh.ru/vacancies", params=payload)
            response.raise_for_status()
            json_response = response.json()

            pages_number = json_response["pages"]
            page += 1

            for vacancy in json_response["items"]:
                if not vacancy["salary"]:
                    predicted_salary = None
                else:
                    predicted_salary = predict_rub_salary(vacancy["salary"]["from"], vacancy["salary"]["to"])
                if predicted_salary:
                    all_salaries.append(predicted_salary)

        average_salary = sum(all_salaries) // len(all_salaries)

        languages_statistics[programming_language]["vacancies_found"] = json_response["found"]
        languages_statistics[programming_language]["vacancies_processed"] = len(all_salaries)
        languages_statistics[programming_language]["average_salary"] = int(average_salary)
    return languages_statistics


def process_language_statistics_sj(apikey):
    languages_statistics = {}
    for programming_language in languages:
        languages_statistics[programming_language] = {}

        json_response = {}

        all_salaries = []
        page = 0
        pages_number = 1
        results_count = 100
        while page < pages_number:
            headers = {
                "X-Api-App-Id": apikey,
            }

            payload = {
                "keyword": f"Программист {programming_language}",
                "page": page,
                "town": "Москва",
                "count": results_count
            }
            response = requests.get("https://api.superjob.ru/2.0/vacancies/not_archive", headers=headers,
                                    params=payload)
            response.raise_for_status()
            json_response = response.json()

            pages_number = math.ceil(json_response["total"] / results_count)
            page += 1

            for vacancy in json_response["objects"]:
                if not vacancy['payment_from'] + vacancy['payment_to']:
                    predicted_salary = None
                else:
                    predicted_salary = predict_rub_salary(vacancy['payment_from'], vacancy['payment_to'])
                if predicted_salary:
                    all_salaries.append(predicted_salary)

        average_salary = sum(all_salaries) // len(all_salaries)

        languages_statistics[programming_language]["vacancies_found"] = json_response["total"]
        languages_statistics[programming_language]["vacancies_processed"] = len(all_salaries)
        languages_statistics[programming_language]["average_salary"] = int(average_salary)
    return languages_statistics


def create_table(table_title, table_payload):
    table = SingleTable(table_payload, table_title)
    return table.table


if __name__ == "__main__":
    load_dotenv()
    apikey = os.getenv("SJ_APIKEY")

    superjob = process_language_statistics_sj(apikey)
    headhunter = process_language_statistics_hh()
    superjob_table_payload = [['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']]
    headhunter_table_payload = [['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']]
    for language in languages:
        superjob_table_payload.append(
            [language, superjob[language]["vacancies_found"], superjob[language]["vacancies_processed"],
             superjob[language]["average_salary"]])
        headhunter_table_payload.append(
            [language, headhunter[language]["vacancies_found"], headhunter[language]["vacancies_processed"],
             headhunter[language]["average_salary"]])

    print(create_table("Headhunter", headhunter_table_payload))
    print(create_table("SuperJob", superjob_table_payload))
