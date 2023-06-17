from Bot import LOG, encoder

import time, math, re, asyncio, subprocess
from ethon.pyfunc import total_frames as tf
from Bot import encoder as sohailpyro
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, User

def time_formatter(milliseconds: int) -> str:
    """Inputs time in milliseconds, to get beautified time,
    as string"""
    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    weeks, days = divmod(days, 7)
    tmp = (
        (f"{str(weeks)}w:" if weeks else "")
        + (f"{str(days)}d:" if days else "")
        + (f"{str(hours)}h:" if hours else "")
        + (f"{str(minutes)}m:" if minutes else "")
        + (f"{str(seconds)}s:" if seconds else "")
    )
    return tmp[:-1] if tmp.endswith(":") else tmp
 
def humanbytes(size):
    if size in [None, ""]:
        return "0 B"
    for unit in ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]:
        if size < 1024:
            break
        size /= 1024
    return f"{size:.2f} {unit}"
   
async def ffmpeg_progress(cmd, file, progress, now, send_msg, ps_name,log=None):
    total_frames = tf(file)
    with open(progress, "w") as fk:
        pass
    proce = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    while proce.returncode != 0:
        await asyncio.sleep(5)
        with open(progress, "r+") as fil:
            text = fil.read()
            frames = re.findall("frame=(\\d+)", text)
            size = re.findall("total_size=(\\d+)", text)
            speed = 0
            if len(frames):
                elapse = int(frames[-1])
            if len(size):
                size = int(size[-1])
                per = elapse * 100 / int(total_frames)
                time_diff = time.time() - int(now)
                speed = round(elapse / time_diff, 2)
            if int(speed) != 0:
                some_eta = ((int(total_frames) - elapse) / speed) * 1000
                progress_str = "**[{0}{1}]** `| {2}%\n\n`".format(
                    "".join("█" for _ in range(math.floor(per / 5))),
                    "".join("" for _ in range(20 - math.floor(per / 5))),
                    round(per, 2),
                )
                e_size = f"{humanbytes(size)} of ~{humanbytes(size / per * 100)}"
                eta = time_formatter(some_eta)
                try:
                    await send_msg.edit(f'{ps_name}\n{progress_str}' + f'GROSS: {e_size}\n\nETA: {eta}',reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Owner", url = 'https://t.me/sohailkhan_indianime')]]))
                except Exception as e:
                    LOG.warn('Error While Editing FFMPEG Status {e}')
                if log != None:
                    await log.edit(f'{ps_name}\n\n{progress_str}' + f'**GROSS:** `{e_size}`\n**ETA:** `{eta}`')  