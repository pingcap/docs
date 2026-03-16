---
title: system_history.login_history
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.764"/>

import EEFeature from '@site/src/components/EEFeature';

<EEFeature featureName='LOGIN HISTORY'/>

**Authentication security audit** - Comprehensive logging of all user login attempts (successful and failed). Critical for:

- **Security Monitoring**: Detect brute force attacks and unauthorized access attempts
- **Compliance Auditing**: Track user authentication for regulatory requirements
- **Access Pattern Analysis**: Monitor when and how users access the system
- **Incident Investigation**: Investigate security incidents and authentication issues


## Fields

| Field          | Type      | Description                                                    |
|----------------|-----------|------------------------------------------------------------    |
| event_time     | TIMESTAMP | The timestamp when the login event occurred                    |
| handler        | VARCHAR   | The protocol or handler used for the login (e.g., `HTTP`)      |
| event_type     | VARCHAR   | The type of login event (e.g., `LoginSuccess`, `LoginFailed`)  |
| connection_uri | VARCHAR   | The URI used for the connection                    |
| auth_type      | VARCHAR   | The authentication method used (e.g., Password)                |
| user_name      | VARCHAR   | The name of the user attempting to log in                      |
| client_ip      | VARCHAR   | The IP address of the client                                   |
| user_agent     | VARCHAR   | The user agent string of the client                            |
| session_id     | VARCHAR   | The session ID associated with the login attempt               |
| node_id        | VARCHAR   | The node ID where the login was processed                      |
| error_message  | VARCHAR   | The error message if the login failed                          |

## Examples

Login successful example:
```sql
SELECT * FROM system_history.login_history LIMIT 1;

*************************** 1. row ***************************
    event_time: 2025-06-03 06:04:57.353108
       handler: HTTP
    event_type: LoginSuccess
connection_uri: /session/login?disable_session_token=true
     auth_type: Password
     user_name: root
     client_ip: 127.0.0.1
    user_agent: bendsql/0.26.2-unknown
    session_id: 9a3ba9d8-44d9-49ca-9446-501deaca15c9
       node_id: 765ChL6Ra949Ioeb5LrTs
 error_message: 
```

Login failed example:
```sql
SELECT * FROM system_history.login_history LIMIT 1;

*************************** 1. row ***************************
    event_time: 2025-06-03 06:07:32.512021
       handler: MySQL
    event_type: LoginFailed
connection_uri: 
     auth_type: Password
     user_name: root1
     client_ip: 127.0.0.1:62050
    user_agent: 
    session_id: 4fb87258-865a-402c-8680-e3be1e01b4e6
       node_id: 765ChL6Ra949Ioeb5LrTs
 error_message: UnknownUser. Code: 2201, Text = User 'root1'@'%' does not exist..
```