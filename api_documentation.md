# Complete CRM API Documentation (For Frontend Developers)

This document provides everything the frontend team needs to build the UI, including authentication flows, API endpoints, JSON payloads, and the Role-Based Access Control (RBAC) rules.

---

## 1. Global API Behavior

### Standard Response Format
Every single API response is wrapped in a standard JSON format so the frontend can handle success/error states universally.

**Success Response:**
```json
{
  "success": true,
  "data": { ... } // Could be an object or an array depending on the endpoint
}
```

**Error Response:**
```json
{
  "success": false,
  "errors": {
      "field_name": ["Error message details..."]
  }
}
```

### Pagination
All `GET` list endpoints (Customers, Projects, Tasks) are paginated to **30 items per page**.
```json
{
  "success": true,
  "data": {
    "count": 150,
    "next": "http://api.../?page=2",
    "previous": null,
    "results": [ ... array of objects ... ]
  }
}
```

### Authentication Header
All endpoints (except Login and Register) require a JWT access token in the headers:
`Authorization: Bearer <your_access_token>`

---

## 2. Roles & Permissions (RBAC)
The UI should dynamically hide/show buttons (like "Delete" or "Create") based on the logged-in user's role.

| Role | Customers | Projects | Tasks | Role Management |
| :--- | :--- | :--- | :--- | :--- |
| **👑 Admin** | Create, Read, Update, Delete | Create, Read, Update, Delete | Create, Read, Update, Delete | **Full Access** |
| **👔 Manager** | Create, Read, Update, Delete | Create, Read, Update, Delete | Create, Read, Update, Delete | *No Access* |
| **👷 Employee** | **Read-Only** | **Read-Only** | **Create, Read, Update** *(Cannot Delete)* | *No Access* |
| **👀 Viewer** | **Read-Only** | **Read-Only** | **Read-Only** | *No Access* |

---

## 3. Authentication APIs

### Register a User
- **Method:** `POST /api/auth/register/`
- **Auth Required:** No
- **Payload:**
```json
{
    "email": "user@example.com",
    "password": "securepassword123",
    "first_name": "John",
    "last_name": "Doe",
    "address": "123 Main St",
    "contact_number": "555-0199"
}
```

### Login
- **Method:** `POST /api/auth/login/`
- **Auth Required:** No
- **Payload:** `{"email": "user@example.com", "password": "mypassword"}`
- **Response Data:** Returns tokens and a `user` object to populate the frontend profile state.
```json
{
    "refresh": "eyJhbG...",
    "access": "eyJhbG...",
    "user": {
        "id": 10,
        "email": "user@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "organization": "Netflix",
        "role": "employee", 
        "is_active": true,
        "address": "123 Main St",
        "contact_number": "555-0199"
    }
}
```

### Get Profile
- **Method:** `GET /api/auth/profile/`
- **Returns:** Same `user` object as the login response.

---

## 4. Core Entities

### Customers
- **List:** `GET /api/customers/` *(Supports filtering: `?company_name=X&projects=Y`, searching: `?search=name`)*
- **Detail:** `GET /api/customers/{id}/`
- **Create:** `POST /api/customers/`
- **Update:** `PATCH /api/customers/{id}/`
- **Delete:** `DELETE /api/customers/{id}/`

**POST/PATCH Payload:**
```json
{
    "name": "Bruce Wayne",
    "email": "bruce@wayneenterprises.com",
    "phone_number": "555-0199",
    "company_name": "Wayne Enterprises",
    "address": "1007 Mountain Drive"
}
```

### Projects
- **List:** `GET /api/projects/` *(Supports filtering: `?status=new&customer=1`)*
- **Detail:** `GET /api/projects/{id}/`
- **Create:** `POST /api/projects/`
- **Update:** `PATCH /api/projects/{id}/`
- **Delete:** `DELETE /api/projects/{id}/`

**POST/PATCH Payload:**
```json
{
    "name": "Batmobile Navigation",
    "description": "GPS routing system.",
    "customer": 1, // ID of the customer
    "status": "new", // choices: "new", "in_progress", "completed"
    "budget": 150000.00,
    "start_date": "2026-08-01",
    "end_date": "2026-12-31"
}
```

### Tasks
- **List:** `GET /api/tasks/` *(Supports filtering: `?status=todo&project=1&assigned_to=5`)*
- **Detail:** `GET /api/tasks/{id}/`
- **Create:** `POST /api/tasks/`
- **Update:** `PATCH /api/tasks/{id}/`
- **Delete:** `DELETE /api/tasks/{id}/`

**POST/PATCH Payload:**
```json
{
    "title": "Design GPS UI interface",
    "description": "Create wireframes.",
    "project": 1, // ID of the project
    "assigned_to": 5, // ID of the user
    "status": "todo", // choices: "todo", "in_progress", "completed"
    "due_date": "2026-08-15"
}
```

---

## 5. Administration (Admin Only)

### Assign a Role to a User
- **Method:** `POST /api/assign-role/`
- **Auth Required:** YES (Admin role only)
- **Payload:**
```json
{
    "user": 5, // ID of the CustomUser
    "organization": 1, // ID of the Organization
    "role": 3 // ID of the Role (1=Admin, 2=Manager, 3=Employee, 4=Viewer)
}
```
