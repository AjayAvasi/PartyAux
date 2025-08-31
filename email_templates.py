def get_otp_email_html(otp):
    """
    Returns the HTML template for OTP email with the provided OTP code.
    
    Args:
        otp (str): The OTP code to include in the email
        
    Returns:
        str: Complete HTML email template
    """
    return f"""
<html>
<head>
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap" rel="stylesheet">
</head>
<body style='font-family: "Space Grotesk", -apple-system, BlinkMacSystemFont, sans-serif; background: #000000; padding: 30px; margin: 0;'>
    <div style='max-width: 400px; margin: auto; background: #000000; border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px; box-shadow: 0 20px 40px rgba(255, 255, 255, 0.05); padding: 40px; text-align: center; backdrop-filter: blur(20px);'>
        
        <!-- Logo Section -->
        <h1 style='color: #ffffff; margin: 0 0 10px 0; font-size: 32px; font-weight: 700; letter-spacing: -1px;'>Party Aux</h1>
        
        <!-- Subtitle -->
        <p style='font-size: 18px; color: #cccccc; margin: 0 0 30px 0; font-weight: 300;'>Your One-Time Password for <strong style="color: #ffffff;">Login</strong></p>
        
        <!-- OTP Code Box -->
        <div style='font-size: 36px; font-weight: 700; letter-spacing: 8px; color: #000000; background: #ffffff; border-radius: 12px; padding: 20px; margin: 30px 0; font-family: "Space Grotesk", -apple-system, BlinkMacSystemFont, sans-serif; box-shadow: 0 4px 12px rgba(255, 255, 255, 0.1);'>{otp}</div>
        
        <!-- Instructions -->
        <div style='background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 20px; margin: 20px 0;'>
            <p style='color: #cccccc; font-size: 15px; line-height: 1.6; margin: 0;'>
                Use this code to complete your login to Party Aux.<br/>
                <strong style="color: #ffffff;">Expires in 10 minutes</strong>
            </p>
        </div>
        
        <!-- Security Note -->
        <p style='color: #999999; font-size: 14px; margin: 20px 0 0 0; line-height: 1.5;'>
            If you didn't request this code, you can safely ignore this email.
        </p>
        
        <!-- Footer -->
        <div style='margin-top: 40px; padding-top: 20px; border-top: 1px solid rgba(255, 255, 255, 0.1);'>
            <p style='color: #666666; font-size: 13px; margin: 0; font-weight: 300;'>
                Party Aux &copy; 2025<br/>
                <span style='color: #999999;'>The ultimate collaborative music experience</span>
            </p>
        </div>
        
    </div>
</body>
</html>
    """


def get_account_deletion_otp_email_html(otp):
    """
    Returns the HTML template for OTP email with the provided OTP code (Account Deletion).
    
    Args:
        otp (str): The OTP code to include in the email
        
    Returns:
        str: Complete HTML email template
    """
    return f"""
<html>
<head>
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap" rel="stylesheet">
</head>
<body style='font-family: "Space Grotesk", -apple-system, BlinkMacSystemFont, sans-serif; background: #000000; padding: 30px; margin: 0;'>
    <div style='max-width: 420px; margin: auto; background: #000000; border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px; box-shadow: 0 20px 40px rgba(255, 255, 255, 0.05); padding: 40px; text-align: center; backdrop-filter: blur(20px);'>
        
        <!-- Logo Section -->
        <h1 style='color: #ffffff; margin: 0 0 10px 0; font-size: 32px; font-weight: 700; letter-spacing: -1px;'>Party Aux</h1>
        
        <!-- Subtitle -->
        <p style='font-size: 18px; color: #ff6b6b; margin: 0 0 25px 0; font-weight: 400;'>
            You're about to <strong style="color: #ffffff;">end the music</strong> 🎵
        </p>
        
        <!-- OTP Code Box -->
        <div style='font-size: 36px; font-weight: 700; letter-spacing: 8px; color: #000000; background: #ffffff; border-radius: 12px; padding: 20px; margin: 30px 0; font-family: "Space Grotesk", -apple-system, BlinkMacSystemFont, sans-serif; box-shadow: 0 4px 12px rgba(255, 255, 255, 0.1);'>{otp}</div>
        
        <!-- Instructions -->
        <div style='background: rgba(255, 0, 0, 0.05); border: 1px solid rgba(255, 0, 0, 0.2); border-radius: 12px; padding: 20px; margin: 20px 0;'>
            <p style='color: #ffcccc; font-size: 15px; line-height: 1.6; margin: 0;'>
                Use this code to confirm the <strong style="color: #ffffff;">permanent deletion</strong> of your Party Aux account.<br/>
                Once confirmed, your playlists, queues, and jam history will be gone forever.<br/>
                <strong style="color: #ff6b6b;">This action cannot be undone</strong>.<br/>
                Code expires in 10 minutes ⏳.
            </p>
        </div>
        
        <!-- Security Note -->
        <p style='color: #999999; font-size: 14px; margin: 20px 0 0 0; line-height: 1.5;'>
            Didn’t request this? Someone might have tried to crash your party — ignore this email and your account will stay safe 🎧.
        </p>
        
        <!-- Footer -->
        <div style='margin-top: 40px; padding-top: 20px; border-top: 1px solid rgba(255, 255, 255, 0.1);'>
            <p style='color: #666666; font-size: 13px; margin: 0; font-weight: 300;'>
                Party Aux &copy; 2025<br/>
                <span style='color: #999999;'>Thanks for jamming with us — we’ll miss you on the aux 🎶</span>
            </p>
        </div>
        
    </div>
</body>
</html>
    """
