# Simple Error Handling System

A lightweight error handling system for the AI Knowledge Assistant API.

## What it does

- Catches errors and returns consistent JSON responses
- Handles validation errors (400)
- Handles not found errors (404)
- Handles general API errors
- Simple to use and understand

## Files

- `exceptions.py` - Custom exception classes
- `handlers.py` - Flask error handlers
- `example.py` - Usage examples

## Usage

### 1. The system is already set up in your main app

No additional setup needed!

### 2. Using the exceptions in your code

```python
from error_handlers import ValidationError, NotFoundError

# For validation errors
if not data:
    raise ValidationError("Data is required")

# For not found errors
if not user:
    raise NotFoundError("User not found")
```

### 3. Error response format

All errors return this simple format:

```json
{
  "success": false,
  "error": "Error message here",
  "status_code": 400
}
```

## Example

```python
from flask import Blueprint, request, jsonify
from error_handlers import ValidationError, NotFoundError

bp = Blueprint('users', __name__)

@bp.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    if not user_id:
        raise ValidationError("User ID is required")
    
    # Your business logic here
    user = find_user(user_id)
    if not user:
        raise NotFoundError("User not found")
    
    return jsonify({"success": True, "data": user})
```

That's it! Simple and effective error handling.
