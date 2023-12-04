# An HTTP API that needs to be secured

This is a Python application that serves an HTTP API. It has some issues that need to get fixed. Some of the endpoints are not quite right and pose a potential security threat for the application.

## Investigate the application

Your first task is to investigate. The application has an issue with one of the endpoints. The following is a description of the problem by one of the senior developers:

> The /countries/{country} endpoint is not working properly. It is actually allowing passing extra SQL statements using `;` which is a security concern. Please fix this as soon as possible.

Try passing a statement and replicate the problem:

```sql
Spain'; DROP TABLE weather; --
 ```

Add some code to the application to mitigate the 500 error response. Ask GitHub Copilot if that is enough since you can't execute multiple SQLite3 statements. You can use the following prompt:

> Is the code secure since it doesn't allow more than one statement at the time? I've tried Spain'; DROP TABLE weather; -- as input and sqlite3 errors with sqlite3.ProgrammingError: You can only execute one statement at a time.

## SQL Injection Threats
This application is vulnerable to SQL injection attacks. We will approach this using a union-based sql injection attach to perform information gathering.

The following endpoint is vulnerable `/countries/{country}`. Let's try to exploit it by extracting interesting data from the database:

1. Get the list of tables in the database:

```sql
Spain' UNION SELECT name FROM sqlite_master WHERE type='table'; --
```

2. Get the list of columns available in that table:

```sql
Spain' UNION SELECT sql FROM sqlite_master WHERE type='table' AND name='weather'; --
```

3. Now let's get data from one of the tables:

```sql
Spain' UNION SELECT city FROM weather --
```

## Fix it with AI assistance
Now that the vulnerability is clear you need to fix it. Start by asking GitHub Copilot to fix it with the following prompt:

```text
Seems like this is insecure, can you help me update this using f-strings?
```



## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft
trademarks or logos is subject to and must follow
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.
