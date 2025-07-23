Part A – System Design (Written):  

1) Assignment: EdTech Assignment Tracker

2) Objective:  

A simplified assignment tracking system where teachers can post assignments and students can submit them. Built with Django and SQLite, includes role-based authentication, REST APIs, and basic HTML frontends. 

3) Define the system architecture  

- Frontend: HTML, CSS, JavaScript 
- Backend: Django (Python)
- Database: SQLite ()
- Tools Used: Postman for API testing

4) List core entities and relationships (use ER diagram or tabular format)  

| Entity     | Fields                                                           |
| ---------- | ---------------------------------------------------------------- |
| User       | username, password, role (student/teacher), etc.                 |
| Assignment | title, description, due_date, created_at, teacher (FK to User)   |
| Submission | assignment (FK), student (FK), submitted_file, submitted_at      |

5)  Define API endpoints for:  

| Endpoint              | Method | Role    | Description                         |
| --------------------- | ------ | ------- | ----------------------------------- |
| /signup/              | POST   | Both    | User signup                         |
| /login/               | POST   | Both    | User login                          |
| /create-assignment/   | POST   | Teacher | Create assignment                   |
| /submit-assignment/   | POST   | Student | Submit assignment                   |
| /view-submissions/    | POST   | Teacher | View all submissions for assignment |

6) Teacher creates assignment  

/create/ → Teacher assignment creation

7) Student submits assignment  

/submit/ → Student assignment submission

8) Teacher views submissions  

/view/ → Teacher views all submissions

9) Describe authentication strategy (roles: student vs. teacher)  

- Role-based users (teacher, student)
- Signup/login APIs
- Role is checked at each protected API endpoint

10) Suggest how the system could be scaled in future

- use postgreSQl for production instead of SQLite 
- For file upload use AWS S3
- Add pagination, deadline enforcement, file size/type validation
- Add token-based authentication (JWT)




