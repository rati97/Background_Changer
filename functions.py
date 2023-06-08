from PIL import Image
from rembg import remove, new_session

# specify model to use
session = new_session("u2net_human_seg")


def change_background(selfie, background, resize_target="background"):
    """
    Change the background of a given selfie image with a specified background.

    This function first cuts the person out of the selfie image, then it puts the
    person into the new background image. Depending on the value of resize_target,
    the person or the background is resized to match the size of the other.

    Parameters:
    selfie (PIL.Image.Image): A PIL Image object of the selfie with the person to cut out.
    background (PIL.Image.Image): A PIL Image object to use as the new background.
    resize_target (str): A string that decides which of the images (selfie or background)
                         to resize. It should be either 'background' or 'selfie'.

    Returns:
    PIL.Image.Image: A new PIL Image object with the person from the selfie
                     placed onto the new background.

    Raises:
    ValueError: If resize_target is not 'background' or 'selfie'.
    """

    if resize_target not in ["background", "selfie"]:
        raise ValueError("resize_target must be either 'background' or 'selfie'")

    # cut person from selfie
    mask = remove(selfie, only_mask=True, session=session)

    if resize_target == "background":
        # resize background to match the selfie size
        background = background.resize(selfie.size)
        mask = mask.resize(selfie.size)
    else:
        # resize selfie and mask to match the background size
        selfie = selfie.resize(background.size)
        mask = mask.resize(background.size)

    # put person into background
    background.paste(selfie, (0, 0), mask=mask)

    return background


if __name__ == "__main__":
    selfie = Image.open("selfie.png")
    background = Image.open("background.png")

    result = change_background(selfie, background, "background")
    result.show()
