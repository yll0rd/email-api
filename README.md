# Email-Api  
This is a RESTful API built with FastAPI that allows you to send emails from your application.  
## Installation

To install the Email API, clone the repository and install the dependencies:

```bash
pip install -r requirements.txt
```

## Usage

To use the Email API, run the following command:

```bash
uvicorn main:app --port 8000
```

This will start the API server on port `8000`.

## Endpoints

The Email API provides the following endpoints:

- `POST /send_email`: Send an email with the following parameters:
  - `to`: The email address of the recipient
  - `subject`: The subject of the email
  - `body`: The body of the email  
  
## Contributions

We welcome contributions from other developers. If you find a bug or have a feature request, please submit an issue or pull request.
