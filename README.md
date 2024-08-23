# Election System

## Overview

This project provides a comprehensive election system. Follow the steps below to set up and use the system. This was initially built for Vaktavya Election 2022, but can be used for any election. 

## Features and Limitations (How it works)

- Can handle a unlimited number of voters and candidates. This can also handle election for multiple positions at once.
- The voter's identity is always kept secret. (**How?** A secret key is mailed to the voters which they use to vote. The mapping of the key to the voter's identity is stored nowhere. Also, as a person casts their vote, the numbers are immediately counted (added to the previous vote count) and as soon as that happens, there is no way to tell which key was used to vote whom)
- The same key can not be used twice. A list of all the keys sent is maintained (without the information of who that key belongs to) and if input key does not belong to the list, the vote is rejected.
- The Voting system only works over the intranet.

## Setup Instructions

1. **Clone the Repository or Download the Code**

   ```bash
   git clone https://github.com/PeithonKing/Voting_System.git
   ```

   Alternatively, download the code as a ZIP file and extract it.

2. **Create a Virtual Environment (Optional)**

   You can create a virtual environment to manage dependencies. If you prefer, you can use Conda instead.

   Navigate to the project directory and create a virtual environment:

   ```bash
   python -m venv venv
   ```

   Activate the virtual environment:

   On Windows:

   ```bash
   venv\Scripts\activate
   ```

   On macOS/Linux:

   ```bash
   source venv/bin/activate
   ```

3. **Install Dependencies**

   Install all required packages using:

   ```bash
   pip install -r requirements.txt
   ```

4. **Prepare the Voter List**

   Create a CSV file named `mail_ids.csv` with the following format:

   ```plaintext
   Email Address
   adam@gmail.com
   bob@niser.ac.in
   charlie@gmail.com
   daniel@gmail.com
   ...
   ```

   This file contains the list of eligible voters. Make sure all the email addresses are correct and unique.

5. **Configure Settings**

   Rename `example_settings.py` to `settings.py`:

   ```bash
   mv example_settings.py settings.py
   ```

   Open `settings.py` and update it with the correct information for your setup.


## `settings.py` Configuration

This section explains the configuration settings required to set up the election system.

- **`IP`**: Enter your device's IPv4 address here. Ensure that your device is connected directly to the NISER intranet and not through a router. The IPv4 address probably should start with "10." (e.g., "10.xxx.xxx.xxx"). If it starts with something like "192.168.x.x," it probably indicates that your device is connected to a router, which is not suitable. To find your IP address:
  - On Windows: Open the terminal and type `ipconfig`.
  - On Linux: Open the terminal and type `ifconfig`.
  - Look for the IPv4 address that starts with "10." and use it in the `IP` field.

- **`PORT`**: The port number on which the application will listen. The default is `5500`, and you probably won't need to change this. If the application isn't working, you might consider changing it to another available port.

- **`DOMAIN`**: No tweaking is required here.

- **`debug`**: Set this to `True` during development to enable debugging features. It should be set to `False` in production (actual voting) to ensure security and performance.

- **`organisation`**: The name of the organization conducting the election. This will be used in communications.

- **`from_name`**: The name that will appear in the "From" field of the emails sent by the system. Typically, this is set to the name of the election committee or organization.

- **`my_email`**: The email address that will be used to send out emails containing the keys. Ensure this is an active and monitored email account.

- **`app_password`**: This is a Google App Password, required to send emails from the specified `my_email` address. Follow the instructions below to generate one:

  1. Log in to the Google account associated with the `my_email` address.
  2. Visit your Google Account settings: [https://myaccount.google.com/](https://myaccount.google.com/).
  3. Go to the **Security** tab.
  4. Ensure that **2-Step Verification** (2FA) is enabled.
  5. Use the search bar at the top to search for "app" and select **App Passwords**.
  6. You may be prompted to enter your account password to proceed.
  7. Choose a name for your app (it can be anything, such as "Election System") and click **Create**.
  8. A 16-digit App Password will be displayed. Copy this code and paste it as the value for the `app_password` variable in `settings.py`, **removing any spaces**.

- **`mail_ids_file`**: The name/path of the CSV file containing the list of eligible voters' email addresses. We generated this file in Step 4 of the [previous section](#setup-instructions) and named it `mail_ids.csv`.

- **`keep_nota`**: Set this to `True` if you want to include a "None of the Above" (NOTA) option in the election. If set to `False`, NOTA will not be included.

- **`allow_empty_submissions`**: This setting is automatically set to opposite of `keep_nota`. If NOTA is not included (`keep_nota = False`), empty submissions (i.e., no vote for one or more positions) are allowed. If NOTA is included, the voter should choose atleast NOTA if they do not want to vote. Although you might also not allow or allow empty submissions independent of `keep_nota`.

- **`candidates`**: This dictionary lists the candidates running for each position. You can add or remove positions and candidates as needed for your election. Follow the existing format in the file `settings.py`.


## Usage

1. **Activate the Virtual Environment**
   - Before proceeding, make sure to activate the virtual environment as discussed in Step 2 of the [Setup Instructions](#setup-instructions).

2. **Prepare for Email Sending**
   - Ensure the `mail_ids_file` (e.g., `mail_ids.csv`) is in the project directory.
   - Verify that the `settings.py` file has been correctly configured. Be cautious, as making changes to `settings.py` after this point might break the system. Additionally, ensure that your IP address remains the same throughout the process.

3. **Send Emails to Voters**
   - Run the `mail.py` file to send out the emails:
   
     ```bash
     python mail.py
     ```

   - The system will take approximately 2-3 seconds to send each email. For example, if you have 100 voters, it will take about 4-5 minutes to send all the emails.

4. **Start the Election Server**
   - Once all the emails have been sent, start the election server by running:
   
     ```bash
     python election.py
     ```

   - Make sure the `debug` setting in `settings.py` is set to `False`. Keep this server running for the entire duration of the election.

5. **Get Election Results**
   - After the election ends, you can retrieve the results by opening the `votes.json` file located in the project directory.


## API

### 1. `GET /`

The homepage serves as the entry point for voters, where they are prompted to enter their voting key and cast their votes. This page presents a straightforward form with a field for the key and options to select candidates for each position. Once the form is filled out, voters can submit their votes using a button provided on the page.

### 2. `POST /vote`

When a voter submits the voting form, the data is sent to this endpoint for processing. The system checks the validity of the vote and, if successful, records it. The voter is then redirected to a success page, confirming that their vote has been counted. If the vote is rejected for any reason, such as an invalid key or duplicate submission, the voter is shown an error page with an explanation of the likely cause for the rejection.

### 3. `GET /res`

This endpoint displays the current results of the election by reading the `votes.json` file, which contains all the recorded votes. The data is presented in a clear, formatted manner, allowing users to see how each candidate is performing. However, in principle, this information should be kept secret from the candidates to maintain the integrity of the election process. 


## Contributing

We welcome contributions! To get started:

1. **Raise an Issue**: Check the existing issues to see if your idea or bug report has already been addressed. If not, create a new issue with a clear title and detailed description.

2. **Discuss and Get Approval**: Wait for feedback on your issue. Once it's approved, you can proceed.

3. **Fork the Repository**: Create a fork of the repository on GitHub, then clone your fork to your local machine.

4. **Make Changes to your Branch**: Make your changes and commit to your fork.

5. **Submit a Pull Request (PR)**: Raise a pull request to merge your fork to the main repo. Provide a clear explanation of your changes, referencing the related issue.

6. **Review and Merge**: Respond to any feedback, make necessary adjustments, and once approved, your PR will be merged into the main codebase.

Thanks you for your contribution!
