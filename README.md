# OGL Test Project

> A project to test and experiment with **OGL**.

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/CentraleSupelec/test-ogl.git
cd test-ogl
```

or 

```bash
git clone git@github.com:CentraleSupelec/test-ogl.git
cd test-ogl
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Copy the `.env_dist` file to create your own `.env` :

```bash
cp .env_dist .env
```

Then open `.env` and fill in the required values.

### 4. Run the project

```bash
python3 -m src.main
```