# How to setup the project environment

1. Clone the repository
2. Create the env of your choice and install the dependencies
    - ```bash
      pip install -r requirements.txt
      ```
3. Run the installation and update of pre-commit hooks
    - ```bash
      pre-commit install
      pre-commit autoupdate
      ```
    - This will install the pre-commit hooks and update them to the latest version.
    - The pre-commit hooks are used to run the tests and the linters before each commit.
    - If the tests or the linters fail, the commit will be aborted.
4. Run the tests and linting in one by doing.
    - ```bash
      pre-commit run
      ```
5. If it is all green - then you are ready to submit a PR!
<img width="572" alt="Screenshot 2024-07-18 at 4 39 19 PM" src="https://github.com/user-attachments/assets/8e5b6ee6-8f62-4af0-acd8-aff2bfad632f">
