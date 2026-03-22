# AI Code Agent - Specification-Based Project Creation

## Overview

You can now create complete projects by writing **natural language specifications** instead of navigating menus. The agent intelligently parses your requirements and generates the appropriate project structure automatically.

## Quick Start

### 1. Write Your Project Specification

Create a file (`.spec`, `.txt`, or any extension) describing your project:

**`my-project.spec`:**
```
I need a Next.js web application called "ecommerce-store" with:
- React components for shopping cart
- TypeScript for type safety
- Tailwind CSS for styling
- Authentication system for users
- Database integration for products
- Docker support for deployment
```

### 2. Create the Project

```bash
python -m ai_code_agent --from-spec my-project.spec
```

### 3. Verify and Confirm

The agent will:
1. Parse your specification
2. Show extracted information (technology, features, project name)
3. Ask for confirmation
4. Generate the complete project

### 4. Start Developing

```bash
cd ecommerce-store
npm install
npm run dev
```

## Specification File Format

Write your specification in **natural language**. The agent understands:

### Project Details
- Project name (the agent extracts it or asks for confirmation)
- Technology stack (Next.js, FastAPI, Django, etc.)
- Required features
- Special requirements

### Example Specifications

#### Next.js Project
```
I need to build a Next.js e-commerce platform called "shop-hub" that includes:
- Product listing and shopping cart
- User authentication with login/signup
- Payment integration
- Admin dashboard
- Responsive design with Tailwind CSS
- Docker containerization for deployment
```

#### FastAPI Project
```
Build a RESTful API backend called "user-service" using FastAPI with:
- User authentication with JWT tokens
- PostgreSQL database
- Pydantic validation
- Comprehensive testing with pytest
- Docker and docker-compose setup
- CORS support for frontend integration
```

#### Django Project
```
Create a Django web application named "content-hub" with:
- User authentication system
- Admin interface for content management
- Database models for articles and users
- REST API with Django REST Framework
- Docker support

The application should be production-ready with best practices.
```

### Supported Keywords

The agent recognizes:

**Technologies:**
- `next.js`, `nextjs`, `react`, `typescript`
- `fastapi`, `python api`, `async api`
- `django`, `python web`
- `spring boot`, `java`
- `kotlin`, `jvm`
- `go`, `golang`
- `rust`, `cargo`

**Features:**
- `api`, `rest`, `endpoints` → API routes
- `database`, `db`, `sql`, `orm`
- `authentication`, `auth`, `login`, `jwt`, `oauth`
- `docker`, `container`, `kubernetes`
- `test`, `pytest`, `jest` → Testing
- `tailwind`, `css`, `styling`
- `validation`
- `security`
- `async`, `concurrent`

## Command Usage

### Basic Specification-Based Creation
```bash
python -m ai_code_agent --from-spec specification.spec
```

### With Different File Names
```bash
python -m ai_code_agent --from-spec my-app.txt
python -m ai_code_agent --from-spec requirements.md
python -m ai_code_agent --from-spec project-description.spec
```

### Show Interactive Menu (Default)
```bash
python -m ai_code_agent
```

### Generate Code Snippets (Legacy)
```bash
python -m ai_code_agent --gen
```

## How It Works

### Specification Parsing Process

1. **Read File**: Loads your specification from the provided file
2. **Parse**: Uses AI (Ollama) or keyword-based matching to extract:
   - Technology stack
   - Project name
   - Features
   - Custom requirements
3. **Validate**: Ensures project name is valid and tech is supported
4. **Confirm**: Shows parsed result and asks for approval
5. **Generate**: Creates project files and directory structure

### Parsing Modes

#### AI-Powered Parsing (Default)
- Uses Ollama with local LLM (if available)
- Understands natural language well
- More flexible with wording
- Requires Ollama to be running

#### Keyword-Based Parsing (Fallback)
- Uses pattern matching and keyword detection
- No external dependencies needed
- Works offline
- Less flexible but still effective

### Confidence Score

The agent provides a confidence score (0-1%) indicating how certain it is about the parsing:
- **0.3-0.5**: Low confidence - review carefully
- **0.6-0.8**: Good confidence - minor review
- **0.8-1.0**: High confidence - likely correct

## Example Workflow

### Step-by-Step Example

**File: `my-api.spec`**
```
I'm building a FastAPI backend called "notification-service" with:
- REST API for sending notifications
- Database integration with PostgreSQL
- User authentication using JWT
- Email and SMS notification support
- Request validation with Pydantic
- Unit and integration tests
- Docker and docker-compose for containerization
```

**Command:**
```bash
python -m ai_code_agent --from-spec my-api.spec
```

**Output & Confirmation:**
```
📖 Reading specification from: my-api.spec

============================================================
📋 Parsed Project Specification
============================================================
Technology: FASTAPI
Project Name: notification-service
Description: I'm building a FastAPI backend called "notification-service"...
Features: api_routes, database, orm, auth, docker, testing, validation, cors
Confidence: 88%
============================================================

Does this look correct? (yes/no): yes

✓ Technology: FastAPI (Python)
✓ Project Name: notification-service
✓ Features: api_routes, database, orm, auth, docker, testing, validation, cors

------------------------------------------------------------
📁 Creating project directory...
✓ Created /path/to/notification-service

📝 Generating project files...
✓ Generated 14 files

✓ Project created successfully!
📁 Location: /path/to/notification-service
📦 Files created: 14

📋 Next steps:
   1. cd notification-service
   2. pip install -r requirements.txt
   3. python main.py
```

## Generated Files

### FastAPI Example
```
notification-service/
├── main.py                          # Application entry point
├── requirements.txt                 # Python dependencies
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── hello.py                # Example API endpoint
│   └── config.py                   # Configuration
├── tests/
│   ├── __init__.py
│   └── test_api.py                 # Test examples
├── Dockerfile                       # Docker configuration
├── docker-compose.yml               # Docker compose setup
├── pytest.ini                       # Test configuration
├── .env.example                     # Environment variables
├── .gitignore                       # Git ignore rules
└── README.md                        # Project documentation
```

###  Next.js Example
```
ecommerce-store/
├── app/
│   ├── page.tsx                    # Home page
│   ├── layout.tsx                  # Root layout
│   ├── globals.css                 # Global styles
│   └── api/
│       └── hello/
│           └── route.ts            # API endpoint example
├── components/                      # React components
├── lib/                            # Utilities and helpers
├── public/                         # Static assets
├── package.json                    # Node dependencies
├── tsconfig.json                   # TypeScript configuration
├── tailwind.config.js              # Tailwind CSS config
├── next.config.js                  # Next.js configuration
├── .eslintrc.json                  # ESLint rules
├── .gitignore
└── README.md
```

## Error Handling

### Common Issues & Solutions

#### "Invalid project name"
The agent validates project names. Use:
- Alphanumeric characters
- Hyphens (`-`)
- Underscores (`_`)

**Examples:**
```
✓ my-awesome-app
✓ MyAwesomeApp
✓ my_awesome_app
✓ awesome123
✗ my awesome app    (spaces not allowed)
✗ my-awesome-app!   (special chars not allowed)
```

#### "Directory already exists"
Choose a different project name or check the directory exists.

#### "Technology not recognized"
Make sure your specification mentions a supported tech:
```
Supported: nextjs, fastapi, django, spring_boot, kotlin, golang, rust
```

#### "Low confidence in parsing"
If confidence is below 0.3, the agent may have misunderstood. You can:
1. Answer "no" to reject and try again
2. Clarify your specification
3. Use the interactive menu instead

### Debugging

Check what was parsed:
```bash
python -m ai_code_agent --from-spec my-spec.spec | head -20
```

Example output shows:
- Detected technology
- Extracted project name
- Identified features
- Confidence score

## Advanced Examples

### Full-Stack Application
```
I need a complete Next.js full-stack application called "task-manager" with:
- React components for task management
- TypeScript and Tailwind CSS
- API routes for backend functionality
- Authentication with JWT
- PostgreSQL database integration
- User profiles and permissions
- Docker containerization
- Comprehensive testing

The app should follow modern development practices and be production-ready.
```

### Microservices Setup
```
Create a FastAPI microservice named "order-service" with features including:
- REST API for order processing
- Async database operations
- PostgreSQL with SQLAlchemy ORM
- User authentication and authorization
- Request/response validation
- Comprehensive error handling
- Unit and integration tests
- Docker and Kubernetes ready
- CORS support for multiple frontends
```

### Enterprise Application
```
Build a Django application called "employee-management-system" with:
- Employee data management
- Role-based access control
- Admin dashboard for management
- REST API for mobile apps
- PostgreSQL backend
- Automated testing
- Docker containerization
- Production-ready deployment configuration
```

## Tips & Tricks

### 1. Be Specific
Instead of:
```
Create a web app
```

Use:
```
Create a Next.js web application called "task-app" with TypeScript,
Tailwind CSS, authentication, database integration, and Docker support
```

### 2. List Features Clearly
```
The app should have:
- User authentication
- Product database
- Shopping cart
- Payment processing
- Admin panel
- API for mobile apps
```

### 3. Mention Project Name Explicitly
```
Create a project called "super-app" with...
```

### 4. Include Technology Stack
```
Build using FastAPI with Python, PostgreSQL, and Docker
```

### 5. Specify Special Requirements
```
The application needs Docker support, JWT authentication, and
comprehensive pytest coverage
```

## Performance

- **Specification Parsing**: ~1-2 seconds
- **Project Generation**: ~1-3 seconds
- **Total Time**: Usually under 5 seconds
- **AI-Enhanced Parsing** (with Ollama): 5-30 seconds depending on model

## Stored Specifications

Each generated project includes a `.project-spec.json` file containing:
- Technology used
- Project name
- Selected features
- Original requirements
- Parsing confidence

This helps you remember what was configured for each project.

## Troubleshooting

### Specification Not Parsed Correctly

1. **Check Technology Name**
   - Is the tech name clear? (nextjs, fastapi, django, etc.)
   - Use explicit names: "Next.js" or "FastAPI"

2. **Clarify Features**
   - List features clearly
   - Use keywords the agent understands
   - Be specific about what you need

3. **Review Confidence**
   - If confidence < 0.3, rewrite more clearly
   - Add explicit technology and project names
   - List features as bullet points

### Ollama/AI Mode Not Working

The agent falls back to keyword-based parsing automatically:
1. Ensure Ollama is running if you want AI-enhanced parsing
2. Keyword-based parsing works offline and is still effective

### Generated files have wrong content

The agent uses templates by default (not AI) for generation:
- Templates are fast and reliable
- They follow best practices
- You can customize them after generation

## Next Steps

1. **Create your first spec file**:
   ```bash
   nano my-project.spec
   ```

2. **Run the scaffolder**:
   ```bash
   python -m ai_code_agent --from-spec my-project.spec
   ```

3. **Navigate to your project**:
   ```bash
   cd <project-name>
   ```

4. **Start developing**:
   ```bash
   npm install && npm run dev  # For Node.js projects
   # OR
   pip install -r requirements.txt && python main.py  # For Python projects
   ```

---

**That's it!** You now have a complete, production-ready project structure tailored to your needs. 🎉

