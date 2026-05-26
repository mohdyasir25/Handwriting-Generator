from flask import Flask, render_template, request
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
import textwrap

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        # User text
        text = request.form["text"]

        # Fix Windows line breaks
        text = text.replace('\r', '')

        # Create notebook page
        img = Image.new("RGB", (1400, 1200), color=(252, 248, 235))

        draw = ImageDraw.Draw(img)

        # Page border
        draw.rectangle(
            [(15, 15), (1385, 1185)],
            outline=(180, 180, 180),
            width=3
        )

        # Top heading line
        draw.line(
            (40, 70, 1350, 70),
            fill=(200, 200, 200),
            width=2
        )

        # Blue notebook lines
        for i in range(100, 1200, 65):

            draw.line(
                (40, i, 1350, i),
                fill=(150, 200, 255),
                width=2
            )

        # Red margin line
        draw.line(
            (120, 40, 120, 1150),
            fill="red",
            width=3
        )

        # Handwriting font
        font = ImageFont.truetype(
            "Yasirfont-Regular.ttf",
            52
        )

        # Automatic text wrapping
        wrapped_text = textwrap.wrap(text, width=32)

        y = 90

        for line in wrapped_text:

            draw.text(
                (140, y + 15),
                line,
                fill=(20, 20, 20),
                font=font
            )

            y += 65

        # Save image
        img.save("static/output.png")

        # Create PDF
        pdf = canvas.Canvas("static/output.pdf")

        pdf.drawImage(
            "static/output.png",
            20,
            50,
            width=560,
            height=800
        )

        pdf.save()

        return render_template(
            "index.html",
            show=True
        )

    return render_template(
        "index.html",
        show=False
    )

if __name__ == "__main__":
    app.run(debug=True)