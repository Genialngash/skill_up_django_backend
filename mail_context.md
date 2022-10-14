## Email Data Context

Data used to populate email templates in JSON format

### Signup Email

```
{
  "protocol': "https",
  "domain": "example.com",
  "url": "example:activation-code",
  "site_name": "The Company X Team",
  "user": {
      "first_name': "Test",
      "last_name": "User",
  }
}
```

### Password Reset Email

```
{
  "protocol": "https",
  "domain": "example.com",
  "url": "reset-code",
  "site_name": "The Company X Team",
  "user": {
      "first_name": "Test",
      "last_name": "User",
  }
}
```

### Signup Credits

```
  {
      "unlock_code": "code",
      "expire_month": "Month",
      "expire_day": 00,
      "expire_year": 2020,
      "date_suffix": "th",
      "job_cards": 0,
      "total_unlocks": 0,
      "site_name":  "The Company X Team"
  }
```
