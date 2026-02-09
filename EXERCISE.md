# Incubyte Salary Management Kata

Hi there!

If you're reading this, it means you're now at the coding exercise step of the engineering hiring process. We're really happy that you made it here and super appreciative of your time!

In this exercise you're asked to implement some features as an API

> This application is an API and has no UI

If you have any questions, don't hesitate to reach out directly to us.

## Expectations

- This exercise is intentionally designed to assess how you leverage AI effectively to work faster, maintain quality, and make thoughtful trade-offs. We expect you to use AI to scaffold code, generate test cases and draft documentation.
- We encourage you to use the programming language and tools best suited for the role you are applying for.
- Be intentional and transparent: note where and how you used AI (tools, prompts, rationale) in the “Implementation Details” section of the README.md.
- It should be production-ready code - the code will show us how you ship things to production and be a mirror of your craft.
- Take whatever time you need - we won’t look at start/end dates, you have a life besides this and we respect that!

> Important: Use the generated GitHub classroom repo for your submission. Do not create a new repository.

### TDD is a must

- Follow a strict Test-Driven Development workflow: write failing tests first, implement the minimal code to pass, then refactor.
- Your commit history should reflect the TDD loop (red → green → refactor). We want to see how your code evolved over time, so please ensure there are incremental commits.
- Include unit tests that are fast, deterministic, and meaningful.
  Aim for clear coverage of:
  - CRUD for the employee resource
  - Salary calculation endpoint
  - Salary metrics endpoints and edge cases

# Features To Implement:

## 1. Employee CRUD Endpoint

You will have to create an employee resource and implement default CRUD operations.

There are a few requirements for the info captured by the employee resource:

- It must have a full name
- It must have a job title
- It must have a country
- It must have a salary

Ensure all the records are saved to a Sqlite database.

## 2. Salary Calculation Endpoint

Add an endpoint that calculates deductions and net salary from a given gross salary, given employee ID.

### Deduction Rules

- India:
  - TDS: 10% of gross
- United States:
  - TDS: 12% of gross
- All other countries:
  - No deductions (net = gross)

## 3. Salary Metrics Endpoint

Create new endpoint(s) to provide data about salaries:

- Given a country, the minimum, maximum, and average salary in that country.
- Given a job title, the average salary for all the employees with that job title.

## When You're Done

- Add a decent README with relevant information.
- Send us the link to your repo once you’re happy with what you have done.
