# 🧩 Serverless User Importer – AWS Lambda + DynamoDB + Pulumi

This project is a lightweight, serverless Python application that fetches user data from a public API and inserts it into an AWS DynamoDB table. The entire infrastructure is provisioned and managed using [Pulumi](https://www.pulumi.com/) (Python SDK), with a simple PowerShell script to automate the build and deployment.

--- 
## 📌 Overview

- **Data Source:** [JSONPlaceholder](https://jsonplaceholder.typicode.com/users) – a mock API for development.
- **Processing:** The first 5 user records are flattened and simplified.
- **Storage:** Simplified records are inserted into a DynamoDB table using `put_item`.

---

## 🧱 Tech Stack

| Layer              | Technology        |
|-------------------|-------------------|
| Language           | Python 3.11       |
| Infrastructure     | Pulumi (Python SDK) |
| Cloud Provider     | AWS               |
| Services Used      | Lambda, DynamoDB, IAM |
| Build Tool         | PowerShell        |
| Dependencies       | `boto3`, `requests` |

---

## 🧱 Project Structure

```
.
├── __main__.py              # Pulumi stack definition (AWS infra)
├── lambda/
│   ├── handler.py             # Lambda handler code
│   └── requirements.txt     # Python dependencies for Lambda
├── build.ps1                # PowerShell script for packaging Lambda
├── build/                   # Auto-generated build folder (created during packaging)
```

---

## 🚀 What It Does

1. **Creates a DynamoDB table** with on-demand capacity and a primary key `id`.
2. **Deploys an AWS Lambda function** written in Python:
   - Fetches user data from `https://jsonplaceholder.typicode.com/users`
   - Simplifies and flattens the JSON structure
   - Stores the first 5 user records into the DynamoDB table
3. **Sets up an IAM role** with permissions for Lambda execution and DynamoDB actions.
4. **Packages and deploys** using `build.ps1`.

---

## 🔧 Setup & Deployment

### Prerequisites

- [Pulumi CLI](https://www.pulumi.com/docs/get-started/)
- AWS credentials (via `aws configure` or environment)
- Python 3.11
- PowerShell

### Steps

1. **Clone the repo**  
   ```sh
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```

2. **Prepare Lambda build**  
   ```powershell
   .\build.ps1
   ```

### Lambda Dependencies

Ensure the following is in `lambda/requirements.txt`:

```txt
requests
```

> 📦 These will be installed into the build directory before packaging using the PowerShell script.

---

## 🔍 Lambda Function Behavior

The function fetches user data from a placeholder API, flattens the JSON, and writes a simplified version of the first 5 users to DynamoDB. Here’s a sample of what's stored:

```json
{
  "id": "1",
  "name": "Leanne Graham",
  "username": "Bret",
  "email": "Sincere@april.biz"
}
```

---

## 📂 Environment Variables

| Variable      | Description                     |
|---------------|---------------------------------|
| `TABLE_NAME`  | Injected via Pulumi, used by Lambda to know where to write |

---

## 📜 Permissions

The IAM Role allows the Lambda function to:

- Perform `PutItem`, `GetItem`, `UpdateItem`, and `DeleteItem` on the created DynamoDB table.
- Write logs to Amazon CloudWatch.

---

## 🧼 Cleanup

To remove all resources:

```sh
pulumi destroy
```

---

## 🧠 Notes

- This project uses **on-demand billing** for DynamoDB — cost-effective for small workloads.
- API responses are trimmed for demo purposes — customize `fetch_users()` as needed.
- Consider adding retry/backoff logic or error metrics for production.

---

## 📃 License

[MIT](LICENSE)

---

## 🙌 Acknowledgments

- [Pulumi AWS SDK](https://www.pulumi.com/registry/packages/aws/)
- [JSONPlaceholder API](https://jsonplaceholder.typicode.com/)