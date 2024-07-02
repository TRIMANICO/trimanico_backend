from django.core.mail import send_mail
from django.conf import settings

def send_otp_via_email(email, otp):
    subject = "Your Account Verification Email"
    message = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f4;
        }}
        .container {{
            width: 100%;
            max-width: 600px;
            margin: 0 auto;
            background-color: #ffffff;
            padding: 0;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }}
        .header {{
            text-align: center;
            background: linear-gradient(90deg, #007BFF, #00BFFF);
            color: #ffffff;
            padding: 30px 20px;
        }}
        .header h1 {{
            font-size: 28px;
            margin: 0;
        }}
        .content {{
            padding: 20px;
            text-align: center;
        }}
        .content p {{
            color: #555555;
            font-size: 16px;
            line-height: 1.5;
            margin: 10px 0;
        }}
        .content .otp {{
            display: inline-block;
            background-color: #007BFF;
            color: #ffffff;
            padding: 15px 25px;
            border-radius: 5px;
            font-size: 24px;
            font-weight: bold;
            letter-spacing: 2px;
            margin: 20px 0;
        }}
        .footer {{
            text-align: center;
            background-color: #007BFF;
            color: #ffffff;
            padding: 20px;
        }}
        .footer p {{
            margin: 5px 0;
        }}
        @media (max-width: 600px) {{
            .header h1 {{
                font-size: 24px;
            }}
            .content p {{
                font-size: 14px;
            }}
            .content .otp {{
                font-size: 20px;
                padding: 10px 20px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Account Verification</h1>
        </div>
        <div class="content">
            <p>Thank you for registering with us. To verify your account, please use the following One-Time Password (OTP):</p>
            <div class="otp">{otp}</div>
            <p>This OTP is valid for the next 10 minutes. Please do not share it with anyone.</p>
            <p>If you did not request this verification, please ignore this email.</p>
        </div>
        <div class="footer">
            <p>Best Regards,</p>
            <p>Trimanico</p>
        </div>
    </div>
</body>
</html>
"""
    email_from = settings.EMAIL_HOST_USER
    try:
        send_mail(
            subject,
            "",  # Plain text message (leave empty if not used)
            email_from,
            [email],
            html_message=message
        )
        return True
    except Exception as e:
        print("error", e)
        return False
