# WhatsApp AI Assistant - Urgency Detection & Email Notifications

This project implements an urgency detection system for WhatsApp messages with automatic email notifications.

## Features

- **Urgency Detection**: Automatically detects urgent messages using configurable keywords
- **Email Notifications**: Sends SMTP email alerts when urgent messages are received
- **Configurable Keywords**: Customizable urgency detection keywords
- **Comprehensive Testing**: Full test suite for all components
- **Easy Setup**: Environment-based configuration

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Copy the example environment file and configure your settings:

```bash
cp .env.example .env
```

Edit `.env` with your SMTP settings:

```env
# SMTP Configuration for Email Notifications
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
SMTP_FROM_EMAIL=your_email@gmail.com
SMTP_TO_EMAIL=alert_recipient@gmail.com

# Urgency Detection Settings
URGENCY_KEYWORDS=urgent,asap,emergency,critical,immediate,help
```

### 3. Run the Demo

```bash
python demo.py
```

## Usage

### Basic Usage

```python
from src import MessageProcessor

# Initialize the processor
processor = MessageProcessor()

# Process a message
message_data = {
    'text': 'This is urgent! Need help ASAP!',
    'sender': 'john_doe',
    'chat_id': 'family_chat',
    'timestamp': datetime.now()
}

result = processor.process_message(message_data)

if result['is_urgent']:
    print(f"Urgent message detected! Keywords: {result['matched_keywords']}")
    print(f"Email sent: {result['email_sent']}")
```

### Urgency Detection Only

```python
from src import UrgencyDetector

detector = UrgencyDetector()

# Check if message is urgent
is_urgent = detector.is_urgent("This is urgent!")
keywords = detector.get_matched_keywords("Help! Emergency situation!")

print(f"Urgent: {is_urgent}")
print(f"Keywords found: {keywords}")
```

### Email Notifications Only

```python
from src import EmailNotifier

notifier = EmailNotifier()

# Send urgent alert
message_data = {
    'text': 'Emergency! System down!',
    'sender': 'admin',
    'matched_keywords': ['emergency']
}

success = notifier.send_urgent_alert(message_data)
print(f"Email sent: {success}")
```

## Configuration

### SMTP Settings

The system supports various SMTP providers. Here are common configurations:

#### Gmail
```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
```

#### Outlook/Hotmail
```env
SMTP_HOST=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_USERNAME=your_email@outlook.com
SMTP_PASSWORD=your_password
```

#### Yahoo
```env
SMTP_HOST=smtp.mail.yahoo.com
SMTP_PORT=587
SMTP_USERNAME=your_email@yahoo.com
SMTP_PASSWORD=your_app_password
```

### Urgency Keywords

Configure detection keywords in the `.env` file:

```env
URGENCY_KEYWORDS=urgent,asap,emergency,critical,immediate,help,priority,rush
```

Keywords are:
- Case-insensitive
- Matched as whole words (word boundaries)
- Comma-separated in configuration

## Testing

### Run All Tests

```bash
python tests/run_tests.py
```

### Run Individual Test Suites

```bash
# Test urgency detection
python -m unittest tests.test_urgency_detector

# Test email notifications
python -m unittest tests.test_email_notifier

# Test message processing
python -m unittest tests.test_message_processor
```

### Test Email Configuration

Use the demo script to test your email configuration:

```bash
python demo.py
```

Then type `test` to send a test urgent message.

## API Reference

### MessageProcessor

Main class for processing WhatsApp messages.

#### Methods

- `process_message(message_data: Dict[str, Any]) -> Dict[str, Any]`
  - Processes a message and returns urgency detection and email results
  - Required: `message_data['text']`
  - Optional: `sender`, `chat_id`, `timestamp`

- `test_system() -> Dict[str, Any]`
  - Runs system tests for urgency detection and email configuration

### UrgencyDetector

Detects urgent messages based on keywords.

#### Methods

- `is_urgent(message: str) -> bool`
  - Returns True if message contains urgent keywords

- `get_matched_keywords(message: str) -> List[str]`
  - Returns list of matched urgency keywords

### EmailNotifier

Sends email notifications for urgent messages.

#### Methods

- `send_urgent_alert(message_data: Dict[str, Any]) -> bool`
  - Sends email alert for urgent message
  - Returns True if successful

- `test_email_configuration() -> bool`
  - Tests SMTP configuration by sending test email

## Error Handling

The system includes comprehensive error handling:

- **Invalid message data**: Returns error in result
- **SMTP configuration missing**: Logs error and returns False
- **Email sending failure**: Logs error but continues processing
- **Network issues**: Gracefully handles SMTP connection errors

## Security Considerations

- Store SMTP credentials in environment variables, not in code
- Use app passwords for Gmail (not your main password)
- Ensure `.env` file is in `.gitignore`
- Consider rate limiting for email notifications in production

## Integration with WhatsApp

This urgency detection system is designed to integrate with:

1. **whatsapp-mcp server**: For receiving WhatsApp messages
2. **Webhook endpoints**: For real-time message processing
3. **Database storage**: For message history and analytics
4. **LLM integration**: For advanced message analysis

See the `github_issues_whatsapp_mcp (1).json` file for the complete roadmap.

## Troubleshooting

### Common Issues

1. **Email not sending**
   - Check SMTP credentials
   - Verify network connectivity
   - Enable "Less secure app access" or use app passwords

2. **Keywords not detected**
   - Verify keyword configuration
   - Check for typos in keywords
   - Ensure keywords are comma-separated

3. **Import errors**
   - Ensure you're running from the project root
   - Check Python path configuration

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

This project is open source and available under the MIT License.