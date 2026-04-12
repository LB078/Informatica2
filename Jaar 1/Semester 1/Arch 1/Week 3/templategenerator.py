MIN_SALARY = 20000
MAX_SALARY = 80000


# Validation functions
def is_name_valid(name: str) -> bool:
    return 2 <= len(name) <= 10 and name.isalpha() and name[0].isupper()


def is_title_valid(title: str) -> bool:
    return len(title) >= 10 and not any(character.isdigit() for character in title)


def is_salary_valid(salary: str) -> bool:
    return MIN_SALARY <= float(salary.replace(".", "").replace(",", ".")) <= MAX_SALARY


def is_date_valid(date: str) -> bool:
    if not len(date.split("-")) == 3:
        return False

    year, month, day = date.split("-")

    if len(year) > 4 and year not in ["2021", "2022"]:
        return False

    if not len(month) == 2 and not 1 <= int(month) <= 12:
        return False

    if not len(day) == 2 and not 1 <= int(day) <= 31:
        return False

    return True


# Letters
def generate_job_offer_letter(
    first_name: str, last_name: str, job_title: str, annual_salary: str, start_date: str
) -> str:
    return f"""Here is the final letter to send:
    Dear {first_name} {last_name},
    After careful evaluation of your application for the position of {job_title},
    we are glad to offer you the job. Your salary will be {annual_salary} euro annually.
    Your start date will be on {start_date}. Please do not hesitate to contact us with any questions.
    Sincerely,
    HR Department of XYZ"""


def generate_rejection_letter(
    first_name: str, last_name: str, job_title: str, with_feedback: str, feedback: str
) -> str:
    if with_feedback == "yes":
        return f"""Here is the final letter to send:
        Dear {first_name} {last_name},
        After careful evaluation of your application for the position of {job_title},
        at this moment we have decided to proceed with another candidate.
        Here we would like to provide you our feedback about the interview.
        {feedback}
        We wish you the best in finding your future desired career.
        Please do not hesitate to contact us with any questions.
        Sincerely,
        HR Department of XYZ"""

    return f"""Here is the final letter to send:
    Dear {first_name} {last_name},
    After careful evaluation of your application for the position of {job_title},
    at this moment we have decided to proceed with another candidate.
    We wish you the best in finding your future desired career.
    Please do not hesitate to contact us with any questions.
    Sincerely,
    HR Department of XYZ"""


def get_input(prompt: str, validation_function) -> str:
    while True:
        input_value = input(prompt)
        if validation_function(input_value):
            return input_value
        else:
            print("Input error")


def main():
    while True:
        continue_input = get_input(
            "More letters? (Yes or No) ",
            lambda x: x.lower() in ["yes", "no"],
        ).lower()
        if continue_input == "no":
            break

        letter_type = get_input(
            "Job Offer or Rejection? ",
            lambda x: x.lower() in ["job offer", "rejection"],
        ).lower()
        first_name = get_input("First Name? ", is_name_valid)
        last_name = get_input("Last Name? ", is_name_valid)
        job_title = get_input("Job Title? ", is_title_valid)

        if letter_type == "job offer":
            annual_salary = get_input("Annual Salary? ", is_salary_valid)
            start_date = get_input("Start Date? (YYYY-MM-DD) ", is_date_valid)
            print(
                generate_job_offer_letter(
                    first_name, last_name, job_title, annual_salary, start_date
                )
            )
        else:
            with_feedback = get_input(
                "Feedback? (Yes or No) ",
                lambda x: x.lower() in ["yes", "no"],
            ).lower()
            feedback = ""
            if with_feedback == "yes":
                feedback = get_input(
                    "Enter your Feedback (One Statement): ", lambda x: len(
                        x) > 0
                )
            print(
                generate_rejection_letter(
                    first_name, last_name, job_title, with_feedback, feedback
                )
            )


if __name__ == "__main__":
    main()
