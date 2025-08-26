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
    <style>
        .network-canvas {{{{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            pointer-events: none;
        }}}}
    </style>
</head>
<body style='font-family: "Space Grotesk", Arial, sans-serif; background: #000000; padding: 30px; margin: 0; position: relative;'>
    <canvas class="network-canvas" id="networkCanvas"></canvas>
    <div style='max-width: 400px; margin: auto; background: #000000; border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px; box-shadow: 0 20px 40px rgba(255, 255, 255, 0.05); padding: 40px; text-align: center; backdrop-filter: blur(20px);'>
        
        <!-- Logo Section -->
        <h1 style='color: #ffffff; margin: 0 0 10px 0; font-size: 32px; font-weight: 700; letter-spacing: -1px;'>Party Aux</h1>
        
        <!-- Subtitle -->
        <p style='font-size: 18px; color: #cccccc; margin: 0 0 30px 0; font-weight: 300;'>Your One-Time Password for <strong style="color: #ffffff;">Login</strong></p>
        
        <!-- OTP Code Box -->
        <div style='font-size: 36px; font-weight: 700; letter-spacing: 8px; color: #000000; background: #ffffff; border-radius: 12px; padding: 20px; margin: 30px 0; font-family: "Space Grotesk", monospace; box-shadow: 0 4px 12px rgba(255, 255, 255, 0.1);'>{otp}</div>
        
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

    <script>
        class NetworkAnimation {{{{
            constructor(canvas) {{{{
                this.canvas = canvas;
                this.ctx = canvas.getContext('2d');
                this.dots = [];
                this.connections = [];
                this.connectionDistance = 80;
                this.numDots = 30; // Fewer dots for email
                
                this.resize();
                this.createDots();
                this.bindEvents();
                this.animate();
            }}}}

            resize() {{{{
                this.canvas.width = window.innerWidth;
                this.canvas.height = window.innerHeight;
            }}}}

            createDots() {{{{
                this.dots = [];
                for (let i = 0; i < this.numDots; i++) {{{{
                    this.dots.push({{{{
                        x: Math.random() * this.canvas.width,
                        y: Math.random() * this.canvas.height,
                        vx: (Math.random() - 0.5) * 1,
                        vy: (Math.random() - 0.5) * 1,
                        radius: Math.random() * 2 + 1
                    }}}});
                }}}}
            }}}}

            updateDots() {{{{
                this.dots.forEach(dot => {{{{
                    dot.x += dot.vx;
                    dot.y += dot.vy;

                    if (dot.x < 0 || dot.x > this.canvas.width) {{{{
                        dot.vx *= -1;
                        dot.x = Math.max(0, Math.min(this.canvas.width, dot.x));
                    }}}}
                    if (dot.y < 0 || dot.y > this.canvas.height) {{{{
                        dot.vy *= -1;
                        dot.y = Math.max(0, Math.min(this.canvas.height, dot.y));
                    }}}}

                    dot.vx += (Math.random() - 0.5) * 0.01;
                    dot.vy += (Math.random() - 0.5) * 0.01;

                    const speed = Math.sqrt(dot.vx * dot.vx + dot.vy * dot.vy);
                    if (speed > 1) {{{{
                        dot.vx = (dot.vx / speed) * 1;
                        dot.vy = (dot.vy / speed) * 1;
                    }}}}
                }}}});
            }}}}

            findConnections() {{{{
                this.connections = [];
                
                for (let i = 0; i < this.dots.length; i++) {{{{
                    for (let j = i + 1; j < this.dots.length; j++) {{{{
                        const distance = this.getDistance(this.dots[i], this.dots[j]);
                        if (distance < this.connectionDistance) {{{{
                            this.connections.push({{{{
                                dot1: this.dots[i],
                                dot2: this.dots[j],
                                distance: distance,
                                opacity: 1 - (distance / this.connectionDistance)
                            }}}});
                        }}}}
                    }}}}
                }}}}
            }}}}

            getDistance(point1, point2) {{{{
                const dx = point1.x - point2.x;
                const dy = point1.y - point2.y;
                return Math.sqrt(dx * dx + dy * dy);
            }}}}

            draw() {{{{
                this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

                this.connections.forEach(connection => {{{{
                    this.ctx.beginPath();
                    this.ctx.moveTo(connection.dot1.x, connection.dot1.y);
                    this.ctx.lineTo(connection.dot2.x, connection.dot2.y);
                    this.ctx.strokeStyle = `rgba(255, 255, 255, ${{{{connection.opacity * 0.2}}}})`;
                    this.ctx.lineWidth = 0.5;
                    this.ctx.stroke();
                }}}});

                this.dots.forEach(dot => {{{{
                    this.ctx.beginPath();
                    this.ctx.arc(dot.x, dot.y, dot.radius, 0, Math.PI * 2);
                    this.ctx.fillStyle = 'rgba(255, 255, 255, 0.6)';
                    this.ctx.fill();
                }}}});
            }}}}

            animate() {{{{
                this.updateDots();
                this.findConnections();
                this.draw();
                requestAnimationFrame(() => this.animate());
            }}}}

            bindEvents() {{{{
                window.addEventListener('resize', () => {{{{
                    this.resize();
                    this.createDots();
                }}}});
            }}}}
        }}}}

        // Initialize network animation when page loads
        window.addEventListener('load', () => {{{{
            const canvas = document.getElementById('networkCanvas');
            if (canvas) {{{{
                new NetworkAnimation(canvas);
            }}}}
        }}}});
    </script>
</body>
</html>
    """
