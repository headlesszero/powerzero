
import time
import math

from PIL import Image, ImageDraw, ImageFont

def bounce(oled, oled2 = None):

    # Detect if we're using Luma or the adafruit library
    use_display = False

    # Display image on OLED
    if hasattr(oled, "display"):  # Luma
        use_display = True

    if oled2 and not use_display:
        raise Exception(f"Double screen only works if both screens are using luma")


    # Create blank image for drawing
    font    = ImageFont.load_default()
    text    = "Pixels on Pi"

    # Calculate our bounding box
    image  = Image.new("1", (oled.width, oled.height))
    bbox   = ImageDraw.Draw(image).textbbox((0, 0), text, font=font)
    width  = bbox[2] - bbox[0]
    height = bbox[3] - bbox[1]


    #
    # Position and velocity
    #
    x = 0.0
    vs = 1.0    # Velocity scaler (direction)
    vx = 20.0   # Desired velocity in pixels per second

    yr = 0.0    # Radians of Y for sin calculation


    #
    # Setup timer and FPS display
    #
    FPS_UPDATE_RATE = 2             # Update every 5 seconds

    last_time   = time.monotonic()  # Initialize time tracking
    show_time   = FPS_UPDATE_RATE
    frame_count = 0


    while True:
        # Create a new mage to draw on
        image = Image.new("1", (oled.width, oled.height))
        draw  = ImageDraw.Draw(image)

        # Measure elapsed time (fractional seconds)
        current_time = time.monotonic()
        seconds      = current_time - last_time
        last_time    = current_time
        
        # Calculate the Y position
        yr += seconds
        y   = (((math.sin(yr) + 1) / 2.0) * (oled.height - height - 2)) # 2 for border

        # Add and upate our text
        draw.text((x, y), text, font=font, fill=255)

        # Bounce off edges
        if x <= 0:
            vs = 1.0
        elif x >= (oled.width - width):
            vs = -1.0

        x += vs * vx * seconds

        # Display image on OLED
        if use_display:
            oled.display(image)

            if oled2:
                oled2.display(image)

        else:
            oled.image(image)
            oled.show()

        # FPS calculation
        frame_count += 1
        show_time   -= seconds
        if show_time <= 0:
            print(f"FPS: {float(frame_count) / float(FPS_UPDATE_RATE)}")

            if FPS_UPDATE_RATE < 16:
                FPS_UPDATE_RATE *= 2

            show_time      += FPS_UPDATE_RATE
            frame_count     = 0


